"""Senado: posicao do governo aproximada pelo voto da bancada do PT; replay de 2023-2026 com a composicao de fev/2027."""
import json
import pathlib
import re
import sys
import unicodedata

import numpy as np
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R))
from congresso27.base import sig

SA = R / "resultados"


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z ]", "", s).strip()


def carregar(anos):
    linhas = []
    meta = []
    for a in anos:
        for sem in (1, 2):
            p = R / f"dados/brutos/senado/votacoes-{a}-{sem}.json"
            if not p.exists():
                continue
            for x in json.loads(p.read_text(encoding="utf8")):
                if x.get("votacaoSecreta") == "S":
                    continue
                vid = x["codigoSessaoVotacao"]
                meta.append({"vid": vid, "ano": a, "data": x.get("dataSessao"), "materia": x.get("identificacao"), "ementa": (x.get("ementa") or "")[:200], "desc": (x.get("descricaoVotacao") or "")[:200], "res": x.get("resultadoVotacao")})
                for v in x.get("votos", []):
                    if v["siglaVotoParlamentar"] in ("Sim", "Não"):
                        linhas.append({"vid": vid, "cod": v["codigoParlamentar"], "nome": v["nomeParlamentar"], "sig": sig(v["siglaPartidoParlamentar"]), "voto": v["siglaVotoParlamentar"], "ano": a})
    return pd.DataFrame(linhas), pd.DataFrame(meta).drop_duplicates("vid").set_index("vid")


def posicao_pt(L):
    """Voto da maioria da bancada do PT, quando pelo menos 3 votaram e 75% concordaram."""
    pt = L[L.sig == "PT"].groupby("vid").voto.agg(lambda x: (x == "Sim").mean())
    n = L[L.sig == "PT"].groupby("vid").voto.count()
    ok = n[n >= 3].index
    pt = pt[pt.index.isin(ok)]
    return pd.Series(np.where(pt >= .75, "Sim", np.where(pt <= .25, "Não", None)), index=pt.index).dropna()


L, M = carregar(range(2023, 2027))
g = posicao_pt(L)
L = L[L.vid.isin(g.index)].copy()
L["orient"] = L.vid.map(g)
L["com"] = (L.voto == L.orient).astype(int)
t = L.groupby("vid").com.agg(["sum", "count"]).rename(columns={"sum": "com_gov", "count": "tot"})
t["contra_gov"] = t.tot - t.com_gov
t = t[t.tot >= 41].copy()
t["venceu"] = t.com_gov > t.contra_gov
t["disputada"] = t[["com_gov", "contra_gov"]].min(axis=1) / t.tot >= .10
t = t.join(M)
print(len(t), t.disputada.sum())
print(t.groupby("ano").apply(lambda x: pd.Series({"n": len(x), "disp": x.disputada.sum(), "vit_todas": x.venceu.mean() * 100, "vit_disp": x[x.disputada].venceu.mean() * 100, "med": x[x.disputada].com_gov.median()}), include_groups=False).round(1).to_string())
C = pd.read_csv(R.parent / "congresso-e-governos-eleicoes-2026/resultados/a2_composicao_fev2027.csv")
C["k"] = C.nome.map(norm)
C["sig"] = C.sig.fillna(C.partido).map(sig)
nomes = L.drop_duplicates("cod").assign(k=lambda d: d.nome.map(norm))[["cod", "k", "nome"]]
Cm = C.merge(nomes, how="left", on="k", suffixes=("", "_sen"))
# segunda via: nome de urna contido no nome parlamentar (primeiro e ultimo nome)
for i, r in Cm[Cm.cod.isna()].iterrows():
    p = r.k.split()
    achou = nomes[nomes.k.map(lambda s: s.split()[0] == p[0] and s.split()[-1] == p[-1])]
    if len(achou) == 1:
        Cm.loc[i, "cod"] = achou.iloc[0].cod
Cm.to_csv(SA / "s0_composicao_2027_casada.csv", index=False, encoding="utf-8")
print(len(Cm), "senadores", Cm.cod.notna().sum(), "com historico 2023-26")
print(Cm[Cm.cod.isna()][["uf", "nome", "sig"]].to_string())

ids = t[t.disputada].index
linhas = []
Ld = L[L.vid.isin(ids)]
tam = Ld.groupby("sig").cod.nunique()
for vid, sub in Ld.groupby("vid"):
    sub = sub.drop_duplicates("cod").set_index("cod")
    com = contra = 0.0
    pg = sub.groupby("sig").com.agg(["sum", "count"])
    pres_casa = len(sub) / 81
    parte = sub.com.mean()
    for _, r in Cm.iterrows():
        if pd.notna(r.cod) and r.cod in sub.index:
            c = sub.loc[r.cod, "com"]
            com += c
            contra += 1 - c
        elif r.sig in pg.index:
            pres = min(1.0, pg.loc[r.sig, "count"] / tam[r.sig])
            s = pg.loc[r.sig, "sum"] / pg.loc[r.sig, "count"]
            com += pres * s
            contra += pres * (1 - s)
        else:
            com += pres_casa * parte
            contra += pres_casa * (1 - parte)
    linhas.append({"vid": vid, "com": com, "contra": contra, "venceu_2027": com > contra})
r = pd.DataFrame(linhas).set_index("vid").join(t)
r.round(2).to_csv(SA / "s1_replay_senado_2027.csv")
def blo(x):
    return {"n": len(x), "vitoria_real_pct": round(x.venceu.mean() * 100, 1), "vitoria_2027_pct": round(x.venceu_2027.mean() * 100, 1), "virariam_contra": int((x.venceu & ~x.venceu_2027).sum()), "mediana_com_real": float(x.com_gov.median()), "mediana_com_2027": round(float(x.com.median()), 1), "p10_com_2027": round(float(x.com.quantile(.1)), 1), "pct_com_27": round((x.com >= 27).mean() * 100, 1), "pct_com_41": round((x.com >= 41).mean() * 100, 1), "pct_contra_41": round((x.contra >= 41).mean() * 100, 1), "pct_contra_49": round((x.contra >= 49).mean() * 100, 1), "pct_contra_54": round((x.contra >= 54).mean() * 100, 1), "max_contra": round(float(x.contra.max()), 1)}
RES = {"total": blo(r), "por_ano": {int(a): blo(g) for a, g in r.groupby("ano")}}
print(json.dumps(RES["total"]))
print(pd.DataFrame(RES["por_ano"]).T.to_string())
Pa = Ld.groupby("sig").com.mean().mul(100).round(1)
Es = pd.DataFrame({"cadeiras_2027": Cm.sig.value_counts()}).join(Pa.rename("alinhamento_2023_26")).sort_values("alinhamento_2023_26", ascending=False)
Es["acum"] = Es.cadeiras_2027.cumsum()
Es.to_csv(SA / "s2_escada_senado.csv")
print(Es.to_string())
RES["escada"] = json.loads(Es.reset_index(names="sig").to_json(orient="records"))
RES["senadores_com_historico"] = int(Cm.cod.notna().sum())
# sensibilidade: lider do governo como posicao, em vez da bancada do PT (Jaques Wagner)
wag = L[L.nome.str.contains("Jaques Wagner")]
RES["concordancia_jaques_wagner_com_pt_pct"] = round(wag.com.mean() * 100, 1)
print("Wagner x PT", RES["concordancia_jaques_wagner_com_pt_pct"], len(wag))
(SA / "RESUMO_SENADO.json").write_text(json.dumps(RES, indent=1, ensure_ascii=False), encoding="utf8")

# Variantes do Senado
AP = pd.read_csv(R.parent / "congresso-e-governos-eleicoes-2026/dados/senado_apoio_flavio.csv")
AP["k"] = AP.candidato.map(norm)
def primeiro_ultimo(s):
    p = s.split()
    return (p[0], p[-1]) if p else ("", "")
pu = set(AP.k.map(primeiro_ultimo))
Cm["apoiou_flavio"] = Cm.k.map(lambda s: primeiro_ultimo(s) in pu or s in set(AP.k))
RES["novos_senadores"] = int(Cm.cod.isna().sum())
RES["novos_que_apoiaram_flavio"] = int((Cm.cod.isna() & Cm.apoiou_flavio).sum())
def rejoga(fn_p):
    out = []
    for vid, sub in Ld.groupby("vid"):
        sub = sub.drop_duplicates("cod").set_index("cod")
        pg = sub.groupby("sig").com.agg(["sum", "count"])
        pres_casa, parte = len(sub) / 81, sub.com.mean()
        com = contra = 0.0
        for _, x in Cm.iterrows():
            if pd.notna(x.cod) and x.cod in sub.index:
                c = sub.loc[x.cod, "com"]; com += c; contra += 1 - c; continue
            pres, s = fn_p(x, pg, pres_casa, parte)
            com += pres * s; contra += pres * (1 - s)
        out.append({"vid": vid, "com": com, "contra": contra, "venceu": com > contra})
    return pd.DataFrame(out).set_index("vid")
def p_sig(s, pg, pres_casa, parte):
    if s in pg.index:
        return min(1.0, pg.loc[s, "count"] / tam[s]), pg.loc[s, "sum"] / pg.loc[s, "count"]
    return pres_casa, parte
def v_apoio(x, pg, pc, pa):
    # novo senador que declarou apoio ao Flavio vota como o PL; os outros, como a propria sigla
    return p_sig("PL" if x.apoiou_flavio else x.sig, pg, pc, pa)
def v_otimista(x, pg, pc, pa):
    # novo senador de sigla fora de PL/NOVO e sem apoio declarado ao Flavio vota como o MDB, a sigla de centro mais proxima do governo
    if x.apoiou_flavio or x.sig in ("PL", "NOVO"):
        return p_sig(x.sig, pg, pc, pa)
    return p_sig("MDB" if x.sig not in ("PT", "PSB", "PDT", "REDE") else x.sig, pg, pc, pa)
for nome, fn in (("v1_novo_com_apoio_flavio_como_PL", v_apoio), ("v2_otimista_novos_de_centro_como_MDB", v_otimista)):
    rv = rejoga(fn)
    RES[nome] = {"vitoria_pct": round(rv.venceu.mean() * 100, 1), "mediana_com": round(float(rv.com.median()), 1), "pct_com_41": round((rv.com >= 41).mean() * 100, 1), "pct_contra_41": round((rv.contra >= 41).mean() * 100, 1), "pct_contra_49": round((rv.contra >= 49).mean() * 100, 1), "pct_contra_54": round((rv.contra >= 54).mean() * 100, 1)}
    print(nome, RES[nome])
# controle: quem votou em 2024 repete 2024
L24 = Ld[Ld.ano == 2024]
print("controle: disputadas 2024", L24.vid.nunique())
# concordancia com o resultado oficial do Senado
chk = t.join(pd.DataFrame([{"vid": v} for v in []]) if False else M[["res"]].rename(columns={"res": "res2"}))
ofic = chk[(chk.res2.isin(["A", "R"]))]
apr = np.where(ofic.res2 == "A", "Sim", "Não")
ori = L.drop_duplicates("vid").set_index("vid").orient.reindex(ofic.index)
RES["acordo_com_resultado_oficial_pct"] = round(float(((apr == ori) == ofic.venceu).mean() * 100), 1)
print("acordo oficial", RES["acordo_com_resultado_oficial_pct"], len(ofic))
# votacoes secretas: autoridades com placar mais apertado (2019-2026)
sec = []
for a in range(2019, 2027):
    for s_ in (1, 2):
        p = R / f"dados/brutos/senado/votacoes-{a}-{s_}.json"
        for x in json.loads(p.read_text(encoding="utf8")):
            if x.get("votacaoSecreta") == "S":
                sec.append({"ano": a, "data": x.get("dataSessao"), "materia": x.get("identificacao"), "ementa": (x.get("ementa") or "")[:160], "sim": int(x.get("totalVotosSim") or 0), "nao": int(x.get("totalVotosNao") or 0), "res": x.get("resultadoVotacao")})
S_ = pd.DataFrame(sec)
S_.to_csv(SA / "s3_votacoes_secretas.csv", index=False, encoding="utf-8")
print(len(S_), S_.groupby("ano").apply(lambda d: pd.Series({"n": len(d), "rejeitadas": (d.res == "R").sum(), "abaixo_50": (d.sim < 50).sum()}), include_groups=False).to_string())
print(S_[(S_.sim < 50) | (S_.res == "R")].sort_values("data").tail(22).to_string(max_colwidth=95))
RES["secretas"] = {"n": len(S_), "rejeitadas": int((S_.res == "R").sum()), "por_ano": {int(a): {"n": len(d), "rejeitadas": int((d.res == "R").sum())} for a, d in S_.groupby("ano")}}
(SA / "RESUMO_SENADO.json").write_text(json.dumps(RES, indent=1, ensure_ascii=False, default=str), encoding="utf8")
