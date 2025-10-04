"""Vault loader utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def VAULT_LOADER(vault_path: str | Path, *, create: bool = False) -> ToolResponse:
    """Load or create a vault file for GhostLink sessions."""
    path = Path(vault_path)
    if create:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
    context: Dict[str, object] = {
        "path": str(path),
        "exists": path.exists(),
        "size": path.stat().st_size if path.exists() else 0,
    }
    status = "loaded" if context["exists"] else "missing"
    return build_response("VAULT_LOADER", context=context, status=status)
