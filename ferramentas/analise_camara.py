"""A serie 2003-2026, o replay de 2023-2026 com o Congresso de 2027, a escada por partido e o teste do passado."""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from congresso27.base import PRES, R, replay, sig, votacoes_ano, votos_ano

SA = R / "resultados"
RES = {}
# 1. serie por ano
T = pd.concat([votacoes_ano(a) for a in range(2003, 2027)])
T.drop(columns=["ultimaApresentacaoProposicao_descricao"]).to_csv(SA / "c1_votacoes_com_orientacao.csv")


def resumo(t):
    d = t[t.disputada]
    return pd.Series({"votacoes": len(t), "disputadas": len(d), "vitoria_todas": t.gov_venceu.mean() * 100,
                      "vitoria_disputadas": d.gov_venceu.mean() * 100 if len(d) else np.nan,
                      "mediana_com_gov": d.com_gov.median() if len(d) else np.nan,
                      "p10_com_gov": d.com_gov.quantile(.1) if len(d) else np.nan})


S = T.groupby("ano")[list(T.columns)].apply(resumo)
S["presidente"] = [PRES[a] for a in S.index]
S.round(1).to_csv(SA / "c1_serie_por_ano.csv")
P = T.assign(pres=T.ano.map(PRES)).groupby("pres", sort=False)[list(T.columns)].apply(resumo)
P.round(1).to_csv(SA / "c1_serie_por_presidente.csv")
print(S.round(1).to_string())
print(P.round(1).to_string())
RES["serie_por_ano"] = json.loads(S.round(1).to_json(orient="index"))
RES["serie_por_presidente"] = json.loads(P.round(1).to_json(orient="index"))

# 2. a composicao eleita em 2026
E = pd.read_csv(R / "dados/derivados/eleitos_2026_camara.csv", dtype=str, encoding="utf-8")
E["sig"] = E.SG_PARTIDO.map(sig)
print(E.sig.value_counts().to_dict())

# 3. replay
ids = T[(T.ano >= 2023) & T.disputada].index
r = replay(set(ids), range(2023, 2027), E[["deputado_id", "sig"]])
r = r.join(T[["com_gov", "contra_gov", "gov_venceu", "descricao", "data", "orient"]])
r.round(2).to_csv(SA / "c2_replay_2027.csv")
assert r.com.add(r.contra).max() <= 513


def bloco(x):
    return {"n": len(x), "vitoria_real_pct": round(x.gov_venceu.mean() * 100, 1), "vitoria_replay_pct": round(x.venceu.mean() * 100, 1),
            "virariam_contra": int((x.gov_venceu & ~x.venceu).sum()), "virariam_a_favor": int((~x.gov_venceu & x.venceu).sum()),
            "mediana_com_real": float(x.com_gov.median()), "mediana_com_2027": round(float(x.com.median()), 1),
            "p10_com_2027": round(float(x.com.quantile(.1)), 1), "p05_com_2027": round(float(x.com.quantile(.05)), 1),
            "min_com_2027": round(float(x.com.min()), 1), "max_contra_2027": round(float(x.contra.max()), 1),
            "pct_com_172": round((x.com >= 172).mean() * 100, 1), "pct_com_257": round((x.com >= 257).mean() * 100, 1),
            "pct_com_308": round((x.com >= 308).mean() * 100, 1), "pct_contra_308": round((x.contra >= 308).mean() * 100, 1),
            "pct_contra_342": round((x.contra >= 342).mean() * 100, 1)}


RES["replay_total"] = bloco(r)
RES["replay_por_ano"] = {int(a): bloco(g) for a, g in r.groupby("ano")}
print(json.dumps(RES["replay_total"], indent=0))
print(pd.DataFrame(RES["replay_por_ano"]).T.to_string())

# 4. alinhamento por partido (2023-2026, disputadas) e escada
linhas = []
for a in range(2023, 2027):
    t = T[(T.ano == a) & T.disputada]
    w = votos_ano(a)
    w = w[w.idVotacao.isin(t.index)].copy()
    w = w.merge(t[["orient"]], left_on="idVotacao", right_index=True)
    w = w[w.voto.isin(["Sim", "Não"])]
    w["ok"] = (w.voto == w.orient).astype(int)
    w["sig"] = w.deputado_siglaPartido.map(sig)
    w["ano"] = a
    linhas.append(w[["ano", "sig", "deputado_id", "ok", "deputado_nome"]])
W = pd.concat(linhas)
Pa = W.groupby("sig").ok.mean().mul(100).round(1)
Pano = W.groupby(["sig", "ano"]).ok.mean().mul(100).round(1).unstack()
assent = E.sig.value_counts()
ass22 = pd.read_csv(R.parent / "congresso-e-governos-eleicoes-2026/resultados/a1_cadeiras_por_partido_e_ano.csv").assign(sig=lambda d: d.sig.map(sig)).groupby("sig")["2022"].sum()
Esc = pd.DataFrame({"cadeiras_2027": assent, "cadeiras_eleitas_2022": ass22}).fillna(0).astype(int).join(Pa.rename("alinhamento_2023_26")).join(Pano)
Esc = Esc[(Esc.cadeiras_2027 > 0) | (Esc.cadeiras_eleitas_2022 > 0)].sort_values("alinhamento_2023_26", ascending=False)
Esc["acum_2027"] = Esc.cadeiras_2027.cumsum()
Esc["acum_2022"] = Esc.cadeiras_eleitas_2022.cumsum()
Esc.to_csv(SA / "c3_escada_por_partido.csv")
print(Esc.to_string())
RES["escada"] = json.loads(Esc.reset_index(names="sig").to_json(orient="records"))
Dd = W.groupby("deputado_id").ok.agg(["mean", "count"])
Er = E.merge(Dd, how="left", left_on="deputado_id", right_index=True)
Er["faixa"] = pd.cut(Er["mean"], [-.01, .3, .5, .7, 1.01], labels=["ate30", "30a50", "50a70", "70mais"])
RES["eleitos_com_voto_2023_26"] = int(Er["mean"].notna().sum())
RES["eleitos_sem_voto_2023_26"] = int(Er["mean"].isna().sum())
RES["faixas_alinhamento"] = {str(k): int(v) for k, v in Er.faixa.value_counts(dropna=False).items()}
Er.to_csv(SA / "c3_eleitos_com_alinhamento.csv", index=False, encoding="utf-8")
print(RES["faixas_alinhamento"])

# 5. a mesma conta com quem efetivamente votou em 2023-2026 (controle: replay deve reproduzir o real)
ctrl = votos_ano(2024).drop_duplicates("deputado_id").copy()
ctrl["sig"] = ctrl.deputado_siglaPartido.map(sig)
ids24 = T[(T.ano == 2024) & T.disputada].index
rc = replay(set(ids24), [2024], ctrl[["deputado_id", "sig"]]).join(T[["com_gov", "contra_gov", "gov_venceu"]])
RES["controle_2024"] = {"n": len(rc), "dif_max_com": float((rc.com - rc.com_gov).abs().max()), "acordo_resultado_pct": round((rc.venceu == rc.gov_venceu).mean() * 100, 1)}
print(RES["controle_2024"])

# 6. teste do passado: mesmo campo no mandato seguinte
casos = [("Lula I para Lula II", range(2003, 2007), 2007), ("Lula II para Dilma I", range(2007, 2011), 2011), ("Dilma I para Dilma II", range(2011, 2015), 2015)]
bt = []
for nome, fonte, alvo in casos:
    idsf = T[T.ano.isin(list(fonte)) & T.disputada].index
    wa = votos_ano(alvo).drop_duplicates("deputado_id").copy()
    wa["sig"] = wa.deputado_siglaPartido.map(sig)
    rr = replay(set(idsf), fonte, wa[["deputado_id", "sig"]]).join(T[["gov_venceu", "com_gov"]])
    real = T[(T.ano == alvo) & T.disputada]
    bt.append({"caso": nome, "n_fonte": len(rr), "vitoria_real_mandato_anterior": round(rr.gov_venceu.mean() * 100, 1),
               "previsto_replay": round(rr.venceu.mean() * 100, 1), "real_no_ano": round(real.gov_venceu.mean() * 100, 1), "n_real": len(real),
               "mediana_prevista": round(float(rr.com.median()), 1), "mediana_real": float(real.com_gov.median()),
               "erro_pontos": round(rr.venceu.mean() * 100 - real.gov_venceu.mean() * 100, 1)})
BT = pd.DataFrame(bt)
BT.to_csv(SA / "c4_teste_do_passado.csv", index=False)
print(BT.to_string())
RES["teste_passado"] = bt
(SA / "RESUMO_CAMARA.json").write_text(json.dumps(RES, indent=1, ensure_ascii=False), encoding="utf8")
