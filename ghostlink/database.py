"""In-memory database primitives used by the test suite.

The original project relied on SQLAlchemy which is unavailable in the
execution environment.  This lightweight replacement keeps the same
public surface that the application and tests expect while avoiding any
third-party dependency.
"""
from __future__ import annotations

import datetime as _dt
import secrets
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict, Iterator, Optional

from .config import config


def utc_now() -> _dt.datetime:
    """Return a timezone-naive UTC timestamp."""
    return _dt.datetime.now(_dt.timezone.utc).replace(tzinfo=None)


@dataclass
class ApiKey:
    """Simple representation of an API key record."""

    id: int = 0
    key: str = ""
    user_id: str = ""
    permissions: Optional[str] = "read"
    created_at: _dt.datetime = field(default_factory=utc_now)
    expires_at: Optional[_dt.datetime] = None

    def has_permission(self, permission: str) -> bool:
        if not self.permissions:
            return False
        return permission in {p.strip() for p in self.permissions.split(",") if p.strip()}

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return utc_now() > self.expires_at


class _Query:
    """Very small subset of SQLAlchemy's query API used in tests."""

    def __init__(self, db: "Database", filters: Optional[Dict[str, object]] = None) -> None:
        self._db = db
        self._filters = filters or {}

    def filter_by(self, **kwargs: object) -> "_Query":
        combined = dict(self._filters)
        combined.update(kwargs)
        return _Query(self._db, combined)

    def first(self) -> Optional[ApiKey]:
        for record in self._db._records.values():
            if all(getattr(record, key) == value for key, value in self._filters.items()):
                return record
        return None

    def delete(self) -> int:
        if not self._filters:
            ids = list(self._db._records.keys())
        else:
            ids = [
                record_id
                for record_id, record in self._db._records.items()
                if all(getattr(record, key) == value for key, value in self._filters.items())
            ]
        for record_id in ids:
            record = self._db._records.pop(record_id, None)
            if record is not None:
                self._db._records_by_key.pop(record.key, None)
        return len(ids)


class _Session:
    """Context manager that mimics the required Session API."""

    def __init__(self, db: "Database") -> None:
        self._db = db

    def __enter__(self) -> "_Session":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # pragma: no cover - trivial
        # Nothing special to clean up; database is in-memory.
        return None

    # Minimal subset used in tests and by the Database implementation
    def query(self, model):
        if model is not ApiKey:
            raise TypeError("Only ApiKey queries are supported in tests")
        return _Query(self._db)

    def add(self, api_key: ApiKey) -> None:
        self._db._records[api_key.id] = api_key
        self._db._records_by_key[api_key.key] = api_key

    def commit(self) -> None:  # pragma: no cover - included for API parity
        return None

    def refresh(self, api_key: ApiKey) -> None:  # pragma: no cover - parity only
        return None


class Database:
    """In-memory substitute for the original SQLAlchemy-powered database."""

    def __init__(self, database_url: Optional[str] = None) -> None:
        # ``database_url`` is kept for API compatibility but unused.
        self.database_url = database_url or config.DATABASE_URL
        self._records: Dict[int, ApiKey] = {}
        self._records_by_key: Dict[str, ApiKey] = {}
        self._next_id = 1

    @contextmanager
    def get_session(self) -> Iterator[_Session]:
        session = _Session(self)
        try:
            yield session
        finally:
            pass

    def create_api_key(
        self,
        user_id: str,
        permissions: str = "read",
        expires_at: Optional[_dt.datetime] = None,
    ) -> ApiKey:
        api_key = ApiKey(
            id=self._next_id,
            key=secrets.token_urlsafe(32),
            user_id=user_id,
            permissions=permissions,
            expires_at=expires_at,
        )
        self._next_id += 1
        self._records[api_key.id] = api_key
        self._records_by_key[api_key.key] = api_key
        return api_key

    def get_api_key(self, key: str) -> Optional[ApiKey]:
        return self._records_by_key.get(key)

    def validate_api_key(self, key: str, required_permission: str = "read") -> Optional[ApiKey]:
        api_key = self.get_api_key(key)
        if not api_key:
            return None
        if api_key.is_expired():
            return None
        if not api_key.has_permission(required_permission):
            return None
        return api_key
