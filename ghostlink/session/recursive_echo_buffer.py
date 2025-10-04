"""Factory for the RECURSIVE_ECHO_BUFFER component."""
from __future__ import annotations

from ..factory import component_factory

RECURSIVE_ECHO_BUFFER = component_factory(__name__, "RECURSIVE_ECHO_BUFFER", "session")

__all__ = ["RECURSIVE_ECHO_BUFFER"]
