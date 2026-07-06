"""
Fuzzy matching service for clinical brand name resolution.
"""

from typing import Optional
from rapidfuzz import process, fuzz

from pharma_ai.models.search_result import SearchResult
from pharma_ai.repositories.interfaces.medicine import MedicineRepositoryInterface
from pharma_ai.search.result_factory import ResultFactory


class FuzzyMatcher:
    """
    Service responsible for fuzzy matching of medicine brand names.
    """

    def __init__(
        self,
        medicine_repository: MedicineRepositoryInterface,
        result_factory: ResultFactory,
        threshold: float = 70.0
    ) -> None:
        if medicine_repository is None:
            raise ValueError("medicine_repository cannot be None.")
        if result_factory is None:
            raise ValueError("result_factory cannot be None.")
        if not 0 <= threshold <= 100:
            raise ValueError("Threshold must be between 0 and 100.")

        self._repository = medicine_repository
        self._factory = result_factory
        self._threshold = threshold

    def match_brand(self, query: str) -> Optional[SearchResult]:
        """Performs a fuzzy search to resolve a brand name query."""
        query = query.strip()
        if not query:
            return None

        brand_names = self._repository.list_brand_names()
        if not brand_names:
            return None

        match = process.extractOne(query, brand_names, scorer=WRatio)
        if not match:
            return None

        matched_name, score, _ = match
        if score < self._threshold:
            return None

        brand_data = self._repository.get_brand(str(matched_name))
        if not brand_data:
            return None

        # Factory API નો યોગ્ય ઉપયોગ
        return self._factory.create_fuzzy_brand(
            data=brand_data,
            query=query,
            matched_name=str(matched_name),
            score=float(score)
        )