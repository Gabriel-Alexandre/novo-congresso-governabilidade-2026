"""Junta as previsoes dos modelos: mediana, faixa, coerencia; e a matriz de hipoteses com a 2a codificacao."""
import csv
import glob
import json
import statistics
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "dados" / "previsoes"
FAIXAS = [(5, "quase nenhuma chance"), (20, "muito improvável"), (45, "improvável"), (55, "chance parecida"), (80, "provável"), (95, "muito provável"), (100, "quase certo")]


def faixa(p):
    return next(nome for limite, nome in FAIXAS if p <= limite)


arq = [json.load(open(a, encoding="utf-8")) for a in sorted(glob.glob(str(PASTA / "rodada2" / "*.json")))]
perg = list(csv.DictReader(open(PASTA / "perguntas_r2.csv", encoding="utf-8")))
cen = list(csv.DictReader(open(PASTA / "cenarios_r2.csv", encoding="utf-8")))
S = {"modelos": [a["modelo"] for a in arq], "perguntas": [], "cenarios": []}
for q in perg:
    v = {a["modelo"]: a["perguntas"][q["id"]]["p"] for a in arq}
    m = statistics.median(v.values())
    S["perguntas"].append({**q, "mediana": m, "menor": min(v.values()), "maior": max(v.values()), "faixa": faixa(m), "por_modelo": v})
    print(q["id"], m, f"[{min(v.values())}-{max(v.values())}]", faixa(m), q["pergunta"][:70])
for c in cen:
    v = {a["modelo"]: a["cenarios"][c["id"]] for a in arq}
    S["cenarios"].append({**c, "mediana": statistics.median(v.values()), "menor": min(v.values()), "maior": max(v.values()), "por_modelo": v})
tot = sum(c["mediana"] for c in S["cenarios"])
for c in S["cenarios"]:
    c["normalizado"] = round(c["mediana"] * 100 / tot, 1)
    print(c["id"], c["cenario"], c["mediana"], c["normalizado"], c["por_modelo"])
p = {q["id"]: q["mediana"] for q in S["perguntas"]}
c = {x["id"]: x["normalizado"] for x in S["cenarios"]}
CO = [("P09 <= P08", p["P09"] <= p["P08"]), ("P18 <= P17", p["P18"] <= p["P17"]), ("P16 <= P15", p["P16"] <= p["P15"]), ("P08 <= P28", p["P08"] <= p["P28"]), ("C2 <= P09", c["C2"] <= p["P09"]), ("C4 >= P17 - 1", c["C4"] + 1e-9 >= p["P17"] - 1), ("soma cenarios ~100", abs(sum(c.values()) - 100) < .5)]
S["coerencia"] = [{"teste": a, "passou": bool(b)} for a, b in CO]
print(CO)
S["discordancia_media_pontos"] = round(statistics.mean(q["maior"] - q["menor"] for q in S["perguntas"]), 1)
# hipoteses
H = ["H1_folga", "H2_negocia", "H3_trava", "H4_cai"]
A = list(csv.DictReader(open(RAIZ / "dados/e_hipoteses.csv", encoding="utf-8")))
B = {x["id"]: x for x in csv.DictReader(open(RAIZ / "dados/e_hipoteses_2a_codificacao.csv", encoding="utf-8"))}
conc = tot_c = 0
pl = {h: {"1a_I": 0, "2a_I": 0} for h in H}
for x in A:
    for h in H:
        tot_c += 1
        conc += x[h].strip() == B[x["id"]][h].strip()
        pl[h]["1a_I"] += x[h].strip() == "I"
        pl[h]["2a_I"] += B[x["id"]][h].strip() == "I"
S["hipoteses"] = {"inconsistencias": pl, "concordancia_pct": round(conc / tot_c * 100, 1), "n_celulas": tot_c}
print(S["hipoteses"])
json.dump(S, open(RAIZ / "resultados" / "previsoes_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
