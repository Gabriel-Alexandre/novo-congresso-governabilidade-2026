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
    d = pd.DataFrame(SEN["escada"]).rename(columns={"cadeiras_2027": "c"})
    d["cadeiras_2027"] = d.c
    escada(d, "cadeiras_2027", [(27, "barra\nimpeachment"), (41, "maioria\nSTF"), (49, "PEC")], "Senado: de quem o governo precisa", "As 81 cadeiras de 2027, na ordem de quanto cada sigla votou com a bancada do PT", "g02_escada_senado", "TSE e Senado, votações nominais abertas de 2023 a 2026", 81)


def g03():
    fig, ax = nova("As mesmas votações, com o novo Congresso", "Quantas o governo venceria: o que aconteceu e o que aconteceria com os eleitos")
    v = [("Câmara", CAM["replay_total"]["vitoria_real_pct"], CAM["replay_total"]["vitoria_replay_pct"], CAM["replay_total"]["n"]), ("Senado", SEN["total"]["vitoria_real_pct"], SEN["total"]["vitoria_2027_pct"], SEN["total"]["n"])]
    for i, (n, a, b, tot) in enumerate(v):
        ax.bar(i * 3, a, color=CLARO, width=1)
        ax.bar(i * 3 + 1.05, b, color=AZUL if n == "Câmara" else VERM, width=1)
        ax.text(i * 3, a + 1.5, f"{a:.0f}%".replace(".", ","), ha="center", fontsize=40, fontweight="bold", color=CINZA)
        ax.text(i * 3 + 1.05, b + 1.5, f"{b:.0f}%".replace(".", ","), ha="center", fontsize=40, fontweight="bold")
        ax.text(i * 3, -5, "o que foi", ha="center", fontsize=20, color=CINZA)
        ax.text(i * 3 + 1.05, -5, "com os eleitos", ha="center", fontsize=20)
        ax.text(i * 3 + .52, -11, f"{n} · {tot} votações", ha="center", fontsize=25, fontweight="bold")
    ax.axhline(50, color="#222222", lw=1.5, ls=":")
    ax.set_ylim(-13, 100)
    ax.set_xlim(-1, 5.2)
    ax.axis("off")
    salvar(fig, "g03_replay", "Câmara e Senado, dados abertos; cada reeleito repete o próprio voto, novo vota como a sigla")


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


def _barra_pres(col, titulo, sub, arq, fonte, fn, fmt):
    d = pd.read_csv(RES / "c5_mp_veto_por_presidente.csv", index_col=0)
    ordem = ["Lula I", "Lula II", "Dilma I", "Temer", "Bolsonaro", "Lula III"]
    fig, ax = nova(titulo, sub)
    v = [fn(d.loc[p]) for p in ordem]
    ax.bar(ordem, v, color=[CLARO] * 5 + [VERM])
    for i, x in enumerate(v):
        ax.text(i, x + max(v) * .02, fmt(d.loc[ordem[i]]), ha="center", fontsize=28, fontweight="bold")
    ax.spines["left"].set_visible(False)
    ax.set_yticks([])
    ax.set_ylim(0, max(v) * 1.2)
    salvar(fig, arq, fonte)


def g05():
    _barra_pres("mp", "A medida provisória parou de virar lei", "De cada 100 MPs editadas, quantas viraram lei", "g05_mp", "Senado, dados abertos de processos. Parte é crédito extraordinário ou virou projeto de lei", lambda r: r.mp_pct_lei, lambda r: f"{r.mp_pct_lei:.0f}%")


def g06():
    _barra_pres("veto", "O veto parou de segurar", "Vetos com alguma parte derrubada, por presidente", "g06_veto", "Senado, dados abertos de processos. Lula III com vetos ainda em aberto", lambda r: r.vetos_derrubados_algum, lambda r: f"{int(r.vetos_derrubados_algum)} de {int(r.vetos)}")


def g07():
    C = pd.read_csv(RES / "c6_curva_do_centro.csv")
    C = C[C.afastamento_centro_pct >= 0]
    fig, ax = nova("O governo não depende do PL. Depende do centro", "Votações que o governo venceria, conforme o centro se afasta do que já votou")
    ax.plot(C.afastamento_centro_pct, C.vitoria_pct, color=AZUL, lw=5, marker="o", ms=11)
    ax.axhline(50, color="#222222", lw=1.5, ls=":")
    ax.annotate("Dilma, 2014: aliados caíram mais\nde 40% e ela venceu 54%", xy=(40, 54.7), xytext=(5, 34), fontsize=22, color=VERM, fontweight="bold", arrowprops=dict(arrowstyle="->", color=VERM, lw=2))
    ax.text(0, 86, "hoje: 81%", fontsize=24, fontweight="bold")
    ax.set_xlabel("quanto o centro se afasta (%)")
    ax.set_ylabel("% de vitórias do governo")
    ax.set_ylim(20, 95)
    salvar(fig, "g07_curva_centro", "cálculo deste projeto sobre as votações nominais da Câmara de 2023 a 2026")


def g08():
    r = pd.read_csv(RES / "s1_replay_senado_2027.csv")
    fig, ax = nova("No Senado, os votos do governo caem", "Votos com o governo em cada votação disputada, de 2023 a 2026 e com os senadores de 2027")
    bins = range(0, 81, 4)
    ax.hist(r.com_gov, bins=bins, color=CLARO, label="o que foi", alpha=.95)
    ax.hist(r.com, bins=bins, color=VERM, label="com os senadores de 2027", alpha=.7)
    ax.axvline(41, color="#222222", lw=2.5, ls="--")
    ax.text(41.6, ax.get_ylim()[1] * .92, "41: maioria e STF", fontsize=22, fontweight="bold")
    ax.legend(frameon=False, loc="upper left", fontsize=20, bbox_to_anchor=(.0, .98))
    ax.set_xlabel("votos com o governo")
    ax.set_ylabel("votações")
    salvar(fig, "g08_senado_votos", "Senado, 83 votações nominais abertas disputadas; 42 senadores sem histórico votam como a sigla")


def g09():
    fig, ax = nova("O que derrubou presidente no Brasil", "Quem caiu e quem ficou: aprovação, presidente da Câmara e os votos que barram o processo (172)")
    cab = ["", "Ruim ou péssimo", "Presidente da Câmara", "Votos com ele", "Fim"]
    lin = [["Collor, 1992", "68%", "abriu o processo", "38", "caiu"],
           ["Dilma, 2016", "71%", "rompido com o governo", "137", "caiu"],
           ["Temer, 2017", "69%", "aliado", "263", "ficou"],
           ["Lula, hoje", "41%", "apoio de Lula a Motta", "esquerda tem 124", "?"]]
    ax.axis("off")
    x = [0, .22, .42, .72, .92]
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
    fig, ax = nova("A tarifa não trouxe o centro para o governo", "Votos do centro com o governo, nos 120 dias antes e nos 120 dias depois")
    for i, (_, r) in enumerate(e.iterrows()):
        ax.bar(i * 3, r.antes_pct, color=CLARO, width=1)
        ax.bar(i * 3 + 1.05, r.depois_pct, color=AZUL, width=1)
        ax.text(i * 3, r.antes_pct + 1, f"{r.antes_pct:.0f}%", ha="center", fontsize=34, fontweight="bold", color=CINZA)
        ax.text(i * 3 + 1.05, r.depois_pct + 1, f"{r.depois_pct:.0f}%", ha="center", fontsize=34, fontweight="bold")
        ax.text(i * 3, -5, "antes", ha="center", fontsize=20, color=CINZA)
        ax.text(i * 3 + 1.05, -5, "depois", ha="center", fontsize=20)
        ax.text(i * 3 + .52, -11, "Tarifa de 50%, jul/25" if "tarifa" in r.evento else "Sanção a Moraes, jul/25", ha="center", fontsize=23, fontweight="bold")
    ax.set_ylim(-13, 90)
    ax.set_xlim(-1, 5.2)
    ax.axis("off")
    salvar(fig, "g10_tarifa_centro", "Câmara. A pauta muda de um período para o outro: é descrição, não prova de causa")


def g11():
    P = json.loads((RES / "previsoes_final.json").read_text(encoding="utf8"))
    cor = {"C1": AZUL, "C2": VERDE, "C3": OURO, "C4": VERM}
    c = sorted(P["cenarios"], key=lambda x: -x["normalizado"])
    fig, ax = nova("O que esperar até o fim de 2027", "4 modelos de IA separados, mediana, somando 100. Previsões gravadas com data")
    for i, x in enumerate(c):
        y = len(c) - 1 - i
        ax.barh(y, x["normalizado"], color=cor[x["id"]], height=.62)
        ax.text(x["normalizado"] + 1, y, f"{x['normalizado']:.0f}%", va="center", fontsize=36, fontweight="bold")
        ax.text(0, y + .43, x["cenario"], fontsize=25, fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_ylim(-.5, 4.1)
    ax.axis("off")
    salvar(fig, "g11_cenarios", "dados/previsoes do repositório. A IA ainda acerta menos que os melhores previsores humanos")


for f in (g01, g02, g03, g04, g05, g06, g07, g08, g09, g10):
    f()
if (RES / "previsoes_final.json").exists():
    g11()
print("ok")
