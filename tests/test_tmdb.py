from app.models import SourceMovie
from app.tmdb import select_best_match


def _source_movie(title: str, year: int | None) -> SourceMovie:
    return SourceMovie(
        original_title=f"{title} (Blu-ray)",
        normalized_title=title,
        year=year,
        link="https://example.com/movie",
        guid="source-guid",
        description="",
        pub_date="",
        category="blu-ray",
    )


def test_select_best_match_prefers_title_and_year_match() -> None:
    match = select_best_match(
        _source_movie("Fight Club", 1999),
        [
            {"id": 550, "title": "Fight Club", "release_date": "1999-10-15"},
            {"id": 999, "title": "Fight Club", "release_date": "2026-01-01"},
        ],
        threshold=0.82,
    )

    assert match is not None
    assert match.tmdb_id == 550
    assert match.title == "Fight Club"


def test_select_best_match_returns_none_below_threshold() -> None:
    match = select_best_match(
        _source_movie("Fight Club", 1999),
        [{"id": 1, "title": "Unrelated Movie", "release_date": "1999-01-01"}],
        threshold=0.82,
    )

    assert match is None

