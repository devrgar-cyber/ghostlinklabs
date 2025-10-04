"""Factory for the SYMBOLIC_FUZZ_TESTER component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_FUZZ_TESTER = component_factory(__name__, "SYMBOLIC_FUZZ_TESTER", "test")

__all__ = ["SYMBOLIC_FUZZ_TESTER"]
