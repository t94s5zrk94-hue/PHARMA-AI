"""Smart Search module - Version 3.0 (Optimized & Error-Proof)."""

from rapidfuzz import process
from modules.database import PharmaDatabase

db = PharmaDatabase()

# Constants
SEARCH_PRODUCT, SEARCH_BRAND, SEARCH_GENERIC = "Product", "Brand", "Generic"

# Precomputed Lists
PRODUCTS = db.product["Product_Name"].astype(str).tolist()
PRODUCTS_LOWER = [p.lower() for p in PRODUCTS]
BRANDS = db.brand["Brand_Name"].astype(str).tolist()
BRANDS_LOWER = [b.lower() for b in BRANDS]
GENERICS = db.generic["Generic_Name"].astype(str).tolist()
GENERICS_LOWER = [g.lower() for g in GENERICS]

def search_medicine(query: str):
    query = query.strip().lower()
    
    # 1. Exact Match with Index Lookup
    if query in BRANDS_LOWER:
        idx = BRANDS_LOWER.index(query)
        return db.get_complete_medicine(BRANDS[idx]), SEARCH_BRAND
    
    if query in GENERICS_LOWER:
        idx = GENERICS_LOWER.index(query)
        generic_row = db.generic.iloc[idx]
        brands = db.get_brands_by_generic(generic_row["Generic_ID"])
        if not brands.empty:
            return db.get_complete_medicine(brands.iloc[0]["Brand_Name"]), SEARCH_GENERIC
            
    if query in PRODUCTS_LOWER:
        idx = PRODUCTS_LOWER.index(query)
        return db.get_complete_medicine(PRODUCTS[idx]), SEARCH_PRODUCT

    # 2. Fuzzy Matching (Score 85+)
    # Fuzzy Brand
    match_brand = process.extractOne(query, BRANDS, score_cutoff=85)
    if match_brand:
        return db.get_complete_medicine(match_brand[0]), f"{SEARCH_BRAND} (Fuzzy)"

    # Fuzzy Generic
    match_generic = process.extractOne(query, GENERICS, score_cutoff=85)
    if match_generic:
        generic_name = match_generic[0]
        generic_row = db.generic[db.generic["Generic_Name"] == generic_name].iloc[0]
        brands = db.get_brands_by_generic(generic_row["Generic_ID"])
        if not brands.empty:
            return db.get_complete_medicine(brands.iloc[0]["Brand_Name"]), f"{SEARCH_GENERIC} (Fuzzy)"

    # Fuzzy Product
    match_product = process.extractOne(query, PRODUCTS, score_cutoff=85)
    if match_product:
        return db.get_complete_medicine(match_product[0]), f"{SEARCH_PRODUCT} (Fuzzy)"

    return None, None

def search_anything(query: str):
    result, _ = search_medicine(query)
    return result