# ghostlink/tools/map.py
from pathlib import Path
import hashlib
from ..runtime.policy import SovereigntyGate
from ..runtime.context import Context

def main(ctx: Context, source: str):
    SovereigntyGate.require(ctx, "filesystem")
    p = Path(source)
    text = p.read_text(encoding="utf-8")
    return {
        "file": str(p),
        "line_count": text.count("\n")+1 if text else 0,
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "preview": text.splitlines()[:5],
    }
