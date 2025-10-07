"""FAILURE_TO_FAIL_PROMPT component module."""
from __future__ import annotations

from ..blueprint import component_factory


FAILURE_TO_FAIL_PROMPT = component_factory("FAILURE_TO_FAIL_PROMPT", "meta", module=__name__)
