"""Minimal FastAPI-compatible stubs for the kata environment.

The real project depends on ``fastapi`` which is not available in the
execution environment.  The tests require only a tiny portion of the
framework, so we provide a purposely small subset that mimics the public
interfaces used by the application.
"""
from __future__ import annotations

import inspect
from dataclasses import asdict, dataclass, is_dataclass
from types import SimpleNamespace
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type

from .testclient import Response

__all__ = [
    "Depends",
    "FastAPI",
    "HTTPException",
    "Request",
]


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: Any) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class Headers(dict):
    def __init__(self, initial: Optional[Dict[str, str]] = None) -> None:
        super().__init__()
        if initial:
            for key, value in initial.items():
                self[key] = value

    def __setitem__(self, key: str, value: str) -> None:  # type: ignore[override]
        super().__setitem__(key.lower(), value)

    def get(self, key: str, default: Any = None) -> Any:  # type: ignore[override]
        return super().get(key.lower(), default)


class Request:
    def __init__(self, method: str, url: str, headers: Optional[Dict[str, str]] = None, json_data: Any = None) -> None:
        self.method = method
        self.url = url
        self.headers = Headers(headers or {})
        self._json = json_data
        self.state = SimpleNamespace()
        self.path_params: Dict[str, str] = {}

    def json(self) -> Any:
        return self._json


class Depends:
    def __init__(self, dependency: Callable[..., Any]) -> None:
        self.dependency = dependency

    def resolve(self, app: "FastAPI", request: Request) -> Any:
        signature = inspect.signature(self.dependency)
        kwargs = {}
        for name, parameter in signature.parameters.items():
            if parameter.annotation is Request or parameter.annotation == Request:
                kwargs[name] = request
        return self.dependency(**kwargs)


@dataclass
class _Route:
    path: str
    methods: Tuple[str, ...]
    endpoint: Callable[..., Any]
    response_model: Optional[Type[Any]] = None

    def match(self, method: str, path: str) -> Optional[Dict[str, str]]:
        if method not in self.methods:
            return None
        template_parts = [part for part in self.path.strip("/").split("/") if part]
        path_parts = [part for part in path.strip("/").split("/") if part]
        if len(template_parts) != len(path_parts):
            return None
        params: Dict[str, str] = {}
        for template, actual in zip(template_parts, path_parts):
            if template.startswith("{") and template.endswith("}"):
                params[template[1:-1]] = actual
            elif template != actual:
                return None
        return params


class FastAPI:
    def __init__(self, *, title: str | None = None) -> None:
        self.title = title or "FastAPI"
        self.routes: List[_Route] = []

    # Decorators ---------------------------------------------------------
    def _register(self, path: str, methods: Iterable[str], response_model: Optional[Type[Any]], endpoint: Callable[..., Any]) -> Callable[..., Any]:
        route = _Route(path=path, methods=tuple(methods), endpoint=endpoint, response_model=response_model)
        self.routes.append(route)
        return endpoint

    def get(self, path: str, *, response_model: Optional[Type[Any]] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            return self._register(path, ("GET",), response_model, func)

        return decorator

    def post(self, path: str, *, response_model: Optional[Type[Any]] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            return self._register(path, ("POST",), response_model, func)

        return decorator

    # Request handling ---------------------------------------------------
    def _find_route(self, method: str, path: str) -> Tuple[_Route, Dict[str, str]]:
        for route in self.routes:
            params = route.match(method, path)
            if params is not None:
                return route, params
        raise HTTPException(status_code=404, detail="Not Found")

    def _call_endpoint(
        self,
        route: _Route,
        request: Request,
        body: Any,
    ) -> Any:
        signature = inspect.signature(route.endpoint)
        kwargs: Dict[str, Any] = {}
        body_data = body

        for name, parameter in signature.parameters.items():
            if name in request.path_params:
                value = request.path_params[name]
                if parameter.annotation is not inspect._empty and parameter.annotation not in (str, Any):
                    try:
                        value = parameter.annotation(value)
                    except Exception:
                        raise HTTPException(status_code=422, detail=f"Invalid value for {name}")
                kwargs[name] = value
                continue

            if parameter.annotation is Request or parameter.annotation == Request:
                kwargs[name] = request
                continue

            if isinstance(parameter.default, Depends):
                kwargs[name] = parameter.default.resolve(self, request)
                continue

            if body_data is not None and parameter.default is inspect._empty and name not in kwargs:
                annotation = parameter.annotation
                if isinstance(annotation, type) and _is_base_model(annotation):
                    kwargs[name] = annotation(**body_data)
                else:
                    kwargs[name] = body_data
                body_data = None
                continue

            if parameter.default is not inspect._empty:
                kwargs[name] = parameter.default

        return route.endpoint(**kwargs)

    def handle_request(self, method: str, path: str, *, json_body: Any = None, headers: Optional[Dict[str, str]] = None) -> Response:
        try:
            route, params = self._find_route(method, path)
            request = Request(method, path, headers=headers, json_data=json_body)
            request.path_params = params
            result = self._call_endpoint(route, request, json_body)
            data = _jsonable(result)
            return Response(status_code=200, data=data)
        except HTTPException as exc:
            return Response(status_code=exc.status_code, data={"detail": exc.detail})


def _is_base_model(cls: Type[Any]) -> bool:
    from pydantic import BaseModel  # local import to avoid circular dependency

    try:
        return issubclass(cls, BaseModel)
    except TypeError:
        return False


def _jsonable(value: Any) -> Any:
    from pydantic import BaseModel

    if isinstance(value, Response):
        return value.json()
    if isinstance(value, BaseModel):
        return _jsonable(value.model_dump())
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {key: _jsonable(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass
    return value
