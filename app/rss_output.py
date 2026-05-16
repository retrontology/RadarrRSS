from __future__ import annotations

import xml.etree.ElementTree as ET
from email.utils import formatdate

from app.feeds.registry import FeedDefinition
from app.models import EnrichedMovie

RADARRRSS_NS = "https://github.com/retrontology/RadarrRSS/ns"

ET.register_namespace("radarrrss", RADARRRSS_NS)


def build_rss(feed: FeedDefinition, movies: list[EnrichedMovie]) -> str:
    rss = ET.Element(
        "rss",
        {
            "version": "2.0",
            "xmlns:atom": "https://www.w3.org/2005/Atom",
        },
    )
    channel = ET.SubElement(rss, "channel")
    _add_text(channel, "title", feed.title)
    _add_text(channel, "link", feed.upstream_url)
    _add_text(channel, "description", feed.description)
    _add_text(channel, "language", "en-us")
    _add_text(channel, "lastBuildDate", formatdate(usegmt=True))

    for movie in movies:
        _add_item(channel, movie)

    ET.indent(rss, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        rss,
        encoding="unicode",
        short_empty_elements=False,
    )


def _add_item(channel: ET.Element, movie: EnrichedMovie) -> None:
    source = movie.source
    match = movie.match
    item = ET.SubElement(channel, "item")

    title = match.title if match is not None else source.normalized_title
    _add_text(item, "title", title)
    _add_text(item, "link", source.link)
    _add_text(item, "description", source.description)
    if source.pub_date:
        _add_text(item, "pubDate", source.pub_date)
    if source.category:
        _add_text(item, "category", source.category)

    guid = match.imdb_id if match is not None and match.imdb_id else source.guid
    guid_element = _add_text(item, "guid", guid)
    guid_element.set("isPermaLink", "false")

    _add_ns_text(item, "originalName", source.original_title)
    _add_ns_text(item, "tmdbTitle", "" if match is None else match.title)
    _add_ns_text(item, "tmdbId", "" if match is None else str(match.tmdb_id))
    _add_ns_text(item, "imdbId", "" if match is None else match.imdb_id)


def _add_text(parent: ET.Element, tag: str, text: str) -> ET.Element:
    element = ET.SubElement(parent, tag)
    element.text = text
    return element


def _add_ns_text(parent: ET.Element, tag: str, text: str) -> ET.Element:
    element = ET.SubElement(parent, ET.QName(RADARRRSS_NS, tag))
    element.text = text
    return element

