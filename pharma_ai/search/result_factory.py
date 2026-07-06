"""
Centralized factory for constructing SearchResult domain objects.

This module enforces consistent object creation across all search strategies,
ensuring that search results adhere to the core domain model requirements.
"""

from typing import Any
from pharma_ai.models.search_result import (
    SearchResult,
    MatchType,
    SearchStrategy
)


class ResultFactory:
    """
    Factory responsible for the instantiation of SearchResult objects.

    This class serves as the single source of truth for creating domain-compliant
    search results, abstracting the construction logic from the search engines.
    """

    def create_exact_brand(self, data: dict[str, Any], query: str) -> SearchResult:
        """Constructs a result for an exact brand name match."""
        return self._build_result(
            data=data,
            query=query,
            matched_name=query,
            match_type=MatchType.EXACT,
            confidence=100.0,
            strategy=SearchStrategy.BRAND
        )

    def create_exact_generic(self, data: dict[str, Any], query: str) -> SearchResult:
        """Constructs a result for an exact generic name match."""
        return self._build_result(
            data=data,
            query=query,
            matched_name=query,
            match_type=MatchType.EXACT,
            confidence=100.0,
            strategy=SearchStrategy.GENERIC
        )

    def create_fuzzy_brand(
        self,
        data: dict[str, Any],
        query: str,
        matched_name: str,
        score: float
    ) -> SearchResult:
        """Constructs a result for a fuzzy brand name match."""
        return self._build_result(
            data=data,
            query=query,
            matched_name=matched_name,
            match_type=MatchType.FUZZY,
            confidence=score,
            strategy=SearchStrategy.BRAND
        )

    def create_search_result(
        self,
        data: dict[str, Any],
        query: str,
        matched_name: str,
        match_type: MatchType,
        confidence: float,
        strategy: SearchStrategy
    ) -> SearchResult:
        """Generic builder for complex or future AI-based search engines."""
        return self._build_result(
            data=data,
            query=query,
            matched_name=matched_name,
            match_type=match_type,
            confidence=confidence,
            strategy=strategy
        )

    def _build_result(
        self,
        data: dict[str, Any],
        query: str,
        matched_name: str,
        match_type: MatchType,
        confidence: float,
        strategy: SearchStrategy
    ) -> SearchResult:
        """Private helper to centralize SearchResult instantiation."""
        return SearchResult(
            data=data,
            query=query,
            matched_name=matched_name,
            match_type=match_type,
            confidence=confidence,
            strategy=strategy
        )