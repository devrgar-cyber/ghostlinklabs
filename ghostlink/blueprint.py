"""Utilities for defining and validating GhostLink conceptual components."""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any, TypedDict, cast

__all__ = [
    "ComponentDict",
    "ComponentFactory",
    "ComponentValidationError",
    "automatic_purpose",
    "component_factory",
    "create_component",
    "define_component",
    "validate_component_structure",
]


class ComponentDict(TypedDict):
    """Canonical dictionary layout for a GhostLink component."""

    name: str
    layer: str
    purpose: str
    inputs: list[str]
    outputs: list[str]
    metadata: dict[str, Any]


ComponentFactory = Callable[[], "ComponentDict"]


@dataclass(slots=True)
class ComponentValidationError(ValueError):
    """Raised when a component dictionary fails validation."""

    message: str
    field: str | None = None

    def __post_init__(self) -> None:
        super().__init__(self.message)

    def __str__(self) -> str:  # pragma: no cover - dataclass convenience
        if self.field is None:
            return self.message
        return f"{self.field}: {self.message}"


def _coerce_signal_list(values: Iterable[str] | None, *, field: str) -> list[str]:
    result: list[str] = []
    if values is None:
        return result
    if isinstance(values, str):
        raise ComponentValidationError(
            "Expected an iterable of strings, received a string",
            field=field,
        )
    for item in values:
        if not isinstance(item, str):
            raise ComponentValidationError(
                f"Expected {field} entries to be strings, received {type(item)!r}",
                field=field,
            )
        result.append(item)
    return result


def _coerce_metadata(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    result: dict[str, Any] = {}
    if metadata is None:
        return result
    if not isinstance(metadata, Mapping):
        raise ComponentValidationError(
            f"Metadata must be a mapping, received {type(metadata)!r}",
            field="metadata",
        )
    for key, value in metadata.items():
        if not isinstance(key, str):
            raise ComponentValidationError(
                f"Metadata keys must be strings, received {type(key)!r}",
                field="metadata",
            )
        result[key] = value
    return result


def define_component(
    name: str,
    layer: str,
    purpose: str,
    *,
    inputs: Iterable[str] | None = None,
    outputs: Iterable[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ComponentDict:
    """Create a component description dictionary with defensive copying."""

    return cast(
        ComponentDict,
        {
            "name": name,
            "layer": layer,
            "purpose": purpose,
            "inputs": _coerce_signal_list(inputs, field="inputs"),
            "outputs": _coerce_signal_list(outputs, field="outputs"),
            "metadata": _coerce_metadata(metadata),
        },
    )


def automatic_purpose(name: str, layer: str) -> str:
    """Generate a default purpose string for a component."""

    readable = name.replace("_", " ").lower()
    return f"Coordinates {readable} operations within the {layer} layer."


def create_component(
    name: str,
    layer: str,
    *,
    purpose: str | None = None,
    inputs: Iterable[str] | None = None,
    outputs: Iterable[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ComponentDict:
    """Return a fully populated component dictionary."""

    return define_component(
        name,
        layer,
        purpose if purpose is not None else automatic_purpose(name, layer),
        inputs=inputs,
        outputs=outputs,
        metadata=metadata,
    )


def component_factory(
    name: str,
    layer: str,
    *,
    purpose: str | None = None,
    inputs: Iterable[str] | None = None,
    outputs: Iterable[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
    module: str | None = None,
) -> ComponentFactory:
    """Return a lazily-evaluated component factory."""

    def factory() -> ComponentDict:
        return create_component(
            name,
            layer,
            purpose=purpose,
            inputs=inputs,
            outputs=outputs,
            metadata=metadata,
        )

    factory.__name__ = name
    factory.__qualname__ = name
    if module is not None:
        factory.__module__ = module
    factory.__doc__ = f"Return the {name} component description."
    return factory


def _require(component: Mapping[str, Any], key: str) -> Any:
    if key not in component:
        raise ComponentValidationError(f"Missing required field {key!r}", field=key)
    return component[key]


def validate_component_structure(
    component: Mapping[str, Any],
    *,
    expect_layer: str | None = None,
) -> ComponentDict:
    """Validate and normalize an arbitrary component mapping.

    Parameters
    ----------
    component:
        Input mapping containing the component definition.
    expect_layer:
        Optional expected layer name to enforce (used by the audit tooling
        to ensure module-local consistency).
    """

    if not isinstance(component, Mapping):
        raise ComponentValidationError(
            f"Component must be a mapping, received {type(component)!r}",
        )

    name = _require(component, "name")
    if not isinstance(name, str):
        raise ComponentValidationError("Component name must be a string", field="name")
    if name != name.upper():
        raise ComponentValidationError("Component name must be uppercase", field="name")

    layer = _require(component, "layer")
    if not isinstance(layer, str):
        raise ComponentValidationError("Component layer must be a string", field="layer")
    if expect_layer is not None and layer != expect_layer:
        raise ComponentValidationError(
            f"Component layer {layer!r} does not match expected {expect_layer!r}",
            field="layer",
        )

    purpose = _require(component, "purpose")
    if not isinstance(purpose, str):
        raise ComponentValidationError("Purpose must be a string", field="purpose")
    if not purpose:
        raise ComponentValidationError("Purpose must not be empty", field="purpose")

    inputs = component.get("inputs", [])
    outputs = component.get("outputs", [])
    metadata = component.get("metadata", {})
    if not isinstance(inputs, Iterable):
        raise ComponentValidationError(
            f"Inputs must be iterable, received {type(inputs)!r}",
            field="inputs",
        )
    if not isinstance(outputs, Iterable):
        raise ComponentValidationError(
            f"Outputs must be iterable, received {type(outputs)!r}",
            field="outputs",
        )
    if not isinstance(metadata, Mapping):
        raise ComponentValidationError(
            f"Metadata must be a mapping, received {type(metadata)!r}",
            field="metadata",
        )

    return define_component(
        name,
        layer,
        purpose,
        inputs=cast(Iterable[str], inputs),
        outputs=cast(Iterable[str], outputs),
        metadata=cast(Mapping[str, Any], metadata),
    )
