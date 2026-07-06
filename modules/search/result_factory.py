from typing import Dict
from pharma_ai.models.search_result import SearchResult, MatchType, SearchStrategy

class ResultFactory:
    """Centralized factory for creating SearchResult objects."""

    def _build_result(
        self, 
        data: Dict, 
        query: str, 
        match_type: MatchType, 
        matched_value: str,
        strategy: SearchStrategy = SearchStrategy.DEFAULT,
        confidence: float = 100.0
    ) -> SearchResult:
        """Private helper to centralize construction and validation."""
        return SearchResult(
            data=data,
            match_type=match_type,
            confidence=confidence,
            matched_value=matched_value,
            query=query,
            search_strategy=strategy
        )

    def create_exact_brand(self, data: Dict, query: str) -> SearchResult:
        return self._build_result(
            data=data,
            query=query,
            match_type=MatchType.EXACT_BRAND,
            matched_value=data.get("Brand_Name", "")
        )

    def create_exact_generic(self, data: Dict, query: str) -> SearchResult:
        return self._build_result(
            data=data,
            query=query,
            match_type=MatchType.EXACT_GENERIC,
            matched_value=data.get("Generic_Name", "")
        )