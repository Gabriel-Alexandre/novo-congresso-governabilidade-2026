"""Refaz os numeros centrais sem importar o modelo: csv puro, dicionarios, outra logica. Publica so com 100% passando."""
import csv
import json
import pathlib
from collections import Counter, defaultdict

R = pathlib.Path(__file__).resolve().parents[1]
B = R / "dados/brutos/camara"
CHECK = []


def ok(nome, a, b, tol=0.0):
    p = abs(float(a) - float(b)) <= tol
    CHECK.append({"item": nome, "modelo": a, "refeito": b, "tol": tol, "passou": p})
    print(("PASSOU" if p else "FALHOU"), nome, a, b)


def ler(nome):
    with open(B / nome, encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f, delimiter=";")


def serie(ano):
    gov = {}
    for x in ler(f"votacoesOrientacoes-{ano}.csv"):
        if x["siglaBancada"].strip().upper() in ("GOV.", "GOVERNO", "GOV") and x["orientacao"].strip() in ("Sim", "Não") and x["idVotacao"] not in gov:
            gov[x["idVotacao"]] = x["orientacao"].strip()
    org = {x["id"]: x["siglaOrgao"] for x in ler(f"votacoes-{ano}.csv")}
    cont = defaultdict(Counter)
    votos = defaultdict(dict)
    for x in ler(f"votacoesVotos-{ano}.csv"):
        if x["idVotacao"] in gov:
            cont[x["idVotacao"]][x["voto"]] += 1
            votos[x["idVotacao"]][x["deputado_id"]] = (x["voto"], x["deputado_siglaPartido"].strip().upper())
    out = {}
    for v, g in gov.items():
        s, n = cont[v]["Sim"], cont[v]["Não"]
        if org.get(v, "PLEN") not in ("PLEN", "", None) or s + n < 100:
            continue
        com, contra = (s, n) if g == "Sim" else (n, s)
        out[v] = {"g": g, "com": com, "contra": contra, "disp": min(com, contra) / (com + contra) >= .10}
    return out, votos


res = json.loads((R / "resultados/RESUMO_CAMARA.json").read_text(encoding="utf8"))
RS = {}
for ano in (2003, 2015, 2021, 2023, 2024, 2025, 2026):
    s, v = serie(ano)
    d = [x for x in s.values() if x["disp"]]
    RS[ano] = (s, v, d)
    ok(f"vitoria nas disputadas {ano}", res["serie_por_ano"][str(ano)]["vitoria_disputadas"], round(sum(x["com"] > x["contra"] for x in d) / len(d) * 100, 1), .05)
    ok(f"numero de disputadas {ano}", res["serie_por_ano"][str(ano)]["disputadas"], len(d))

# fatos publicos conhecidos: PDL do IOF em 25/06/2025 (383 a 98)
achou = False
s25, v25, _ = RS[2025]
for k, x in s25.items():
    if x["contra"] == 383 and x["com"] == 98:
        achou = True
ok("o placar do decreto do IOF aparece como 98 com o governo e 383 contra", 1, int(achou))

# replay de 2023 refeito por dicionarios, sem a funcao do modelo
EL = list(csv.DictReader(open(R / "dados/derivados/eleitos_2026_camara.csv", encoding="utf-8")))
AL = {"UNIÃO": "UNIAO", "MISSÃO": "NOVO", "PODEMOS": "PODE", "SDD": "SOLIDARIEDADE", "PATRIOTA": "PRD", "PTB": "PRD", "PATRI": "PRD", "REPUBLICANO": "REPUBLICANOS", "PC DO B": "PCDOB"}
def nsig(x):
    x = x.strip().upper()
    return AL.get(x, x)
ids = [e["deputado_id"] for e in EL]
sigs = [nsig(e["SG_PARTIDO"]) for e in EL]
def rep(ano):
    s, v, _ = RS[ano]
    tam = defaultdict(set)
    for vid, x in s.items():
        if x["disp"]:
            for d, (_, p) in v[vid].items():
                tam[nsig(p)].add(d)
    venc = meds = 0
    total = 0
    coms = []
    for vid, x in s.items():
        if not x["disp"]:
            continue
        por = defaultdict(lambda: [0, 0])
        vv = v[vid]
        for d, (voto, p) in vv.items():
            if voto in ("Sim", "Não"):
                por[nsig(p)][0 if voto == x["g"] else 1] += 1
        tc = sum(a for a, _ in por.values())
        tx = sum(b for _, b in por.values())
        com = contra = 0.0
        for d, sg in zip(ids, sigs):
            if d in vv:
                voto = vv[d][0]
                if voto == x["g"]:
                    com += 1
                elif voto in ("Sim", "Não"):
                    contra += 1
            else:
                a, b = por[sg] if sg in por else (0, 0)
                if a + b > 0:
                    pres = min(1, (a + b) / len(tam[sg]))
                    com += pres * a / (a + b)
                    contra += pres * b / (a + b)
                else:
                    pres = (tc + tx) / 513
                    com += pres * tc / (tc + tx)
                    contra += pres * tx / (tc + tx)
        venc += com > contra
        total += 1
        coms.append(com)
    return round(venc / total * 100, 1), total
for ano in (2023, 2024, 2025, 2026):
    p, n = rep(ano)
    # o modelo usa a sigla do ano inteiro; a validacao usa so as disputadas para o tamanho: tolerancia de 1 ponto
    ok(f"replay {ano} (vitoria com a composicao de 2027)", res["replay_por_ano"][str(ano)]["vitoria_replay_pct"], p, 1.0)

# bancadas contra o projeto do video 6
EX = {"PL": 121, "PT": 70, "PSD": 43, "MDB": 36}
c = Counter(sigs)
for k, n in EX.items():
    ok(f"bancada eleita {k}", c[k], n)
ok("total de eleitos", len(EL), 513)
# senado: composicao
import pandas as pd
A = pd.read_csv(R.parent / "congresso-e-governos-eleicoes-2026/resultados/a2_composicao_fev2027.csv")
ok("senadores na composicao de 2027", len(A), 81)
ok("PL no Senado em 2027", (A.partido == "PL").sum(), 28)
Sn = json.loads((R / "resultados/RESUMO_SENADO.json").read_text(encoding="utf8"))
ok("Senado: acordo do placar com o resultado oficial acima de 95%", 1, int(Sn["acordo_com_resultado_oficial_pct"] >= 95))
# MP e veto da rodada 2: conta direta a partir das respostas brutas, sem o codigo do modelo
R2 = json.loads((R / "resultados/RESUMO.json").read_text(encoding="utf8"))
ed = lei = 0
for a in range(2023, 2027):
    for x in json.loads((R / f"dados/brutos/senado/processos/MPV-{a}.json").read_text(encoding="utf8")):
        if (x.get("dataApresentacao") or "") >= "2023-01-02":
            ed += 1
            s = (x.get("situacaoAtual") or "").upper()
            d = x.get("siglaTipoDeliberacao") or ""
            nr = x.get("normaGerada") or ""
            if ("TRANSFORMADA EM NORMA" in s or nr.startswith("Lei") or d.startswith("APROVADO")) and "SEM EFIC" not in s and "VETADA" not in s and not (x["dataApresentacao"] >= "2026-01-01" and not nr):
                lei += 1
ok("MPs editadas em Lula III", R2["mp"]["Lula III"]["editadas"], ed, 1)
ok("MPs que viraram lei em Lula III", R2["mp"]["Lula III"]["lei"], lei, 1)
cam = R2["camara"]
ok("replay total (2023 a 2026), media dos anos pesada", cam["total"]["novo_pct"], round(sum(res["replay_por_ano"][str(a)]["vitoria_replay_pct"] * res["replay_por_ano"][str(a)]["n"] for a in (2023, 2024, 2025, 2026)) / cam["total"]["n"], 1), .1)
ok("cadeiras somam 513", sum(R2["cadeiras"].values()), 513)
(R / "resultados/validacao_independente.json").write_text(json.dumps(CHECK, indent=1, ensure_ascii=False, default=str), encoding="utf8")
f = [c for c in CHECK if not c["passou"]]
print(len(CHECK), "itens,", len(f), "falharam")
