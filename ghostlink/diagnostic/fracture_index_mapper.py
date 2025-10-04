"""FRACTURE_INDEX_MAPPER component module."""
from __future__ import annotations

from ..blueprint import create_component


def FRACTURE_INDEX_MAPPER() -> dict[str, object]:
    """Return the FRACTURE_INDEX_MAPPER component description."""
    return create_component(
        "FRACTURE_INDEX_MAPPER",
        "diagnostic",
    )
