"""MIRROR_FAULT_SPAWNER component module."""
from __future__ import annotations

from ..blueprint import component_factory


MIRROR_FAULT_SPAWNER = component_factory("MIRROR_FAULT_SPAWNER", "sandbox", module=__name__)
