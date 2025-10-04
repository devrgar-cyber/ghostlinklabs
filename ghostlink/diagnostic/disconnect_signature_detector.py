"""Factory for the DISCONNECT_SIGNATURE_DETECTOR component."""
from __future__ import annotations

from ..factory import component_factory

DISCONNECT_SIGNATURE_DETECTOR = component_factory(__name__, "DISCONNECT_SIGNATURE_DETECTOR", "diagnostic")

__all__ = ["DISCONNECT_SIGNATURE_DETECTOR"]
