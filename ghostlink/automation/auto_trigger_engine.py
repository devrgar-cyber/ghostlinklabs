"""Factory for the AUTO_TRIGGER_ENGINE component."""
from __future__ import annotations

from ..factory import component_factory

AUTO_TRIGGER_ENGINE = component_factory(__name__, "AUTO_TRIGGER_ENGINE", "automation")

__all__ = ["AUTO_TRIGGER_ENGINE"]
