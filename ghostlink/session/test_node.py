"""TEST_NODE component module."""
from __future__ import annotations

from ..blueprint import component_factory


TEST_NODE = component_factory("TEST_NODE", "session", module=__name__)
