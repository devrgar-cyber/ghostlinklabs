"""SYMBOLIC_FUZZ_TESTER component module."""
from __future__ import annotations

from ..blueprint import component_factory


SYMBOLIC_FUZZ_TESTER = component_factory("SYMBOLIC_FUZZ_TESTER", "test", module=__name__)
