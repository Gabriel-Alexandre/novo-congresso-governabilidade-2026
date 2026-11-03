# CLAUDE.md

Projeto do vídeo longo 23. Comece por `ESTADO.md`. A doutrina está em `.cursor/rules/novo-congresso-fundamentos.mdc`.

- Todo número sai de `resultados/RESUMO.json` ou de `resultados/previsoes_final.json`, por script. Número à mão não existe.
- `ferramentas/rodada2.py` é o dono dos números; os scripts anteriores alimentam os CSV que ele lê.
- Previsão congelada não se reescreve. Mudança nova vira rodada nova em `docs/RODADAS.md`.
- "Pêndulo", ou "o meio", são as 257 cadeiras fora da esquerda e de PL e Novo. "Centro" são os 124 da regra de três grupos do vídeo 6. Não misturar.
- ⛔ *"mentiu"*, voto, julgar intenção, *"vai cair"*. Sempre o limite: é retrato, com a pauta do passado.
- Antes de mudar, `python ferramentas/validacao_independente.py`, `python ferramentas/conferir_linguagem.py` e `python -m pytest -q`.
