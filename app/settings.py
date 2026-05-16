from __future__ import annotations

import os
from dataclasses import dataclass


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return int(value)


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return float(value)


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    tmdb_api_key: str
    app_port: int
    request_timeout_seconds: float
    cache_ttl_seconds: int
    user_agent: str
    match_confidence_threshold: float
    include_unmatched_items: bool


def get_settings() -> Settings:
    return Settings(
        tmdb_api_key=os.getenv("TMDB_API_KEY", "").strip(),
        app_port=_get_int("APP_PORT", 8734),
        request_timeout_seconds=_get_float("REQUEST_TIMEOUT_SECONDS", 10.0),
        cache_ttl_seconds=_get_int("CACHE_TTL_SECONDS", 1800),
        user_agent=os.getenv(
            "USER_AGENT",
            "RadarrRSS/0.1 (+https://github.com/retrontology/RadarrRSS)",
        ),
        match_confidence_threshold=_get_float("MATCH_CONFIDENCE_THRESHOLD", 0.82),
        include_unmatched_items=_get_bool("INCLUDE_UNMATCHED_ITEMS", True),
    )

