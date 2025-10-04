"""Factory for the VAULT_LOADER component."""
from __future__ import annotations

from ..factory import component_factory

VAULT_LOADER = component_factory(__name__, "VAULT_LOADER", "boot")

__all__ = ["VAULT_LOADER"]
