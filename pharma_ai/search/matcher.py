"""
Exact matching service for clinical medication resolution.
"""

from typing import Optional
from pharma_ai.models.search_result import SearchResult
from pharma_ai.repositories.interfaces.medicine import MedicineRepositoryInterface
from pharma_ai.search.result_factory import ResultFactory


class Matcher:
    """Service responsible for exact matching of medication names."""

    def __init__(
        self,
        medicine_repository: MedicineRepositoryInterface,
        result_factory: ResultFactory
    ) -> None:
        if medicine_repository is None:
            raise ValueError("medicine_repository cannot be None.")
        if result_factory is None:
            raise ValueError("result_factory cannot be None.")

        self._repository = medicine_repository
        self._factory = result_factory

    def _normalize_query(self, query: Optional[str]) -> Optional[str]:
        """Defensive normalization of search queries."""
        if query is None:
            return None
        normalized = query.strip()
        return normalized if normalized else None

    def match_brand(self, query: str) -> Optional[SearchResult]:
        """Performs an exact match search for a brand name."""
        normalized_query = self._normalize_query(query)
        if not normalized_query:
            return None

        brand_data = self._repository.get_brand(normalized_query)
        if not brand_data:
            return None

        return self._factory.create_exact_brand(
            data=brand_data,
            query=normalized_query
        )

    def match_generic(self, query: str) -> Optional[SearchResult]:
        """Performs an exact match search for a generic name."""
        normalized_query = self._normalize_query(query)
        if not normalized_query:
            return None

        # અપડેટેડ મેથડ કોલ
        generic_data = self._repository.get_generic_by_name(normalized_query)
        if not generic_data:
            return None

        return self._factory.create_exact_generic(
            data=generic_data,
            query=normalized_query
        )