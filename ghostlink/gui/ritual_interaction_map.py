"""Factory for the RITUAL_INTERACTION_MAP component."""
from __future__ import annotations

from ..factory import component_factory

RITUAL_INTERACTION_MAP = component_factory(__name__, "RITUAL_INTERACTION_MAP", "gui")

__all__ = ["RITUAL_INTERACTION_MAP"]
