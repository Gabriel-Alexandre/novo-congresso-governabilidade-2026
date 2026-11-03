"""Coerência dos números publicados."""
import csv
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = json.loads((R / "resultados/RESUMO.json").read_text(encoding="utf8"))
P = json.loads((R / "resultados/previsoes_final.json").read_text(encoding="utf8"))


def test_cadeiras_somam_513():
    assert sum(D["cadeiras"].values()) == 513


def test_senado_composicao():
    assert D["senado"]["senadores_com_historico"] + D["senado"]["senadores_novos"] == 81


def test_pendulo_soma_as_votacoes():
    c = D["camara"]
    assert c["pendulo_com_governo"]["votacoes"] + c["pendulo_contra_governo"]["votacoes"] == c["total"]["n"]


def test_cenarios_somam_100():
    assert abs(sum(c["normalizado"] for c in P["cenarios"]) - 100) < .5


def test_coerencia_previsoes():
    assert all(x["passou"] for x in P["coerencia"])


def test_hipoteses_colunas():
    for x in csv.DictReader(open(R / "dados/e_hipoteses.csv", encoding="utf-8")):
        for h in ("H1_folga", "H2_negocia", "H3_trava", "H4_cai"):
            assert x[h].strip() in ("C", "I", "N")


def test_escada_senado_cresce():
    e = D["senado"]["escada_trazidos"]
    assert e["2"] <= e["4"] <= e["6"] <= e["8"]


def test_mp_lula3_abaixo_de_lula1():
    assert D["mp"]["Lula III"]["pct"] < D["mp"]["Lula I"]["pct"]
