"""Factory for the SYMBOLIC_SANDBOX component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_SANDBOX = component_factory(__name__, "SYMBOLIC_SANDBOX", "sandbox")

__all__ = ["SYMBOLIC_SANDBOX"]
