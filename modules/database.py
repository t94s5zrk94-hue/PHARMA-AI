import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")


class PharmaDatabase:

    def __init__(self):

        self.brand = pd.read_csv(
            os.path.join(DATABASE_DIR, "brand_master.csv")
        )

        self.generic = pd.read_csv(
            os.path.join(DATABASE_DIR, "generic_master.csv")
        )

        self.company = pd.read_csv(
            os.path.join(DATABASE_DIR, "company_master.csv")
        )

        self.product = pd.read_csv(
            os.path.join(DATABASE_DIR, "product_master.csv")
        )

    # -------------------------------------------------

    def get_product(self, product_name):

        query = str(product_name).strip().lower()

        df = self.product.copy()

        result = df[
        df["Product_Name"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.contains(query, na=False)        ]

        if result.empty:
         return None

        return result.iloc[0]

    # -------------------------------------------------

    def get_brand(self, brand_id):

        brand_id = str(brand_id).strip()

        df = self.brand.copy()

        df["Brand_ID"] = (
            df["Brand_ID"]
            .astype(str)
            .str.strip()
        )

        result = df[
            df["Brand_ID"] == brand_id
        ]

        if result.empty:
            return None

        return result.iloc[0]

    # -------------------------------------------------

    def get_generic(self, generic_id):

        generic_id = str(generic_id).strip()

        df = self.generic.copy()

        df["Generic_ID"] = (
            df["Generic_ID"]
            .astype(str)
            .str.strip()
        )

        result = df[
            df["Generic_ID"] == generic_id
        ]

        if result.empty:
            return None

        return result.iloc[0]

    # -------------------------------------------------

    def get_company(self, company_id):

        company_id = str(company_id).strip()

        df = self.company.copy()

        df["Company_ID"] = (
            df["Company_ID"]
            .astype(str)
            .str.strip()
        )

        result = df[
            df["Company_ID"] == company_id
        ]

        if result.empty:
            return None

        return result.iloc[0]

    # -------------------------------------------------

    def get_complete_medicine(self, product_name):

        product = self.get_product(product_name)

        if product is None:
            return None

        brand = self.get_brand(product["Brand_ID"])

        if brand is None:
            return None

        generic = self.get_generic(brand["Generic_ID"])

        if generic is None:
            return None

        company = self.get_company(brand["Company_ID"])

        if company is None:
            return None

        return {
            "product": product,
            "brand": brand,
            "generic": generic,
            "company": company
        }
    # -------------------------------------------------

    def get_brands_by_generic(self, generic_id):

        generic_id = str(generic_id).strip()

        brands = self.brand[
        self.brand["Generic_ID"].astype(str).str.strip() == generic_id
        ]

        return brands