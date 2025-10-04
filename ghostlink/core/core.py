"""Core nucleus tooling."""
from __future__ import annotations

from typing import Dict

from ._shared import ToolResponse, build_response


def CORE(identity: Dict[str, str] | None = None) -> ToolResponse:
    """Return the symbolic nucleus for the lattice."""
    return build_response("CORE", context=identity or {"axis": "central"}, status="aligned")
