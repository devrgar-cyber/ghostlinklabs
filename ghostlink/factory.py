"""Utilities for constructing lightweight component factory callables."""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any

from .blueprint import ComponentDict, create_component

ComponentFactory = Callable[[], ComponentDict]

__all__ = ["ComponentFactory", "component_factory"]


def _copy_optional_iterable(value: Iterable[str] | None) -> list[str] | None:
    if value is None:
        return None
    return list(value)


def _copy_optional_mapping(value: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if value is None:
        return None
    return dict(value)


def component_factory(
    module_name: str,
    name: str,
    layer: str,
    *,
    purpose: str | None = None,
    inputs: Iterable[str] | None = None,
    outputs: Iterable[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ComponentFactory:
    """Return a component factory bound to ``module_name``."""

    copied_inputs = _copy_optional_iterable(inputs)
    copied_outputs = _copy_optional_iterable(outputs)
    copied_metadata = _copy_optional_mapping(metadata)

    def _factory() -> ComponentDict:
        return create_component(
            name,
            layer,
            purpose=purpose,
            inputs=copied_inputs,
            outputs=copied_outputs,
            metadata=copied_metadata,
        )

    _factory.__name__ = name
    _factory.__qualname__ = name
    _factory.__module__ = module_name
    _factory.__doc__ = f"Return the {name} component description."

    return _factory
