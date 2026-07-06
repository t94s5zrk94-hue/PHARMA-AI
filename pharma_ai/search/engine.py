"""
Orchestrates the clinical search pipeline.
"""

import time
from dataclasses import replace
from typing import Optional
from pharma_ai.search.normalizer import Normalizer
from pharma_ai.search.matcher import Matcher
from pharma_ai.search.fuzzy_matcher import FuzzyMatcher
from pharma_ai.models.search_result import SearchResult

class SearchEngine:
    """Orchestrates the search pipeline using normalized queries and tiered matching."""

    _EXECUTION_TIME_PRECISION = 2

    def __init__(
        self, 
        normalizer: Normalizer, 
        matcher: Matcher, 
        fuzzy_matcher: FuzzyMatcher
    ) -> None:
        """
        Initializes the SearchEngine with validated dependencies.
        """
        if normalizer is None:
            raise ValueError("normalizer cannot be None.")
        if matcher is None:
            raise ValueError("matcher cannot be None.")
        if fuzzy_matcher is None:
            raise ValueError("fuzzy_matcher cannot be None.")

        self._normalizer = normalizer
        self._matcher = matcher
        self._fuzzy_matcher = fuzzy_matcher

    def search(self, query: str) -> Optional[SearchResult]:
        """
        Executes the tiered search pipeline: Normalization -> Exact Match -> Fuzzy Match.
        """
        start_time = time.perf_counter()
        
        # 1. Normalize
        normalized_query = self._normalizer.normalize(query)
        if not normalized_query:
            return None

        # 2. Exact Match Pipeline
        result = self._matcher.match_brand(normalized_query)
        if not result:
            result = self._matcher.match_generic(normalized_query)

        # 3. Fuzzy Match Pipeline (if exact fails)
        if not result:
            result = self._fuzzy_matcher.match_brand(normalized_query)

        # 4. Finalize Metrics (Inject timing)
        if result:
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            return replace(
                result, 
                execution_time_ms=round(execution_time_ms, self._EXECUTION_TIME_PRECISION)
            )

        return None