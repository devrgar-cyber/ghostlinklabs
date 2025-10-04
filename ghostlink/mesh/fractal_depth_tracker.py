"""Factory for the FRACTAL_DEPTH_TRACKER component."""
from __future__ import annotations

from ..factory import component_factory

FRACTAL_DEPTH_TRACKER = component_factory(__name__, "FRACTAL_DEPTH_TRACKER", "mesh")

__all__ = ["FRACTAL_DEPTH_TRACKER"]
