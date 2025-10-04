"""SCHEMA_INTEGRITY_TEST component module."""
from __future__ import annotations

from ..blueprint import component_factory


SCHEMA_INTEGRITY_TEST = component_factory("SCHEMA_INTEGRITY_TEST", "test", module=__name__)
