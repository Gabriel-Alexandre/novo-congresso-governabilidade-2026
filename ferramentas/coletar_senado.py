"""Votacoes nominais do Senado por ano (2011 a 2026), pelo servico novo, com manifesto."""
import json, pathlib, urllib.request, hashlib, datetime as dt, time, sys
RAIZ = pathlib.Path(__file__).resolve().parents[1]
D = RAIZ / "dados" / "brutos" / "senado"; D.mkdir(parents=True, exist_ok=True)
man = []
for ano in range(2011, 2027):
    for sem, (a, b) in enumerate([("01-01", "06-30"), ("07-01", "12-31")]):
        arq = D / f"votacoes-{ano}-{sem+1}.json"
        url = f"https://legis.senado.leg.br/dadosabertos/votacao?dataInicio={ano}-{a}&dataFim={ano}-{b}"
        if not arq.exists():
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
            for t in range(4):
                try:
                    arq.write_bytes(urllib.request.urlopen(req, timeout=240).read()); break
                except Exception as e:
                    print("erro", url, e, file=sys.stderr); time.sleep(5)
        if arq.exists():
            b_ = arq.read_bytes()
            man.append({"url": url, "arquivo": arq.name, "bytes": len(b_), "sha256": hashlib.sha256(b_).hexdigest(), "capturado": dt.datetime.now().isoformat(timespec="seconds")})
            print(arq.name, len(b_), flush=True)
(RAIZ / "dados" / "MANIFESTO_SENADO.json").write_text(json.dumps(man, indent=1), encoding="utf8")
