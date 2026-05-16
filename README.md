# Radarr RSS

Radarr RSS is a small FastAPI service that turns hardcoded outside movie RSS feeds into Radarr-friendly RSS import lists. The first feed reads Blu-ray.com's new movie releases feed, normalizes each title, matches it against TMDB, and emits RSS items with original title, matched TMDB title, TMDB id, and IMDB id metadata.

Disclaimer: this project was generated with AI assistance. Review and test it for your own environment before relying on it.

## Feeds

| Path | Upstream |
| --- | --- |
| `/feeds/bluray/new` | `https://www.blu-ray.com/rss/newreleasesfeed.xml` |

Feed paths, upstream URLs, and feed metadata are hardcoded in `app/feeds/`. Add future Blu-ray.com feeds in `app/feeds/bluray.py`; add other providers as separate modules.

## Environment

Copy `.env.example` to `.env` and set values when you need to override defaults:

```sh
TMDB_API_KEY=your_tmdb_api_key
APP_PORT=8734
REQUEST_TIMEOUT_SECONDS=10
CACHE_TTL_SECONDS=1800
USER_AGENT=RadarrRSS/0.1
MATCH_CONFIDENCE_THRESHOLD=0.82
INCLUDE_UNMATCHED_ITEMS=true
```

`TMDB_API_KEY` is optional for startup, but without it the feed will return unmatched items with blank TMDB/IMDB metadata.

## Docker

```sh
docker compose up -d --build
docker compose logs -f radarr-rss
```

The default Radarr URL is:

```text
http://host:8734/feeds/bluray/new
```

Set `APP_PORT` in `.env` to change the host port used by Docker Compose.

## Local Development

```sh
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8734
```

Run tests:

```sh
pytest
```

