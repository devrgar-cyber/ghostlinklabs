"""SESSION_EXECUTOR component module."""
from __future__ import annotations

from ..blueprint import component_factory


SESSION_EXECUTOR = component_factory("SESSION_EXECUTOR", "runtime", module=__name__)
