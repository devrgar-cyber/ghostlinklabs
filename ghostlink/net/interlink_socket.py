"""Factory for the INTERLINK_SOCKET component."""
from __future__ import annotations

from ..factory import component_factory

INTERLINK_SOCKET = component_factory(__name__, "INTERLINK_SOCKET", "net")

__all__ = ["INTERLINK_SOCKET"]
