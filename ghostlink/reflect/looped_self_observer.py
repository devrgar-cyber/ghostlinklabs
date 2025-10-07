"""LOOPED_SELF_OBSERVER component module."""
from __future__ import annotations

from ..blueprint import component_factory


LOOPED_SELF_OBSERVER = component_factory("LOOPED_SELF_OBSERVER", "reflect", module=__name__)
