"""Factory for the VAULT component."""
from __future__ import annotations

from ..factory import component_factory

VAULT = component_factory(__name__, "VAULT", "core")

__all__ = ["VAULT"]
