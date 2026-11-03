"""Variantes do replay da Camara e a curva do centro: quanto o centro precisa se afastar para o governo parar de ganhar."""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from congresso27.base import R, replay, sig, votacoes_ano, votos_ano

SA = R / "resultados"
RES = {}
ESQ = {"PT", "PCDOB", "PV", "PSOL", "REDE", "PSB", "PDT"}
DIR = {"PL", "NOVO"}
T = pd.concat([votacoes_ano(a) for a in range(2023, 2027)])
E = pd.read_csv(R / "dados/derivados/eleitos_2026_camara.csv", dtype=str, encoding="utf-8")
E["sig"] = E.SG_PARTIDO.map(sig)


def taxa(r, ref=None):
    return {"n": len(r), "vitoria_pct": round(r.venceu.mean() * 100, 1), "mediana_com": round(float(r.com.median()), 1)}


# V0 base
ids = set(T[T.disputada].index)
base = replay(ids, range(2023, 2027), E[["deputado_id", "sig"]])
RES["base"] = taxa(base)
# V1 quem trocou de partido passa a votar como a nova bancada (ninguem repete o proprio voto se mudou de partido)
ult = pd.concat([votos_ano(a)[["deputado_id", "deputado_siglaPartido"]].assign(ano=a) for a in range(2023, 2027)]).drop_duplicates("deputado_id", keep="last")
ult["sig_ant"] = ult.deputado_siglaPartido.map(sig)
E1 = E.merge(ult[["deputado_id", "sig_ant"]], how="left", on="deputado_id")
mudou = E1.sig_ant.notna() & (E1.sig_ant != E1.sig)
RES["trocaram_de_partido"] = int(mudou.sum())
RES["trocas_principais"] = {f"{a}>{b}": int(n) for (a, b), n in E1[mudou].groupby(["sig_ant", "sig"]).size().sort_values(ascending=False).head(15).items()}
c1 = E1[["deputado_id", "sig"]].copy()
c1.loc[mudou, "deputado_id"] = None
RES["v1_quem_trocou_vota_como_a_nova_bancada"] = taxa(replay(ids, range(2023, 2027), c1))
# V2 ninguem repete o proprio voto: conta so por partido (2o caminho, sem deputado)
c2 = E[["deputado_id", "sig"]].copy()
c2["deputado_id"] = None
RES["v2_so_por_partido"] = taxa(replay(ids, range(2023, 2027), c2))
# V3 pisos de disputada
for piso in (.05, .20, .30):
    Tp = pd.concat([votacoes_ano(a, piso) for a in range(2023, 2027)])
    idp = set(Tp[Tp.disputada].index)
    rp = replay(idp, range(2023, 2027), E[["deputado_id", "sig"]]).join(Tp[["gov_venceu"]])
    RES[f"v3_piso_{int(piso*100)}"] = {**taxa(rp), "vitoria_real_pct": round(rp.gov_venceu.mean() * 100, 1)}
# V4 so o merito (sem requerimento, adiamento, urgencia, preferencia)
d = T.descricao.fillna("")
proc = d.str.contains(r"Requerimento|Urg[eê]ncia|Retirada de pauta|Adiamento|Prefer[eê]ncia|Destaque|Encerramento|Vota[cç][aã]o Nominal|Mantido o texto|Suprimido o texto|Rejeitado o Requerimento", case=False, regex=True)
mer = set(T[T.disputada & ~proc].index)
rm = base.loc[base.index.isin(mer)].join(T[["gov_venceu"]])
RES["v4_so_merito"] = {**taxa(rm), "vitoria_real_pct": round(rm.gov_venceu.mean() * 100, 1)}
# Tabelas para a curva: voto a voto da composicao, separando centro+centro-direita
linhas = []
for ano in range(2023, 2027):
    t = T[(T.ano == ano) & T.disputada]
    w = votos_ano(ano)
    w = w[w.idVotacao.isin(t.index)].copy()
    w["sig"] = w.deputado_siglaPartido.map(sig)
    w = w.merge(t[["orient"]], left_on="idVotacao", right_index=True)
    w = w[w.voto.isin(["Sim", "Não"])]
    w["ok"] = (w.voto == w.orient).astype(int)
    pv = w.groupby(["idVotacao", "sig"]).ok.agg(["sum", "count"]).reset_index()
    linhas.append(pv)
PV = pd.concat(linhas)
tamanho = E.sig.value_counts()
# presenca media da bancada nas disputadas
pres = (PV.groupby("sig")["count"].mean() / PV.groupby("sig")["count"].max()).clip(upper=1)
curva = []
for d in [-.20, -.10, 0, .05, .10, .15, .20, .25, .30, .40, .50]:
    venceu = []
    coms = []
    for vid, g in PV.groupby("idVotacao"):
        g = g.set_index("sig")
        c = x = 0.0
        for s, n in tamanho.items():
            if s not in g.index or g.loc[s, "count"] == 0:
                continue
            p = g.loc[s, "sum"] / g.loc[s, "count"]
            pr = pres.get(s, .8)
            if s not in ESQ and s not in DIR:
                p = p * (1 - d) if d >= 0 else p + (1 - p) * (-d)
            c += n * pr * p
            x += n * pr * (1 - p)
        venceu.append(c > x)
        coms.append(c)
    curva.append({"afastamento_centro_pct": int(d * 100), "vitoria_pct": round(np.mean(venceu) * 100, 1), "mediana_com": round(float(np.median(coms)), 1)})
C = pd.DataFrame(curva)
C.to_csv(SA / "c6_curva_do_centro.csv", index=False)
print(C.to_string())
RES["curva"] = curva
# quanto o centro ja se afastou de um ano para o outro (medido)
Pano = PV.merge(T[["ano"]], left_on="idVotacao", right_index=True).groupby(["ano", "sig"])[["sum", "count"]].sum()
Pano["a"] = Pano["sum"] / Pano["count"] * 100
centro = [s for s in tamanho.index if s not in ESQ and s not in DIR]
pond = {}
for a in range(2023, 2027):
    g = Pano.loc[a]
    g = g[g.index.isin(centro)]
    pond[a] = round(float((g.a * tamanho.reindex(g.index).fillna(0)).sum() / tamanho.reindex(g.index).fillna(0).sum()), 1)
RES["alinhamento_centro_ponderado_por_cadeira_2027"] = pond
print(pond)
# a mesma medida no passado, com os partidos fora da esquerda e do PL/NOVO (anos Dilma), para ancorar o choque de 2015
hist = {}
for a in range(2011, 2016):
    t = votacoes_ano(a)
    t = t[t.disputada]
    w = votos_ano(a)
    w = w[w.idVotacao.isin(t.index)].copy()
    w = w.merge(t[["orient"]], left_on="idVotacao", right_index=True)
    w = w[w.voto.isin(["Sim", "Não"])]
    w["sig"] = w.deputado_siglaPartido.map(sig)
    w["ok"] = w.voto == w.orient
    hist[a] = w.groupby("sig").ok.mean().mul(100).round(1)
H = pd.DataFrame(hist)
H.to_csv(SA / "c6_alinhamento_partidos_2011_2015.csv")
print(H.loc[[s for s in ["PMDB", "MDB", "PP", "PSD", "PR", "PRB", "PTB", "PSB", "PDT", "PT", "DEM", "PSDB"] if s in H.index]].to_string())
RES["dilma_partidos"] = json.loads(H.to_json(orient="index"))
# novato x veterano dentro do partido em 2023, 1o ano da legislatura anterior: o novato vota diferente?
w23 = votos_ano(2023)
t23 = T[(T.ano == 2023) & T.disputada]
w23 = w23[w23.idVotacao.isin(t23.index)].merge(t23[["orient"]], left_on="idVotacao", right_index=True)
w23 = w23[w23.voto.isin(["Sim", "Não"])]
w23["ok"] = w23.voto == w23.orient
ant = set(votos_ano(2022).deputado_id) | set(votos_ano(2021).deputado_id)
w23["novato"] = ~w23.deputado_id.isin(ant)
w23["sig"] = w23.deputado_siglaPartido.map(sig)
nv = w23.groupby(["sig", "novato"]).ok.mean().mul(100).round(1).unstack()
nv.columns = ["veterano", "novato"]
nv["n_dep"] = w23.groupby("sig").deputado_id.nunique()
nv = nv[nv.n_dep >= 8]
nv.to_csv(SA / "c6_novato_x_veterano_2023.csv")
print(nv.to_string())
RES["novato_x_veterano_2023"] = json.loads(nv.to_json(orient="index"))
# Variante: novatos do centro votam mais proximo do PL que o veterano do proprio partido (desconto de 10 pontos)
(SA / "RESUMO_SENSIBILIDADE.json").write_text(json.dumps(RES, indent=1, ensure_ascii=False, default=str), encoding="utf8")
print(json.dumps({k: v for k, v in RES.items() if k.startswith("v") or k in ("base", "trocaram_de_partido", "trocas_principais")}, indent=0, ensure_ascii=False))
