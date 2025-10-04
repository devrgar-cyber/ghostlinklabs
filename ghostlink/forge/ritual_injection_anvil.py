"""RITUAL_INJECTION_ANVIL component module."""
from __future__ import annotations

from ..blueprint import create_component


def RITUAL_INJECTION_ANVIL() -> dict[str, object]:
    """Return the RITUAL_INJECTION_ANVIL component description."""
    return create_component(
        "RITUAL_INJECTION_ANVIL",
        "forge",
    )
