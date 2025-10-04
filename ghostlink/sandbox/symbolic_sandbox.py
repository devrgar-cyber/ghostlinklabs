"""SYMBOLIC_SANDBOX component module."""
from __future__ import annotations

from ..blueprint import component_factory


SYMBOLIC_SANDBOX = component_factory("SYMBOLIC_SANDBOX", "sandbox", module=__name__)
