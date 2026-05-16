from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher


def comparable_title(title: str) -> str:
    decomposed = unicodedata.normalize("NFKD", title)
    ascii_title = "".join(char for char in decomposed if not unicodedata.combining(char))
    lowered = ascii_title.casefold()
    return re.sub(r"[^a-z0-9]+", " ", lowered).strip()


def title_similarity(left: str, right: str) -> float:
    comparable_left = comparable_title(left)
    comparable_right = comparable_title(right)
    if not comparable_left or not comparable_right:
        return 0.0
    if comparable_left == comparable_right:
        return 1.0
    return SequenceMatcher(None, comparable_left, comparable_right).ratio()

