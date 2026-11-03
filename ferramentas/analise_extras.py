"""Tres contas que faltavam: veto com as duas Casas, efeito das medidas dos EUA no voto do centro, e o placar da Dilma contra o do Lula."""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from congresso27.base import R, sig, votacoes_ano, votos_ano

SA = R / "resultados"
RES = {}
ESQ = {"PT", "PCDOB", "PV", "PSOL", "REDE", "PSB", "PDT"}
DIR = {"PL", "NOVO"}
r = pd.read_csv(SA / "c2_replay_2027.csv")
RES["camara_contra_257_pct"] = round((r.contra >= 257).mean() * 100, 1)
RES["camara_contra_257_real_pct"] = round((r.contra_gov >= 257).mean() * 100, 1)
RES["camara_com_abaixo_172_pct"] = round((r.com < 172).mean() * 100, 1)
RES["camara_com_abaixo_172_n"] = int((r.com < 172).sum())
RES["camara_contra_342_n"] = int((r.contra >= 342).sum())
RES["camara_contra_342_real_n"] = int((r.contra_gov >= 342).sum())
RES["camara_n"] = len(r)
s = pd.read_csv(SA / "s1_replay_senado_2027.csv")
RES["senado_contra_41_real_pct"] = round((s.contra_gov >= 41).mean() * 100, 1)
RES["senado_contra_41_2027_pct"] = round((s.contra >= 41).mean() * 100, 1)
RES["senado_com_41_real_pct"] = round((s.com_gov >= 41).mean() * 100, 1)
RES["senado_com_41_2027_pct"] = round((s.com >= 41).mean() * 100, 1)
RES["senado_com_27_real_pct"] = round((s.com_gov >= 27).mean() * 100, 1)
RES["senado_com_27_2027_pct"] = round((s.com >= 27).mean() * 100, 1)

# Voto do centro em torno das medidas dos EUA
T = pd.concat([votacoes_ano(a) for a in (2025, 2026)])
T = T[T.disputada].copy()
T["data"] = pd.to_datetime(T.data)
linhas = []
for a in (2025, 2026):
    w = votos_ano(a)
    w = w[w.idVotacao.isin(T.index)].merge(T[["orient", "data"]], left_on="idVotacao", right_index=True)
    w = w[w.voto.isin(["Sim", "Não"])]
    w["ok"] = (w.voto == w.orient).astype(int)
    w["sig"] = w.deputado_siglaPartido.map(sig)
    w["campo"] = np.where(w.sig.isin(ESQ), "esquerda", np.where(w.sig.isin(DIR), "PL e Novo", "centro"))
    linhas.append(w[["data", "campo", "ok", "idVotacao"]])
W = pd.concat(linhas)
eventos = {"tarifa de 50% anunciada (09/jul/2025)": "2025-07-09", "sancao a Moraes (30/jul/2025)": "2025-07-30", "tarifa de 25% em vigor (22/jul/2026)": "2026-07-22"}
ev = []
for nome, d in eventos.items():
    d0 = pd.Timestamp(d)
    for janela in (60, 120):
        a = W[(W.data >= d0 - pd.Timedelta(days=janela)) & (W.data < d0)]
        b = W[(W.data >= d0) & (W.data < d0 + pd.Timedelta(days=janela))]
        for campo in ("centro", "PL e Novo", "esquerda"):
            aa, bb = a[a.campo == campo], b[b.campo == campo]
            # erro pelo agrupamento por votacao
            ma = aa.groupby("idVotacao").ok.mean()
            mb = bb.groupby("idVotacao").ok.mean()
            ep = float(np.sqrt(ma.var() / max(1, len(ma)) + mb.var() / max(1, len(mb)))) if len(ma) > 1 and len(mb) > 1 else np.nan
            ev.append({"evento": nome, "janela_dias": janela, "campo": campo, "votacoes_antes": len(ma), "votacoes_depois": len(mb), "antes_pct": round(ma.mean() * 100, 1) if len(ma) else None, "depois_pct": round(mb.mean() * 100, 1) if len(mb) else None, "dif_pontos": round((mb.mean() - ma.mean()) * 100, 1) if len(ma) and len(mb) else None, "erro_padrao_pontos": round(ep * 100, 1) if ep == ep else None})
E = pd.DataFrame(ev)
E.to_csv(SA / "c8_centro_em_torno_dos_eua.csv", index=False, encoding="utf-8")
print(E.to_string())
RES["eventos_eua"] = ev
Wc = W[W.campo == "centro"]
m = Wc.groupby(Wc.data.dt.to_period("M")).ok.mean().mul(100).round(1)
m.index = m.index.astype(str)
m.to_csv(SA / "c8_centro_por_mes.csv")
print(m.to_string())

# Dilma 2015 e Lula 2025, lado a lado; os mesmos partidos pivo
S = pd.read_csv(SA / "c1_serie_por_ano.csv", index_col=0)
RES["dilma_2015"] = S.loc[2015].to_dict()
RES["lula_2025"] = S.loc[2025].to_dict()
RES["primeiro_ano"] = {int(a): float(S.loc[a, "vitoria_disputadas"]) for a in (2003, 2007, 2011, 2015, 2019, 2023)}
RES["primeiro_ano_media"] = round(float(np.mean(list(RES["primeiro_ano"].values()))), 1)
# queda do 1o ao ultimo ano de cada mandato completo
RES["queda_no_mandato"] = {"Lula I": [S.loc[2003, "vitoria_disputadas"], S.loc[2006, "vitoria_disputadas"]], "Lula II": [S.loc[2007, "vitoria_disputadas"], S.loc[2010, "vitoria_disputadas"]], "Dilma I": [S.loc[2011, "vitoria_disputadas"], S.loc[2014, "vitoria_disputadas"]], "Bolsonaro": [S.loc[2019, "vitoria_disputadas"], S.loc[2022, "vitoria_disputadas"]], "Lula III": [S.loc[2023, "vitoria_disputadas"], S.loc[2026, "vitoria_disputadas"]]}
print(json.dumps({k: v for k, v in RES.items() if k != "eventos_eua"}, indent=0, ensure_ascii=False, default=float))
(SA / "RESUMO_EXTRAS.json").write_text(json.dumps(RES, indent=1, ensure_ascii=False, default=float), encoding="utf8")
