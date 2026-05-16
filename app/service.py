from __future__ import annotations

from app.cache import TtlCache
from app.feeds.registry import FeedDefinition
from app.http_client import fetch_text
from app.models import EnrichedMovie
from app.rss_output import build_rss
from app.settings import Settings
from app.tmdb import TmdbClient


class FeedService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._cache: TtlCache[str] = TtlCache()

    async def render_feed(self, feed: FeedDefinition) -> str:
        cached = self._cache.get(feed.key)
        if cached is not None:
            return cached

        source_xml = await fetch_text(
            feed.upstream_url,
            self._settings.request_timeout_seconds,
            self._settings.user_agent,
        )
        source_movies = feed.parser(source_xml)

        tmdb = TmdbClient(
            api_key=self._settings.tmdb_api_key,
            timeout_seconds=self._settings.request_timeout_seconds,
            user_agent=self._settings.user_agent,
        )
        try:
            enriched = [
                EnrichedMovie(
                    source=movie,
                    match=await tmdb.match_movie(
                        movie,
                        self._settings.match_confidence_threshold,
                    ),
                )
                for movie in source_movies
            ]
        finally:
            await tmdb.close()

        if not self._settings.include_unmatched_items:
            enriched = [movie for movie in enriched if movie.match is not None]

        rss = build_rss(feed, enriched)
        self._cache.set(feed.key, rss, self._settings.cache_ttl_seconds)
        return rss

