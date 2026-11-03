"""Casa os 513 deputados eleitos em 2026 (TSE) com o cadastro da Camara por nome civil + nascimento."""
import pandas as pd, unicodedata, pathlib, re, zipfile, io, json
R = pathlib.Path(__file__).resolve().parents[1]
def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z ]", "", s).strip()
z = zipfile.ZipFile(R / "dados/brutos/tse/consulta_cand_2026.zip")
d = pd.read_csv(io.BytesIO(z.read("consulta_cand_2026_BRASIL.csv")), sep=";", encoding="latin1", dtype=str)
f = d[(d.DS_CARGO == "DEPUTADO FEDERAL") & d.DS_SIT_TOT_TURNO.str.startswith("ELEITO", na=False)].copy()
f["k_nome"] = f.NM_CANDIDATO.map(norm)
f["nasc"] = pd.to_datetime(f.DT_NASCIMENTO, dayfirst=True, errors="coerce").dt.strftime("%Y-%m-%d")
c = pd.read_csv(R / "dados/brutos/camara/deputados.csv", sep=";", dtype=str, encoding="utf-8-sig")
c["id"] = c.uri.str.extract(r"(\d+)$")
c["k_nome"] = c.nomeCivil.map(norm)
c["nasc"] = c.dataNascimento
m = f.merge(c[["id", "k_nome", "nasc", "idLegislaturaFinal", "nome"]], how="left", on=["k_nome", "nasc"])
sem = m[m.id.isna()].copy()
# segunda via: so a data de nascimento + primeiro e ultimo nome
c["pu"] = c.k_nome.map(lambda s: (s.split()[0], s.split()[-1]) if s else ("", ""))
ids = {}
for i, r in sem.iterrows():
    p = r.k_nome.split()
    cand = c[(c.nasc == r.nasc) & (c.pu.map(lambda x: x == (p[0], p[-1])))]
    if len(cand) == 1:
        ids[i] = cand.iloc[0]
for i, x in ids.items():
    m.loc[i, ["id", "idLegislaturaFinal", "nome"]] = [x.id, x.idLegislaturaFinal, x.nome]
saida = m[["NM_URNA_CANDIDATO", "NM_CANDIDATO", "SG_UF", "SG_PARTIDO", "SQ_CANDIDATO", "id", "idLegislaturaFinal", "DS_SIT_TOT_TURNO"]].rename(columns={"id": "deputado_id"})
assert saida.SQ_CANDIDATO.is_unique, "duplicata no casamento"
saida.to_csv(R / "dados/derivados/eleitos_2026_camara.csv", index=False, encoding="utf-8")
print(len(saida), "eleitos;", saida.deputado_id.notna().sum(), "com id;", (saida.idLegislaturaFinal == "57").sum(), "na 57;")
print(saida.SG_PARTIDO.value_counts().to_dict())
