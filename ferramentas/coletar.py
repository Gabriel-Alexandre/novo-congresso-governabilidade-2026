"""Baixa as votacoes nominais da Camara (2003 a 2026) e grava o manifesto com hash."""
import hashlib, json, pathlib, time, urllib.request, datetime as dt, sys
RAIZ = pathlib.Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "dados" / "brutos" / "camara"
BASE = "https://dadosabertos.camara.leg.br/arquivos"
TIPOS = {"votacoes": "votacoes", "votacoesVotos": "votacoesVotos", "votacoesOrientacoes": "votacoesOrientacoes", "votacoesObjetos": "votacoesObjetos"}
def baixar(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 projeto-publico"})
    for tent in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r, open(destino, "wb") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b: break
                    f.write(b)
            return True
        except Exception as e:
            print("erro", url, e, file=sys.stderr); time.sleep(5 * (tent + 1))
    return False
def main():
    BRUTOS.mkdir(parents=True, exist_ok=True)
    man = []
    for ano in range(2003, 2027):
        for t in TIPOS:
            url = f"{BASE}/{t}/csv/{t}-{ano}.csv"
            d = BRUTOS / f"{t}-{ano}.csv"
            if not d.exists() or d.stat().st_size == 0:
                if not baixar(url, d):
                    continue
            h = hashlib.sha256(d.read_bytes()).hexdigest()
            man.append({"url": url, "arquivo": d.name, "bytes": d.stat().st_size, "sha256": h, "capturado": dt.datetime.now().isoformat(timespec="seconds")})
            print(d.name, d.stat().st_size, flush=True)
    (RAIZ / "dados" / "MANIFESTO_CAMARA.json").write_text(json.dumps(man, indent=1), encoding="utf8")
if __name__ == "__main__":
    main()
