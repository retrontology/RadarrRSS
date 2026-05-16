from pathlib import Path

from app.feeds.bluray import extract_bluray_year, normalize_bluray_title, parse_bluray_new_releases


def test_normalize_bluray_title_removes_release_qualifiers() -> None:
    assert normalize_bluray_title("Fight Club 4K (Blu-ray)") == "Fight Club"
    assert normalize_bluray_title("Moneyball 4K (Blu-ray)") == "Moneyball"
    assert normalize_bluray_title("Twinless (Blu-ray)") == "Twinless"


def test_extract_bluray_year_from_description_metadata() -> None:
    description = '<b><font color="#666666">Disney | 1999 | 139 mins | Rated R</font></b>'
    assert extract_bluray_year(description) == 1999


def test_parse_bluray_new_releases_fixture() -> None:
    fixture = Path("tests/fixtures/bluray_newreleases.xml").read_text()

    movies = parse_bluray_new_releases(fixture)

    assert len(movies) == 2
    assert movies[0].original_title == "Fight Club 4K (Blu-ray)"
    assert movies[0].normalized_title == "Fight Club"
    assert movies[0].year == 1999
    assert movies[1].normalized_title == "Twinless"
    assert movies[1].year == 2025

