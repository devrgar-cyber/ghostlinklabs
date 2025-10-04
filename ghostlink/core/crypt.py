"""Factory for the CRYPT component."""
from __future__ import annotations

from ..factory import component_factory

CRYPT = component_factory(__name__, "CRYPT", "core")

__all__ = ["CRYPT"]
