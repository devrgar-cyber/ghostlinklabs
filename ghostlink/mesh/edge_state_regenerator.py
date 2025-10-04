"""Factory for the EDGE_STATE_REGENERATOR component."""
from __future__ import annotations

from ..factory import component_factory

EDGE_STATE_REGENERATOR = component_factory(__name__, "EDGE_STATE_REGENERATOR", "mesh")

__all__ = ["EDGE_STATE_REGENERATOR"]
