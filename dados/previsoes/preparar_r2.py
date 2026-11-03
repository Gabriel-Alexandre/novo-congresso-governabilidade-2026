"""Gera o dossie, as perguntas e os cenarios da rodada 2, com as correcoes da revisao. Roda uma vez, antes das respostas."""
import csv
import pathlib

BASE = pathlib.Path(__file__).resolve().parent
R = BASE
d = (R / "dossie.md").read_text(encoding="utf8")
i = d.index("## O teste com as votações reais")
j = d.index("## Fatos da articulação")
novo = """## O teste com as votações reais (conta deste repositório, corrigida depois de revisão)
- Atenção de vocabulário: "pêndulo" são as 257 cadeiras que não são da esquerda (124) nem de PL e Novo (132). Inclui União, PP e Republicanos, que se declaram direita.
- Câmara. Repetindo 678 votações nominais disputadas de 2023 a 2026 com os 513 eleitos (reeleito repete o voto, novo vota como a sigla): governo vence 81,4% contra 82,0% reais, 4 viram contra. É retrato com o pêndulo votando igual, não previsão. Em 2025 e 2026: 77,1 contra 77,7. Desde 09/jul/2025: 70,3 contra 71,1. Contando as votações sem orientação do governo pela posição do PT: 76,5 no período e 72,5 e 74,5 em 2025 e 2026. Com perdedor em pelo menos 40% dos votos, 66 contra 73. Só mérito, por ano: 89,7; 91,7; 74,0; 72,7. Novatos do pêndulo a meio caminho do PL: 78,5; iguais ao PL: 72,1.
- Votos com o governo, normalizados à presença real: mediana cai de 277 para 262,5. Votações com 257 votos ou mais com o governo: de 65% para 56%. Com 308 ou mais: de 28% para 19%. Com 172 ou mais: 83%. Oposição com 342 ou mais em 11 de 678. Votação comum não é impeachment.
- Com a maioria do pêndulo o governo venceu 548 de 548; sem ela, 8 de 130. Alinhamento do pêndulo com o governo: 73,1 em 2023; 68,0; 62,1; 65,0 em 2026.
- Senado. 83 votações nominais abertas disputadas, 53 matérias, posição do governo aproximada pela bancada do PT (coincide com o líder do governo em 96% sem contar ele). Governo vence 32,5% contra 66,3% reais; faixa honesta de 30 a 45 pelas variantes (de 17 no piso a 41); intervalo por matéria de 23 a 44. Em 2025 e 2026 são só 19 votações: de 53 para 42. Mediana de votos com o governo de 39 para 29. 41 votos com o governo em 16% contra 47% reais; 49 votos em 2%. Oposição com 49 em 17% e com 54 em 7%. Trazer 4 senadores do outro lado leva a 53%; 8 leva a 66%. 40 senadores não têm histórico no Senado. O mesmo método errou de 14 a 30 pontos a distância: acerta retrato.
- Vitórias do governo nas disputadas por ano, 1º ano de mandato: 2003 100 (só 12 votações); 2007 93,3; 2011 92,7; 2015 71,1; 2019 88,3; 2023 88,3. Lula III: 88,3; 84,0; 77,3; 79,2. Dilma em 2015, ano anterior ao impeachment: 71,1, igual à do Lula desde jul/2025. A taxa não avisa queda. Teste do passado: erro médio de 3,6 pontos contra 4,1 de só repetir o mandato anterior, em 3 casos.
- MPs que viraram lei por data e autor: Lula I 91%; Lula II 83%; Dilma I 75%; Dilma II 77%; Temer 57%; Bolsonaro 58%; Lula III 21%. Sem crédito extraordinário: 90; 82; 77; 80; 60; 68; 20. Lula III: 154 perderam a validade, 12 revogadas, 0 rejeitadas no voto; não se mediu quantas viraram projeto de lei.
- Vetos com algo derrubado, dos decididos: Dilma II 8%; Temer 17%; Bolsonaro 45%; Lula III 52% (46 de 89). Em 24 meses, Lula III e Bolsonaro empatam, perto de 44%. Antes de 2013 a regra era outra, e muitos vetos nem eram votados.
- Tarifa de 50% em jul/2025: pêndulo votou com o governo 71,8% nos 120 dias antes e 59,7% nos 120 depois, e agosto subiu a 78,5. Placebo em 61 datas tem desvio de 12,9 pontos: a tarifa não uniu o plenário, e não dá para dizer mais que isso.

"""
d = d[:i] + novo + d[j:]
d = d.replace("Quaest 24/out: aprova 48, desaprova 45.", "Quaest 24/out: aprova 48, desaprova 45. Datafolha já deu 24% de ótimo/bom a Lula em fev/2025.")
d = d.replace("Presidente eleito com pedido recebido e processo aberto desde 1990: Collor e Dilma, 2 em cerca de 36 anos de mandato, cerca de 5,5% ao ano.", "Presidente eleito com denúncia recebida desde 1990: Collor e Dilma, 2 em 32 anos de mandato de eleitos, cerca de 6% ao ano, com intervalo de 0,7% a 20%. Temer teve 2 denúncias da PGR barradas pela Câmara.")
d = d.replace("# Fatos e contas até 02/nov/2026", "# Fatos e contas até 02/nov/2026 (rodada 2)")
(R / "dossie_r2.md").write_text(d, encoding="utf8")
q = list(csv.DictReader(open(R / "perguntas.csv", encoding="utf8")))
ch = {
    "P01": ("Hugo Motta é reeleito presidente da Câmara na eleição de fevereiro de 2027", "2027-02-28", "resultado oficial da Câmara"),
    "P02": ("Davi Alcolumbre é reeleito presidente do Senado na eleição de fevereiro de 2027", "2027-02-28", "resultado oficial do Senado"),
    "P03": ("O PL integra formalmente o bloco de Motta na eleição da Mesa", "2027-02-28", "registro oficial do bloco; apoio sem bloco formal vale não"),
    "P04": ("PSD e MDB somam pelo menos 4 ministros filiados no governo em 30/04/2027", "2027-04-30", "foto em 30/04; conta ministro de Estado filiado ao partido, segundo duas agências"),
    "P05": ("Há ao menos 1 ministro filiado a União ou PP no governo em 30/04/2027", "2027-04-30", "foto em 30/04; ministro de Estado filiado, segundo duas agências; decisão formal do partido não é exigida"),
    "P08": ("O governo vence pelo menos 75% das votações nominais disputadas da Câmara em 2027", "2027-12-31", "script ferramentas/analise_camara.py deste repositório, piso de 30 votações; só onde o governo orientou"),
    "P09": ("O governo vence pelo menos 85% das votações nominais disputadas da Câmara em 2027", "2027-12-31", "mesmo script, piso de 30 votações"),
    "P10": ("A posição da bancada do PT vence pelo menos 50% das votações nominais abertas disputadas do Senado em 2027", "2027-12-31", "script ferramentas/rodada2.py, piso de 15 votações; sem o piso, resolve não"),
    "P11": ("O Congresso derruba total ou parcialmente pelo menos 5 mensagens de veto de Lula em 2027", "2027-12-31", "dados do Congresso; processo VET com rótulo REJEITADO_PLENARIO ou MANTIDO_PARCIALMENTE, ato de votação em 2027"),
    "P12": ("Pelo menos 30% das MPs editadas em 2027 viram lei", "2028-06-30", "norma publicada; dados do Congresso"),
    "P14": ("Lei ou emenda que extinga a punibilidade de Jair Bolsonaro pelos atos de 8 de janeiro é aprovada pelas 2 Casas", "2027-12-31", "resultado oficial; redução de pena não conta"),
    "P15": ("O presidente do Senado faz a leitura ou instala comissão de pedido de impeachment de ministro do STF", "2027-12-31", "ato oficial; protocolo não conta"),
    "P17": ("O presidente da Câmara despacha o recebimento de denúncia de crime de responsabilidade contra Lula", "2027-12-31", "despacho oficial; protocolo de pedido não conta"),
    "P19": ("Lula deixa a Presidência antes do fim do mandato por impeachment ou renúncia diante de processo", "2030-12-31", "resultado oficial; saída por saúde não conta"),
    "P20": ("O Datafolha registra avaliação ótimo ou bom de Lula abaixo de 25% em alguma pesquisa", "2027-12-31", "pesquisa publicada do Datafolha; é a avaliação do governo, não a aprovação"),
    "P22": ("O Congresso aprova mudança na meta de 2027 para um resultado pior que o da LDO original", "2027-12-31", "lei publicada; exceção à meta não conta"),
    "P23": ("É instalada CPI ou CPMI cujo requerimento cita ato de autoridade federal do governo Lula como objeto", "2027-12-31", "ato oficial de instalação e texto do requerimento"),
    "P24": ("Delegação dos EUA à posse de Lula é anunciada pelo governo americano", "2027-01-05", "anúncio do Departamento de Estado ou da Casa Branca, ou duas agências; encarregado de negócios por conta própria não conta"),
    "P26": ("A PEC da reforma administrativa é aprovada em 2 turnos no plenário da Câmara", "2027-12-31", "resultado oficial"),
}
for x in q:
    if x["id"] in ch:
        x["pergunta"], x["prazo"], x["resolve_sim_se"] = ch[x["id"]]
q.append({"id": "P27", "pergunta": "Lula deixa a Presidência por qualquer motivo, inclusive saúde", "prazo": "2027-12-31", "resolve_sim_se": "fato oficial"})
q.append({"id": "P28", "pergunta": "O governo vence pelo menos 70% das votações nominais disputadas da Câmara em 2027", "prazo": "2027-12-31", "resolve_sim_se": "mesmo script de P08, piso de 30 votações"})
with open(R / "perguntas_r2.csv", "w", encoding="utf8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=q[0].keys())
    w.writeheader()
    w.writerows(q)
c = [
    {"id": "C4", "ordem": 1, "cenario": "A ruptura", "descricao": "Denúncia de crime de responsabilidade recebida contra Lula", "regra_de_resolucao_em_31_12_2027": "P17 resolve sim, ou renúncia diante de processo"},
    {"id": "C3", "ordem": 2, "cenario": "A trava", "descricao": "Sem processo; o Congresso toca a própria pauta e o governo perde parte grande das disputas", "regra_de_resolucao_em_31_12_2027": "não é C4; e o governo venceu menos de 70% das disputadas da Câmara em 2027, ou o Senado rejeitou mais uma indicação ao STF"},
    {"id": "C2", "ordem": 3, "cenario": "A folga", "descricao": "Ganha quase tudo e aprova o que precisa de muitos votos", "regra_de_resolucao_em_31_12_2027": "não é C4 nem C3; venceu pelo menos 85% na Câmara e aprovou um indicado ao STF ou uma PEC de iniciativa do governo"},
    {"id": "C1", "ordem": 4, "cenario": "A negociação caso a caso", "descricao": "Vence de 70% a 85% na Câmara, ou mais sem a vitória grande; depende do pêndulo a cada votação; sem rejeição nova no STF", "regra_de_resolucao_em_31_12_2027": "todos os outros casos"},
]
with open(R / "cenarios_r2.csv", "w", encoding="utf8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=c[0].keys())
    w.writeheader()
    w.writerows(c)
hp = BASE.parent / "e_hipoteses.csv"
h = hp.read_text(encoding="utf8").splitlines()
linhas = [["id", "evidencia", "H1_folga", "H2_negocia", "H3_trava", "H4_cai"]]
for l in h[1:]:
    p = l.split(",")
    linhas.append([p[0], ",".join(p[1:-4])] + p[-4:])
novas = {"E02": "No Senado o mesmo teste cai de 66% para cerca de 32%, faixa de 30 a 45", "E04": "Vetos com algo derrubado: 52% dos decididos em Lula III e 45% em Bolsonaro; 8% em Dilma II", "E05": "MPs que viram lei: 21% em Lula III contra 91% em Lula I; nenhuma rejeitada no voto", "E17": "Tarifa de 2025 não uniu o plenário"}
for x in linhas:
    if x[0] in novas:
        x[1] = novas[x[0]]
with open(hp, "w", encoding="utf8", newline="") as f:
    csv.writer(f).writerows(linhas)
print(len(q), "perguntas")
