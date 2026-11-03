"""Graficos 1920x1080 a partir de resultados/. Uso: python ferramentas/graficos.py (grava em resultados/figuras/)."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
FIG = RES / "figuras"
AZUL, VERM, CINZA, VERDE, OURO = "#2D6A8A", "#C8553D", "#6B6B6B", "#2E8B57", "#C9902B"
CLARO = "#D9D9D9"
RODAPE = "github.com/Gabriel-Alexandre/novo-congresso-governabilidade-2026 · análise feita pelo Claude"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 22, "axes.spines.top": False, "axes.spines.right": False})
CAM = json.loads((RES / "RESUMO_CAMARA.json").read_text(encoding="utf8"))
SEN = json.loads((RES / "RESUMO_SENADO.json").read_text(encoding="utf8"))
EXT = json.loads((RES / "RESUMO_EXTRAS.json").read_text(encoding="utf8"))
R2 = json.loads((RES / "RESUMO.json").read_text(encoding="utf8"))
NOMES = {"UNIAO": "União", "PCDOB": "PCdoB", "PODE": "Podemos", "REPUBLICANOS": "Repub.", "SOLIDARIEDADE": "Solidariedade", "S/PARTIDO": "sem partido", "REDE": "Rede", "NOVO": "Novo", "AVANTE": "Avante"}


def nome(s):
    return NOMES.get(s, s)


def nova(titulo, subtitulo):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.subplots_adjust(left=0.08, right=0.95, top=0.78, bottom=0.18)
    fig.suptitle(titulo, x=0.05, y=0.965, ha="left", fontsize=36, fontweight="bold")
    fig.text(0.05, 0.86, subtitulo, ha="left", fontsize=21, color="#444444")
    return fig, ax


def salvar(fig, nome_arq, fonte):
    fig.text(0.05, 0.05, f"Fonte: {fonte}", fontsize=15, color="#555555")
    fig.text(0.05, 0.018, RODAPE, fontsize=15, color="#555555")
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{nome_arq}.png")
    plt.close(fig)


def escada(df, col, linhas, titulo, sub, arq, fonte, total):
    fig, ax = nova(titulo, sub)
    x = df[df[col] > 0]
    ini = 0
    for _, r in x.iterrows():
        a = r["alinhamento_2023_26"]
        cor = AZUL if a >= 80 else (OURO if a >= 40 else VERM)
        ax.barh(0, r[col], left=ini, color=cor, edgecolor="white", height=.55)
        if r[col] >= total * .035:
            ax.text(ini + r[col] / 2, 0, f"{nome(r['sig'])}\n{int(r[col])}", ha="center", va="center", color="white", fontsize=15, fontweight="bold")
        ini += r[col]
    for v, rot in linhas:
        ax.axvline(v, color="#222222", lw=2.5, ls="--", ymin=.1, ymax=.84)
        ax.text(v, .47, f"{v}\n{rot}", ha="center", va="bottom", fontsize=17, fontweight="bold")
    ax.set_xlim(0, total)
    ax.set_ylim(-.6, 1)
    ax.axis("off")
    ax.text(0, -.48, "Da sigla que mais votou com o governo em 2023 a 2026 (esquerda do gráfico) à que menos votou (direita)", fontsize=18, color="#444444")
    salvar(fig, arq, fonte)


def g01():
    d = pd.DataFrame(CAM["escada"])
    d = d[d.cadeiras_2027 > 0]
    escada(d, "cadeiras_2027", [(172, "barra\nimpeachment"), (257, "maioria"), (308, "PEC")], "Câmara: de quem o governo precisa", "As 513 cadeiras eleitas, na ordem de quanto cada sigla votou com o governo", "g01_escada_camara", "TSE e Câmara, votações nominais disputadas de 2023 a 2026", 513)


def g02():
    d = pd.DataFrame(R2["senado"]["escada"])
    escada(d, "cadeiras_2027", [(27, "barra\nimpeachment"), (41, "maioria\nSTF"), (49, "PEC")], "Senado: de quem o governo precisa", "As 81 cadeiras de 2027, na ordem de quanto cada sigla votou com a bancada do PT", "g02_escada_senado", "TSE e Senado, votações nominais abertas de 2023 a 2026", 81)


def g03():
    fig, ax = nova("As mesmas votações, com o novo Congresso", "De 100 votações apertadas de 2023 a 2026, quantas o governo venceria. Retrato, não previsão")
    C_, S_ = R2["camara"]["total"], R2["senado"]["total"]
    v = [("Câmara", C_["real_pct"], C_["novo_pct"], C_["n"], f"{C_['novo_pct']:.0f}%", AZUL), ("Senado", S_["real_pct"], S_["novo_pct"], S_["n"], "30 a 45%", VERM)]
    for i, (n, a, b, tot, rot, cor) in enumerate(v):
        ax.bar(i * 3, a, color=CLARO, width=1)
        ax.bar(i * 3 + 1.05, b, color=cor, width=1)
        ax.text(i * 3, a + 1.5, f"{a:.0f}%", ha="center", fontsize=40, fontweight="bold", color=CINZA)
        ax.text(i * 3 + 1.05, b + 1.5, rot, ha="center", fontsize=36, fontweight="bold")
        ax.text(i * 3, -6, "o que foi", ha="center", fontsize=20, color=CINZA)
        ax.text(i * 3 + 1.05, -6, "com os eleitos", ha="center", fontsize=20)
        ax.text(i * 3 + .52, -14, f"{n} · {tot} votações", ha="center", fontsize=25, fontweight="bold")
    ax.axhline(50, color="#222222", lw=1.5, ls=":")
    ax.set_ylim(-18, 100)
    ax.set_xlim(-1, 5.2)
    ax.axis("off")
    salvar(fig, "g03_replay", "Câmara e Senado, dados abertos; reeleito repete o voto, novo vota como a sigla; Senado pela posição do PT")


def g04():
    S = pd.read_csv(RES / "c1_serie_por_ano.csv", index_col=0)
    fig, ax = nova("O governo vence menos do que vencia", "Votações disputadas da Câmara vencidas pelo governo, por ano, de 2003 a 2026")
    ax.plot(S.index, S.vitoria_disputadas, color=AZUL, lw=4, marker="o", ms=9)
    for a, dy in ((2014, -9), (2015, -9), (2025, -9), (2026, 5), (2023, 4)):
        ax.text(a, S.loc[a, "vitoria_disputadas"] + dy, f"{S.loc[a, 'vitoria_disputadas']:.0f}%", ha="center", fontsize=22, fontweight="bold", color=VERM if a in (2014, 2015, 2025) else "#222222")
    for a, n in ((2003, "Lula I"), (2007, "Lula II"), (2011, "Dilma I"), (2015, "Dilma II"), (2016.6, "Temer"), (2019, "Bolsonaro"), (2023, "Lula III")):
        ax.axvline(a - .5, color=CLARO, lw=1.5)
        ax.text(a - .4, 40, n, fontsize=16, color=CINZA)
    ax.set_ylim(38, 106)
    ax.set_xlim(2002.4, 2026.6)
    ax.set_ylabel("% de vitórias")
    salvar(fig, "g04_serie", "Câmara, votações nominais de plenário com orientação do governo; perdedor com pelo menos 10% dos votos")


def g05():
    o = ["Lula I", "Lula II", "Dilma I", "Dilma II", "Temer", "Bolsonaro", "Lula III"]
    v = [R2["mp"][p]["pct"] for p in o]
    fig, ax = nova("A medida provisória parou de virar lei", "De cada 100 MPs editadas, quantas viraram lei")
    ax.bar(o, v, color=[CLARO] * 6 + [VERM])
    for i, x in enumerate(v):
        ax.text(i, x + 2, f"{x:.0f}%", ha="center", fontsize=30, fontweight="bold")
    ax.spines["left"].set_visible(False)
    ax.set_yticks([])
    ax.set_ylim(0, 110)
    salvar(fig, "g05_mp", "Congresso, dados abertos. Em Lula III nenhuma rejeitada no voto; 154 perderam a validade. Sem crédito extraordinário, 20%")


def g06():
    o = ["Dilma II", "Temer", "Bolsonaro", "Lula III"]
    fig, ax = nova("O veto parou de segurar", "Dos vetos já decididos pelo Congresso, quantos tiveram alguma parte derrubada")
    v = [R2["veto"][p]["pct_decididos"] for p in o]
    ax.bar(o, v, color=[CLARO] * 3 + [VERM])
    for i, x in enumerate(v):
        q = R2["veto"][o[i]]
        ax.text(i, x + 1.5, f"{x:.0f}%", ha="center", fontsize=36, fontweight="bold")
        ax.text(i, x / 2, f"{int(q['com_algo_derrubado'])} de {int(q['decididos'])}", ha="center", fontsize=22)
    ax.spines["left"].set_visible(False)
    ax.set_yticks([])
    ax.set_ylim(0, 70)
    salvar(fig, "g06_veto", "Congresso, dados abertos. Antes de 2013 muitos vetos nem eram votados. Em 24 meses, Lula III e Bolsonaro empatam")


def g07():
    a, b = R2["camara"]["pendulo_com_governo"], R2["camara"]["pendulo_contra_governo"]
    fig, ax = nova("Quem decide é quem está no meio", "As 257 cadeiras que não são da esquerda nem de PL e Novo, em 678 votações apertadas")
    ax.axis("off")
    for i, (txt, x, cor) in enumerate((("Quando a maioria do meio foi com o governo", a, AZUL), ("Quando a maioria do meio foi contra", b, VERM))):
        y = .68 - i * .42
        ax.text(0, y + .13, txt, fontsize=28, color="#333333")
        ax.text(0, y - .03, f"o governo venceu {x['venceu']} de {x['votacoes']}", fontsize=50, fontweight="bold", color=cor)
    ax.set_ylim(0, 1)
    salvar(fig, "g07_pendulo", "Câmara, votações nominais de plenário de 2023 a 2026 com orientação do governo")


def g08():
    r = pd.read_csv(RES / "s1_replay_senado_r2.csv")
    fig, ax = nova("No Senado, os votos do governo caem", "Votos com o governo em cada votação disputada, de 2023 a 2026 e com os senadores de 2027")
    bins = range(0, 81, 4)
    ax.hist(r.com_gov, bins=bins, color=CLARO, label="o que foi", alpha=.95)
    ax.hist(r.com, bins=bins, color=VERM, label="com os senadores de 2027", alpha=.7)
    ax.axvline(41, color="#222222", lw=2.5, ls="--")
    ax.text(41.6, ax.get_ylim()[1] * .92, "41: maioria e STF", fontsize=22, fontweight="bold")
    ax.legend(frameon=False, loc="upper left", fontsize=20, bbox_to_anchor=(.0, .98))
    ax.set_xlabel("votos com o governo")
    ax.set_ylabel("votações")
    salvar(fig, "g08_senado_votos", "Senado, 83 votações nominais abertas disputadas; 40 senadores sem histórico votam como a sigla")


def g09():
    fig, ax = nova("O que derrubou presidente no Brasil", "Quem caiu e quem ficou: aprovação, presidente da Câmara e os votos que barram o processo (172)")
    cab = ["", "Ruim ou péssimo", "Presidente da Câmara", "Votos com ele", "Fim"]
    lin = [["Collor, 1992", "68%", "abriu o processo", "38", "caiu"],
           ["Dilma, 2016", "71%", "rompido com o governo", "137", "caiu"],
           ["Temer, 2017", "69%", "aliado", "263", "ficou"],
           ["Lula, hoje", "41%", "apoio de Lula a Motta", "esquerda: 124", "?"]]
    ax.axis("off")
    x = [0, .2, .38, .69, .92]
    for j, c in enumerate(cab):
        ax.text(x[j], .95, c, fontsize=20, fontweight="bold", color=CINZA, va="center")
    for i, l in enumerate(lin):
        y = .75 - i * .21
        for j, c in enumerate(l):
            cor = VERM if (j == 4 and c == "caiu") else (VERDE if (j == 4 and c == "ficou") else "#222222")
            ax.text(x[j], y, c, fontsize=24, fontweight="bold" if j in (0, 4) else "normal", color=cor, va="center")
        if i == 3:
            ax.axhspan(y - .08, y + .08, color="#EEF3F6", zorder=0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    salvar(fig, "g09_queda", "Câmara dos Deputados; Datafolha (set/1992, ago/2015, jun/2017, out/2026); Pérez-Liñán")


def g10():
    E = pd.DataFrame(EXT["eventos_eua"])
    e = E[(E.janela_dias == 120) & (E.campo == "centro") & (~E.evento.str.contains("25%"))]
    fig, ax = nova("A tarifa não uniu o plenário", "Votos com o governo das 257 cadeiras do meio, nos 120 dias antes e nos 120 dias depois")
    for i, (_, r) in enumerate(e.iterrows()):
        ax.bar(i * 3, r.antes_pct, color=CLARO, width=1)
        ax.bar(i * 3 + 1.05, r.depois_pct, color=AZUL, width=1)
        ax.text(i * 3, r.antes_pct + 1, f"{r.antes_pct:.0f}%", ha="center", fontsize=34, fontweight="bold", color=CINZA)
        ax.text(i * 3 + 1.05, r.depois_pct + 1, f"{r.depois_pct:.0f}%", ha="center", fontsize=34, fontweight="bold")
        ax.text(i * 3, -6, "antes", ha="center", fontsize=20, color=CINZA)
        ax.text(i * 3 + 1.05, -6, "depois", ha="center", fontsize=20)
        ax.text(i * 3 + .52, -14, "Tarifa de 50%, jul/25" if "tarifa" in r.evento else "Sanção a Moraes, jul/25", ha="center", fontsize=23, fontweight="bold")
    ax.set_ylim(-18, 90)
    ax.set_xlim(-1, 5.2)
    ax.axis("off")
    salvar(fig, "g10_tarifa_centro", "Câmara. A pauta muda de um período para o outro, e em agosto de 2025 subiu a 78%: descrição, não causa")


def g11():
    P = json.loads((RES / "previsoes_final.json").read_text(encoding="utf8"))
    cor = {"C1": AZUL, "C2": VERDE, "C3": OURO, "C4": VERM}
    c = sorted(P["cenarios"], key=lambda x: -x["normalizado"])
    fig, ax = nova("O que esperar até o fim de 2027", "4 modelos de IA da mesma empresa, mediana, somando 100. Previsões gravadas com data")
    for i, x in enumerate(c):
        y = len(c) - 1 - i
        ax.barh(y, x["normalizado"], color=cor[x["id"]], height=.62)
        ax.text(x["normalizado"] + 1, y, f"{x['normalizado']:.0f}%", va="center", fontsize=36, fontweight="bold")
        ax.text(0, y + .43, x["cenario"], fontsize=25, fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_ylim(-.5, 4.1)
    ax.axis("off")
    salvar(fig, "g11_cenarios", "dados/previsoes do repositório. A IA ainda acerta menos que os melhores previsores humanos")


def g12():
    e = R2["senado"]["escada_trazidos"]
    xs = [0, 2, 4, 6, 8]
    ys = [R2["senado"]["total"]["novo_pct"]] + [e[str(k)] for k in xs[1:]]
    fig, ax = nova("Quantos senadores o governo precisa trazer", "Votações apertadas que venceria, conforme traz senadores do outro lado")
    ax.bar([str(x) for x in xs], ys, color=[VERM, OURO, AZUL, AZUL, AZUL])
    for i, y in enumerate(ys):
        ax.text(i, y + 1.5, f"{y:.0f}%", ha="center", fontsize=34, fontweight="bold")
    ax.axhline(50, color="#222222", lw=1.5, ls=":")
    ax.set_xlabel("senadores trazidos")
    ax.spines["left"].set_visible(False)
    ax.set_yticks([])
    ax.set_ylim(0, 80)
    salvar(fig, "g12_senadores_trazidos", "Senado, 83 votações nominais abertas de 2023 a 2026, com os senadores de 2027")


def g13():
    c = R2["camara"]
    s = R2["senado"]
    lin = [("Ganhar votação comum na Câmara", f"{c['total']['novo_pct']:.0f}% das apertadas", "consegue, com o meio", VERDE),
           ("Ganhar votação comum no Senado", "3 a 4 em cada 10", "precisa trazer gente", OURO),
           ("Fazer a MP virar lei", f"{R2['mp']['Lula III']['pct']:.0f}% das editadas", "quase não consegue", VERM),
           ("Segurar veto", f"{R2['veto']['Lula III']['pct_decididos']:.0f}% com algo derrubado", "não segura", VERM),
           ("Mudar a Constituição", f"308 em {c['pct_308_novo']:.0f}%, 49 em {s['pct_49_novo']:.0f}%", "só com acordo amplo", VERM),
           ("Aprovar nome no STF", f"41 votos em {s['pct_41_novo']:.0f}%", "depende do Senado", OURO),
           ("Barrar processo contra ele", f"172 votos em {c['pct_172_novo']:.0f}%", "consegue", VERDE)]
    fig, ax = nova("Lula consegue governar? Depende do poder", "O retrato com os eleitos, se quem está no meio votar como votou de 2023 a 2026")
    ax.axis("off")
    for i, (a, b, d, cor) in enumerate(lin):
        y = .94 - i * .145
        ax.text(0, y, a, fontsize=22, fontweight="bold", va="center")
        ax.text(.46, y, b, fontsize=19, va="center")
        ax.text(.74, y, d, fontsize=20, color=cor, fontweight="bold", va="center")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    salvar(fig, "g13_placar", "este repositório; Câmara e Senado, dados abertos. Votação comum não é impeachment")


def g14():
    fig, ax = nova("Os 3 pedaços do novo Congresso", "Esquerda, PL e Novo, e quem fica no meio")
    cad = R2["cadeiras"]
    cs = {"esquerda": 15, "pendulo": 35, "PL e Novo": 31}
    for y, (nom, v, tot) in enumerate((("Senado", cs, 81), ("Câmara", cad, 513))):
        ini = 0
        for k, cor, rot in (("esquerda", AZUL, "esquerda"), ("pendulo", OURO, "o meio"), ("PL e Novo", VERM, "PL e Novo")):
            w = v[k] / tot * 100
            ax.barh(y, w, left=ini, color=cor, edgecolor="white", height=.6)
            ax.text(ini + w / 2, y, f"{rot}\n{v[k]}", ha="center", va="center", color="white", fontsize=25, fontweight="bold")
            ini += w
        ax.text(0, y + .36, nom, fontsize=26, fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_ylim(-.5, 1.75)
    ax.axis("off")
    salvar(fig, "g14_tres_pedacos", "TSE. O meio inclui União, PP e Republicanos, que se declaram direita, e o centro")


for f in (g01, g02, g03, g04, g05, g06, g07, g08, g09, g10, g12, g13, g14):
    f()
if (RES / "previsoes_final.json").exists():
    g11()
print("ok")
