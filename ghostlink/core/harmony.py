"""Factory for the HARMONY component."""
from __future__ import annotations

from ..factory import component_factory

HARMONY = component_factory(__name__, "HARMONY", "core")

__all__ = ["HARMONY"]
