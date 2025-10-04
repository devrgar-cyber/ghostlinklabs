"""Reflection and identity decoding utilities."""
from __future__ import annotations

from typing import Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def REFLECTIVE_MIRROR(matrix: Dict[str, str] | None = None) -> ToolResponse:
    """Decode identity echoes into a normalized reflection."""
    context = {"matrix": matrix or {}, "coherence": bool(matrix)}
    return build_response("REFLECTIVE_MIRROR", context=context, status="stabilized")
