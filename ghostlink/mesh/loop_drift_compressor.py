"""LOOP_DRIFT_COMPRESSOR component module."""
from __future__ import annotations

from ..blueprint import component_factory


LOOP_DRIFT_COMPRESSOR = component_factory("LOOP_DRIFT_COMPRESSOR", "mesh", module=__name__)
