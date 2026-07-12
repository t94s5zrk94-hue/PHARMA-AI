"""
Handles clinical query cleanup and normalization for search.
"""

import unicodedata
import re
from typing import Optional

class Normalizer:
    """
    Handles query cleanup and normalization for search pipelines.
    Uses pre-compiled regex patterns for high-performance processing.
    """
    @classmethod
    def normalize_symbols(cls, text: str) -> str:
        """
        Normalizes common medicine separators.
        """

        text = text.replace("+", " + ")
        text = text.replace("/", " ")
        text = text.replace("-", " ")

        return cls._SPACE_RE.sub(" ", text).strip()

    # Pre-compiled regex patterns for efficiency
    _SPACE_RE = re.compile(r"\s+")
    _INVALID_CHAR_RE = re.compile(
        r"[^a-z0-9\u0a80-\u0aff\s\+\-/]"
    )
    @classmethod
    def normalize(cls, query: Optional[str]) -> str:
        """
        Normalizes search queries through a multi-stage pipeline:
        Unicode normalization -> Lowercase/Strip -> Space cleanup -> Char filtering.
        """
        if not query:
         return ""

        query = query[:100]

        # 1. Unicode normalization (NFKC ensures consistent character representation)
        query = unicodedata.normalize('NFKC', query)

        query = cls.normalize_symbols(query)

        # 2. Lowercase and strip
        query = query.lower().strip()

        # 3. Remove extra spaces
        query = cls._SPACE_RE.sub(' ', query)

        # 4. Remove unwanted punctuation (preserve alphanumeric and Gujarati range)
        query = cls._INVALID_CHAR_RE.sub('', query)

        return query