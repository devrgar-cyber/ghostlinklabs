"""SYMBOLIC_LOSS_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import component_factory


SYMBOLIC_LOSS_DETECTOR = component_factory("SYMBOLIC_LOSS_DETECTOR", "reflect", module=__name__)
