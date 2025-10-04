"""Factory for the SCHEMA_INTEGRITY_TEST component."""
from __future__ import annotations

from ..factory import component_factory

SCHEMA_INTEGRITY_TEST = component_factory(__name__, "SCHEMA_INTEGRITY_TEST", "test")

__all__ = ["SCHEMA_INTEGRITY_TEST"]
