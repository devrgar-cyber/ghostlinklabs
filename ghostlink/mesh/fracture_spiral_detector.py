"""Factory for the FRACTURE_SPIRAL_DETECTOR component."""
from __future__ import annotations

from ..factory import component_factory

FRACTURE_SPIRAL_DETECTOR = component_factory(__name__, "FRACTURE_SPIRAL_DETECTOR", "mesh")

__all__ = ["FRACTURE_SPIRAL_DETECTOR"]
