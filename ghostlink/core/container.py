"""Factory for the CONTAINER component."""
from __future__ import annotations

from ..factory import component_factory

CONTAINER = component_factory(__name__, "CONTAINER", "core")

__all__ = ["CONTAINER"]
