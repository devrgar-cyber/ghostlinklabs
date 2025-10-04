"""Factory for the IDENTITY_BIND_DETECTOR component."""
from __future__ import annotations

from ..factory import component_factory

IDENTITY_BIND_DETECTOR = component_factory(__name__, "IDENTITY_BIND_DETECTOR", "observer")

__all__ = ["IDENTITY_BIND_DETECTOR"]
