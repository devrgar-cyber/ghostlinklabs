"""Factory for the TEST_NODE component."""
from __future__ import annotations

from ..factory import component_factory

TEST_NODE = component_factory(__name__, "TEST_NODE", "session")

__all__ = ["TEST_NODE"]
