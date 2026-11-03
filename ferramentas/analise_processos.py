"""Medidas provisorias e vetos por ano (2003-2026), pelo servico de processos do Senado (Congresso Nacional)."""
import hashlib
import json
import pathlib
import sys
import time
import urllib.request

import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
D = R / "dados/brutos/senado/processos"
D.mkdir(parents=True, exist_ok=True)
SA = R / "resultados"
MAN = []
sys.path.insert(0, str(R))
from congresso27.base import PRES


def pega(sigla, ano):
    arq = D / f"{sigla}-{ano}.json"
    url = f"https://legis.senado.leg.br/dadosabertos/processo?sigla={sigla}&ano={ano}"
    if not arq.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        for t in range(4):
            try:
                arq.write_bytes(urllib.request.urlopen(req, timeout=120).read())
                break
            except Exception as e:
                print("erro", url, e, file=sys.stderr)
                time.sleep(4)
    b = arq.read_bytes()
    MAN.append({"url": url, "arquivo": arq.name, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
    return json.loads(b)


linhas = []
for ano in range(2003, 2027):
    for s in ("MPV", "VET"):
        for x in pega(s, ano):
            linhas.append({"sigla": s, "ano": ano, "id": x.get("identificacao"), "autoria": x.get("autoria"), "delib": x.get("siglaTipoDeliberacao"),
                           "situacao": x.get("situacaoAtual"), "norma": x.get("normaGerada"), "tramitando": x.get("tramitando"),
                           "data_delib": x.get("dataDeliberacao"), "ementa": (x.get("ementa") or "")[:300]})
A = pd.DataFrame(linhas)
A.to_csv(SA / "c5_processos_mp_veto.csv", index=False, encoding="utf-8")
(R / "dados/MANIFESTO_PROCESSOS.json").write_text(json.dumps(MAN, indent=1), encoding="utf8")
print(A.groupby("sigla").delib.value_counts(dropna=False).to_string())
print(A[A.sigla == "MPV"].situacao.value_counts().head(20).to_string())

# MP: virou lei x perdeu a validade, por ano de edicao
M = A[A.sigla == "MPV"].copy()
s = M.situacao.fillna("").str.upper()
d = M.delib.fillna("").str.upper()
M["virou_lei"] = s.str.contains("TRANSFORMADA") | d.str.contains("APROVADO") | M.norma.fillna("").str.startswith("Lei")
M["caducou"] = s.str.contains("VIG.NCIA ENCERRADA|PERDA|PREJUDIC|REJEITADA|REVOGADA") & ~M.virou_lei
Mm = M.groupby("ano").agg(editadas=("id", "count"), viraram_lei=("virou_lei", "sum"), nao_viraram=("caducou", "sum"), em_aberto=("tramitando", lambda x: (x == "Sim").sum()))
Mm["pct_lei"] = (Mm.viraram_lei / Mm.editadas * 100).round(1)
Mm["presidente"] = [PRES[a] for a in Mm.index]
Mm.to_csv(SA / "c5_mp_por_ano.csv")
print(Mm.to_string())

# Veto: derrubado total ou parcial
V = A[A.sigla == "VET"].copy()
dv = V.delib.fillna("")
V["derrubado_total"] = dv.str.contains("REJEITADO") & ~dv.str.contains("PARCIAL")
V["derrubado_parcial"] = dv.str.contains("REJEITADO_PARCIALMENTE|MANTIDO_PARCIALMENTE|PARCIAL")
Vm = V.groupby("ano").agg(vetos=("id", "count"), total=("derrubado_total", "sum"), parcial=("derrubado_parcial", "sum"), em_aberto=("tramitando", lambda x: (x == "Sim").sum()))
Vm["presidente"] = [PRES[a] for a in Vm.index]
Vm["pct_com_algo_derrubado"] = ((Vm.total + Vm.parcial) / (Vm.vetos - Vm.em_aberto).clip(lower=1) * 100).round(1)
Vm.to_csv(SA / "c5_veto_por_ano.csv")
print(Vm.to_string())
print(V.delib.value_counts(dropna=False).to_string())
porp = pd.DataFrame({"mp_pct_lei": Mm.groupby("presidente").viraram_lei.sum() / Mm.groupby("presidente").editadas.sum() * 100,
                     "mp_editadas": Mm.groupby("presidente").editadas.sum(),
                     "vetos": Vm.groupby("presidente").vetos.sum(),
                     "vetos_derrubados_algum": (Vm.groupby("presidente").total.sum() + Vm.groupby("presidente").parcial.sum())}).round(1)
porp.to_csv(SA / "c5_mp_veto_por_presidente.csv")
print(porp.to_string())
(SA / "RESUMO_PROCESSOS.json").write_text(json.dumps({"mp_por_ano": json.loads(Mm.to_json(orient="index")), "veto_por_ano": json.loads(Vm.to_json(orient="index")), "por_presidente": json.loads(porp.to_json(orient="index"))}, indent=1, ensure_ascii=False), encoding="utf8")
