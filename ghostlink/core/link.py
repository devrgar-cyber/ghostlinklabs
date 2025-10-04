"""Bridge creation tooling for symbolic paths."""
from __future__ import annotations

from typing import Iterable, Tuple

from ._shared import ToolResponse, build_response


def LINK(path: Iterable[Tuple[str, str]] | None = None) -> ToolResponse:
    """Bridge two or more symbolic nodes."""
    context = {"bridges": list(path or [])}
    return build_response("LINK", context=context, status="connected")
