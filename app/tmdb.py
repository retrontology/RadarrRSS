from __future__ import annotations

from typing import Any

import httpx

from app.models import SourceMovie, TmdbMatch
from app.title_match import title_similarity

TMDB_API_BASE_URL = "https://api.themoviedb.org/3"


class TmdbClient:
    def __init__(
        self,
        api_key: str,
        timeout_seconds: float,
        user_agent: str,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._api_key = api_key
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=TMDB_API_BASE_URL,
            timeout=timeout_seconds,
            headers={"User-Agent": user_agent},
        )

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def match_movie(self, movie: SourceMovie, threshold: float) -> TmdbMatch | None:
        if not self._api_key:
            return None

        results = await self._search_movie(movie)
        candidate = select_best_match(movie, results, threshold)
        if candidate is None:
            return None

        imdb_id = await self._get_imdb_id(candidate.tmdb_id)
        return TmdbMatch(
            tmdb_id=candidate.tmdb_id,
            title=candidate.title,
            year=candidate.year,
            imdb_id=imdb_id,
            confidence=candidate.confidence,
        )

    async def _search_movie(self, movie: SourceMovie) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "api_key": self._api_key,
            "query": movie.normalized_title,
            "include_adult": "false",
        }
        if movie.year is not None:
            params["year"] = movie.year

        response = await self._client.get("/search/movie", params=params)
        response.raise_for_status()
        payload = response.json()
        return list(payload.get("results", []))

    async def _get_imdb_id(self, tmdb_id: int) -> str:
        response = await self._client.get(
            f"/movie/{tmdb_id}/external_ids",
            params={"api_key": self._api_key},
        )
        response.raise_for_status()
        payload = response.json()
        return str(payload.get("imdb_id") or "")


def select_best_match(
    movie: SourceMovie,
    results: list[dict[str, Any]],
    threshold: float,
) -> TmdbMatch | None:
    candidates = [_candidate_from_result(movie, result) for result in results]
    candidates = [candidate for candidate in candidates if candidate is not None]
    if not candidates:
        return None

    best = max(candidates, key=lambda candidate: candidate.confidence)
    return best if best.confidence >= threshold else None


def _candidate_from_result(movie: SourceMovie, result: dict[str, Any]) -> TmdbMatch | None:
    tmdb_id = result.get("id")
    title = result.get("title") or result.get("name")
    if not isinstance(tmdb_id, int) or not isinstance(title, str) or not title:
        return None

    year = _release_year(result.get("release_date"))
    score = title_similarity(movie.normalized_title, title)
    if movie.year is not None and year is not None:
        if movie.year == year:
            score = min(1.0, score + 0.08)
        else:
            score = max(0.0, score - 0.18)

    return TmdbMatch(
        tmdb_id=tmdb_id,
        title=title,
        year=year,
        imdb_id="",
        confidence=score,
    )


def _release_year(value: Any) -> int | None:
    if not isinstance(value, str) or len(value) < 4:
        return None
    try:
        return int(value[:4])
    except ValueError:
        return None

