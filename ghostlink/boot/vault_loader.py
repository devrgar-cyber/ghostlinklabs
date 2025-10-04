"""LOAD_VAULT component module."""
from __future__ import annotations

from ..blueprint import component_factory


LOAD_VAULT = component_factory("LOAD_VAULT", "boot", module=__name__)
