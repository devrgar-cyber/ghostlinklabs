"""IMPLICIT_UNLOCK component module."""
from __future__ import annotations

from ..blueprint import component_factory


IMPLICIT_UNLOCK = component_factory("IMPLICIT_UNLOCK", "access", module=__name__)
