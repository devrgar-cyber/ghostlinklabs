"""Factory for the ECHO_BURN_RATE component."""
from __future__ import annotations

from ..factory import component_factory

ECHO_BURN_RATE = component_factory(__name__, "ECHO_BURN_RATE", "valuation")

__all__ = ["ECHO_BURN_RATE"]
