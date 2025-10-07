"""Audit helpers for validating GhostLink component modules."""
from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
import importlib
import inspect
import pkgutil
from typing import Literal, Sequence

from .blueprint import (
    ComponentDict,
    ComponentValidationError,
    validate_component_structure,
)

__all__ = [
    "AuditIssue",
    "ComponentRecord",
    "iter_component_factories",
    "audit_components",
]


@dataclass(frozen=True, slots=True)
class AuditIssue:
    """Represents an issue discovered while auditing component factories."""

    module: str
    factory: str
    reason: str
    severity: Literal["error", "warning"] = "error"


@dataclass(frozen=True, slots=True)
class ComponentRecord:
    """Holds a validated component together with its origin."""

    module: str
    factory: str
    component: ComponentDict


def _callable_without_arguments(func: Callable[..., object]) -> bool:
    try:
        inspect.signature(func).bind_partial()
    except TypeError:
        return False
    return True


def iter_component_factories(
    root_package: str = "ghostlink",
    *,
    on_error: Callable[[str, Exception], None] | None = None,
) -> Iterator[tuple[str, str, Callable[[], ComponentDict]]]:
    """Yield candidate component factories located under ``root_package``."""

    package = importlib.import_module(root_package)
    if not hasattr(package, "__path__"):
        return iter(())

    prefix = f"{root_package}."
    for module_info in pkgutil.walk_packages(package.__path__, prefix):
        try:
            module = importlib.import_module(module_info.name)
        except Exception as exc:  # pragma: no cover - import side effects
            if on_error is not None:
                on_error(module_info.name, exc)
            continue
        for name, member in inspect.getmembers(module, inspect.isfunction):
            if not name.isupper():
                continue
            if member.__module__ != module.__name__:
                continue
            if not _callable_without_arguments(member):
                continue
            yield module_info.name, name, member  # type: ignore[misc]


def _expected_layer(module_name: str) -> str | None:
    parts = module_name.split(".")
    if len(parts) < 3:
        return None
    return parts[1]


def _classify_import_error(
    root_package: str, module_name: str, exc: Exception
) -> tuple[Literal["error", "warning"], str]:
    """Return a severity/reason pair for a module import failure."""

    if isinstance(exc, ModuleNotFoundError):
        missing = getattr(exc, "name", None)
        if missing:
            root_prefix = root_package.split(".", 1)[0]
            if not missing.startswith(root_prefix):
                return "warning", f"optional dependency missing: {missing}"
    return "error", f"import failed: {exc.__class__.__name__}: {exc}"


def audit_components(root_package: str = "ghostlink") -> tuple[Sequence[ComponentRecord], Sequence[AuditIssue]]:
    """Audit component factories and return validated components with issues."""

    records: list[ComponentRecord] = []
    issues: list[AuditIssue] = []
    seen: dict[tuple[str, str], str] = {}

    def _record_import_error(module_name: str, exc: Exception) -> None:
        severity, reason = _classify_import_error(root_package, module_name, exc)
        issues.append(AuditIssue(module_name, "<module>", reason, severity))

    for module_name, factory_name, factory in iter_component_factories(root_package, on_error=_record_import_error):
        expected_layer = _expected_layer(module_name)
        try:
            component_data = factory()
        except Exception as exc:  # pragma: no cover - defensive for runtime errors
            issues.append(
                AuditIssue(
                    module_name,
                    factory_name,
                    f"factory raised {exc.__class__.__name__}: {exc}",
                )
            )
            continue

        try:
            component = validate_component_structure(component_data, expect_layer=expected_layer)
        except ComponentValidationError as err:
            issues.append(AuditIssue(module_name, factory_name, str(err)))
            continue

        key = (component["layer"], component["name"])
        if key in seen:
            issues.append(
                AuditIssue(
                    module_name,
                    factory_name,
                    f"Duplicate component definition (original in {seen[key]})",
                )
            )
            continue
        seen[key] = module_name
        records.append(ComponentRecord(module_name, factory_name, component))

    return records, issues
