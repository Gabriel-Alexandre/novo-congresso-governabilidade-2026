"""Confere tamanho contra Content-Length, retoma com curl o que veio truncado e regrava o manifesto com hash."""
import hashlib, json, pathlib, urllib.request, subprocess, datetime as dt
R = pathlib.Path(__file__).resolve().parents[1]; M = R/"dados/MANIFESTO_CAMARA.json"; man = json.loads(M.read_text())
ruins = []
for m in man:
    d = R/"dados/brutos/camara"/m["arquivo"]
    req = urllib.request.Request(m["url"], method="HEAD", headers={"User-Agent":"Mozilla/5.0"})
    n = int(urllib.request.urlopen(req, timeout=60).headers.get("Content-Length") or -1)
    for t in range(25):
        if d.stat().st_size == n: break
        print("retomando", d.name, d.stat().st_size, n, flush=True)
        subprocess.run(["curl","-s","-A","Mozilla/5.0","-C","-","-m","300","-o",str(d),m["url"]])
    if d.stat().st_size != n: ruins.append(d.name)
    b = d.read_bytes(); m.update(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), capturado=dt.datetime.now().isoformat(timespec="seconds"))
M.write_text(json.dumps(man, indent=1)); print("ok", len(man), "incompletos:", ruins)
