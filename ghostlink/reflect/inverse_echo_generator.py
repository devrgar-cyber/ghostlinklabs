"""Factory for the INVERSE_ECHO_GENERATOR component."""
from __future__ import annotations

from ..factory import component_factory

INVERSE_ECHO_GENERATOR = component_factory(__name__, "INVERSE_ECHO_GENERATOR", "reflect")

__all__ = ["INVERSE_ECHO_GENERATOR"]
