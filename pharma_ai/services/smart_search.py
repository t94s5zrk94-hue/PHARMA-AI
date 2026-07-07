import logging
import pandas as pd
from typing import Any, Optional, Final
from rapidfuzz import process, fuzz
from pharma_ai.services.database import PharmaDatabase

logger: Final = logging.getLogger(__name__)

class SmartSearch:
    """
    Enterprise-grade search orchestration service for Pharma AI.
    Implements a multi-tiered search pipeline (Exact -> Fuzzy).
    """

    _FUZZY_SCORE_CUTOFF: Final[float] = 60.0

    def __init__(self) -> None:
        self._db = PharmaDatabase()

    def _normalize(self, query: str) -> str:
        return str(query).strip().lower()

    def search_anything(self, medicine_name: str) -> Optional[dict[str, Any]]:
        """
        Executes a tiered search pipeline to resolve a medicine by name.
        """
        if not medicine_name or not isinstance(medicine_name, str):
            return None

        clean_query = self._normalize(medicine_name)

        # 1. Exact Search Pipeline
        # Pharma AI's existing flow: Query -> DB -> Complete Data Structure
        exact_result = self._db.get_complete_medicine(clean_query)
        if exact_result:
            return self._format_response(exact_result, "exact", 100.0, medicine_name)

        # 2. Fuzzy Search Pipeline
        return self._run_fuzzy_search(clean_query)

    def _run_fuzzy_search(self, query: str) -> Optional[dict[str, Any]]:
        """
        Performs multi-stage fuzzy matching (Brand -> Generic).
        """
        # Tier 1: Fuzzy Brand Lookup
        brand_names = self._db.brand["Brand_Name"].dropna().astype(str).tolist()
        best_brand = process.extractOne(query, brand_names, scorer=fuzz.WRatio, score_cutoff=self._FUZZY_SCORE_CUTOFF)

        if best_brand:
            matched_name, score, _ = best_brand
            result = self._db.get_complete_medicine(matched_name)
            if result:
                return self._format_response(result, "fuzzy_brand", float(score), matched_name)

        # Tier 2: Fuzzy Generic Lookup
        generic_names = self._db.generic["Generic_Name"].dropna().astype(str).tolist()
        best_generic = process.extractOne(query, generic_names, scorer=fuzz.WRatio, score_cutoff=self._FUZZY_SCORE_CUTOFF)

        if best_generic:
            matched_name, score, _ = best_generic
            # Find brand via generic link (Generic_ID)
            generic_row = self._db.generic[self._db.generic["Generic_Name"] == matched_name]
            if not generic_row.empty:
                g_id = generic_row.iloc[0]["Generic_ID"]
                brand_row = self._db.brand[self._db.brand["Generic_ID"] == g_id]
                if not brand_row.empty:
                    result = self._db.get_complete_medicine(brand_row.iloc[0]["Brand_Name"])
                    if result:
                        return self._format_response(result, "fuzzy_generic", float(score), matched_name)

        logger.warning(f"No match found for query: {query}")
        return None

    def _format_response(self, data: dict[str, Any], match_type: str, confidence: float, matched_value: str) -> dict[str, Any]:
        return {
            "data": data,
            "match_type": match_type,
            "confidence": confidence,
            "matched_value": matched_value
        }

    def get_brand_list(self, search_result: dict[str, Any]) -> pd.DataFrame:
        """
        Retrieves all available brands for the generic group of the matched result.
        """
        try:
            # Consistent with Frozen Database Contract
            generic_id = search_result.get("data", {}).get("generic", {}).get("Generic_ID")
            if generic_id is None:
                return pd.DataFrame()
            
            return self._db.brand[self._db.brand["Generic_ID"] == generic_id]
        except Exception as e:
            logger.error(f"Error retrieving brand list: {e}")
            return pd.DataFrame()

# Singleton Instance for internal use
_instance = SmartSearch()

def search_anything(medicine_name: str) -> Optional[dict[str, Any]]:
    return _instance.search_anything(medicine_name)

def get_brand_list(search_result: dict[str, Any]) -> pd.DataFrame:
    return _instance.get_brand_list(search_result)