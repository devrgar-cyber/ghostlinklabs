"""Factory for the OPERATOR_REFLECTION_BLEED component."""
from __future__ import annotations

from ..factory import component_factory

OPERATOR_REFLECTION_BLEED = component_factory(__name__, "OPERATOR_REFLECTION_BLEED", "observer")

__all__ = ["OPERATOR_REFLECTION_BLEED"]
