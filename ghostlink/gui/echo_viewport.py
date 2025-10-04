"""Factory for the ECHO_VIEWPORT component."""
from __future__ import annotations

from ..factory import component_factory

ECHO_VIEWPORT = component_factory(__name__, "ECHO_VIEWPORT", "gui")

__all__ = ["ECHO_VIEWPORT"]
