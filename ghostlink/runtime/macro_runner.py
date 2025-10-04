# ghostlink/runtime/macro_runner.py
from __future__ import annotations
import yaml
from pathlib import Path
from typing import Any, Dict

from .context import Context
from .policy import Wraithgate
from .verify_and_restore import verify_manifest
from .ghostlink import RUNTIME_EXECUTION
from .template import render
from .snapshot import snapshot_vault

BASE = Path(__file__).resolve().parents[1]
VAULT = BASE / "vault"
MANIFEST = VAULT / "manifest.json"

def _load_macros() -> Dict[str, Any]:
    y = (VAULT / "macros.vault").read_text(encoding="utf-8")
    data = yaml.safe_load(y) or {}
    return data.get("macros", data) or {}

def run_macro(ctx: Context, macro_name: str, params: Dict[str, Any]) -> Any:
    verify_manifest(MANIFEST)
    macros = _load_macros()
    if macro_name not in macros:
        raise KeyError(f"macro not found: {macro_name}")

    spec = macros[macro_name]
    steps = spec.get("steps", [])
    required = (spec.get("params") or {}).get("required", [])
    missing = [p for p in required if p not in params]
    if missing:
        raise ValueError(f"macro missing params: {', '.join(missing)}")

    # snapshots
    snaps_dir = VAULT / "snapshots" / ctx.run_id
    before = snapshot_vault(VAULT, snaps_dir / "before")

    env = dict(params)
    prev: Any = None
    last_output: Any = None

    for step in steps:
        tool = step["tool"]
        raw_with = step.get("with", {})
        resolved = render(raw_with, env | {"prev": prev})
        Wraithgate.enforce(ctx, tool, resolved)
        out = RUNTIME_EXECUTION(tool, resolved, ctx)
        last_output = out
        prev = out
        env["prev"] = out

    after = snapshot_vault(VAULT, snaps_dir / "after")
    return {"macro": macro_name, "result": last_output, "_artifacts": [before, after]}

def expand_macro_steps(macro_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Preview resolved step parameters WITHOUT executing tools."""
    verify_manifest(MANIFEST)
    macros = _load_macros()
    if macro_name not in macros:
        raise KeyError(f"macro not found: {macro_name}")
    spec = macros[macro_name]
    steps = spec.get("steps", [])
    env = dict(params)
    prev: Any = None
    preview = []
    for idx, step in enumerate(steps, start=1):
        tool = step["tool"]
        raw_with = step.get("with", {})
        resolved = render(raw_with, env | {"prev": prev})
        preview.append({"index": idx, "tool": tool, "with": resolved})
        prev = f"<{tool}_output>"
        env["prev"] = prev
    return {"macro": macro_name, "expanded": preview}
