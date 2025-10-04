# ghostlink/runtime/macro_linter.py
from __future__ import annotations
import importlib, inspect, yaml
from pathlib import Path
from typing import Any, Dict, List

from .template import referenced_keys
from .verify_and_restore import verify_manifest

BASE = Path(__file__).resolve().parents[1]
VAULT = BASE / "vault"
MANIFEST = VAULT / "manifest.json"

def _load_macros() -> Dict[str, Any]:
    y = (VAULT / "macros.vault").read_text(encoding="utf-8")
    data = yaml.safe_load(y) or {}
    return data.get("macros", data) or {}

def _tool_signature(tool: str) -> List[str]:
    """
    Return parameter names of ghostlink.tools.<tool>.main
    """
    mod = importlib.import_module(f"ghostlink.tools.{tool.lower()}")
    sig = inspect.signature(mod.main)
    params = list(sig.parameters.values())
    argnames = [p.name for p in params if p.name != "ctx" and p.kind in (
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        inspect.Parameter.KEYWORD_ONLY
    )]
    return argnames

def lint_macro(macro_name: str) -> Dict[str, Any]:
    verify_manifest(MANIFEST)
    macros = _load_macros()
    if macro_name not in macros:
        return {"macro": macro_name, "status": "fail", "errors": [f"macro not found: {macro_name}"]}

    spec = macros[macro_name]
    steps = spec.get("steps", [])
    required = (spec.get("params") or {}).get("required", [])
    report = {"macro": macro_name, "status": "ok", "errors": [], "warnings": [], "steps": []}

    if not isinstance(required, list):
        report["errors"].append("params.required must be a list")

    env = {k: f"<{k}>" for k in required}
    env["prev"] = "<prev>"
    prev = "<prev>"

    for idx, step in enumerate(steps, start=1):
        tool = step.get("tool")
        if not tool or not isinstance(tool, str):
            report["errors"].append(f"step {idx}: missing or invalid 'tool'")
            continue
        try:
            argnames = _tool_signature(tool)
        except Exception as e:
            report["errors"].append(f"step {idx} ({tool}): tool import/signature failed: {e}")
            continue

        raw_with = step.get("with", {})
        if raw_with is None: raw_with = {}
        if not isinstance(raw_with, (dict, list, str)):
            report["errors"].append(f"step {idx} ({tool}): 'with' must be dict/list/str")
            continue

        keys = referenced_keys(raw_with)
        unknown = [k for k in keys if k.split(".")[0] not in env]
        if unknown:
            report["warnings"].append(f"step {idx} ({tool}): unknown placeholders: {unknown}")

        present = set(raw_with.keys()) if isinstance(raw_with, dict) else set()
        missing_for_tool = [a for a in argnames if a not in present]
        if "data" in missing_for_tool and isinstance(raw_with, dict) and "data" not in raw_with:
            if any(k == "prev" or k.startswith("prev.") for k in keys):
                try:
                    missing_for_tool.remove("data")
                    report["warnings"].append(f"step {idx} ({tool}): 'data' param inferred from {{prev}}")
                except ValueError:
                    pass
        if missing_for_tool:
            report["warnings"].append(f"step {idx} ({tool}): params possibly missing: {missing_for_tool}")

        report["steps"].append({"index": idx, "tool": tool, "args": argnames})
        prev = f"<{tool}_output>"

    if report["errors"]:
        report["status"] = "fail"
    return report

def lint_all() -> Dict[str, Any]:
    verify_manifest(MANIFEST)
    macros = _load_macros()
    out = {"macros": {}, "status": "ok"}
    for name in macros:
        r = lint_macro(name)
        out["macros"][name] = r
        if r["status"] != "ok":
            out["status"] = "fail"
    return out
