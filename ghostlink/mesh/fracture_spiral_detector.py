"""FRACTURE_SPIRAL_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def FRACTURE_SPIRAL_DETECTOR() -> dict[str, object]:
    """Return the FRACTURE_SPIRAL_DETECTOR component description."""
    return create_component(
        "FRACTURE_SPIRAL_DETECTOR",
        "mesh",
    )
