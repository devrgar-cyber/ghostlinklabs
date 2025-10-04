"""BIOLOGICAL_TRACE_INTEGRATOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def BIOLOGICAL_TRACE_INTEGRATOR() -> dict[str, object]:
    """Return the BIOLOGICAL_TRACE_INTEGRATOR component description."""
    return create_component(
        "BIOLOGICAL_TRACE_INTEGRATOR",
        "bio",
    )
