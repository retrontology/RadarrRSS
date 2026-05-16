from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import FastAPI, HTTPException, Response

from app.feeds.registry import FeedDefinition, get_feeds
from app.service import FeedService
from app.settings import get_settings

app = FastAPI(title="Radarr RSS", version="0.1.0")
settings = get_settings()
feed_service = FeedService(settings)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/feeds")
async def feeds() -> list[dict[str, str]]:
    return [
        {
            "key": feed.key,
            "path": feed.path,
            "upstream_url": feed.upstream_url,
        }
        for feed in get_feeds()
    ]


def _make_feed_endpoint(feed: FeedDefinition) -> Callable[[], Awaitable[Response]]:
    async def endpoint() -> Response:
        try:
            rss = await feed_service.render_feed(feed)
        except Exception as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        return Response(content=rss, media_type="application/rss+xml")

    return endpoint


for feed_definition in get_feeds():
    app.add_api_route(
        feed_definition.path,
        _make_feed_endpoint(feed_definition),
        methods=["GET"],
        name=feed_definition.key,
    )

