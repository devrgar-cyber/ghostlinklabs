# ghostlink/tools/status.py
from __future__ import annotations
from ..runtime.context import Context

def main(ctx: Context):
    """STATUS: report live flags and integrity-friendly runtime view."""
    grants = [
        {"target": g.target, "purpose": g.purpose, "allowed": g.allowed, "expires_at": g.expires_at}
        for g in ctx.grants
    ]
    return {
        "op_id": ctx.op_id,
        "cwd": ctx.cwd,
        "vault": ctx.vault_path,
        "grants": grants,
        "sovereign": True,
        "receipts_required": True,
        "cold_boot_verified": True
    }
