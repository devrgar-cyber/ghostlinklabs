"""LOOP_DRIFT_COMPRESSOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def LOOP_DRIFT_COMPRESSOR() -> dict[str, object]:
    """Return the LOOP_DRIFT_COMPRESSOR component description."""
    return create_component(
        "LOOP_DRIFT_COMPRESSOR",
        "mesh",
    )
