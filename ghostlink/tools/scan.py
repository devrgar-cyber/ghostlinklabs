# ghostlink/tools/scan.py
from __future__ import annotations
from pathlib import Path
import hashlib, re
from ..runtime.policy import SovereigntyGate
from ..runtime.context import Context

_WORD = re.compile(r"[A-Za-z0-9_'\-]+")

def main(ctx: Context, source: str):
    """SCAN {topic|file|fragment}: reflect & bind atoms from a file."""
    SovereigntyGate.require(ctx, "filesystem", path=source)
    p = Path(source)
    data = p.read_bytes()
    text = data.decode("utf-8", errors="replace")
    words = _WORD.findall(text)
    atoms = sorted(set(w.lower() for w in words))
    return {
        "file": str(p),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "line_count": text.count("\n") + (1 if text else 0),
        "atoms": atoms[:256],
        "atom_count": len(atoms),
        "preview": text.splitlines()[:10],
    }
