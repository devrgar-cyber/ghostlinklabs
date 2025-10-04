# ghostlink/tools/link.py
from __future__ import annotations
from pathlib import Path
import json, time
from ..runtime.policy import SovereigntyGate
from ..runtime.context import Context

def main(ctx: Context, target: str, role: str = ""):
    """
    LINK {thread|role}: stitch a reference into the current lane.
    Implementation: append to vault/ghoststate.json (ephemeral continuity).
    """
    SovereigntyGate.require(ctx, "filesystem")
    state_path = Path(ctx.vault_path) / "ghoststate.json"
    state = {}
    if state_path.exists():
        try: state = json.loads(state_path.read_text())
        except Exception: state = {}
    links = state.get("links", [])
    entry = {"ts": time.time(), "target": target, "role": role}
    links.append(entry)
    state["links"] = links
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True))
    return {"linked": entry, "total_links": len(links)}
