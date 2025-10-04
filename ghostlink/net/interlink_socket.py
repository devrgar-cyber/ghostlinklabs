"""INTERLINK_SOCKET component module."""
from __future__ import annotations

from ..blueprint import component_factory


INTERLINK_SOCKET = component_factory("INTERLINK_SOCKET", "net", module=__name__)
