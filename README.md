# O novo Congresso: Lula consegue governar?

Análise aberta feita pelo Claude, a pedido de Gabriel Alexandre, para o vídeo longo 23 do canal. A IA repetiu as votações reais de 2023 a 2026 com os deputados e senadores eleitos em 2026, comparou com a história desde 2003, leu o que a ciência política diz e registrou previsões com data para cobrar depois.

**Comece por:** [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md) → [`RELATORIO.md`](RELATORIO.md) → [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md) → [`docs/RODADAS.md`](docs/RODADAS.md).

**Limite principal:** é retrato com a pauta do passado, não previsão. Quem está no meio pode votar diferente.

## O que tem aqui

| Pasta | O que é |
|---|---|
| `congresso27/` | a função que lê as votações e repete cada uma com outra composição |
| `ferramentas/` | coleta, análises, validação independente, gráficos, relatório |
| `dados/` | manifestos com hash, derivados, previsões congeladas por rodada, hipóteses |
| `resultados/` | `RESUMO.json` (dono dos números), tabelas e `figuras/` em 1920x1080 |
| `docs/` | plano, rodadas, fontes, como refazer, e a revisão por 3 leitores em `revisao/` |

## Refazer

[`docs/REPLICAR.md`](docs/REPLICAR.md). Os dados brutos não ficam no git, e o `dados/MANIFESTO_*.json` guarda endereço e sha256 de cada um.

## Fontes

Dados abertos da Câmara dos Deputados, do Senado Federal e do Congresso Nacional, e os candidatos do TSE. Composição do Senado de 2027 lida do projeto [`congresso-e-governos-eleicoes-2026`](https://github.com/Gabriel-Alexandre/congresso-e-governos-eleicoes-2026).
