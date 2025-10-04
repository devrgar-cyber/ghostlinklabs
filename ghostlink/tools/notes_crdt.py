# ghostlink/tools/notes_crdt.py
from __future__ import annotations
from pathlib import Path
import time, yaml
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate

"""Simple CRDT-like ops on memory_layer_01.vault: add_line|set_kv|del_k (commutative for these ops)."""

def main(ctx: Context, op: str, key: str = "notes", value: str | None = None):
    SovereigntyGate.require(ctx, "filesystem", path=ctx.vault_path)
    p = Path(ctx.vault_path) / "memory_layer_01.vault"
    raw = yaml.safe_load(p.read_text()) if p.exists() else None
    if not isinstance(raw, dict):
        data: dict[str, object] = {"version": 1}
    else:
        data = raw
    if "notes" not in data or not isinstance(data["notes"], list):
        data["notes"] = []
    if op == "add_line":
        existing = data.get(key)
        arr = list(existing) if isinstance(existing, list) else []
        arr.append(f"{int(time.time())}: {value if value is not None else ''}")
        data[key] = arr
    elif op == "set_kv":
        kv = data.get("kv")
        if not isinstance(kv, dict):
            kv = {}
        kv[key] = value
        data["kv"] = kv
    elif op == "del_k":
        if "kv" in data and key in data["kv"]: del data["kv"][key]
    else:
        return {"error": "unknown op"}
    p.write_text(yaml.safe_dump(data, sort_keys=True))
    return {"ok": True}
