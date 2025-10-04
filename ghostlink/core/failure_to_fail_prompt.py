"""Tooling that probes the failure modality."""
from __future__ import annotations

from typing import Iterable

from ._shared import ToolResponse, build_response


def FAILURE_TO_FAIL_PROMPT(boundary: Iterable[str] | None = None) -> ToolResponse:
    """Guide probes into failure modalities."""
    steps = list(boundary or [])
    context = {"sequence": steps, "failure_ready": bool(steps)}
    return build_response("FAILURE_TO_FAIL_PROMPT", context=context, status="primed")
