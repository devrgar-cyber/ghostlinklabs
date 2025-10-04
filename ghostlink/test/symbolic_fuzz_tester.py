"""SYMBOLIC_FUZZ_TESTER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_FUZZ_TESTER() -> dict[str, object]:
    """Return the SYMBOLIC_FUZZ_TESTER component description."""
    return create_component(
        "SYMBOLIC_FUZZ_TESTER",
        "test",
    )
