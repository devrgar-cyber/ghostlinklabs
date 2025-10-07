from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

KERNEL_PATH = Path(__file__).resolve().parents[2] / "kernel" / "gl-kernel.max.json"


NEWLINE = chr(10)

@lru_cache(maxsize=1)
def _kernel_payload() -> Dict[str, Any]:
    with KERNEL_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_tools() -> List[str]:
    '''Return the ordered list of tool primitives registered by the kernel.'''
    return list(_kernel_payload()["tools"])


def describe_tool(name: str) -> Dict[str, Any]:
    '''Return metadata for the requested tool.'''
    kernel = _kernel_payload()
    pipelines = {pipe["name"]: pipe for pipe in kernel["pipelines"]}
    info = pipelines.get(name)
    if info is None:
        return {
            "name": name,
            "action": None,
            "multipaths": [],
        }
    return {
        "name": name,
        "action": info["action"],
        "multipaths": list(info["multipaths"]),
    }


def tool_manifest() -> Dict[str, Dict[str, Any]]:
    '''Return the tool manifest keyed by tool name.'''
    return {tool: describe_tool(tool) for tool in list_tools()}


__all__ = ["list_tools", "describe_tool", "tool_manifest"]
