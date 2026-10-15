"""S23 retrieval (Verifier, RA-1, RA-2): every source a canonical claim cites, re-retrieved once from the URL its
record holds, with plain curl (no changed client identity), into BYTES/<source_id>.bin. One JSON line per request:
source, URL, host, UTC time, HTTP status, effective URL, content type, size, SHA-256. A refusal is an access gap;
nothing is retried under another identity. Standard library + the system curl. Run from the repository root."""
import datetime, hashlib, json, subprocess, sys, urllib.parse
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
claims = json.load(open("data/claims.json")); sources = {s["id"]: s for s in json.load(open("data/sources.json"))}
cited = sorted({ci["source_id"] for c in claims for ci in c.get("citations", [])})
for sid in cited:
    url = sources[sid]["url"]; f = out / f"{sid}.bin"
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "180", "-o", str(f), "-w",
                        "%{http_code}\t%{url_effective}\t%{content_type}", url], capture_output=True, text=True)
    status, eff, ctype = (r.stdout.split("\t") + ["", "", ""])[:3]
    data = f.read_bytes() if f.exists() else b""
    print(json.dumps({"source_id": sid, "url": url, "host": urllib.parse.urlsplit(url).hostname, "time": t,
                      "status": status, "effective_url": eff, "content_type": ctype, "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest() if data else None,
                      "curl_error": r.stderr.strip() or None, "method_registered": sources[sid]["retrieval"]["method"]}),
          flush=True)
