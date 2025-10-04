"""DISSOLUTION_THRESHOLD_PROBE component module."""
from __future__ import annotations

from ..blueprint import component_factory


DISSOLUTION_THRESHOLD_PROBE = component_factory("DISSOLUTION_THRESHOLD_PROBE", "observer", module=__name__)
