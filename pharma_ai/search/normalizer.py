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

    # Pre-compiled regex patterns for efficiency
    _SPACE_RE = re.compile(r"\s+")
    _INVALID_CHAR_RE = re.compile(r"[^a-z0-9\u0a80-\u0aff\s]")

    @classmethod
    def normalize(cls, query: Optional[str]) -> str:
        """
        Normalizes search queries through a multi-stage pipeline:
        Unicode normalization -> Lowercase/Strip -> Space cleanup -> Char filtering.
        """
        if not query:
            return ""

        # 1. Unicode normalization (NFKC ensures consistent character representation)
        query = unicodedata.normalize('NFKC', query)

        # 2. Lowercase and strip
        query = query.lower().strip()

        # 3. Remove extra spaces
        query = cls._SPACE_RE.sub(' ', query)

        # 4. Remove unwanted punctuation (preserve alphanumeric and Gujarati range)
        query = cls._INVALID_CHAR_RE.sub('', query)

        return query