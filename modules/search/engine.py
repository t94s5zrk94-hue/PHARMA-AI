import time
from dataclasses import replace
from typing import Optional
from modules.search.normalizer import Normalizer
from modules.search.matcher import Matcher
from modules.search.fuzzy_matcher import FuzzyMatcher
from pharma_ai.models.search_result import SearchResult

class SearchEngine:
    """Orchestrates the search pipeline."""

    def __init__(
        self, 
        normalizer: Normalizer, 
        matcher: Matcher, 
        fuzzy_matcher: FuzzyMatcher
    ):
        self.normalizer = normalizer
        self.matcher = matcher
        self.fuzzy_matcher = fuzzy_matcher

    def search(self, query: str) -> Optional[SearchResult]:
        start_time = time.perf_counter()
        
        # 1. Normalize
        normalized_query = self.normalizer.normalize(query)
        if not normalized_query:
            return None

        # 2. Exact Match Pipeline
        result = self.matcher.match_brand(normalized_query)
        if not result:
            result = self.matcher.match_generic(normalized_query)

        # 3. Fuzzy Match Pipeline (if exact fails)
        if not result:
            result = self.fuzzy_matcher.match_brand(normalized_query)

        # 4. Finalize Metrics (Inject timing)
        if result:
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            return replace(result, execution_time_ms=round(execution_time_ms, 2))

        return None