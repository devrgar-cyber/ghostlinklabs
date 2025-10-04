"""Detect unreachable symbolic paths."""
from __future__ import annotations

from typing import Iterable

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def BROKEN_LINK_DETECTOR(paths: Iterable[str] | None = None) -> ToolResponse:
    """Identify missing or broken links in the lattice."""
    entries = list(paths or [])
    broken = [path for path in entries if not path]
    context = {"paths": entries, "broken": broken}
    status = "clean" if not broken else "fractured"
    return build_response("BROKEN_LINK_DETECTOR", context=context, status=status)
