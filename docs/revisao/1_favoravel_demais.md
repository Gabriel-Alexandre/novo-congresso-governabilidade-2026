# Revisão 1: o resultado é favorável demais ao governo?

Leitor adversário, sem ter escrito o código. Rodado sobre `dados/brutos` em 02/nov/2026. Nenhum arquivo do projeto foi alterado.

## Veredito
"A Câmara não muda" não se sustenta como frase geral. O 81,4 contra 82,0 está certo como conta, mas responde a uma pergunta estreita: quem ganharia as mesmas votações, com o centro votando igual. Três problemas pesam: a amostra deixa de fora as votações em que o governo não orientou, e nelas o PT ganha 57%; a mediana de 279 votos é artefato de presença; e o centro é mantido fixo por construção.

## O que o 81% esconde: contas
Sempre: real e replay no mesmo recorte. "Presença real" = reeleito que votou naquele ano e faltou segue ausente.

| Variante | n | Real | Replay |
|---|---:|---:|---:|
| Base do projeto | 678 | 82,0 | 81,4 |
| Governo oposto a Oposição, Minoria ou PL | 601 | 79,7 | 79,0 |
| Governo oposto ao PL, só onde o PL orientou | 400 | 77,8 | 76,8 |
| Matéria com peso igual (324 matérias) | 678 | 80,7 | 80,2 |
| Sem 2023 (2024 a 2026) | 499 | 79,8 | 79,0 |
| 2025 e 2026 | 336 | 77,7 | 77,1 |
| 2025 e 2026, opostos, sem requerimento | 139 | 72,7 | 71,9 |
| Desde a tarifa, 09/jul/2025 | 232 | 71,1 | 70,3 |
| Perdedor com 35% ou mais | 116 | 75,0 | 71,6 |
| Perdedor com 40% ou mais | 56 | 73,2 | 66,1 |
| Perdedor com 45% ou mais | 21 | 71,4 | 52,4 |
| Somando as sem orientação, com a posição do PT | 872 | 76,5 | 75,8 |
| Isso, só em 2025 e 2026 | 451 | 72,9 | 72,1 |
| Novato do centro 10 pontos abaixo da sigla | 678 | 82,0 | 80,8 |
| Novato do centro a meio caminho do PL | 678 | 82,0 | 78,5 |
| Novato de União, PP, Republicanos, Podemos, PSDB, PRD, Avante e Solidariedade como PL | 678 | 82,0 | 77,1 |

1. **Efeito de agenda, o maior achado.** `base.py` L38 só aceita orientação Sim ou Não. Das 877 disputadas de plenário, 199 caem: 171 sem orientação, 26 Liberado, 2 Obstrução. Nas 194 com PT coeso, o PT ganha 57,2%; onde PT e PL ficaram opostos (150), 44,7%; no Liberado (25), 32%, incluindo a PEC de 16/set/2025, 353 a 134. A posição do PT coincide com a do governo em 98,5% das 675 que dá para comparar. Por ano, juntando tudo: 80,4; 80,2; 72,5; 74,5. Faixa: de 75,2 (somar só PT contra PL) a 80,2 (só Liberado). Ressalva: silêncio do governo pode ser falta de interesse, então 76,5 é piso razoável, não número exato. O viés já existia: Dilma em 2015 vai de 71,1 para 64,8 na mesma conta.
2. **Presença inflada.** `base.py` L94 e L100 a L105 tratam o reeleito ausente como novo e lhe dão chance de votar. Total médio: 402 real, 422 no replay. A vitória quase não muda (81,3), mas os quóruns mudam. Normalizando cada votação ao total real: mediana com o governo 277 real e **262,5** em 2027 (não 279,1); 257 votos ou mais, 64,9% real e **55,9%** (não 65,2); 308 ou mais, 27,9% real e **18,7%** (não 27,3). Margem mediana das vitórias: 44,4 para 36,3 pontos. Vitórias com margem abaixo de 10 pontos: 15 para 22.
3. **O centro é a variável, e está congelado.** Com a maioria dos votos do centro, o governo ganhou 549 de 549; sem ela, 7 de 129. O replay repete o voto dado com os ministérios de 2023 a 2026, e até 02/nov ninguém se declarou base.
4. **A curva do centro é otimista.** Ela reduz o alinhamento de forma uniforme. Afastar 30% leva o centro de 66,5 a 46,6 e dá 71% de vitórias. Em 2014, com o centro em 47,8 (PMDB, PP, PSD, PR, PRB, PTB, PROS, PSC e menores), Dilma venceu 54,2. Pela reta do próprio Lula III (1,04 ponto de vitória por ponto de alinhamento, 4 anos) daria 61.
5. **O corte de 10% esconde onde a composição pesa.** Até 30% o efeito é de 1,5 ponto; com 40%, 7; com 45%, 19 (n pequeno, 4 viradas). Poucas votações são apertadas, e é nelas que as cadeiras contam.
6. **Novatos não entram no modelo.** São 204 de 513 sem voto disputado em 2023 a 2026 (89 no centro). `sensibilidade_camara.py` L137 anuncia a variante em comentário e não tem código. Pela `c6`, ponderada pelas cadeiras novas, o novato do centro fica 4,0 pontos abaixo do veterano, com União, Republicanos e Podemos entre 9,5 e 13,5 abaixo e PSD e PSDB acima. No caso mais duro, a parte média dos votos com o governo vai de 62,6 a 57,6.
7. **Mérito por ano cai mais que o total.** Com classificação refeita (127 votações): 93,8; 89,3; 77,4; 71,4. Das 21 derrotas de mérito, 16 são de 2025 e 2026.
8. **Fora da amostra por definição.** Nenhuma das 678 é sessão de veto: o filtro é `PLEN` (`base.py` L56), os arquivos não trazem voto de deputado em sessão do Congresso, e o veto da Dosimetria, 318 a 144, não entra. Lula III teve 46 de 205 vetos com algo derrubado. Só 6 votações tratam de MP, contra 245 editadas; 105 fecharam sem virar lei e sem ser crédito extraordinário. Contar todas como derrota daria 59,9% por matéria: é teto de pessimismo, não estimativa.
9. **O teste do passado prova menos do que parece.** Os erros de 2,8 a 4,8 são da vitória; a mediana errou +8,8, +58,5 e +39,6 votos (c4), e isso o dossiê não diz. Repetir o mandato anterior erra em média 4,1 pontos; o replay, 3,6. Com 3 casos, não dá para dizer que a composição acrescenta algo além da persistência. No único análogo, Dilma I para II, o replay foi otimista em 3,3.

## Hipóteses que testei e não se confirmaram
- **Requerimento não infla:** requerimento 82,8; mérito 83,5; destaque e emenda 79,8.
- **Reeleitos não são os mais governistas de forma relevante:** centro 67,0 contra 65,6 dos que saíram; PL 19,3 contra 22,0.
- **Votações repetidas pesam pouco:** por matéria caiu 1,3 ponto; última votação de cada matéria, 79,6; 21,9% das matérias tiveram alguma derrota. **Peso igual por ano:** 82,2, sem efeito; o que pesa é olhar o período recente.
- **Obstrução contada como voto contra:** 0 viradas. **Quórum oficial:** 81,7 para 81,2, em 542 com resultado oficial.
- Por matéria, o intervalo de 95% é de 76,1 a 87,3 no real e 75,6 a 86,3 no replay: a diferença de 0,6 não se distingue de zero, e o projeto não mostra esse intervalo.

## Formulação mais honesta
"Se o centro votar como votou de 2023 a 2026, trocar as cadeiras quase não muda quem ganha votação de maioria simples: de 82% para 81%. Mas o governo perde cerca de 15 votos na mediana, e os casos com 257 votos caem de 65% para 56%, e com 308, de 28% para 19%. O ponto de partida também é mais baixo que 82%: 71% desde julho de 2025, e cerca de 73% em 2025 e 2026 contando as votações em que o governo não orientou. Quem decide é o centro: com ele o governo ganhou todas, sem ele quase nenhuma."

## Correções
1. `base.py` L94 a L105: ausente reeleito segue ausente, ou normalizar ao total real. Trocar no dossiê L11 e L13 os números de mediana e quórum (262,5; 55,9; 18,7; 342 contrários: 11, não 14). Isso também muda `analise_camara.py` L53 a L58.
2. `base.py` L34 a L39: gerar a série paralela com a posição do PT nas sem orientação e publicar 76,5 e 75,8 ao lado de 82,0 e 81,4. Em P08 e P09, que usam "o mesmo script", resolver também por essa série: o governo melhora a própria nota ao liberar a bancada.
3. `sensibilidade_camara.py` L44: acrescentar pisos de 35, 40 e 45%.
4. `sensibilidade_camara.py` L51 e `votacoes_marcantes.py` L12: a regex pega "ressalvados os destaques" e tira 64 votações de mérito, incluindo a PEC 45. A `v4` diz 75,9 (n=137); o certo fica perto de 83,5 (n=127). Essa correção favorece o governo e vale do mesmo jeito.
5. `votacoes_marcantes.py` L9: `drop_duplicates` fica com o primeiro objeto, e 472 de 678 viram REQ em `c7` (o PL 996/2015 aparece como REQ 2360/2023). Usar o prefixo do `idVotacao` como matéria.
6. `sensibilidade_camara.py` L137: implementar a variante de novato ou apagar o comentário; publicar a faixa de 80,8 a 77,1.
7. `sensibilidade_camara.py` L72 a L89: avisar que a curva é um limite otimista e ancorar nos pontos de 2014 e do Lula III, os dois lado a lado no dossiê L14.
8. `analise_camara.py` L116 a L119 e dossiê L15: publicar o erro da mediana e o erro da persistência junto do erro de vitória.
9. Dado: `2399598-70` tem 315 a 87 nos votos e 35 a 375 na descrição; conta como vitória e foi derrota. Conferir na fonte. Afeta 1 votação de 678.
10. Dossiê L11: declarar que a amostra não tem veto e quase não tem MP, e trazer 2025 e 2026 (77,7) e o período desde 09/jul/2025 (71,1) como linha de base ao lado de 82,0.
