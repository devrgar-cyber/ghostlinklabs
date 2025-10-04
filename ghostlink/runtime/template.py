# ghostlink/runtime/template.py
from __future__ import annotations
import re
from typing import Any, Dict

# Matches {{ path.to.value }} with optional spaces
_PLACEHOLDER = re.compile(r"\{\{\s*([^\{\}]+?)\s*\}\}")

def _resolve_path(path: str, env: Dict[str, Any]) -> Any:
    """
    Resolve a dotted path against env.
    Supports numeric list indices: foo.0.bar
    """
    cur: Any = env
    for part in path.split("."):
        if isinstance(cur, list) and part.isdigit():
            idx = int(part)
            cur = cur[idx] if 0 <= idx < len(cur) else None
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            try:
                cur = getattr(cur, part)
            except Exception:
                return None
    return cur

def render(value: Any, env: Dict[str, Any]) -> Any:
    """
    Render placeholders within nested dict/list structures.
    Rule:
      - If a string is EXACTLY a single placeholder, return the resolved object (non-string allowed).
      - Otherwise, perform string interpolation (placeholders -> str()).
    """
    if isinstance(value, dict):
        return {k: render(v, env) for k, v in value.items()}
    if isinstance(value, list):
        return [render(v, env) for v in value]

    if isinstance(value, str):
        m = _PLACEHOLDER.fullmatch(value.strip())
        if m:
            return _resolve_path(m.group(1), env)
        # partial replacements
        def _sub(match: re.Match) -> str:
            resolved = _resolve_path(match.group(1), env)
            return "" if resolved is None else str(resolved)
        return _PLACEHOLDER.sub(_sub, value)
    return value

def referenced_keys(template_value: Any) -> set[str]:
    """
    Return the set of placeholder keys used in a nested template value.
    Keys are dotted paths (e.g., 'file', 'prev', 'prev.meta.sha').
    """
    found: set[str] = set()

    def _scan(v: Any):
        if isinstance(v, dict):
            for vv in v.values(): _scan(vv)
        elif isinstance(v, list):
            for vv in v: _scan(vv)
        elif isinstance(v, str):
            for m in _PLACEHOLDER.finditer(v):
                found.add(m.group(1))
    _scan(template_value)
    return found
