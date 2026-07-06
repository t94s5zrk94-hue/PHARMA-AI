from typing import Optional
from rapidfuzz import process, fuzz
from modules.repositories.interfaces import MedicineRepositoryInterface
from modules.search.result_factory import ResultFactory
from pharma_ai.models.search_result import SearchResult

class FuzzyMatcher:
    """Production-hardened Fuzzy Matcher with defensive checks and DI."""
    
    def __init__(
        self, 
        medicine_repo: MedicineRepositoryInterface, 
        result_factory: ResultFactory,
        threshold: float = 70.0
    ):
        if not (0 <= threshold <= 100):
            raise ValueError("Threshold must be between 0 and 100.")
            
        self.repo = medicine_repo
        self.factory = result_factory
        self.threshold = threshold

    def match_brand(self, normalized_query: str) -> Optional[SearchResult]:
        # Contract-compliant candidate retrieval
        # Note: Ensure get_all_brand_names is part of MedicineRepositoryInterface
        all_brands = self.repo.get_all_brand_names()
        
        if not all_brands:
            return None
        
        result = process.extractOne(
            normalized_query, 
            all_brands, 
            scorer=fuzz.WRatio
        )
        
        if result and result[1] >= self.threshold:
            matched_name, score, _ = result
            brand_data = self.repo.get_brand(matched_name)
            
            # Defensive check for repository consistency
            if not brand_data:
                return None
            
            return self.factory.create_fuzzy_brand(
                data=brand_data,
                query=normalized_query,
                confidence=float(score)
            )
        return None