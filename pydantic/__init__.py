"""Minimal stub of pydantic BaseModel for testing without dependency."""
from __future__ import annotations

class BaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    def dict(self) -> dict:
        return self.__dict__.copy()
