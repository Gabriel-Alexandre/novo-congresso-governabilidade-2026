# Como refazer

```bash
pip install -r requirements.txt
python ferramentas/coletar.py
python ferramentas/conferir_download.py
python ferramentas/coletar_senado.py
curl -o dados/brutos/tse/consulta_cand_2026.zip https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2026.zip
curl -A "Mozilla/5.0" -o dados/brutos/camara/deputados.csv https://dadosabertos.camara.leg.br/arquivos/deputados/csv/deputados.csv
python ferramentas/derivar_eleitos.py
python ferramentas/analise_processos.py
python ferramentas/analise_camara.py
python ferramentas/analise_senado.py
python ferramentas/sensibilidade_camara.py
python ferramentas/analise_extras.py
python ferramentas/rodada2.py
python ferramentas/agregar_previsoes.py
python ferramentas/validacao_independente.py
python ferramentas/graficos.py
python ferramentas/gerar_relatorio.py
python ferramentas/conferir_linguagem.py
python -m pytest -q
```

⚠️ O servidor da Câmara corta downloads longos: `conferir_download.py` compara o tamanho com o Content-Length e retoma. A composição do Senado de 2027 e as cadeiras de 2022 são lidas do projeto vizinho `congresso-e-governos-eleicoes-2026`, que precisa estar ao lado. Os arquivos podem mudar: o `dados/MANIFESTO_*.json` traz o sha256 do que foi lido em 02/nov/2026.
