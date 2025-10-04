"""Factory for the RITUAL_FAIL_SAFE component."""
from __future__ import annotations

from ..factory import component_factory

RITUAL_FAIL_SAFE = component_factory(__name__, "RITUAL_FAIL_SAFE", "mesh")

__all__ = ["RITUAL_FAIL_SAFE"]
