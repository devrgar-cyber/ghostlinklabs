"""Very small TestClient compatible with the real FastAPI API used in tests."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional


class Response:
    def __init__(self, status_code: int, data: Any) -> None:
        self.status_code = status_code
        self._data = data

    def json(self) -> Any:
        return self._data

    @property
    def text(self) -> str:
        return json.dumps(self._data)


class TestClient:
    def __init__(self, app) -> None:
        self.app = app

    def post(self, path: str, *, json: Optional[Any] = None, headers: Optional[Dict[str, str]] = None) -> Response:
        return self.app.handle_request("POST", path, json_body=json, headers=headers)

    def get(self, path: str, *, headers: Optional[Dict[str, str]] = None) -> Response:
        return self.app.handle_request("GET", path, headers=headers)
