"""ARCHIVE component module."""
from __future__ import annotations

from ..blueprint import component_factory


ARCHIVE = component_factory("ARCHIVE", "core", module=__name__)
