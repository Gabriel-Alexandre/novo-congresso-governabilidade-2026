"""As votacoes de merito disputadas, com a materia, para a tabela das marcantes."""
import pandas as pd, pathlib, re
R = pathlib.Path(__file__).resolve().parents[1]
r = pd.read_csv(R/"resultados/c2_replay_2027.csv", dtype={"idVotacao":str})
ob = []
for a in range(2023,2027):
    o = pd.read_csv(R/f"dados/brutos/camara/votacoesObjetos-{a}.csv", sep=";", dtype=str, encoding="utf-8-sig", usecols=lambda c: c in("idVotacao","proposicao_siglaTipo","proposicao_numero","proposicao_ano","proposicao_ementa","proposicao_titulo","proposicao_id"))
    ob.append(o)
O = pd.concat(ob).drop_duplicates("idVotacao")
O["materia"] = O.proposicao_titulo if "proposicao_titulo" in O else O.proposicao_siglaTipo+" "+O.proposicao_numero+"/"+O.proposicao_ano
x = r.merge(O, how="left", on="idVotacao")
proc = x.descricao.fillna("").str.contains(r"Requerimento|Urg[eê]ncia|Retirada|Adiamento|Prefer[eê]ncia|Destaque|Encerramento|Mantido o texto|Suprimido o texto|Emenda de Plen", case=False, regex=True)
x["merito"] = ~proc
x.to_csv(R/"resultados/c7_disputadas_com_materia.csv", index=False, encoding="utf-8")
m = x[x.merito].sort_values("data")
print(len(m), m.gov_venceu.mean()*100, m.venceu.mean()*100)
pd.set_option("display.width",250)
print(m[["data","materia","com_gov","contra_gov","com","contra","gov_venceu","venceu","proposicao_ementa"]].round(0).to_string(max_colwidth=70))
