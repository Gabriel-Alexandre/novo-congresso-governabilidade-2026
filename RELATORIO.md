# Relatório: o novo Congresso, Lula consegue governar?

**Rodada 2, 02/nov/2026.** Análise feita pelo Claude, a pedido de Gabriel Alexandre, sobre dados abertos da Câmara, do Senado e do TSE. Todo número sai de `resultados/RESUMO.json`, por script.

## O que este projeto não consegue dizer

- **Isto é retrato, não previsão.** As votações repetidas têm a pauta, os ministérios e o clima de 2023 a 2026. Cada um repete o que fez. Quem está no meio pode votar diferente em 2027: 03 e 04/nov já trazem PEC da Segurança, decisão do PL sobre Motta e a candidatura de Marinho.
- **Quem não põe em votação não perde.** A amostra só tem o que foi a voto nominal. O governo evita o que vai perder, e a amostra não tem sessão de veto.
- **O Senado tem amostra pequena:** 83 votações, 53 matérias, posição do governo aproximada pela bancada do PT, 40 senadores sem histórico na Casa. O mesmo método errou de 14 a 30 pontos em anos distantes (`docs/revisao/2_alarmista.md`).
- **MP que perdeu a validade não é derrota no voto.** Não se mediu quantas viraram projeto de lei.
- **Votação comum não é impeachment.** Nenhuma conta aqui mede disposição de derrubar presidente. Em 2015 Dilma venceu 71% e caiu.
- **As previsões são de 4 modelos de IA da mesma empresa com o mesmo dossiê.** Não são independentes, e na literatura a IA fica abaixo da multidão humana (Brier 0,179 contra 0,149, Halawi 2024).
- **Tudo vale até 02/nov/2026.** Refazer antes de publicar.

## 1. A resposta

Pelo método deste projeto, Lula consegue governar o dia a dia, se pagar o preço do meio, e não consegue fazer a agenda que depende de muitos votos sem um acordo amplo. O risco de queda não aparece nos dados de hoje. O ponto mais fraco é o Senado.

| Poder | Medida | Com os eleitos | Leitura |
|---|---|---|---|
| Ganhar votação comum na Câmara | 678 votações disputadas | 81,4% (real 82,0%) | consegue, se o meio vier |
| Ganhar votação comum no Senado | 83 votações disputadas | 32,5%, faixa de 30 a 45 (real 66,3%) | precisa trazer gente |
| Fazer a MP virar lei | editadas em Lula III | 21% | quase não consegue |
| Segurar veto | decididos em Lula III | 52% com algo derrubado | não segura |
| Mudar a Constituição | 308 e 49 votos | 19% e 2% das disputadas | só com acordo amplo |
| Aprovar nome no STF | 41 votos | 16% das disputadas | depende de quem preside o Senado |
| Barrar processo contra ele | 172 votos | 83% das disputadas | consegue |

## 2. O teste: as mesmas votações, com os eleitos

**O método.** Cada votação nominal de plenário de 2023 a 2026, com orientação do governo e perdedor com pelo menos 10% dos votos, foi repetida com os 513 eleitos em 2026: quem votou repete o voto, quem não tem voto naquela votação recebe a proporção da própria sigla. Votos normalizados ao total real de cada votação.

| Recorte da Câmara | Votações | Real | Com os eleitos |
|---|---:|---:|---:|
| 2023 a 2026 | 678 | 82,0% | 81,4% |
| 2025 e 2026 | 336 | 77,7% | 77,1% |
| Desde 09/jul/2025 | 232 | 71,1% | 70,3% |
| Perdedor com 35% ou mais | 116 | 75,0% | 71,6% |
| Perdedor com 40% ou mais | 56 | 73,2% | 66,1% |
| Perdedor com 45% ou mais | 21 | 71,4% | 52,4% |
| Só texto da matéria | 124 | 82,3% | 82,3% |

Intervalo por matéria: real 76 a 87, com os eleitos 76 a 87: a diferença de 0,6 ponto não se distingue de zero. Só mérito, por ano: 90% em 2023, 92% em 2024, 74% em 2025, 73% em 2026.

**O que muda é o tamanho da vitória:** a mediana de votos com o governo cai de 277 para 262,5; votações com 257 ou mais, de 65% para 56%; com 308 ou mais, de 28% para 19%.

**Votações sem orientação.** O governo não orientou em parte das disputadas. Contando-as pela posição do PT, a taxa real de 2023 a 2026 é 76,5% em 872 votações. Por ano: 64,8% em 2015, 80,4% em 2023, 80,2% em 2024, 72,5% em 2025, 74,5% em 2026.

**Novatos do meio.** Votando como a sigla, 81,1%; 10 pontos abaixo, 80,7%; a meio caminho do PL, 78,5%; iguais ao PL, 72,1%.

**Quem decide.** A Câmara tem 124 cadeiras da esquerda, 132 de PL e Novo e 257 no meio (o "bloco pêndulo": centro mais União, PP, Republicanos e PRD, que se declaram direita). Com a maioria do meio, o governo venceu 548 de 548; sem ela, 8 de 130. Alinhamento do meio com o governo: 73% em 2023, 68% em 2024, 62% em 2025, 65% em 2026.

### Senado

| | Votações | Real | Com os eleitos |
|---|---:|---:|---:|
| 2023 a 2026 | 83 | 66,3% | 32,5% |
| 2023 e 2024 | 64 | 70,3% | 29,7% |
| 2025 e 2026 | 19 | 52,6% | 42,1% |

Intervalo por matéria: real 53 a 80, com os eleitos 23 a 44. Mediana de votos com o governo: 39 para 29. Variantes: deputados com a taxa pessoal da Câmara 34,9%; novos com apoio declarado a Flávio iguais ao PL 27,7%; novos do meio fora dessa lista iguais ao MDB 41,0%; piso, todos os novos fora da esquerda iguais ao PL 16,9%. Faixa honesta: 30 a 45. Trazendo senadores do outro lado: 2, 45%; 4, 53%; 6, 61%; 8, 66%.

Votações secretas, como as de autoridades, ficam de fora: são 557 de 2019 a 2026, com 9 rejeições, entre elas Messias ao STF, 42 a 34, em 29/abr/2026, a 1ª rejeição ao STF desde 1894.

## 3. O histórico

| Ano | Presidente | Disputadas | Governo venceu |
|---|---|---:|---:|
| 2003 | Lula I | 12 | 100,0% |
| 2004 | Lula I | 17 | 94,1% |
| 2005 | Lula I | 23 | 91,3% |
| 2006 | Lula I | 18 | 77,8% |
| 2007 | Lula II | 45 | 93,3% |
| 2008 | Lula II | 30 | 93,3% |
| 2009 | Lula II | 54 | 87,0% |
| 2010 | Lula II | 20 | 85,0% |
| 2011 | Dilma I | 41 | 92,7% |
| 2012 | Dilma I | 24 | 79,2% |
| 2013 | Dilma I | 44 | 75,0% |
| 2014 | Dilma I | 24 | 54,2% |
| 2015 | Dilma II | 149 | 71,1% |
| 2016 | Dilma II e Temer | 62 | 96,8% |
| 2017 | Temer | 84 | 97,6% |
| 2018 | Temer | 40 | 97,5% |
| 2019 | Bolsonaro | 111 | 88,3% |
| 2020 | Bolsonaro | 254 | 91,7% |
| 2021 | Bolsonaro | 442 | 95,9% |
| 2022 | Bolsonaro | 289 | 94,1% |
| 2023 | Lula III | 179 | 88,3% |
| 2024 | Lula III | 163 | 84,0% |
| 2025 | Lula III | 264 | 77,3% |
| 2026 | Lula III | 72 | 79,2% |

⚠️ Média de 29 disputadas por ano até 2014, e cerca de 240 de 2019 a 2025. 2016 separado: Dilma 12 de 14, Temer 48 de 48.

**Desde jul/2025 o governo vence 71,1%, a mesma taxa de Dilma em 2015 (71,1%).** Isso não prevê queda: mostra que a taxa não avisa. O que derrubou presidente foi outra coisa (seção 5).

### Medida provisória, por data

| Presidente | Editadas | Viraram lei | % | % sem crédito extraordinário | Perderam a validade | Rejeitadas no voto |
|---|---:|---:|---:|---:|---:|---:|
| Lula I | 240 | 219 | 91% | 90% | 7 | 6 |
| Lula II | 179 | 148 | 83% | 82% | 16 | 4 |
| Dilma I | 145 | 108 | 74% | 77% | 36 | 0 |
| Dilma II | 61 | 47 | 77% | 80% | 13 | 1 |
| Temer | 143 | 81 | 57% | 60% | 57 | 3 |
| Bolsonaro | 284 | 164 | 58% | 68% | 115 | 1 |
| Lula III | 244 | 52 | 21% | 20% | 154 | 0 |

O crédito extraordinário não explica a queda: sem ele, Lula III fica em 20%.

### Veto, por autor

| Presidente | Vetos | Decididos | Com algo derrubado | % dos decididos |
|---|---:|---:|---:|---:|
| Lula I | 150 | 125 | 2 | 2% |
| Lula II | 207 | 83 | 2 | 2% |
| Dilma I | 183 | 72 | 1 | 1% |
| Dilma II | 80 | 79 | 6 | 8% |
| Temer | 128 | 125 | 21 | 17% |
| Bolsonaro | 259 | 255 | 114 | 45% |
| Lula III | 205 | 89 | 46 | 52% |

Antes de 2013 a regra era outra e muitos vetos nem eram votados; a comparação vale de Dilma II em diante. Em 24 meses, Lula III e Bolsonaro empatam, perto de 44%. O rótulo conta a mensagem de veto: o licenciamento, com 52 de 63 dispositivos derrubados, conta 1.

## 4. O método contra o passado

| Caso | Previsto | Só repetir o mandato | Real no 1º ano | Erro | Erro de só repetir |
|---|---:|---:|---:|---:|---:|
| Lula I para Lula II | 88,6% | 90,0% | 93,3% | 4,7 | 3,3 |
| Lula II para Dilma I | 89,9% | 89,9% | 92,7% | 2,8 | 2,8 |
| Dilma I para Dilma II | 74,4% | 77,4% | 71,1% | 3,3 | 6,3 |

Erro médio de 3,6 pontos contra 4,1 de só repetir o mandato anterior, em 3 casos. Mal supera a regra simples. Em votos, o método erra muito: por isso a fala cita taxa, e nunca número de votos previsto.

## 5. O que derruba presidente

| Caso | Ruim ou péssimo | Presidente da Câmara | Votos com ele | Fim |
|---|---:|---|---:|---|
| Collor, 1992 | 68% | abriu o processo | 38 | caiu |
| Dilma, 2016 | 71% | rompido | 137 | caiu |
| Temer, 2017 | 69% | aliado | 263 | ficou |
| Lula, hoje | 41% (Datafolha, out) | Lula apoia Motta | esquerda tem 124; 172 barram | |

Pérez-Liñán liga a queda a aprovação baixa com rua, sem o escudo dos leais. A taxa-base é de cerca de 6% ao ano para presidentes eleitos, com intervalo de 0,7% a 20%.

## 6. A pressão de fora

Tarifa de 50% anunciada em 09/jul/2025: nas 257 cadeiras do meio, 71,8% com o governo nos 120 dias antes e 59,7% nos 120 depois; agosto subiu a 78,5%. Sanção a Moraes: 64,2% e 60,8%. Placebo em 61 datas tem desvio de 12,9 pontos. A tarifa não uniu o plenário, e não dá para dizer mais que isso. Na opinião pública os institutos discordam: Quaest subiu, Datafolha ficou estável.

## 7. Hipóteses concorrentes (Heuer)

Inconsistências por hipótese, em 2 codificações, a 2ª às cegas (concordância de 83,3%): folga 8 e 8; negociação 0 e 0; trava 2 e 3; queda 8 e 5. ⚠️ A negociação quase não tem inconsistência porque é a mais genérica: não venceu um teste. O teste real são as previsões abaixo.

## 8. O que esperar até o fim de 2027

| Cenário | Chance | Faixa entre os modelos | O que é | Regra de resolução em 31/12/2027 |
|---|---:|---:|---|---|
| A negociação caso a caso | **56%** | 50 a 67 | Vence de 70% a 85% na Câmara, ou mais sem a vitória grande; depende do pêndulo a cada votação; sem rejeição nova no STF | todos os outros casos |
| A trava | **31%** | 20 a 36 | Sem processo; o Congresso toca a própria pauta e o governo perde parte grande das disputas | não é C4; e o governo venceu menos de 70% das disputadas da Câmara em 2027, ou o Senado rejeitou mais uma indicação ao STF |
| A folga | **9%** | 8 a 11 | Ganha quase tudo e aprova o que precisa de muitos votos | não é C4 nem C3; venceu pelo menos 85% na Câmara e aprovou um indicado ao STF ou uma PEC de iniciativa do governo |
| A ruptura | **4%** | 4 a 9 | Denúncia de crime de responsabilidade recebida contra Lula | P17 resolve sim, ou renúncia diante de processo |

| # | Pergunta | Prazo | Chance | Menor e maior | Faixa |
|---|---|---|---:|---:|---|
| P01 | Hugo Motta é reeleito presidente da Câmara na eleição de fevereiro de 2027 | 2027-02-28 | 88.5% | 80 a 93 | muito provável |
| P02 | Davi Alcolumbre é reeleito presidente do Senado na eleição de fevereiro de 2027 | 2027-02-28 | 79% | 68 a 85 | provável |
| P03 | O PL integra formalmente o bloco de Motta na eleição da Mesa | 2027-02-28 | 47.5% | 30 a 62 | chance parecida |
| P04 | PSD e MDB somam pelo menos 4 ministros filiados no governo em 30/04/2027 | 2027-04-30 | 60% | 35 a 75 | provável |
| P05 | Há ao menos 1 ministro filiado a União ou PP no governo em 30/04/2027 | 2027-04-30 | 48.5% | 35 a 58 | chance parecida |
| P06 | Um novo indicado de Lula ao STF é aprovado pelo Senado | 2027-12-31 | 59% | 49 a 78 | provável |
| P07 | O Senado rejeita mais uma indicação de Lula ao STF | 2027-12-31 | 12% | 7 a 15 | muito improvável |
| P08 | O governo vence pelo menos 75% das votações nominais disputadas da Câmara em 2027 | 2027-12-31 | 51% | 50 a 55 | chance parecida |
| P09 | O governo vence pelo menos 85% das votações nominais disputadas da Câmara em 2027 | 2027-12-31 | 14% | 11 a 18 | muito improvável |
| P10 | A posição da bancada do PT vence pelo menos 50% das votações nominais abertas disputadas do Senado em 2027 | 2027-12-31 | 17.5% | 14 a 25 | muito improvável |
| P11 | O Congresso derruba total ou parcialmente pelo menos 5 mensagens de veto de Lula em 2027 | 2027-12-31 | 80% | 72 a 85 | provável |
| P12 | Pelo menos 30% das MPs editadas em 2027 viram lei | 2028-06-30 | 20% | 18 a 35 | muito improvável |
| P13 | A PEC da tarifa zero é promulgada | 2027-12-31 | 18% | 10 a 25 | muito improvável |
| P14 | Lei ou emenda que extinga a punibilidade de Jair Bolsonaro pelos atos de 8 de janeiro é aprovada pelas 2 Casas | 2027-12-31 | 19.5% | 15 a 20 | muito improvável |
| P15 | O presidente do Senado faz a leitura ou instala comissão de pedido de impeachment de ministro do STF | 2027-12-31 | 11.5% | 11 a 15 | muito improvável |
| P16 | Ministro do STF é condenado ou afastado por impeachment | 2027-12-31 | 2% | 2 a 3 | quase nenhuma chance |
| P17 | O presidente da Câmara despacha o recebimento de denúncia de crime de responsabilidade contra Lula | 2027-12-31 | 4% | 3 a 8 | quase nenhuma chance |
| P18 | A Câmara autoriza processo contra Lula por 342 votos ou mais | 2027-12-31 | 1% | 1 a 3 | quase nenhuma chance |
| P19 | Lula deixa a Presidência antes do fim do mandato por impeachment ou renúncia diante de processo | 2030-12-31 | 5.5% | 4 a 15 | muito improvável |
| P20 | O Datafolha registra avaliação ótimo ou bom de Lula abaixo de 25% em alguma pesquisa | 2027-12-31 | 16.5% | 13 a 30 | muito improvável |
| P21 | A lei do Orçamento de 2027 é sancionada | 2027-03-31 | 72% | 60 a 93 | provável |
| P22 | O Congresso aprova mudança na meta de 2027 para um resultado pior que o da LDO original | 2027-12-31 | 20% | 15 a 45 | muito improvável |
| P23 | É instalada CPI ou CPMI cujo requerimento cita ato de autoridade federal do governo Lula como objeto | 2027-12-31 | 53.5% | 30 a 58 | chance parecida |
| P24 | Delegação dos EUA à posse de Lula é anunciada pelo governo americano | 2027-01-05 | 35% | 30 a 35 | improvável |
| P25 | Os EUA aplicam nova sanção nominal a autoridade brasileira | 2027-12-31 | 18% | 12 a 25 | muito improvável |
| P26 | A PEC da reforma administrativa é aprovada em 2 turnos no plenário da Câmara | 2027-12-31 | 16% | 8 a 30 | muito improvável |
| P27 | Lula deixa a Presidência por qualquer motivo, inclusive saúde | 2027-12-31 | 7% | 5 a 8 | muito improvável |
| P28 | O governo vence pelo menos 70% das votações nominais disputadas da Câmara em 2027 | 2027-12-31 | 74.5% | 72 a 82 | provável |

Modelos: fable, haiku, opus, sonnet. Discordância média entre o menor e o maior: 15,0 pontos. Coerência: 7 de 7 testes. Previsão congelada em `dados/previsoes/rodada2/`, com o commit anterior ao vídeo.

## 9. Como conferir

Validação por outro caminho: 31 de 31 itens em `resultados/validacao_independente.json`. Revisão por 3 leitores em `docs/revisao/`. O que mudou entre as rodadas, em `docs/RODADAS.md`. Refazer: `docs/REPLICAR.md`.
