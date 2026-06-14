import xml.etree.ElementTree as ET

from app.feeds.bluray import BLURAY_NEW_RELEASES
from app.models import EnrichedMovie, SourceMovie, TmdbMatch
from app.rss_output import RADARRRSS_NS, build_rss


def test_build_rss_includes_requested_metadata_tags() -> None:
    source = SourceMovie(
        original_title="Fight Club 4K (Blu-ray)",
        normalized_title="Fight Club",
        year=1999,
        link="https://www.blu-ray.com/movies/Fight-Club-4K-Blu-ray/406956/",
        guid="source-guid",
        description="Original description",
        pub_date="Tue, 12 May 2026 00:00:00 -0400",
        category="blu-ray",
    )
    match = TmdbMatch(
        tmdb_id=550,
        title="Fight Club",
        year=1999,
        imdb_id="tt0137523",
        confidence=1.0,
    )

    rss = build_rss(BLURAY_NEW_RELEASES, [EnrichedMovie(source=source, match=match)])
    root = ET.fromstring(rss)
    item = root.find("./channel/item")

    assert "\n  <channel>" in rss
    assert "\n    <item>" in rss
    assert item is not None
    assert item.findtext("title") == "Fight Club"
    assert item.findtext("guid") == "550"
    assert item.findtext(f"{{{RADARRRSS_NS}}}originalName") == "Fight Club 4K (Blu-ray)"
    assert item.findtext(f"{{{RADARRRSS_NS}}}tmdbTitle") == "Fight Club"
    assert item.findtext(f"{{{RADARRRSS_NS}}}tmdbId") == "550"
    assert item.findtext(f"{{{RADARRRSS_NS}}}imdbId") == "tt0137523"


def test_build_rss_keeps_blank_metadata_for_unmatched_items() -> None:
    source = SourceMovie(
        original_title="Unknown Movie (Blu-ray)",
        normalized_title="Unknown Movie",
        year=None,
        link="https://example.com/unknown",
        guid="source-guid",
        description="Original description",
        pub_date="",
        category="blu-ray",
    )

    rss = build_rss(BLURAY_NEW_RELEASES, [EnrichedMovie(source=source, match=None)])
    root = ET.fromstring(rss)
    item = root.find("./channel/item")

    assert item is not None
    assert item.findtext("title") == "Unknown Movie"
    assert item.findtext("guid") == "source-guid"
    assert item.findtext(f"{{{RADARRRSS_NS}}}tmdbTitle") == ""
    assert item.findtext(f"{{{RADARRRSS_NS}}}tmdbId") == ""
    assert item.findtext(f"{{{RADARRRSS_NS}}}imdbId") == ""

