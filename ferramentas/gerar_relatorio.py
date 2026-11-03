"""Escreve RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md a partir de resultados/RESUMO.json e resultados/previsoes_final.json."""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = json.loads((R / "resultados/RESUMO.json").read_text(encoding="utf8"))
P = json.loads((R / "resultados/previsoes_final.json").read_text(encoding="utf8"))
V = json.loads((R / "resultados/validacao_independente.json").read_text(encoding="utf8"))
c, s = D["camara"], D["senado"]
q = {x["id"]: x for x in P["perguntas"]}
cn = {x["id"]: x for x in P["cenarios"]}


def br(x, n=1):
    return f"{x:.{n}f}".replace(".", ",")


def tab_cen():
    linhas = ["| Cenário | Chance | Faixa entre os modelos | O que é | Regra de resolução em 31/12/2027 |", "|---|---:|---:|---|---|"]
    for k in ("C1", "C3", "C2", "C4"):
        x = cn[k]
        linhas.append(f"| {x['cenario']} | **{br(x['normalizado'],0)}%** | {x['menor']:g} a {x['maior']:g} | {x['descricao']} | {x['regra_de_resolucao_em_31_12_2027']} |")
    return "\n".join(linhas)


def tab_perg():
    linhas = ["| # | Pergunta | Prazo | Chance | Menor e maior | Faixa |", "|---|---|---|---:|---:|---|"]
    for x in P["perguntas"]:
        linhas.append(f"| {x['id']} | {x['pergunta']} | {x['prazo']} | {x['mediana']:g}% | {x['menor']:g} a {x['maior']:g} | {x['faixa']} |")
    return "\n".join(linhas)


m = D["mp"]
v = D["veto"]
tm = "\n".join(f"| {p} | {x['editadas']:.0f} | {x['lei']:.0f} | {br(x['pct'],0)}% | {br(x['sem_credito_pct'],0)}% | {x['sem_eficacia']:.0f} | {x['rejeitadas']:.0f} |" for p, x in m.items())
tv = "\n".join(f"| {p} | {x['vetos']:.0f} | {x['decididos']:.0f} | {x['com_algo_derrubado']:.0f} | {br(x['pct_decididos'],0)}% |" for p, x in v.items())
ser = "\n".join(f"| {a} | {x['presidente']} | {x['n']} | {br(x['vitoria_disputadas'])}% |" for a, x in D["serie"].items())
bt = "\n".join(f"| {b['caso']} | {br(b['previsto'])}% | {br(b['repetir_o_mandato'])}% | {br(b['real'])}% | {br(b['erro'])} | {br(b['erro_regra_ingenua'])} |" for b in D["teste_passado"]["casos"])
ev = [e for e in D["eventos_eua"] if e["janela_dias"] == 120 and e["campo"] == "centro" and "25%" not in e["evento"]]
hi = P["hipoteses"]["inconsistencias"]
passou = sum(x["passou"] for x in V)

RELATORIO = f"""# Relatório: o novo Congresso, Lula consegue governar?

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
| Ganhar votação comum na Câmara | 678 votações disputadas | {br(c['total']['novo_pct'])}% (real {br(c['total']['real_pct'])}%) | consegue, se o meio vier |
| Ganhar votação comum no Senado | 83 votações disputadas | {br(s['total']['novo_pct'])}%, faixa de 30 a 45 (real {br(s['total']['real_pct'])}%) | precisa trazer gente |
| Fazer a MP virar lei | editadas em Lula III | {br(m['Lula III']['pct'],0)}% | quase não consegue |
| Segurar veto | decididos em Lula III | {br(v['Lula III']['pct_decididos'],0)}% com algo derrubado | não segura |
| Mudar a Constituição | 308 e 49 votos | {br(c['pct_308_novo'],0)}% e {br(s['pct_49_novo'],0)}% das disputadas | só com acordo amplo |
| Aprovar nome no STF | 41 votos | {br(s['pct_41_novo'],0)}% das disputadas | depende de quem preside o Senado |
| Barrar processo contra ele | 172 votos | {br(c['pct_172_novo'],0)}% das disputadas | consegue |

## 2. O teste: as mesmas votações, com os eleitos

**O método.** Cada votação nominal de plenário de 2023 a 2026, com orientação do governo e perdedor com pelo menos 10% dos votos, foi repetida com os 513 eleitos em 2026: quem votou repete o voto, quem não tem voto naquela votação recebe a proporção da própria sigla. Votos normalizados ao total real de cada votação.

| Recorte da Câmara | Votações | Real | Com os eleitos |
|---|---:|---:|---:|
| 2023 a 2026 | {c['total']['n']} | {br(c['total']['real_pct'])}% | {br(c['total']['novo_pct'])}% |
| 2025 e 2026 | {c['2025_26']['n']} | {br(c['2025_26']['real_pct'])}% | {br(c['2025_26']['novo_pct'])}% |
| Desde 09/jul/2025 | {c['desde_09jul2025']['n']} | {br(c['desde_09jul2025']['real_pct'])}% | {br(c['desde_09jul2025']['novo_pct'])}% |
| Perdedor com 35% ou mais | {c['perdedor_35']['n']} | {br(c['perdedor_35']['real_pct'])}% | {br(c['perdedor_35']['novo_pct'])}% |
| Perdedor com 40% ou mais | {c['perdedor_40']['n']} | {br(c['perdedor_40']['real_pct'])}% | {br(c['perdedor_40']['novo_pct'])}% |
| Perdedor com 45% ou mais | {c['perdedor_45']['n']} | {br(c['perdedor_45']['real_pct'])}% | {br(c['perdedor_45']['novo_pct'])}% |
| Só texto da matéria | {c['merito']['total']['n']} | {br(c['merito']['total']['real_pct'])}% | {br(c['merito']['total']['novo_pct'])}% |

Intervalo por matéria: real {br(c['ic95_real'][0],0)} a {br(c['ic95_real'][1],0)}, com os eleitos {br(c['ic95_novo'][0],0)} a {br(c['ic95_novo'][1],0)}: a diferença de {br(c['total']['real_pct']-c['total']['novo_pct'])} ponto não se distingue de zero. Só mérito, por ano: {', '.join(br(x['real_pct'],0)+'% em '+a for a,x in c['merito']['por_ano'].items())}.

**O que muda é o tamanho da vitória:** a mediana de votos com o governo cai de {c['mediana_com_real']:.0f} para {br(c['mediana_com_novo'])}; votações com 257 ou mais, de {br(c['pct_257_real'],0)}% para {br(c['pct_257_novo'],0)}%; com 308 ou mais, de {br(c['pct_308_real'],0)}% para {br(c['pct_308_novo'],0)}%.

**Votações sem orientação.** O governo não orientou em parte das disputadas. Contando-as pela posição do PT, a taxa real de 2023 a 2026 é {br(D['com_posicao_do_pt_2023_26']['vitoria_pct'])}% em {D['com_posicao_do_pt_2023_26']['n']} votações. Por ano: {', '.join(br(x['vitoria_pct'],1)+'% em '+a for a,x in D['com_posicao_do_pt_nas_sem_orientacao'].items())}.

**Novatos do meio.** Votando como a sigla, {br(c['novatos']['base'])}%; 10 pontos abaixo, {br(c['novatos']['menos10'])}%; a meio caminho do PL, {br(c['novatos']['meio_pl'])}%; iguais ao PL, {br(c['novatos']['como_pl'])}%.

**Quem decide.** A Câmara tem {D['cadeiras']['esquerda']} cadeiras da esquerda, {D['cadeiras']['PL e Novo']} de PL e Novo e {D['cadeiras']['pendulo']} no meio (o "bloco pêndulo": centro mais União, PP, Republicanos e PRD, que se declaram direita). Com a maioria do meio, o governo venceu {c['pendulo_com_governo']['venceu']} de {c['pendulo_com_governo']['votacoes']}; sem ela, {c['pendulo_contra_governo']['venceu']} de {c['pendulo_contra_governo']['votacoes']}. Alinhamento do meio com o governo: {', '.join(br(x,0)+'% em '+a for a,x in D['pendulo_alinhamento'].items())}.

### Senado

| | Votações | Real | Com os eleitos |
|---|---:|---:|---:|
| 2023 a 2026 | {s['total']['n']} | {br(s['total']['real_pct'])}% | {br(s['total']['novo_pct'])}% |
| 2023 e 2024 | {s['por_periodo']['2023_24']['n']} | {br(s['por_periodo']['2023_24']['real_pct'])}% | {br(s['por_periodo']['2023_24']['novo_pct'])}% |
| 2025 e 2026 | {s['por_periodo']['2025_26']['n']} | {br(s['por_periodo']['2025_26']['real_pct'])}% | {br(s['por_periodo']['2025_26']['novo_pct'])}% |

Intervalo por matéria: real {br(s['ic95_real'][0],0)} a {br(s['ic95_real'][1],0)}, com os eleitos {br(s['ic95_novo'][0],0)} a {br(s['ic95_novo'][1],0)}. Mediana de votos com o governo: {s['total']['mediana_com_real']:.0f} para {br(s['total']['mediana_com_novo'],0)}. Variantes: deputados com a taxa pessoal da Câmara {br(s['variantes']['deputados_com_taxa_pessoal'])}%; novos com apoio declarado a Flávio iguais ao PL {br(s['variantes']['flavio_como_pl'])}%; novos do meio fora dessa lista iguais ao MDB {br(s['variantes']['pendulo_fora_da_lista_como_mdb'])}%; piso, todos os novos fora da esquerda iguais ao PL {br(s['variantes']['piso_novo_fora_da_esquerda_como_pl'])}%. Faixa honesta: 30 a 45. Trazendo senadores do outro lado: 2, {br(s['escada_trazidos']['2'],0)}%; 4, {br(s['escada_trazidos']['4'],0)}%; 6, {br(s['escada_trazidos']['6'],0)}%; 8, {br(s['escada_trazidos']['8'],0)}%.

Votações secretas, como as de autoridades, ficam de fora: são {D['secretas']['n']} de 2019 a 2026, com {D['secretas']['rejeitadas']} rejeições, entre elas Messias ao STF, 42 a 34, em 29/abr/2026, a 1ª rejeição ao STF desde 1894.

## 3. O histórico

| Ano | Presidente | Disputadas | Governo venceu |
|---|---|---:|---:|
{ser}

⚠️ Média de 29 disputadas por ano até 2014, e cerca de 240 de 2019 a 2025. 2016 separado: Dilma {D['2016']['dilma'][0]} de {D['2016']['dilma'][1]}, Temer {D['2016']['temer'][0]} de {D['2016']['temer'][1]}.

**Desde jul/2025 o governo vence {br(c['desde_09jul2025']['real_pct'])}%, a mesma taxa de Dilma em 2015 ({br(D['serie']['2015']['vitoria_disputadas'])}%).** Isso não prevê queda: mostra que a taxa não avisa. O que derrubou presidente foi outra coisa (seção 5).

### Medida provisória, por data

| Presidente | Editadas | Viraram lei | % | % sem crédito extraordinário | Perderam a validade | Rejeitadas no voto |
|---|---:|---:|---:|---:|---:|---:|
{tm}

O crédito extraordinário não explica a queda: sem ele, Lula III fica em {br(m['Lula III']['sem_credito_pct'],0)}%.

### Veto, por autor

| Presidente | Vetos | Decididos | Com algo derrubado | % dos decididos |
|---|---:|---:|---:|---:|
{tv}

Antes de 2013 a regra era outra e muitos vetos nem eram votados; a comparação vale de Dilma II em diante. Em 24 meses, Lula III e Bolsonaro empatam, perto de 44%. O rótulo conta a mensagem de veto: o licenciamento, com 52 de 63 dispositivos derrubados, conta 1.

## 4. O método contra o passado

| Caso | Previsto | Só repetir o mandato | Real no 1º ano | Erro | Erro de só repetir |
|---|---:|---:|---:|---:|---:|
{bt}

Erro médio de {br(D['teste_passado']['erro_medio'])} pontos contra {br(D['teste_passado']['erro_medio_ingenua'])} de só repetir o mandato anterior, em 3 casos. Mal supera a regra simples. Em votos, o método erra muito: por isso a fala cita taxa, e nunca número de votos previsto.

## 5. O que derruba presidente

| Caso | Ruim ou péssimo | Presidente da Câmara | Votos com ele | Fim |
|---|---:|---|---:|---|
| Collor, 1992 | 68% | abriu o processo | 38 | caiu |
| Dilma, 2016 | 71% | rompido | 137 | caiu |
| Temer, 2017 | 69% | aliado | 263 | ficou |
| Lula, hoje | 41% (Datafolha, out) | Lula apoia Motta | esquerda tem 124; 172 barram | |

Pérez-Liñán liga a queda a aprovação baixa com rua, sem o escudo dos leais. A taxa-base é de cerca de 6% ao ano para presidentes eleitos, com intervalo de 0,7% a 20%.

## 6. A pressão de fora

Tarifa de 50% anunciada em 09/jul/2025: nas 257 cadeiras do meio, {br(ev[0]['antes_pct'],1)}% com o governo nos 120 dias antes e {br(ev[0]['depois_pct'],1)}% nos 120 depois; agosto subiu a 78,5%. Sanção a Moraes: {br(ev[1]['antes_pct'],1)}% e {br(ev[1]['depois_pct'],1)}%. Placebo em 61 datas tem desvio de 12,9 pontos. A tarifa não uniu o plenário, e não dá para dizer mais que isso. Na opinião pública os institutos discordam: Quaest subiu, Datafolha ficou estável.

## 7. Hipóteses concorrentes (Heuer)

Inconsistências por hipótese, em 2 codificações, a 2ª às cegas (concordância de {br(P['hipoteses']['concordancia_pct'])}%): folga {hi['H1_folga']['1a_I']} e {hi['H1_folga']['2a_I']}; negociação {hi['H2_negocia']['1a_I']} e {hi['H2_negocia']['2a_I']}; trava {hi['H3_trava']['1a_I']} e {hi['H3_trava']['2a_I']}; queda {hi['H4_cai']['1a_I']} e {hi['H4_cai']['2a_I']}. ⚠️ A negociação quase não tem inconsistência porque é a mais genérica: não venceu um teste. O teste real são as previsões abaixo.

## 8. O que esperar até o fim de 2027

{tab_cen()}

{tab_perg()}

Modelos: {', '.join(P['modelos'])}. Discordância média entre o menor e o maior: {br(P['discordancia_media_pontos'])} pontos. Coerência: {sum(x['passou'] for x in P['coerencia'])} de {len(P['coerencia'])} testes. Previsão congelada em `dados/previsoes/rodada2/`, com o commit anterior ao vídeo.

## 9. Como conferir

Validação por outro caminho: {passou} de {len(V)} itens em `resultados/validacao_independente.json`. Revisão por 3 leitores em `docs/revisao/`. O que mudou entre as rodadas, em `docs/RODADAS.md`. Refazer: `docs/REPLICAR.md`.
"""
(R / "RELATORIO.md").write_text(RELATORIO, encoding="utf8")

SIMPLES = f"""# Resumo simples

**A pergunta:** com o novo Congresso, Lula consegue governar?

**A resposta curta:** consegue tocar o dia a dia, se pagar o preço de quem está no meio. Não consegue fazer o que precisa de muitos votos sem um acordo amplo. O ponto mais fraco é o Senado. Queda não aparece nos dados de hoje.

| O que a IA fez | O que achou |
|---|---|
| Repetiu {c['total']['n']} votações apertadas da Câmara de 2023 a 2026 com os 513 eleitos | o governo venceria {br(c['total']['novo_pct'],0)}%, contra {br(c['total']['real_pct'],0)}% reais. Quase igual, se o meio votar como votou |
| Fez o mesmo com {s['total']['n']} votações do Senado | de {br(s['total']['real_pct'],0)}% para algo entre 30 e 45% |
| Olhou quem decide | com a maioria das {D['cadeiras']['pendulo']} cadeiras do meio, {c['pendulo_com_governo']['venceu']} de {c['pendulo_com_governo']['votacoes']}; sem ela, {c['pendulo_contra_governo']['venceu']} de {c['pendulo_contra_governo']['votacoes']} |
| Mediu a MP | {br(m['Lula I']['pct'],0)}% viravam lei no Lula I; {br(m['Lula III']['pct'],0)}% no Lula III |
| Mediu o veto | {br(v['Lula III']['pct_decididos'],0)}% dos decididos com algo derrubado no Lula III, e {br(v['Bolsonaro']['pct_decididos'],0)}% no Bolsonaro |
| Pediu previsão a 4 modelos | negociação caso a caso {br(cn['C1']['normalizado'],0)}%; trava {br(cn['C3']['normalizado'],0)}%; folga {br(cn['C2']['normalizado'],0)}%; ruptura {br(cn['C4']['normalizado'],0)}% |

**O que pode fazer errar:** isso é retrato, com a pauta do passado. O meio pode mudar de lado. E a taxa de vitórias não avisa queda: Dilma venceu {br(D['serie']['2015']['vitoria_disputadas'],0)}% em 2015.

Detalhes: `RELATORIO.md`. Leitura da IA: `docs/LEITURA_DA_IA.md`.
"""
(R / "RESUMO_SIMPLES.md").write_text(SIMPLES, encoding="utf8")

LEITURA = f"""# Leitura da IA (opinião marcada como opinião)

Esta é a leitura do Claude sobre os números, e não fato.

1. **A pergunta que circula está mal posta.** "Consegue governar" são pelo menos 7 perguntas, com respostas diferentes.
2. **A eleição mudou menos a Câmara do que parece e mais o Senado.** O PL cresceu sobre gente que já votava contra o governo, e a esquerda ficou perto de onde estava. No Senado, cadeiras do meio viraram cadeiras de PL e Novo.
3. **O problema de Lula é anterior a 2027.** Em 2025 e 2026 ele já perdia muito mais que em 2023. O veto, a MP e o orçamento já tinham mudado de mão. O novo Congresso encontra um governo que já negociava caso a caso.
4. **O preço importa mais que a contagem.** Com {D['cadeiras']['pendulo']} cadeiras no meio e {c['pendulo_com_governo']['venceu']} de {c['pendulo_com_governo']['votacoes']} quando elas vêm, tudo se resume a quanto custa trazê-las, com R$ 44,8 bi em emendas que já não dependem do governo.
5. **Impeachment de Lula é o medo da internet. Impeachment de ministro e anistia são a disputa de verdade.** Quem tem nome e data está mirando o Supremo.
6. **O que me faria mudar de ideia:** o PL fora do bloco de Motta e Marinho eleito; ótimo e bom abaixo de 25% com gente na rua; o meio votando abaixo de 50% com o governo por 6 meses; um escândalo com denúncia contra o próprio presidente.
"""
(R / "docs/LEITURA_DA_IA.md").write_text(LEITURA, encoding="utf8")
print("ok")
