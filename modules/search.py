import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

generic_df = pd.read_csv(os.path.join(BASE_DIR, "database", "generic_master.csv"))
brand_df = pd.read_csv(os.path.join(BASE_DIR, "database", "brand_master.csv"))
company_df = pd.read_csv(os.path.join(BASE_DIR, "database", "company_master.csv"))
product_df = pd.read_csv(os.path.join(BASE_DIR, "database", "product_master.csv"))


def search_medicine(query):

    query = query.strip().lower()

    product = product_df[
        product_df["Product_Name"].astype(str).str.lower().str.contains(query)
    ]

    if not product.empty:
        return product, "product"

    brand = brand_df[
        brand_df["Brand_Name"].astype(str).str.lower().str.contains(query)
    ]

    if not brand.empty:
        return brand, "brand"

    generic = generic_df[
        generic_df["Generic_Name"].astype(str).str.lower().str.contains(query)
    ]

    if not generic.empty:
        return generic, "generic"

    return None, None