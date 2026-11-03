# Auditoria 3: método e linguagem (02/nov/2026)
Tudo recontado sobre `dados/brutos` e `resultados`, sem alterar o código nem os resultados. Os números novos abaixo ainda precisam entrar em `ferramentas/`. Regra de autoria aplicada: data de chegada da mensagem ao Congresso menos 1 dia. A data da norma não serve, porque a lei pode nascer da própria derrubada (VET 58/2022: norma de 22/12/2023).
## 1. MPs: a classificação erra pouco, e o crédito extraordinário não explica a queda
- `virou_lei` mistura 4 coisas. Falsos positivos: 8 que viraram projeto de conversão e perderam a validade (MPV 258/2005, 605/2013 e outras), 2 com projeto vetado inteiro (756/2016, 770/2017), 2 aprovadas sem lei ainda (1370 e 1375/2026). De 2003 a 2014 a maior parte dos "sim" vem só do rótulo APROVADO, sem norma no campo. Bug: `nao_viraram` não reconhece SEM EFICÁCIA. A coluna dá 12 em Lula III; o certo é 153 sem eficácia e 12 revogadas. Lula III, 245 MPs: 53 leis, 2 aprovadas, 153 sem eficácia, 12 revogadas pelo próprio governo, 25 sem desfecho (24 tramitando). **Nenhuma rejeitada em plenário.** Crédito extraordinário: 98 (23 viraram lei).

| Por data | Editadas | Lei | % | Sem crédito | % sem crédito |
|---|---|---|---|---|---|
| Lula I | 240 | 220 | 91,7 (era 92,1) | 164 de 181 | 90,6 |
| Lula II | 179 | 148 | 82,7 (83,8) | 116 de 141 | 82,3 |
| Dilma I | 145 | 108 | 74,5 (77,9) | 90 de 117 | 76,9 |
| Dilma II (até 11/05/16) | 59 | 45 | 76,3 | 37 de 47 | 78,7 |
| Temer | 144 | 82 | 56,9 (52,9) | 79 de 131 | 60,3 |
| Bolsonaro | 284 | 165 | 58,1 | 144 de 211 | 68,2 |
| Lula III | 245 | 53 | 21,6 (22,4) | 30 de 147 | 20,4 |
- Tirar o crédito **aumenta** a distância para Bolsonaro (de 36,5 para 47,8 pontos). A ressalva do dossiê ("parte é crédito extraordinário") não sustenta a leitura de que o número engana por isso. Só em 2024: 0 de 46 sem crédito viraram lei; as 16 leis do ano são crédito. Fontes: Poder360 reproduzido exato (37 de 179 = 20,7% em 31/12/2025). Ranking dos Políticos: 22,9% é 38 de 166 **decididas**, denominador diferente do nosso; em 02/04/2026 temos 41 de 193 = 21,2%, contra 38 de 192 (3 MPs sem conciliar). Coorte 2023 a 2025 hoje: 43 de 179 = 24,0%, porque 6 viraram lei depois. Limite: o dado não diz quantas caducaram com o conteúdo aprovado em projeto de lei. "Caducou" não é "derrota" nem "perdeu no voto".
## 2. Vetos: os rótulos valem com ressalva, a autoria quase não muda, o denominador muda tudo
- MANTIDO_PARCIALMENTE: parte caiu, parte ficou (API, VET 3/2023). Certo.
- REJEITADO_PLENARIO não significa "total": 56 de 109 são vetos parciais, e o VET 29/2025 (licenciamento, 52 de 63 dispositivos derrubados, 7 prejudicados) leva esse rótulo. Renomear `derrubado_total`. A unidade é a mensagem: esses 63 dispositivos contam 1. `dataDeliberacao` é o último ato: o mesmo VET 29/2025 está em 22/06/2026, com a votação principal em nov/2025.
- **Lula III não herdou veto de Bolsonaro numerado em 2023.** O último dele é VET 65/2022 (30/12/2022); o VET 1/2023 chega em 11/01/2023, de lei sancionada por Lula. Veto de 2022 derrubado em 2023 já conta para Bolsonaro no código. O único erro de autoria por ano é 2016, separado abaixo.

| Autor real | Vetos | Derrubados | Em aberto | % dos decididos | Até 24 meses |
|---|---|---|---|---|---|
| Lula I | 150 | 2 | 2 | 1,4 | |
| Lula II | 207 | 2 | 100 | 1,9 | |
| Dilma I | 183 | 1 | 105 | 1,3 | |
| Dilma II | 80 | 6 | 0 | 7,5 | |
| Temer | 128 | 21 | 0 | 16,4 | 16,4 |
| Bolsonaro | 259 | 114 | 1 | 44,2 | 43,6 |
| Lula III | 205 | 46 | 111 | 48,9 (46 de 94) | 44,6 (37 de 83) |
- Por data da derrubada: no governo Lula III caíram 54 (46 dele, 7 de Bolsonaro, 1 de Lula II). No de Bolsonaro, 112 (107 dele, 4 de Temer, 1 de Lula II). Os 7 de Bolsonaro saem da conta como derrota de Lula.
- Corrigir no dossiê: "Temer 17 de 92" vira 21 de 128; "46 de 205" vira 46 de 94 decididos. Na mesma janela de 24 meses, **Lula III e Bolsonaro empatam** (44,6 e 43,6): o veto não mostra Lula III pior. "2 de 150" compara regimes: antes de jul/2013, 207 de 468 vetos nunca foram votados; depois, 1 de 539. Ruptura de regra (Res. CN 1/2013 e EC 76/2013, conferir na fonte), que não é só força política.
## 3. Série 2003 a 2026
- Amostra: média de 29 disputadas por ano em 2003 a 2014, contra 243 em 2019 a 2025. 2003 tem 12 (100%, intervalo 75,7 a 100). 2014 tem 24 (54,2%, intervalo 35,1 a 72,1). Bolsonaro é 41% das linhas. A fala não pode tratar 2003 e 2021 com o mesmo peso. 2016 separado: Dilma 12 de 14 (85,7, intervalo 60,1 a 96,0); Temer 48 de 48. Corrigido: Dilma II 118 de 163 = 72,4; Temer 169 de 172 = 98,3.
- Orientação existe em Bolsonaro: 78,5% a 88,0% das nominais, com rótulos GOV. e Governo lidos. Não é problema. A cobertura varia de 64% a 90%, e a votação sem orientação sai da conta: Dilma liberou 46 em 2015; em 2025, 109 de 428 ficaram de fora (99 sem linha, 10 liberadas). Tende a favorecer o governo.
- Pauta: procedimento é 51% em Lula I e 80% em Lula III. Só mérito: Lula I 82,4 (n 34), Lula II 80,6, Dilma I 76,2, Dilma II 63,5, Temer 91,2, Bolsonaro 93,0, Lula III 77,4 (n 137). Por proposição: Lula I 85,9, Lula III 81,0. A distância Lula I x Lula III cai de 8 para 5 pontos. Destaques da mesma matéria repetem (1.096 votações de Bolsonaro são 322 proposições).
- Quórum ignorado: `gov_venceu` usa só Sim > Não. Discorda do campo `aprovacao` em 61 de 2.002 (3%): urgência com 243 a 170 "vence" e foi rejeitada; 6 PECs do governo "vencem" abaixo de 308. Pelo oficial: Lula I 85,7, Lula II 86,6, Dilma I 71,4, Dilma II 71,1, Temer 95,0, Bolsonaro 94,6, Lula III 81,2. Conferir também a votação 2399598-70 (arquivo 315 a 87, descrição 35 a 375). 2026 vai até 14/out e é ano eleitoral.
## 4. Teste do passado
- Prova só que o método acerta a taxa do **1º ano** dentro de 3 a 5 pontos, em 3 casos. Não bate a regra ingênua "repetir a taxa do mandato anterior": erro médio 3,63 contra 4,13 (melhor em 1, empate em 1, pior em 1).
- **Em votos erra muito:** mediana +8,8, +58,5 e +39,6, média de 35,6. Parte é bug: a composição usa quem votou no ano-alvo, 533 a 553 deputados, e não 513. O controle de 2024 mostra diferença máxima de 108 votos, embora o script diga que deveria reproduzir o real. A mediana de 2027 muda com a variante: 279,1, 249,6 (curva) e 235,1 (só partido). **Citar taxa, nunca mediana de votos.** Os 81,4 são os mesmos com e sem voto individual: o replay herda a pauta e a posição do passado, então não mede mudança de comportamento. Dilma II ilustra: 74,4 previsto, 71,1 real, sem nenhum aviso de impeachment. Frase segura: "repete o passado com os novos nomes; serve de piso de comparação, não de previsão".
## 5. Previsões
- Taxa-base: 2 em 36 anos dá 5,5% ao ano, conta certa, mas o dossiê diz "presidente eleito" e o denominador inclui Itamar e Temer. Só eleitos: 2 em 31,8 anos = 6,3%. Intervalo exato de 2 eventos: 0,7% a 20%. Por 1º ano de mandato: 1 em 9. Com 14 meses até 31/12/2027, 5,5% ao ano já dão 6,4%: o P17 de 6% é a própria taxa-base, sem desconto por Motta nem acréscimo pela economia.
- C4 de 8% contra P17 de 6%: a regra inclui "Lula deixou o cargo" por qualquer causa, inclusive saúde, aos 81 anos, e nenhum modelo tratou disso. Literal, 8% é **baixo**. Como "ruptura", é **alto**, porque fora a denúncia quase nada sobra em 14 meses. Trocar por "renúncia ou afastamento por crime de responsabilidade" e medir saúde à parte; C4 fica perto de 6 a 7.
- Aritmética coerente: 15,3 + 14,9 + 61,9 + 7,9 = 100; P(70 a 75) perto de 15 e P(75 a 85) de 44,5. O defeito é de desenho: C3 só olha a Câmara. Câmara em 80%, Senado em 30% e indicado rejeitado resolve como "negociação", contra a tese do próprio projeto. C1 é resíduo: 62% por construção, com "pagando caro" sem medida. Incluir P10 ou P07 em C3. P19 de 5,5% até 2030 contra 2 quedas em 9 mandatos (22%) pede razão escrita, e Collor renunciou: definir se conta.
- P20: o dossiê omite que o Datafolha já deu 24% em fev/2025 ([Congresso em Foco](https://congressoemfoco.com.br/noticia/106236/aprovacao-de-lula-despenca-para-24--segundo-datafolha)), e o Opus escreveu "Lula nunca ficou perto de 25". Reabrir P20 (19%) com o fato no dossiê. 4 modelos do mesmo fornecedor com o mesmo dossiê não são independentes; dizer "4 modelos da mesma empresa". Erro no dossiê passa para os 4.
- **Bug em `e_hipoteses.csv`:** E15 e E16 têm vírgula sem aspas ("13,88%", "44,8") e as colunas deslizam. Correto: inconsistências 1ª codificação H1 8, H2 0, H3 2, H4 8; concordância 83,3% (não 76,4), kappa 0,74. H2 tem **0 inconsistências nas 2 codificações** e 15 a 17 de 18 compatíveis: é genérica, não venceu um teste. Separar em previsões que possam falhar.
## 6. Regras de resolução
- Boas: P06, P07, P13 (dando o número da PEC), P16, P18, P21, P25. P01 e P02: trocar 01/02 por "na eleição de fevereiro" (em 2019 o Senado terminou em 02/02). P03: e se o PL apoiar sem bloco formal? Vale não. P04: fixar foto em 30/04 e o que conta como ministério. **P05:** "decisão formal" quase nunca existe; dividir em filiado no cargo e nota do partido. P08 e P09: gravar o commit do script, piso de 30 votações, usar `aprovacao` quando houver. P10: 3 votações em 2026 e 16 em 2025; sem piso de 15 pode não resolver. **P11:** dizer processo VET, autor por data, rótulo REJEITADO ou MANTIDO_PARCIALMENTE, data do ato de votação. Base por ano: 17, 15, 12 e 2 (com o licenciamento em 2025), em 2 a 3 sessões por ano. P12: lei só com norma publicada. P14: "alcance" precisa dizer extinção de punibilidade; redução de pena não conta. P15: "andamento" = leitura ou comissão. P17: despacho de recebimento, nunca protocolo. P20: é "avaliação ótimo ou bom", não "aprovação". P22: exceção à meta não conta. **P23:** "objeto principal" é subjetivo (faixa de 25 a 65); exigir ato de autoridade federal do governo citado no requerimento. **P24:** "representante" inclui encarregado? (faixa de 30 a 65); fixar delegação anunciada pelos EUA. P26: número da PEC e os 2 turnos.
## 7. Tarifa
- Pode dizer: "nos 120 dias seguintes o bloco votou com o governo em 59,7%, contra 71,8%; não houve união em plenário". Não pode dizer "depois dela" como efeito. Placebo: a mesma conta em 61 datas de mai/2025 a jun/2026 tem desvio de 12,9 pontos, e 44% dão 12 ou mais. A queda de 13 pontos já aparecia em datas de maio e junho, antes do anúncio. Junho e julho estavam em 54,9 e 51,7; **agosto subiu a 78,5**. A esquerda também caiu 4,4. A sanção dá +18,6 em 60 dias e -3,3 em 120. Só mérito: 9 votações antes. O erro-padrão de 3,5 não cobre a troca de pauta. Conferir "não o Datafolha": 29 em 02/ago/2025 e 33 em setembro.
## 8. "Centro": contradição real
- O script chama de centro tudo fora da esquerda e de PL e Novo: **257 cadeiras**, com União, PP, Republicanos e PRD (133), que são direita na regra do vídeo 6. O dossiê diz "centro 124" e 5 linhas depois usa "centro" para 257. `g07`, `g10`, E17 e c6 e c8 usam o sentido de 257. Nome: **"bloco pêndulo"** no código e no gráfico (`pendulo`). Na fala: "os 257 deputados que não são da esquerda nem de PL e Novo". Reservar "centro" para os 124 e os 17 do Senado. Título do g07: "O governo depende do bloco pêndulo". Corrigir também PESQUISA §0.3, "a esquerda ficou em 124, igual": eram 128 eleitos em 2022 (c3), a direita 250 e o centro 135.
## 9. Frases que exageram causa
| Frase | Problema | Troca |
|---|---|---|
| "Ministério compra menos voto [...] e a MP quase parou de virar lei" (§0.6) | nada mede; MP não tem ligação com ministério | "emendas obrigatórias de R$ 44,8 bi não dependem do governo" e, separado, "1 em 5 MPs virou lei, nenhuma rejeitada no voto" |
| "no plenário o centro votou menos com o governo depois dela" (§0.7) | sugere efeito; ver item 7 | "a tarifa não uniu o plenário" |
| "O problema mora no Senado" (§0.3) | replay de 83 votações, 42 senadores sem histórico, posição aproximada pelo PT, 19 votações em 2025 e 2026 | "o sinal mais forte de dificuldade vem do Senado, com amostra pequena" |
| "PMDB de 89,9 para 51,2 [...] e Dilma foi a 54,2%" | encadeia causa; n 24, e em 2015 subiu a 71,1 | apresentar como 2 fatos, com o n |
| "A MP perdeu força" | sem medir conteúdo aprovado em PL | "a MP deixou de ser votada" |
| "a queda vem das emendas impositivas" (Ranking) | parte interessada, sem teste | atribuir à fonte ou cortar |
| E12 "Dilma venceu 71% e caiu" | não testa a taxa como causa | usar para dizer que a taxa não avisa queda |
## Correções, por ordem
1. `analise_processos.py`: regra nova de lei, conserto de `nao_viraram`, autoria por data, 2016 separado.
2. Trocar no dossiê os números de MP e veto dos itens 1 e 2, e rodar de novo os modelos, com os 24% do Datafolha e os 257.
3. Aspas no `e_hipoteses.csv` e `csv.reader` validando colunas.
4. Renomear centro para pêndulo em scripts, gráficos e textos.
5. Composição de 513 no teste do passado; medir também contra a regra ingênua.
6. Reescrever C3, C4 e as perguntas P03, P05, P11, P14, P17, P23 e P24 **antes** da 2ª rodada, registrando a mudança.
