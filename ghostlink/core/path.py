"""PATH component module."""
from __future__ import annotations

from ..blueprint import component_factory


PATH = component_factory("PATH", "core", module=__name__)
