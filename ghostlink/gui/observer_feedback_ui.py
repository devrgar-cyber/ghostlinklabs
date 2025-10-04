"""Factory for the OBSERVER_FEEDBACK_UI component."""
from __future__ import annotations

from ..factory import component_factory

OBSERVER_FEEDBACK_UI = component_factory(__name__, "OBSERVER_FEEDBACK_UI", "gui")

__all__ = ["OBSERVER_FEEDBACK_UI"]
