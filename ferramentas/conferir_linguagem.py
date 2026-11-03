"""Procura no texto público as construções que este projeto não usa. Sai com erro se achar."""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQS = ["RELATORIO.md", "RESUMO_SIMPLES.md", "docs/LEITURA_DA_IA.md", "README.md"]
PROIBIDO = [r"\bmentiu\b", r"\bvai cair\b", r"\bvai ganhar\b", r"\btomou conta\b", r"\bvote\b", r"\bfavorito\b", r"—", r"semipresidencialismo"]
erros = 0
for a in ARQS:
    t = (RAIZ / a).read_text(encoding="utf-8")
    for p in PROIBIDO:
        for m in re.finditer(p, t, re.I):
            print(a, repr(t[max(0, m.start() - 50):m.end() + 40]))
            erros += 1
print(f"{erros} ocorrências")
sys.exit(1 if erros else 0)
