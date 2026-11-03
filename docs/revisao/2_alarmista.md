# Revisão 2: o leitor que acha o Senado alarmista
Pergunta: "no Senado cai de 66% para 37%, mediana de 39 para 27" se sustenta? Tudo abaixo foi recontado sobre `dados/brutos`, sem alterar arquivo do projeto. "Corrigido" = presença que fecha o total real de votantes + Veneziano e Alessandro Vieira como veteranos.
## Veredito
A direção se sustenta e resistiu a todas as variantes razoáveis. Os números exatos não. A tese do "alarmismo" cai pela metade: há erros nos dois sentidos, e o método também é generoso com o governo em dois pontos. O que está exagerado é a forma de apresentar (66 contra 37 sem dizer que 2025 e 2026 já estavam em 53, e o "6% contra 47%").
## Dois defeitos no código
1. **Presença errada (`analise_senado.py`, `tam`).** A presença do novo é votantes da sigla ÷ nomes únicos da sigla em 4 anos (PSD 21 nomes, PL 23, para 5 e 28 cadeiras). O replay vota com 59 presentes, contra 66 reais. O resultado depende da amostra: 2023 dá 41,9% rodando tudo e 29,0% rodando só 2023. Na Câmara o desvio é o contrário (429,6 contra 407,5), então as duas Casas não estão na mesma régua.
2. **Dois senadores atuais tratados como novos.** "VENEZIANO" (cód. 5748, 88,9% com o PT) e "DELEGADO ALESSANDRO" (Alessandro Vieira, cód. 5982, 70%) não casaram pelo nome. São 41 com histórico e 40 novos, não 39 e 42.

| Medida | Projeto | Corrigido |
|---|---|---|
| Vitória nas 83 | 37,3% | **32,5%** |
| Mediana com o governo | 27,3 | **29,3** |
| Parcela mediana dos votantes | 45,7% | 44,4% |
| 41 votos com o governo (real 47%) | 6,0% | **15,7%** |

Corrigir a presença melhora votos e 41, e piora a vitória, porque o erro subcontava o PL. O "6%" é artefato; o "37%" não é exagero.
## Testes pedidos
| Teste | Real | Projeto | Corrigido |
|---|---|---|---|
| Posição = voto de Wagner, senão PT | 67,5 | 41,0 | 36,1 |
| Só onde Wagner e Randolfe votaram com o PT (65) | 73,8 | 38,5 | 32,3 |
| Sem as 7 duplicatas idênticas (76) | 67,1 | 36,8 | 31,6 |
| Deputados: taxa pessoal na Câmara | 66,3 | 42,2 | **33,7** (mediana 30,6) |
| Deputados: desvio pessoal sobre a sigla | 66,3 | 38,6 | 32,5 (mediana 29,5) |
| Novos pela sigla na Câmara, limite amigo | 66,3 | 50,6 | 43,4 |
| Fufuca e Julim do Lula como MDB | 66,3 | 41,0 | 34,9 |
| Lista do Flávio como PL (lista corrigida, 24) | 66,3 | 33,7 | 27,7 |
| Centro fora da lista como MDB | 66,3 | 45,8 | 41,0 |
| Piso: novo fora da esquerda como PL | 66,3 | 21,7 | 16,9 |

- **Câmara como histórico:** 19 eleitos têm voto em 2023-2026. A média pessoal deles (27,7%) é quase a da sigla no Senado que os substituía (26,5%). Sobem Julim 86, Fufuca 73 (60 votos) e Lira 60 (70 votos); descem Derrite 9 (PP) e Evair 6 (Republicanos), além de Gayer 5,9, De Toni 7,4 e Sanderson 7,7. Não resgata o governo. A escala das Casas difere (PP 64,7 na Câmara, 25,7 no Senado), por isso a linha da sigla é teto, não estimativa.
- **Proxy do PT:** os 98,1% de Wagner são circulares, ele está no grupo que define a posição. Sem ele: 95,9% em 74 disputadas; divergiu na PEC 8/2021 (2 turnos) e numa emenda da MPV 1185. Teste limpo na Câmara: PT = orientação do governo em 98,5% de 675, porém 193 de 868 votações (22%) não têm orientação, e nelas o PT vence 57,5%. O proxy dá 75,7% onde a orientação real dá 82,1%. No Senado isso rebaixa o ponto de partida: na agenda do governo (classificação manual minha, 39 votações) o real é 89,7%, fora dela 45,5%.
- **Mas a agenda não salva:** cai de 89,7% para 38,5%. No texto principal da agenda (12) cai de 100% para 66,7%. O proxy explica o nível de 66, não a queda.
- **Presença e empate:** ausentes não contam como voto contra; veterano ausente recebe a taxa da sigla. PEC 54 em 1º turno empata em 37,0 e conta como derrota.
- **Peso de 2026:** são só 3 votações. 2023-24 (64): real 70,3, corrigido 29,7. **2025-26 (19): real 52,6, replay 42,1.** A queda de 29 pontos vem sobretudo de 2023-24; no Senado recente são cerca de 10.
- **Corte de disputada (real / projeto / corrigido):** todas as 178: 84,3 / 70,8 / 68,5. 5%: 69,6 / 43,5 / 39,1. 10%: 66,3 / 37,3 / 32,5. 20%: 67,9 / 37,2 / 32,1. 30%: 71,2 / 26,9 / 19,2. Estável de 10% a 20%. Sem a frase "nas disputadas" o número engana.
- **Amostra:** 83 votações são 53 matérias; 41 são destaques (corrigido 22,0), 14 requerimentos (42,9), 28 texto principal (42,9). Bootstrap por matéria: real 53 a 79; 2027 de 26 a 50 (projeto) e 22 a 44 (corrigido); queda de 17 a 46 pontos, nunca perto de zero.
- **Margem:** 17 votações ficam a até 4 votos. Com a presença corrigida, trazer senadores do outro lado dá: 2, 44,6%; **4, 53,0%**; 6, 61,4%; **8, 66,3%**. Esta é a leitura mais útil, e é o que distingue dificuldade de impossibilidade.
- **Teste do passado (o projeto não tem no Senado):** 2017-18 para 2019, 54 cadeiras, PT na oposição: previsto 23,7, real 22,2 (18 votações). Para 2020, mesma composição: real 54,5. Sem eleição, 2023-24 para 2025: previsto 70,3, real 56,2. 2015 tem só 5 votações. O método acerta um retrato e erra de 14 a 30 pontos a distância.
## Contra o governo, o que o método esconde
`venceu` é maioria simples. Com o quórum real no texto principal, PEC 45/2019 fica em 41,2 (precisa de 49), PEC 54 em 38, PLP 68 em 38,1 e PLP 163 em 40,1. Na agenda principal seriam 4 de 12, não 8. Ressalva: em votação de quórum o governo mobiliza presença e negocia, então isto também é teto de pessimismo.
## Diap
16 firmes, 31 condicionados, 34 oposição não contradiz. Com a presença real, a mediana corrigida equivale aos condicionados votando 64% com o governo; para maioria simples precisariam de 79%. Com todos os 47, à presença de hoje, dá 38,3, abaixo dos 39 atuais. A diferença está na oposição: por histórico, 42 senadores ficam abaixo de 30%, contra 34 do Diap. São PP e Republicanos, e nisso o replay é mais duro. Se o Diap estiver certo sobre eles, vale a faixa de cima.
## Intervalo honesto
Vitória nas disputadas: **de 30% a 45%, centro perto de 35%**. Votos com o governo: **de 28 a 31 na mediana**. Ponto de partida: 66% no período, 53% em 2025-26. Contando todas as votações: cerca de 70%.
## Frase que pode ir ao vídeo
"Repeti 83 votações apertadas do Senado com os senadores de 2027, usando o voto do PT como sinal do governo. O governo, que ganhava 2 em cada 3 dessas votações, ganharia entre 3 e 4 em cada 10. Para ganhar metade delas, precisa trazer uns 4 senadores do outro lado, e para voltar aos 2 em cada 3, uns 8."

Não pode ir: "cai para 37%" com decimal, "6% contra 47%", "mediana 27", "Lula perde o Senado", ou qualquer previsão de 2027 sem dizer que é retrato.
## Correções
1. Trocar `tam` pela presença que fecha o total real, ou por cadeiras da época; aplicar o mesmo critério em `base.py`.
2. Casar Veneziano (5748) e Alessandro Vieira (5982); corrigir "42 dos 81" para 40, em `RESUMO_SENADO.json` e no dossiê.
3. Remover as 7 duplicatas idênticas ou contar por matéria; publicar o bootstrap.
4. Corrigir na lista do Flávio Marina JHC, Zé Medeiros, Sanderson, Fernando Máximo e Nicoletti (19 vira 24).
5. Publicar a variante com o histórico da Câmara e deixar claro que a escala difere.
6. Trocar a concordância de Wagner pela versão sem ele, e publicar o teste do proxy na Câmara.
7. Mostrar sempre 2025-26 ao lado do período, e a escada de senadores trazidos.
8. Acrescentar a regra de quórum no texto principal de PEC e PLP, e o teste do passado do Senado.
9. Refazer E02 e o dossiê com a faixa. Os modelos receberam 37,3 e "6% contra 47%"; reavaliar P10 (mediana 32) depois da correção.
