# ghostlink/runtime/metrics.py
import json, time
from pathlib import Path

def write_metric(path: Path, **kv):
    obj = {"ts": time.time()} | kv
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, sort_keys=True) + "\n")
