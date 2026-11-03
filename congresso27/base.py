"""Funcoes centrais: leitura das votacoes da Camara, orientacao do governo e replay com outra composicao."""
import functools
import pathlib

import numpy as np
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
BR = R / "dados/brutos/camara"
PRES = {**{y: "Lula I" for y in range(2003, 2007)}, **{y: "Lula II" for y in range(2007, 2011)},
        **{y: "Dilma I" for y in range(2011, 2015)}, 2015: "Dilma II", 2016: "Dilma II e Temer", 2017: "Temer", 2018: "Temer",
        **{y: "Bolsonaro" for y in range(2019, 2023)}, **{y: "Lula III" for y in range(2023, 2027)}}
# a mesma legenda em anos diferentes; MISSAO nao tem historico e usa NOVO
ALIAS = {"UNIÃO": "UNIAO", "SDD": "SOLIDARIEDADE", "PODEMOS": "PODE", "MISSÃO": "NOVO", "REPUBLICANO": "REPUBLICANOS",
         "PC DO B": "PCDOB", "PATRIOTA": "PRD", "PTB": "PRD", "PATRI": "PRD"}


def sig(s):
    s = str(s).strip().upper()
    s = s.encode("latin1", "ignore").decode("latin1") if False else s
    return ALIAS.get(s, s)


@functools.lru_cache(maxsize=32)
def _carregar(ano):
    colsv = ("id", "data", "siglaOrgao", "aprovacao", "descricao", "ultimaApresentacaoProposicao_descricao")
    v = pd.read_csv(BR / f"votacoes-{ano}.csv", sep=";", dtype=str, encoding="utf-8-sig", usecols=lambda c: c in colsv)
    o = pd.read_csv(BR / f"votacoesOrientacoes-{ano}.csv", sep=";", dtype=str, encoding="utf-8-sig", usecols=["idVotacao", "siglaBancada", "orientacao"])
    w = pd.read_csv(BR / f"votacoesVotos-{ano}.csv", sep=";", dtype=str, encoding="utf-8-sig",
                    usecols=["idVotacao", "voto", "deputado_id", "deputado_nome", "deputado_siglaPartido", "deputado_siglaUf"])
    return v, o, w


def orientacao_governo(o):
    b = o.siglaBancada.fillna("").str.strip().str.upper()
    g = o[b.isin(["GOV.", "GOVERNO", "GOV"])].copy()
    g["orientacao"] = g.orientacao.str.strip()
    g = g[g.orientacao.isin(["Sim", "Não"])]
    return g.drop_duplicates("idVotacao").set_index("idVotacao").orientacao


def votacoes_ano(ano, piso_perdedor=0.10):
    """Uma linha por votacao nominal de plenario com orientacao do governo.
    Disputada: o lado perdedor teve pelo menos piso_perdedor dos votos Sim+Nao."""
    v, o, w = _carregar(ano)
    g = orientacao_governo(o)
    w = w[w.idVotacao.isin(g.index)]
    t = w.pivot_table(index="idVotacao", columns="voto", values="deputado_id", aggfunc="count", fill_value=0)
    for c in ("Sim", "Não"):
        if c not in t:
            t[c] = 0
    t = t[["Sim", "Não"]].copy()
    t["orient"] = g
    t["ano"] = ano
    t = t.join(v.drop_duplicates("id").set_index("id")[["data", "siglaOrgao", "aprovacao", "descricao", "ultimaApresentacaoProposicao_descricao"]])
    t = t[(t.siglaOrgao == "PLEN") | t.siglaOrgao.isna()]
    t["com_gov"] = np.where(t.orient == "Sim", t.Sim, t["Não"])
    t["contra_gov"] = np.where(t.orient == "Sim", t["Não"], t.Sim)
    tot = t.com_gov + t.contra_gov
    t = t[tot >= 100].copy()
    tot = t.com_gov + t.contra_gov
    t["gov_venceu"] = t.com_gov > t.contra_gov
    t["disputada"] = t[["com_gov", "contra_gov"]].min(axis=1) / tot >= piso_perdedor
    return t


def votos_ano(ano):
    return _carregar(ano)[2]


def replay(ids_votacoes, anos, composicao):
    """Repete votacoes reais com outra composicao.
    composicao: DataFrame com deputado_id (pode ser vazio) e sig (sigla padronizada).
    Quem votou naquela votacao repete o proprio voto. Quem nao votou recebe a proporcao e a presenca da bancada da sigla
    naquela votacao; sigla sem voto nela recebe a presenca e a proporcao da Casa.
    Devolve, por votacao: votos esperados com o governo, contra, e se venceu."""
    linhas = []
    comp = composicao.copy()
    comp["deputado_id"] = comp.deputado_id.astype("object")
    for ano in anos:
        t = votacoes_ano(ano)
        t = t[t.index.isin(ids_votacoes)]
        if t.empty:
            continue
        w = votos_ano(ano)
        w = w[w.idVotacao.isin(t.index)].copy()
        w["sig"] = w.deputado_siglaPartido.map(sig)
        w = w.merge(t[["orient"]], left_on="idVotacao", right_index=True)
        w["com"] = (w.voto == w.orient).astype(int)
        w["contra"] = (w.voto.isin(["Sim", "Não"]) & (w.voto != w.orient)).astype(int)
        tam = w.groupby("sig").deputado_id.nunique()
        for vid, sub in w.groupby("idVotacao"):
            sub = sub.drop_duplicates("deputado_id").set_index("deputado_id")
            achou = comp.deputado_id.isin(sub.index)
            s2 = sub.loc[comp.deputado_id[achou].values]
            com, contra = float(s2.com.sum()), float(s2.contra.sum())
            pg = sub.groupby("sig")[["com", "contra"]].sum()
            pres_casa = (sub.com.sum() + sub.contra.sum()) / 513
            parte = sub.com.sum() / max(1, sub.com.sum() + sub.contra.sum())
            for s, n in comp[~achou].sig.value_counts().items():
                if s in pg.index and pg.loc[s, "com"] + pg.loc[s, "contra"] > 0:
                    c, x = pg.loc[s, "com"], pg.loc[s, "contra"]
                    pres = min(1.0, (c + x) / tam[s])
                    com += n * pres * c / (c + x)
                    contra += n * pres * x / (c + x)
                else:
                    com += n * pres_casa * parte
                    contra += n * pres_casa * (1 - parte)
            linhas.append({"idVotacao": vid, "ano": ano, "com": com, "contra": contra, "venceu": com > contra})
    return pd.DataFrame(linhas).set_index("idVotacao")
