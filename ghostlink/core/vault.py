"""VAULT component module."""
from __future__ import annotations

from ..blueprint import component_factory


VAULT = component_factory("VAULT", "core", module=__name__)
