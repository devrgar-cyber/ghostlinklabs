"""Factory for the FEEDBACK_LOOP_RECEPTOR component."""
from __future__ import annotations

from ..factory import component_factory

FEEDBACK_LOOP_RECEPTOR = component_factory(__name__, "FEEDBACK_LOOP_RECEPTOR", "bio")

__all__ = ["FEEDBACK_LOOP_RECEPTOR"]
