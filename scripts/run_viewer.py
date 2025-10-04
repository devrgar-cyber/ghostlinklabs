# scripts/run_viewer.py
from __future__ import annotations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
rec_path = ROOT/"vault"/"receipts.log"
if not rec_path.exists():
    raise SystemExit("receipts.log not found; run at least one tool")
recs = rec_path.read_text().splitlines()
rows = [json.loads(x) for x in recs if x.strip()]
html = ["<html><body><h1>GhostLink Runs</h1><table border=1>"]
html.append("<tr><th>ts</th><th>run_id</th><th>tool</th><th>status</th><th>duration_ms</th></tr>")
for r in rows:
    html.append(f"<tr><td>{r.get('iso_ts')}</td><td>{r.get('run_id')}</td><td>{r.get('tool')}</td><td>{r.get('status')}</td><td>{r.get('duration_ms')}</td></tr>")
html.append("</table></body></html>")
(Path("outputs")).mkdir(exist_ok=True)
(Path("outputs/receipts.html")).write_text("\n".join(html), encoding="utf-8")
print("wrote outputs/receipts.html")
