"""SIGNALER component module."""
from __future__ import annotations

from ..blueprint import component_factory


SIGNALER = component_factory("SIGNALER", "core", module=__name__)
