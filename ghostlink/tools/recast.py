# ghostlink/tools/recast.py
from __future__ import annotations
from ..runtime.context import Context
import json

def main(ctx: Context, data: dict, to: str = "json"):
    if to == "json": return {"text": json.dumps(data, indent=2, sort_keys=True)}
    if to == "table":
        k = list(data.keys()); rows = zip(*data.values())
        lines = ["\t".join(k)] + ["\t".join(map(str,r)) for r in rows]
        return {"text": "\n".join(lines)}
    return {"text": str(data)}
