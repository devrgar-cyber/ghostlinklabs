"""RECOVERY_TREE component module."""
from __future__ import annotations

from ..blueprint import component_factory


RECOVERY_TREE = component_factory("RECOVERY_TREE", "session", module=__name__)
