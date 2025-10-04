"""Factory for the SIGNAL_CASCADE_CHECK component."""
from __future__ import annotations

from ..factory import component_factory

SIGNAL_CASCADE_CHECK = component_factory(__name__, "SIGNAL_CASCADE_CHECK", "diagnostic")

__all__ = ["SIGNAL_CASCADE_CHECK"]
