# ghostlink/runtime/dag.py
from __future__ import annotations
from typing import List, Dict, Any

def ascii_dag(steps: List[Dict[str, Any]]) -> str:
    lines = []
    for i, st in enumerate(steps, 1):
        tool = st.get("tool", "?")
        lines.append(f"[{i}] {tool}")
        if i < len(steps):
            lines.append("  |\n  v")
    return "\n".join(lines)
