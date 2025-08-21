"""Minimal stub implementation of the FastAPI interface used in tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


@dataclass
class Route:
    method: str
    path: str
    func: Callable


class FastAPI:
    def __init__(self, title: str | None = None):
        self.title = title
        self.routes: List[Route] = []

    def post(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes.append(Route("POST", path, func))
            return func
        return decorator

    def get(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes.append(Route("GET", path, func))
            return func
        return decorator
