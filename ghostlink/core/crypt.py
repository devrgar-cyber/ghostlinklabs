"""CRYPT component module."""
from __future__ import annotations

from ..blueprint import component_factory


CRYPT = component_factory("CRYPT", "core", module=__name__)
