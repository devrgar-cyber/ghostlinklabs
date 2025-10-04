"""Lightweight subset of Pydantic used for the exercises."""
from __future__ import annotations

from typing import Any, Dict, Type


class ValidationError(ValueError):
    pass


class BaseModel:
    """Minimal stand-in for :class:`pydantic.BaseModel`."""

    def __init__(self, **data: Any) -> None:
        annotations = getattr(self.__class__, "__annotations__", {})
        values: Dict[str, Any] = {}

        for name, annotation in annotations.items():
            if name in data:
                values[name] = data[name]
            elif hasattr(self.__class__, name):
                values[name] = getattr(self.__class__, name)
            else:
                raise ValidationError(f"Missing field: {name}")

        for name, value in values.items():
            setattr(self, name, value)

    def model_dump(self) -> Dict[str, Any]:
        annotations = getattr(self.__class__, "__annotations__", {})
        return {name: getattr(self, name) for name in annotations}

    @classmethod
    def model_validate(cls: Type["BaseModel"], data: Dict[str, Any]) -> "BaseModel":
        return cls(**data)

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        fields = ", ".join(f"{key}={value!r}" for key, value in self.model_dump().items())
        return f"{self.__class__.__name__}({fields})"
