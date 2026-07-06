"""
Smart Search Module.
Provides multi-layered search functionality (Exact + Fuzzy).
Optimized with Dynamic Schema Validation for resilient column handling.
"""

from typing import Dict, Any, Optional
import pandas as pd
from rapidfuzz import process
from modules.database import PharmaDatabase

# API Public Exposure
__all__ = ["search_anything", "get_brand_list"]

db = PharmaDatabase()
FUZZY_SCORE_CUTOFF = 60

# Internal Constant Keys
KEY_DATA = "data"
KEY_GENERIC = "generic"
KEY_GENERIC_ID = "Generic_ID"

def _get_validated_generic_columns() -> list:
    """Dynamically returns generic columns available in the current schema."""
    available_cols = ["Generic_Name", "Generic_Name_Gujarati"]
    return [col for col in available_cols if col in db.generic.columns]

def _create_search_result(brand_name: str, match_type: str, confidence: float = 100.0, matched_value: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Structured Result Object."""
    medicine = db.get_complete_medicine(brand_name)
    if medicine:
        return {
            KEY_DATA: medicine,
            "match_type": match_type,
            "confidence": float(confidence),
            "matched_value": matched_value
        }
    return None

def search_anything(keyword: str) -> Optional[Dict[str, Any]]:
    """Performs multi-layered search with dynamic schema awareness."""
    keyword = str(keyword).strip().lower()
    generic_cols = _get_validated_generic_columns()

    def get_df_match(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        return df[df[col_name].fillna("").str.lower() == keyword]

    # 1. Exact Search
    b_match = get_df_match(db.brand, "Brand_Name")
    if not b_match.empty:
        return _create_search_result(b_match.iloc[0]["Brand_Name"], "Exact Brand")

    for col in generic_cols:
        g_match = get_df_match(db.generic, col)
        if not g_match.empty:
            brand = db.brand[db.brand[KEY_GENERIC_ID] == g_match.iloc[0][KEY_GENERIC_ID]]
            if not brand.empty:
                return _create_search_result(brand.iloc[0]["Brand_Name"], f"Exact {col}")

    # 2. Fuzzy Search
    # Brand
    match = process.extractOne(keyword, db.brand["Brand_Name"].astype(str).tolist(), score_cutoff=FUZZY_SCORE_CUTOFF)
    if match:
        return _create_search_result(match[0], "Fuzzy Brand", match[1], match[0])

    # Generic / Gujarati (Dynamic)
    for col in generic_cols:
        choices = db.generic[col].fillna("").astype(str).tolist()
        match = process.extractOne(keyword, choices, score_cutoff=FUZZY_SCORE_CUTOFF)
        if match:
            g_row = db.generic[db.generic[col] == match[0]].iloc[0]
            brand = db.brand[db.brand[KEY_GENERIC_ID] == g_row[KEY_GENERIC_ID]]
            if not brand.empty:
                return _create_search_result(brand.iloc[0]["Brand_Name"], f"Fuzzy {col}", match[1], match[0])

    return None

def get_brand_list(search_result: Optional[Dict[str, Any]]) -> pd.DataFrame:
    """Return all brands belonging to the matched generic, resilient to schema changes."""
    empty_df = db.brand.iloc[0:0].copy()

    if search_result is None or KEY_DATA not in search_result:
        return empty_df

    generic = search_result[KEY_DATA].get(KEY_GENERIC)
    if generic is None or KEY_GENERIC_ID not in generic:
        return empty_df

    generic_id = generic[KEY_GENERIC_ID]
    brands = db.brand[db.brand[KEY_GENERIC_ID] == generic_id].copy()

    return brands if not brands.empty else empty_df