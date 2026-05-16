from __future__ import annotations

import httpx


async def fetch_text(url: str, timeout_seconds: float, user_agent: str) -> str:
    async with httpx.AsyncClient(
        timeout=timeout_seconds,
        headers={"User-Agent": user_agent},
        follow_redirects=True,
    ) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

