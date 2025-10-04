# ghostlink/runtime/receipts.py
import json, time
from pathlib import Path
from .context import Receipt

def write_receipt(path: Path, r: Receipt):
    obj = r.__dict__ | {"iso_ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(r.ts))}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, sort_keys=True) + "\n")
