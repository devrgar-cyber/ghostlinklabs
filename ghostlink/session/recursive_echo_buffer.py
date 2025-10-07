"""RECURSIVE_ECHO_BUFFER component module."""
from __future__ import annotations

from ..blueprint import component_factory


RECURSIVE_ECHO_BUFFER = component_factory("RECURSIVE_ECHO_BUFFER", "session", module=__name__)
