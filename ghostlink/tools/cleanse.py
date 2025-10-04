# ghostlink/tools/cleanse.py
from __future__ import annotations
from ..runtime.context import Context

def main(ctx: Context, data: dict, rules: dict | None = None):
    # trivial cleanser: drop empty lines and trim strings in a {"lines":[...]} payload
    if not isinstance(data, dict) or "lines" not in data:
        return {"data": data}
    lines = [str(ln).strip() for ln in data["lines"] if str(ln).strip()]
    return {"lines": lines}
