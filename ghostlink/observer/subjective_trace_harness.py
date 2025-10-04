"""SUBJECTIVE_TRACE_HARNESS component module."""
from __future__ import annotations

from ..blueprint import create_component


def SUBJECTIVE_TRACE_HARNESS() -> dict[str, object]:
    """Return the SUBJECTIVE_TRACE_HARNESS component description."""
    return create_component(
        "SUBJECTIVE_TRACE_HARNESS",
        "observer",
    )
