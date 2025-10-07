"""SYMBOLIC_TASK_SCHEDULER component module."""
from __future__ import annotations

from ..blueprint import component_factory


SYMBOLIC_TASK_SCHEDULER = component_factory("SYMBOLIC_TASK_SCHEDULER", "automation", module=__name__)
