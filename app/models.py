from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceMovie:
    original_title: str
    normalized_title: str
    year: int | None
    link: str
    guid: str
    description: str
    pub_date: str
    category: str


@dataclass(frozen=True)
class TmdbMatch:
    tmdb_id: int
    title: str
    year: int | None
    imdb_id: str
    confidence: float


@dataclass(frozen=True)
class EnrichedMovie:
    source: SourceMovie
    match: TmdbMatch | None

