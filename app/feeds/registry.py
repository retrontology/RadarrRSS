from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.models import SourceMovie

FeedParser = Callable[[str], list[SourceMovie]]


@dataclass(frozen=True)
class FeedDefinition:
    key: str
    path: str
    upstream_url: str
    title: str
    description: str
    source_name: str
    parser: FeedParser


def get_feeds() -> tuple[FeedDefinition, ...]:
    from app.feeds.bluray import FEEDS as BLURAY_FEEDS

    return (*BLURAY_FEEDS,)


def get_feed_by_path(path: str) -> FeedDefinition | None:
    normalized_path = path if path.startswith("/") else f"/{path}"
    return next((feed for feed in get_feeds() if feed.path == normalized_path), None)

