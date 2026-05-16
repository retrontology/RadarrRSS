from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET

from app.feeds.registry import FeedDefinition
from app.models import SourceMovie

BLURAY_NEW_RELEASES_URL = "https://www.blu-ray.com/rss/newreleasesfeed.xml"

_RELEASE_QUALIFIERS = (
    r"\((?:4K\s+)?Blu-ray\)",
    r"\[(?:4K\s+)?Blu-ray\]",
    r"\b(?:Ultra\s+HD|UHD|4K)\b",
)


def parse_bluray_new_releases(xml_text: str) -> list[SourceMovie]:
    root = ET.fromstring(_extract_xml_document(xml_text))
    channel = root.find("channel")
    if channel is None:
        return []

    movies: list[SourceMovie] = []
    for item in channel.findall("item"):
        original_title = _child_text(item, "title")
        description = html.unescape(_child_text(item, "description"))
        movies.append(
            SourceMovie(
                original_title=original_title,
                normalized_title=normalize_bluray_title(original_title),
                year=extract_bluray_year(description),
                link=_child_text(item, "link"),
                guid=_child_text(item, "guid"),
                description=description,
                pub_date=_child_text(item, "pubDate"),
                category=_child_text(item, "category"),
            )
        )
    return movies


def normalize_bluray_title(title: str) -> str:
    normalized = html.unescape(title).strip()
    for qualifier in _RELEASE_QUALIFIERS:
        normalized = re.sub(qualifier, "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"\s+([:;,.!?])", r"\1", normalized)
    return normalized.strip(" -")


def extract_bluray_year(description: str) -> int | None:
    metadata = re.sub(r"<[^>]+>", " ", html.unescape(description))
    match = re.search(r"\|\s*(19\d{2}|20\d{2})\s*\|", metadata)
    if not match:
        return None
    return int(match.group(1))


def _extract_xml_document(text: str) -> str:
    start = text.find("<?xml")
    if start == -1:
        start = text.find("<rss")
    return text[start:] if start > 0 else text


def _child_text(element: ET.Element, name: str) -> str:
    child = element.find(name)
    return "" if child is None or child.text is None else child.text.strip()


BLURAY_NEW_RELEASES = FeedDefinition(
    key="bluray-new-releases",
    path="/feeds/bluray/new",
    upstream_url=BLURAY_NEW_RELEASES_URL,
    title="Blu-ray.com New Movie Releases",
    description="TMDB-matched Blu-ray.com movie new releases for Radarr.",
    source_name="Blu-ray.com New Releases",
    parser=parse_bluray_new_releases,
)

FEEDS = (BLURAY_NEW_RELEASES,)

