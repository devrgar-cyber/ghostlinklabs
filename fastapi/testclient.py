"""Minimal TestClient compatible with the stub FastAPI."""
from __future__ import annotations

import inspect
from typing import Any, Dict, Tuple

from pydantic import BaseModel

from . import FastAPI, HTTPException


class Response:
    def __init__(self, status_code: int, data: Any):
        self.status_code = status_code
        self._data = data

    def json(self) -> Any:
        return self._data


class TestClient:
    def __init__(self, app: FastAPI):
        self.app = app

    def _resolve(self, method: str, path: str) -> Tuple[Any, Dict[str, str]]:
        for route in self.app.routes:
            if route.method != method:
                continue
            pattern_parts = route.path.strip("/").split("/")
            path_parts = path.strip("/").split("/")
            if len(pattern_parts) != len(path_parts):
                continue
            kwargs: Dict[str, str] = {}
            match = True
            for pattern, part in zip(pattern_parts, path_parts):
                if pattern.startswith("{") and pattern.endswith("}"):
                    key = pattern[1:-1]
                    kwargs[key] = part
                elif pattern != part:
                    match = False
                    break
            if match:
                return route.func, kwargs
        raise KeyError(f"Route {method} {path} not found")

    def post(self, path: str, json: Dict[str, Any] | None = None) -> Response:
        func, _ = self._resolve("POST", path)
        try:
            if json is None:
                result = func()
            else:
                sig = inspect.signature(func)
                param = next(iter(sig.parameters.values()))
                model_cls = param.annotation
                if inspect.isclass(model_cls) and issubclass(model_cls, BaseModel):
                    obj = model_cls(**json)
                else:
                    obj = json
                result = func(obj)
            return Response(200, result)
        except HTTPException as exc:
            return Response(exc.status_code, {"detail": exc.detail})

    def get(self, path: str) -> Response:
        func, kwargs = self._resolve("GET", path)
        try:
            result = func(**kwargs)
            return Response(200, result)
        except HTTPException as exc:
            return Response(exc.status_code, {"detail": exc.detail})
