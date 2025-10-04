# ghostlink/boot/init.py
from pathlib import Path
from ..runtime.context import Context

def INIT_GHOSTLINK(base_dir: str | None = None) -> Context:
    base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[2]
    (base / "vault" / "logs").mkdir(parents=True, exist_ok=True)
    return Context.default()
