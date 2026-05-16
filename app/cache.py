from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class _CacheEntry(Generic[T]):
    value: T
    expires_at: float


class TtlCache(Generic[T]):
    def __init__(self) -> None:
        self._entries: dict[str, _CacheEntry[T]] = {}

    def get(self, key: str) -> T | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        if entry.expires_at <= time.monotonic():
            self._entries.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: T, ttl_seconds: int) -> None:
        self._entries[key] = _CacheEntry(
            value=value,
            expires_at=time.monotonic() + ttl_seconds,
        )

