"""Factory for the LOOP_DRIFT_COMPRESSOR component."""
from __future__ import annotations

from ..factory import component_factory

LOOP_DRIFT_COMPRESSOR = component_factory(__name__, "LOOP_DRIFT_COMPRESSOR", "mesh")

__all__ = ["LOOP_DRIFT_COMPRESSOR"]
