"""RUNTIME_STATE_MANAGER component module."""
from __future__ import annotations

from ..blueprint import component_factory


RUNTIME_STATE_MANAGER = component_factory("RUNTIME_STATE_MANAGER", "runtime", module=__name__)
