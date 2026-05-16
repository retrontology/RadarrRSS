from app.feeds.bluray import BLURAY_NEW_RELEASES_URL
from app.feeds.registry import get_feed_by_path


def test_feed_definition_is_hardcoded(monkeypatch) -> None:
    monkeypatch.setenv("UPSTREAM_RSS_URL", "https://example.invalid/feed.xml")
    monkeypatch.setenv("FEED_PATH", "/not-used")

    feed = get_feed_by_path("/feeds/bluray/new")

    assert feed is not None
    assert feed.path == "/feeds/bluray/new"
    assert feed.upstream_url == BLURAY_NEW_RELEASES_URL

