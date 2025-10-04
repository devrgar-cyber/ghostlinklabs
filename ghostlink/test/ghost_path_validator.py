"""Factory for the GHOST_PATH_VALIDATOR component."""
from __future__ import annotations

from ..factory import component_factory

GHOST_PATH_VALIDATOR = component_factory(__name__, "GHOST_PATH_VALIDATOR", "test")

__all__ = ["GHOST_PATH_VALIDATOR"]
