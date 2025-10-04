"""FRACTAL_DEPTH_TRACKER component module."""
from __future__ import annotations

from ..blueprint import create_component


def FRACTAL_DEPTH_TRACKER() -> dict[str, object]:
    """Return the FRACTAL_DEPTH_TRACKER component description."""
    return create_component(
        "FRACTAL_DEPTH_TRACKER",
        "mesh",
    )
