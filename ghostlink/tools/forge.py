# ghostlink/tools/forge.py
from __future__ import annotations
from pathlib import Path
import json
from ..runtime.policy import SovereigntyGate
from ..runtime.context import Context
import yaml

def _allowed_ext(vault_path: str) -> set[str]:
    core = Path(vault_path) / "core.vault"
    if core.exists():
        cfg = yaml.safe_load(core.read_text()) or {}
        return set((cfg.get("constants") or {}).get("allowed_outputs", []))
    return {".txt", ".md", ".json"}

def main(ctx: Context, artifact: str, content: str = "", mode: str = "text"):
    """
    FORGE {artifact}: write a copy-pasteable structured block.
    mode: "text"|"json"
    """
    outdir = Path(ctx.vault_path).parent / "outputs"
    outdir.mkdir(parents=True, exist_ok=True)
    target = outdir / artifact
    if target.suffix not in _allowed_ext(ctx.vault_path):
        raise ValueError(f"forbidden extension: {target.suffix}")
    encoded = content
    if mode == "json":
        encoded = json.dumps(json.loads(content), indent=2, sort_keys=True)
    SovereigntyGate.require(ctx, "filesystem", path=str(target), bytes_out=len(encoded.encode("utf-8")))
    target.write_text(encoded, encoding="utf-8")
    return {"artifact": str(target), "bytes": target.stat().st_size}
