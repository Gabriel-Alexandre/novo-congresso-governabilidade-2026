"""Rodada 2: refaz as contas com as correcoes da revisao por 3 leitores (docs/revisao/) e grava resultados/RESUMO.json, dono dos numeros.

Mudancas: presenca fecha o total real de votantes; bloco pendulo no lugar de "centro"; serie com a posicao do PT nas votacoes sem orientacao;
novatos em 3 variantes; MP e veto por autor e por data; Senado com os nomes corrigidos, bootstrap por materia e a escada de senadores.
"""
import json
import pathlib
import re
import sys
import unicodedata

import numpy as np
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R))
from congresso27.base import PRES, sig, votacoes_ano, votos_ano, _carregar

SA = R / "resultados"
OUT = {}
ESQ = {"PT", "PCDOB", "PV", "PSOL", "REDE", "PSB", "PDT"}
DIR = {"PL", "NOVO"}
rng = np.random.default_rng(2027)


def pct(x):
    return round(float(x) * 100, 1)


def materia(i):
    return str(i).split("-")[0]


def boot(df, col, n=2000):
    g = df.groupby("materia")[col].agg(["sum", "count"])
    a = g.values
    res = []
    for _ in range(n):
        s = a[rng.integers(0, len(a), len(a))]
        res.append(s[:, 0].sum() / s[:, 1].sum())
    return [pct(np.quantile(res, .025)), pct(np.quantile(res, .975))]


# ===== CAMARA =====
T = pd.concat([votacoes_ano(a) for a in range(2023, 2027)])
D = T[T.disputada].copy()
E = pd.read_csv(R / "dados/derivados/eleitos_2026_camara.csv", dtype=str, encoding="utf-8")
E["sig"] = E.SG_PARTIDO.map(sig)
E["grupo"] = np.where(E.sig.isin(ESQ), "esquerda", np.where(E.sig.isin(DIR), "PL e Novo", "pendulo"))
OUT["cadeiras"] = E.grupo.value_counts().to_dict()
r = pd.read_csv(SA / "c2_replay_2027.csv", dtype={"idVotacao": str}).set_index("idVotacao")
r["materia"] = [materia(i) for i in r.index]
real_tot = r.com_gov + r.contra_gov
esc = real_tot / (r.com + r.contra)
r["com_n"] = r.com * esc
r["contra_n"] = r.contra * esc
r["dv"] = pd.to_datetime(r.data)


def camara_bloco(x):
    return {"n": len(x), "real_pct": pct(x.gov_venceu.mean()), "novo_pct": pct(x.venceu.mean()), "viram_contra": int((x.gov_venceu & ~x.venceu).sum()), "viram_a_favor": int((~x.gov_venceu & x.venceu).sum())}


cam = {"total": camara_bloco(r), "por_ano": {int(a): camara_bloco(g) for a, g in r.groupby("ano")},
       "2025_26": camara_bloco(r[r.ano >= 2025]), "desde_09jul2025": camara_bloco(r[r.dv >= "2025-07-09"]),
       "ic95_real": boot(r.assign(v=r.gov_venceu.astype(int)), "v"), "ic95_novo": boot(r.assign(v=r.venceu.astype(int)), "v"),
       "mediana_com_real": float(r.com_gov.median()), "mediana_com_novo": round(float(r.com_n.median()), 1),
       "pct_257_real": pct((r.com_gov >= 257).mean()), "pct_257_novo": pct((r.com_n >= 257).mean()),
       "pct_308_real": pct((r.com_gov >= 308).mean()), "pct_308_novo": pct((r.com_n >= 308).mean()),
       "pct_172_real": pct((r.com_gov >= 172).mean()), "pct_172_novo": pct((r.com_n >= 172).mean()),
       "contra_342_real": int((r.contra_gov >= 342).sum()), "contra_342_novo": int((r.contra_n >= 342).sum()),
       "contra_257_real_pct": pct((r.contra_gov >= 257).mean()), "contra_257_novo_pct": pct((r.contra_n >= 257).mean())}
for piso in (.35, .40, .45):
    x = r[r[["com_gov", "contra_gov"]].min(axis=1) / real_tot >= piso]
    cam[f"perdedor_{int(piso*100)}"] = camara_bloco(x)

# Merito, com regex nova: so o texto da materia, nao requerimento, destaque ou emenda
d = r.descricao.fillna("").str.replace(r"ressalvad[oa]s? (?:os|as)? ?destaques?", "", regex=True, case=False)
proc = d.str.contains(r"Requerimento|Urg[eê]ncia|Retirada|Adiamento|Prefer[eê]ncia|Encerramento|Mantido o texto|Suprimido o texto|Destaque|^\s*(?:Aprovad[oa]|Rejeitad[oa])\s+a\s+Emenda de Plen|Recurso", case=False, regex=True)
mer = ~proc
cam["merito"] = {"total": camara_bloco(r[mer]), "por_ano": {int(a): camara_bloco(g) for a, g in r[mer].groupby("ano")}}

# O pendulo decide: com a maioria dele, quanto o governo ganhou
linhas = []
for a in range(2023, 2027):
    w = votos_ano(a)
    w = w[w.idVotacao.isin(D.index)].merge(D[["orient"]], left_on="idVotacao", right_index=True)
    w = w[w.voto.isin(["Sim", "Não"])].copy()
    w["sig"] = w.deputado_siglaPartido.map(sig)
    w["ok"] = (w.voto == w.orient).astype(int)
    linhas.append(w[["idVotacao", "sig", "ok", "deputado_id"]])
W = pd.concat(linhas)
Wp = W[~W.sig.isin(ESQ) & ~W.sig.isin(DIR)]
mp = Wp.groupby("idVotacao").ok.mean() > .5
ven = D.gov_venceu.reindex(mp.index)
cam["pendulo_com_governo"] = {"votacoes": int(mp.sum()), "venceu": int(ven[mp].sum())}
cam["pendulo_contra_governo"] = {"votacoes": int((~mp).sum()), "venceu": int(ven[~mp].sum())}
# alinhamento do pendulo por ano, pesado pelas cadeiras de 2027
pend_sigs = E[E.grupo == "pendulo"].sig.value_counts()
Wa = W.merge(D[["ano"]], left_on="idVotacao", right_index=True)
OUT["pendulo_alinhamento"] = {}
for a in range(2023, 2027):
    g = Wa[(Wa.ano == a) & Wa.sig.isin(pend_sigs.index)].groupby("sig").ok.mean()
    OUT["pendulo_alinhamento"][a] = pct((g * pend_sigs.reindex(g.index)).sum() / pend_sigs.reindex(g.index).sum())

# Com a posicao do PT nas votacoes sem orientacao
def serie_pt(ano):
    v, o, w = _carregar(ano)
    w = w[w.voto.isin(["Sim", "Não"])].copy()
    w = w[w.idVotacao.isin(v[v.siglaOrgao == "PLEN"].id)]
    w["sig"] = w.deputado_siglaPartido.map(sig)
    t = votacoes_ano(ano)
    pt = w[w.sig == "PT"].groupby("idVotacao").voto.agg(lambda s: (s == "Sim").mean())
    tot = w.groupby(["idVotacao", "voto"]).deputado_id.count().unstack(fill_value=0)
    for c in ("Sim", "Não"):
        if c not in tot:
            tot[c] = 0
    linhas = []
    for vid, row in tot.iterrows():
        n = row.Sim + row["Não"]
        if n < 100 or min(row.Sim, row["Não"]) / n < .10:
            continue
        if vid in t.index:
            o_ = t.loc[vid, "orient"]
        elif vid in pt.index and (pt[vid] >= .75 or pt[vid] <= .25):
            o_ = "Sim" if pt[vid] >= .75 else "Não"
        else:
            continue
        linhas.append(row.Sim > row["Não"] if o_ == "Sim" else row["Não"] > row.Sim)
    return len(linhas), float(np.mean(linhas))


sp = {a: serie_pt(a) for a in (2015, 2023, 2024, 2025, 2026)}
OUT["com_posicao_do_pt_nas_sem_orientacao"] = {int(a): {"n": v[0], "vitoria_pct": pct(v[1])} for a, v in sp.items()}
n2326 = sum(sp[a][0] for a in (2023, 2024, 2025, 2026))
OUT["com_posicao_do_pt_2023_26"] = {"n": n2326, "vitoria_pct": pct(sum(sp[a][0] * sp[a][1] for a in (2023, 2024, 2025, 2026)) / n2326)}


# Novatos em 3 variantes (replay proprio, com o mesmo criterio de presenca do projeto)
def replay_novato(modo):
    res = []
    com_voto = set(W.deputado_id)
    novatos = ~E.deputado_id.isin(com_voto)
    for ano in range(2023, 2027):
        t = D[D.ano == ano]
        w = votos_ano(ano)
        w = w[w.idVotacao.isin(t.index)].merge(t[["orient"]], left_on="idVotacao", right_index=True)
        w = w[w.voto.isin(["Sim", "Não"])].copy()
        w["sig"] = w.deputado_siglaPartido.map(sig)
        w["ok"] = (w.voto == w.orient).astype(int)
        for vid, s in w.groupby("idVotacao"):
            s = s.drop_duplicates("deputado_id").set_index("deputado_id")
            ach = E.deputado_id.isin(s.index)
            com = float(s.loc[E.deputado_id[ach].values].ok.sum())
            contra = float(ach.sum() - com)
            pg = s.groupby("sig").ok.agg(["sum", "count"])
            pl = pg.loc["PL", "sum"] / pg.loc["PL", "count"] if "PL" in pg.index else 0
            pres = len(s) / 513
            for (sg, nov), n in E[~ach].assign(nov=novatos[~ach]).groupby(["sig", "nov"]).size().items():
                p = pg.loc[sg, "sum"] / pg.loc[sg, "count"] if sg in pg.index else s.ok.mean()
                if nov and sg not in ESQ and sg not in DIR:
                    p = {"base": p, "menos10": max(0, p - .10), "meio_pl": (p + pl) / 2, "como_pl": pl}[modo]
                com += n * pres * p
                contra += n * pres * (1 - p)
            res.append(com > contra)
    return pct(np.mean(res))


cam["novatos"] = {m: replay_novato(m) for m in ("base", "menos10", "meio_pl", "como_pl")}
OUT["camara"] = cam
print(json.dumps(cam, indent=0, ensure_ascii=False, default=float)[:2500])

# Serie por ano e 2016 separado
S = pd.read_csv(SA / "c1_serie_por_ano.csv", index_col=0)
t16 = votacoes_ano(2016)
t16 = t16[t16.disputada]
dt16 = pd.to_datetime(t16.data)
OUT["2016"] = {"dilma": [int(t16[dt16 < "2016-05-12"].gov_venceu.sum()), int((dt16 < "2016-05-12").sum())], "temer": [int(t16[dt16 >= "2016-05-12"].gov_venceu.sum()), int((dt16 >= "2016-05-12").sum())]}
OUT["serie"] = {int(a): {"vitoria_disputadas": float(S.loc[a, "vitoria_disputadas"]), "n": int(S.loc[a, "disputadas"]), "presidente": S.loc[a, "presidente"]} for a in S.index}
OUT["primeiro_ano"] = {int(a): float(S.loc[a, "vitoria_disputadas"]) for a in (2003, 2007, 2011, 2015, 2019, 2023)}

# Teste do passado com 513 e contra a regra ingenua
Tt = pd.concat([votacoes_ano(a) for a in range(2003, 2016)])
from congresso27.base import replay

bt = []
for nome, fonte, alvo in [("Lula I para Lula II", range(2003, 2007), 2007), ("Lula II para Dilma I", range(2007, 2011), 2011), ("Dilma I para Dilma II", range(2011, 2015), 2015)]:
    tf = Tt[Tt.ano.isin(list(fonte)) & Tt.disputada]
    wa = votos_ano(alvo)
    cont = wa.groupby("deputado_id").idVotacao.count().sort_values(ascending=False).head(513).index
    comp = wa.drop_duplicates("deputado_id")
    comp = comp[comp.deputado_id.isin(cont)].copy()
    comp["sig"] = comp.deputado_siglaPartido.map(sig)
    rr = replay(set(tf.index), fonte, comp[["deputado_id", "sig"]])
    real = Tt[(Tt.ano == alvo) & Tt.disputada]
    bt.append({"caso": nome, "previsto": pct(rr.venceu.mean()), "repetir_o_mandato": pct(tf.gov_venceu.mean()), "real": pct(real.gov_venceu.mean()), "n_real": len(real)})
for b in bt:
    b["erro"] = round(abs(b["previsto"] - b["real"]), 1)
    b["erro_regra_ingenua"] = round(abs(b["repetir_o_mandato"] - b["real"]), 1)
OUT["teste_passado"] = {"casos": bt, "erro_medio": round(np.mean([b["erro"] for b in bt]), 2), "erro_medio_ingenua": round(np.mean([b["erro_regra_ingenua"] for b in bt]), 2)}
print(OUT["teste_passado"])


# ===== SENADO =====
def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z ]", "", s).strip()


linhas, meta = [], []
for a in range(2023, 2027):
    for s_ in (1, 2):
        for x in json.loads((R / f"dados/brutos/senado/votacoes-{a}-{s_}.json").read_text(encoding="utf8")):
            if x.get("votacaoSecreta") == "S":
                continue
            vid = x["codigoSessaoVotacao"]
            meta.append({"vid": vid, "ano": a, "materia": x.get("identificacao"), "data": x.get("dataSessao"), "desc": x.get("descricaoVotacao"), "cod_materia": x.get("codigoMateria")})
            for v in x.get("votos", []):
                if v["siglaVotoParlamentar"] in ("Sim", "Não"):
                    linhas.append({"vid": vid, "cod": v["codigoParlamentar"], "nome": v["nomeParlamentar"], "sig": sig(v["siglaPartidoParlamentar"]), "voto": v["siglaVotoParlamentar"], "ano": a})
L = pd.DataFrame(linhas)
M = pd.DataFrame(meta).drop_duplicates("vid").set_index("vid")
pt = L[L.sig == "PT"].groupby("vid").voto.agg(["count", lambda s: (s == "Sim").mean()])
pt.columns = ["n", "sim"]
pt = pt[pt.n >= 3]
o = pd.Series(np.where(pt.sim >= .75, "Sim", np.where(pt.sim <= .25, "Não", None)), index=pt.index).dropna()
L = L[L.vid.isin(o.index)].copy()
L["com"] = (L.voto == L.vid.map(o)).astype(int)
t = L.groupby("vid").com.agg(["sum", "count"]).rename(columns={"sum": "com_gov", "count": "tot"})
t["contra_gov"] = t.tot - t.com_gov
t = t[t.tot >= 41].copy()
t["real"] = t.com_gov > t.contra_gov
t["disp"] = t[["com_gov", "contra_gov"]].min(axis=1) / t.tot >= .10
t = t.join(M)
D2 = t[t.disp]
C = pd.read_csv(SA / "s0_composicao_2027_casada.csv")
C.loc[C.nome == "VENEZIANO", "cod"] = 5748
C.loc[C.nome == "DELEGADO ALESSANDRO", "cod"] = 5982
OUT_S = {"senadores_com_historico": int(C.cod.notna().sum()), "senadores_novos": int(C.cod.isna().sum())}
AP = pd.read_csv(R.parent / "congresso-e-governos-eleicoes-2026/dados/senado_apoio_flavio.csv")
ap = set(AP.candidato.map(norm))
pu = {(a.split()[0], a.split()[-1]) for a in ap}
C["k"] = C.nome.map(norm)
C["flavio"] = C.k.map(lambda s: s in ap or (s.split()[0], s.split()[-1]) in pu) | C.nome.isin(["MARINA JHC", "ZÉ MEDEIROS", "SANDERSON", "DR. FERNANDO MÁXIMO", "NICOLETTI"])
OUT_S["novos_com_apoio_declarado_flavio"] = int((C.cod.isna() & C.flavio).sum())

# historico pessoal na Camara dos deputados eleitos senadores
dep_alin = W.groupby("deputado_id").ok.agg(["mean", "count"])
cand = pd.read_csv(R / "dados/derivados/eleitos_2026_camara.csv", dtype=str, encoding="utf-8")
# nome de urna dos senadores novos contra os nomes de deputado
nomes_dep = W.drop_duplicates("deputado_id")
wn = pd.concat([votos_ano(a)[["deputado_id", "deputado_nome"]] for a in range(2023, 2027)]).drop_duplicates("deputado_id")
wn["k"] = wn.deputado_nome.map(norm)
mapa = {"BIA KICIS": "BIA KICIS", "GUSTAVO GAYER": "GUSTAVO GAYER", "FUFUCA": "ANDRE FUFUCA", "DOMINGOS SAVIO": "DOMINGOS SAVIO", "CARLOS JORDY": "CARLOS JORDY", "SANDERSON": "SANDERSON", "MARCEL VAN HATTEM": "MARCEL VAN HATTEM", "CAROL DE TONI": "CAROLINE DE TONI", "GUILHERME DERRITE": "GUILHERME DERRITE", "ARTHUR LIRA": "ARTHUR LIRA", "FILIPE BARROS": "FILIPE BARROS", "EVAIR DE MELO": "EVAIR VIEIRA DE MELO", "DR FERNANDO MAXIMO": "DR FERNANDO MAXIMO", "MARILIA ARRAES": "MARILIA ARRAES", "JULIO CESAR O JULIM DO LULA": "JULIO CESAR", "CHICAO": "", "NICOLETTI": "NICOLETTI", "ZE MEDEIROS": "", "MARA ROCHA": "MARA ROCHA"}
dep_de = {}
for k, alvo in mapa.items():
    if alvo:
        q = wn[wn.k == alvo]
        if len(q):
            i = q.iloc[0].deputado_id
            if i in dep_alin.index:
                dep_de[k] = float(dep_alin.loc[i, "mean"])
OUT_S["deputados_com_historico_na_camara"] = len(dep_de)
OUT_S["alinhamento_na_camara"] = {k: pct(v) for k, v in dep_de.items()}


def rejogar(fn=None, extra=0):
    """fn(linha, pg, parte_casa) -> proporcao com o governo do senador sem voto naquela votacao. Presenca fecha o total real de votantes."""
    out = []
    for vid, s in L[L.vid.isin(D2.index)].groupby("vid"):
        s = s.drop_duplicates("cod").set_index("cod")
        pg = s.groupby("sig").com.agg(["sum", "count"])
        parte = s.com.mean()
        tem = C.cod.isin(s.index)
        sub = s.loc[C.cod[tem].astype(int).values]
        com = float(sub.com.sum())
        contra = float(len(sub) - com)
        pool = C[~tem]
        falta = max(0, len(s) - len(sub))
        pres = min(1.0, falta / max(1, len(pool)))
        for _, x in pool.iterrows():
            p = fn(x, pg, parte) if fn else (pg.loc[x.sig, "sum"] / pg.loc[x.sig, "count"] if x.sig in pg.index else parte)
            com += pres * p
            contra += pres * (1 - p)
        out.append({"vid": vid, "com": com + extra, "contra": contra - extra, "novo": com + extra > contra - extra})
    return pd.DataFrame(out).set_index("vid")


def psig(s, pg, parte):
    return pg.loc[s, "sum"] / pg.loc[s, "count"] if s in pg.index else parte


b0 = rejogar().join(D2)
b0["materia_id"] = b0.materia
b0.round(2).to_csv(SA / "s1_replay_senado_r2.csv")


def sen_blo(x):
    return {"n": len(x), "real_pct": pct(x.real.mean()), "novo_pct": pct(x.novo.mean()), "viram_contra": int((x.real & ~x.novo).sum()), "mediana_com_real": float(x.com_gov.median()), "mediana_com_novo": round(float(x.com.median()), 1)}


sen = {**OUT_S, "total": sen_blo(b0), "por_periodo": {"2023_24": sen_blo(b0[b0.ano <= 2024]), "2025_26": sen_blo(b0[b0.ano >= 2025])}, "materias": int(b0.materia.nunique())}
bb = b0.assign(materia=b0.materia, v_r=b0.real.astype(int), v_n=b0.novo.astype(int))
sen["ic95_real"] = boot(bb, "v_r")
sen["ic95_novo"] = boot(bb, "v_n")
sen["pct_41_real"] = pct((b0.com_gov >= 41).mean())
sen["pct_41_novo"] = pct((b0.com >= 41).mean())
sen["pct_49_novo"] = pct((b0.com >= 49).mean())
sen["pct_contra_41_real"] = pct((b0.contra_gov >= 41).mean())
sen["pct_contra_41_novo"] = pct((b0.contra >= 41).mean())
sen["pct_contra_49_novo"] = pct((b0.contra >= 49).mean())
sen["pct_contra_54_novo"] = pct((b0.contra >= 54).mean())
sen["max_contra_novo"] = round(float(b0.contra.max()), 1)
sen["escada_trazidos"] = {k: pct(rejogar(extra=k).novo.mean()) for k in (2, 4, 6, 8)}
vars_ = {}
vars_["deputados_com_taxa_pessoal"] = pct(rejogar(lambda x, pg, pa: dep_de.get(norm(x.nome), psig(x.sig, pg, pa))).novo.mean())
vars_["flavio_como_pl"] = pct(rejogar(lambda x, pg, pa: psig("PL", pg, pa) if x.flavio else psig(x.sig, pg, pa)).novo.mean())
vars_["pendulo_fora_da_lista_como_mdb"] = pct(rejogar(lambda x, pg, pa: psig(x.sig, pg, pa) if (x.flavio or x.sig in DIR or x.sig in ESQ) else psig("MDB", pg, pa)).novo.mean())
vars_["piso_novo_fora_da_esquerda_como_pl"] = pct(rejogar(lambda x, pg, pa: psig(x.sig, pg, pa) if x.sig in ESQ else psig("PL", pg, pa)).novo.mean())
sem_dup = b0[~b0.duplicated(["materia", "com_gov", "contra_gov"])]
vars_["sem_duplicatas"] = {"n": len(sem_dup), "real": pct(sem_dup.real.mean()), "novo": pct(sem_dup.novo.mean())}
sen["variantes"] = vars_
Es = pd.DataFrame({"cadeiras_2027": C.sig.value_counts()}).join(L[L.vid.isin(D2.index)].groupby("sig").com.mean().mul(100).round(1).rename("alinhamento_2023_26")).sort_values("alinhamento_2023_26", ascending=False)
Es["acum"] = Es.cadeiras_2027.cumsum()
sen["escada"] = json.loads(Es.reset_index(names="sig").to_json(orient="records"))
Es.to_csv(SA / "s2_escada_senado.csv")
OUT["senado"] = sen
print(json.dumps({k: v for k, v in sen.items() if k not in ("escada", "alinhamento_na_camara")}, indent=0, ensure_ascii=False, default=float))

# ===== MP E VETO, por data e por autor =====
def presidente_por_data(d):
    d = pd.Timestamp(d)
    for lim, nome in [("2007-01-01", "Lula I"), ("2011-01-01", "Lula II"), ("2015-01-01", "Dilma I"), ("2016-05-12", "Dilma II"), ("2019-01-01", "Temer"), ("2023-01-01", "Bolsonaro"), ("2027-01-01", "Lula III")]:
        if d < pd.Timestamp(lim):
            return nome
    return "?"


reg = []
for ano in range(2003, 2027):
    for s_ in ("MPV", "VET"):
        for x in json.loads((R / f"dados/brutos/senado/processos/{s_}-{ano}.json").read_text(encoding="utf8")):
            reg.append({"sigla": s_, "id": x.get("identificacao"), "data": x.get("dataApresentacao"), "delib": x.get("siglaTipoDeliberacao") or "", "situ": (x.get("situacaoAtual") or "").upper(), "norma": x.get("normaGerada") or "", "tram": x.get("tramitando"), "ementa": (x.get("ementa") or "").upper()})
G = pd.DataFrame(reg).drop_duplicates(["sigla", "id"])
G["pres"] = [presidente_por_data(pd.Timestamp(d) - pd.Timedelta(days=1)) if d else "?" for d in G.data]
Mp = G[G.sigla == "MPV"].copy()
Mp["lei"] = (Mp.situ.str.contains("TRANSFORMADA EM NORMA") | Mp.norma.str.startswith("Lei") | Mp.delib.str.startswith("APROVADO")) & ~Mp.situ.str.contains("SEM EFIC|VETADA") & ~((Mp.data >= "2026-01-01") & (Mp.norma == ""))
Mp["credito"] = Mp.ementa.str.contains("CRÉDITO EXTRAORDINÁRIO")
Mp["sem_eficacia"] = Mp.situ.str.contains("SEM EFIC") | (Mp.delib == "PERDA_EFICACIA")
Mp["rejeitada"] = Mp.delib.str.startswith("REJEITADO")
Mp["revogada"] = Mp.situ.str.contains("REVOGADA") | (Mp.delib == "REVOGADO")
ORDEM = ["Lula I", "Lula II", "Dilma I", "Dilma II", "Temer", "Bolsonaro", "Lula III"]
tm = {}
for p in ORDEM:
    x = Mp[Mp.pres == p]
    y = x[~x.credito]
    tm[p] = {"editadas": len(x), "lei": int(x.lei.sum()), "pct": pct(x.lei.mean()), "sem_credito_n": len(y), "sem_credito_lei": int(y.lei.sum()), "sem_credito_pct": pct(y.lei.mean()), "sem_eficacia": int(x.sem_eficacia.sum()), "rejeitadas": int(x.rejeitada.sum()), "revogadas": int(x.revogada.sum())}
OUT["mp"] = tm
Vt = G[G.sigla == "VET"].copy()
Vt["derrubou"] = Vt.delib.isin(["REJEITADO_PLENARIO", "MANTIDO_PARCIALMENTE"])
Vt["decidido"] = Vt.delib.isin(["REJEITADO_PLENARIO", "MANTIDO_PARCIALMENTE", "MANTIDA_MATE"])
tv = {}
for p in ORDEM:
    x = Vt[Vt.pres == p]
    tv[p] = {"vetos": len(x), "com_algo_derrubado": int(x.derrubou.sum()), "decididos": int(x.decidido.sum()), "pct_decididos": pct(x.derrubou.sum() / max(1, x.decidido.sum()))}
OUT["veto"] = tv
pd.DataFrame(tm).T.to_csv(SA / "c5_mp_por_presidente_r2.csv")
pd.DataFrame(tv).T.to_csv(SA / "c5_veto_por_presidente_r2.csv")
print(pd.DataFrame(tm).T.to_string())
print(pd.DataFrame(tv).T.to_string())

ex = json.loads((SA / "RESUMO_EXTRAS.json").read_text(encoding="utf8"))
OUT["eventos_eua"] = ex["eventos_eua"]
sn = json.loads((SA / "RESUMO_SENADO.json").read_text(encoding="utf8"))
OUT["secretas"] = sn["secretas"]
(SA / "RESUMO.json").write_text(json.dumps(OUT, indent=1, ensure_ascii=False, default=float), encoding="utf8")
print("ok")
