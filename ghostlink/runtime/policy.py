# ghostlink/runtime/policy.py
from __future__ import annotations
from typing import Dict, Any, Optional
from pathlib import Path
import yaml, os
from .context import Context

class Denied(Exception): ...

BASE = Path(__file__).resolve().parents[1]
VAULT = BASE / "vault"

# Load tool allowlist & profiles at import (best-effort; fall back permissive within sovereignty constraints)
_DEF_ALLOW = {"MAP","CLEANSE","RECAST","REFLECT","SCAN","MIRROR","FORGE","LINK","STATUS",
              "LENS","MACRO","SUMMARIZE","EMBED_INDEX","DNA_ARCHIVE","DNA_RESTORE",
              "VAULT_ENCRYPT","VAULT_DECRYPT",
              "GPIO_READ","CAN_READ","OBD_READ","ADC_READ","SERIAL_SNIFF","CAMERA_SNAP","FLIR_READ",
              "NOTES_CRDT"}

def _load_yaml(p: Path) -> dict:
    try:
        return yaml.safe_load(p.read_text()) if p.exists() else {}
    except Exception:
        return {}

def _panic_flag() -> bool:
    return (VAULT / ".panic").exists() or os.environ.get("GL_PANIC_MODE") == "1"

class Wraithgate:
    """Admission control: deny unsafe parameters or tools + panic/profile rules."""
    @staticmethod
    def enforce(ctx: Context, tool: str, params: Dict[str, Any]):
        tool = tool.upper()
        # PANIC: only allow status, scan, mirror, verify-like tools
        if _panic_flag() and tool not in {"STATUS","SCAN","MIRROR"}:
            raise Denied("panic mode: only STATUS/SCAN/MIRROR permitted")

        # Allowlist
        policy = _load_yaml(VAULT / "tool_policy.vault") or {}
        allow = set(policy.get("allow", _DEF_ALLOW))
        if tool not in allow:
            raise Denied(f"tool not allowed by policy: {tool}")

        # Path traversal / size caps for common parameters
        for key in ("source","path","artifact"):
            if key in params:
                val = str(params[key])
                if ".." in val:
                    raise Denied("path traversal")
        # Profile-specific restrictions
        profiles = _load_yaml(VAULT / "policy_profiles.vault") or {}
        prof = (profiles.get("profiles", {}) or {}).get(ctx.policy_profile, {})
        max_bytes = int(prof.get("max_bytes", 10_000_000))
        for key in ("content",):
            if key in params and isinstance(params[key], (str, bytes)):
                size = len(params[key]) if isinstance(params[key], (bytes,bytearray)) else len(params[key].encode())
                if size > max_bytes:
                    raise Denied("payload too large for profile")
        return True

class SovereigntyGate:
    """Explicit operator grant enforcement + scope enforcement."""
    @staticmethod
    def require(ctx: Context, target: str, path: Optional[str] = None, bytes_out: Optional[int] = None):
        for g in ctx.grants:
            if g.target != target or not g.allowed:
                continue
            # TTL
            if g.expires_at and g.expires_at <= __import__("time").time():
                continue
            # Scope (filesystem path prefixes)
            if path and g.scopes:
                p = Path(path).resolve()
                ok: bool = False
                for pref in g.scopes:
                    try:
                        if str(p).startswith(str(Path(pref).resolve())):
                            ok = True; break
                    except Exception:
                        continue
                if not ok:
                    raise Denied("path outside grant scope")
            # Size cap
            if bytes_out is not None and g.max_bytes is not None and bytes_out > g.max_bytes:
                raise Denied("bytes exceed grant cap")
            return True
        raise Denied(f"sovereignty gate closed for {target}")
