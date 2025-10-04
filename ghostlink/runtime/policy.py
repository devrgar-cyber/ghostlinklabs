# ghostlink/runtime/policy.py
from __future__ import annotations
from typing import Dict, Any
from .context import Context

class Denied(Exception): ...

class Wraithgate:
    """Admission control: deny unsafe parameters or tools."""
    @staticmethod
    def enforce(ctx: Context, tool: str, params: Dict[str, Any]):
        # deny banned tools
        if tool in {"os","sys","subprocess","shutil"}:
            raise Denied("unsafe tool")
        # coarse path safety for common param names
        for key in ("source","path","artifact"):
            if key in params:
                val = str(params[key])
                if ".." in val:
                    raise Denied("path traversal")
        return True

class SovereigntyGate:
    """Explicit operator grant enforcement."""
    @staticmethod
    def require(ctx: Context, target: str):
        for g in ctx.grants:
            if g.target == target and g.allowed:
                return True
        raise Denied(f"sovereignty gate closed for {target}")
