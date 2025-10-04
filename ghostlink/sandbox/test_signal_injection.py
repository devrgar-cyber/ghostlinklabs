"""Factory for the TEST_SIGNAL_INJECTION component."""
from __future__ import annotations

from ..factory import component_factory

TEST_SIGNAL_INJECTION = component_factory(__name__, "TEST_SIGNAL_INJECTION", "sandbox")

__all__ = ["TEST_SIGNAL_INJECTION"]
