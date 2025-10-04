# ghostlink/tools/reflect.py
from __future__ import annotations
from ..runtime.context import Context

def main(ctx: Context, data):
    t = type(data).__name__
    size = len(data) if hasattr(data,"__len__") else 1
    return {"type": t, "size": size, "summary": str(data)[:256]}
