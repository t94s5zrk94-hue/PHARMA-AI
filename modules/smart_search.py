from rapidfuzz import process
from modules.database import PharmaDatabase

db = PharmaDatabase()


def fuzzy_match(keyword, choices, score=60):

    result = process.extractOne(
        keyword,
        choices,
        score_cutoff=score
    )

    if result:
        return result[0]

    return None


def search_anything(keyword):

    keyword = str(keyword).strip().lower()

    # =====================================================
    # 1. Exact Product Search
    # =====================================================

    for _, row in db.product.iterrows():

        if keyword in str(row["Product_Name"]).lower():

            return db.get_complete_medicine(
                row["Product_Name"]
            )

    # =====================================================
    # 2. Exact Brand Search
    # =====================================================

    for _, row in db.brand.iterrows():

        if keyword in str(row["Brand_Name"]).lower():

            return db.get_complete_medicine(
                row["Brand_Name"]
            )

    # =====================================================
    # 3. Exact Generic Search
    # =====================================================

    for _, row in db.generic.iterrows():

        if keyword in str(row["Generic_Name"]).lower():

            brand = db.brand[
                db.brand["Generic_ID"] == row["Generic_ID"]
            ]

            if not brand.empty:

                return db.get_complete_medicine(
                    brand.iloc[0]["Brand_Name"]
                )

    # =====================================================
    # 4. Exact Gujarati Generic Search
    # =====================================================

    for _, row in db.generic.iterrows():

        if keyword in str(
            row["Generic_Name_Gujarati"]
        ).lower():

            brand = db.brand[
                db.brand["Generic_ID"] == row["Generic_ID"]
            ]

            if not brand.empty:

                return db.get_complete_medicine(
                    brand.iloc[0]["Brand_Name"]
                )

    # =====================================================
    # 5. Exact Company Search
    # =====================================================

    for _, row in db.company.iterrows():

        if keyword in str(row["Company_Name"]).lower():

            brand = db.brand[
                db.brand["Company_ID"] == row["Company_ID"]
            ]

            if not brand.empty:

                return db.get_complete_medicine(
                    brand.iloc[0]["Brand_Name"]
                )

    # =====================================================
    # 6. Fuzzy Product Search
    # =====================================================

    products = db.product["Product_Name"].astype(str).tolist()

    match = fuzzy_match(keyword, products)

    if match:

        return db.get_complete_medicine(match)

    # =====================================================
    # 7. Fuzzy Brand Search
    # =====================================================

    brands = db.brand["Brand_Name"].astype(str).tolist()

    match = fuzzy_match(keyword, brands)

    if match:

        return db.get_complete_medicine(match)

    # =====================================================
    # 8. Fuzzy Generic Search
    # =====================================================

    generics = db.generic["Generic_Name"].astype(str).tolist()

    match = fuzzy_match(keyword, generics)

    if match:

        generic_row = db.generic[
            db.generic["Generic_Name"] == match
        ].iloc[0]

        brand = db.brand[
            db.brand["Generic_ID"] == generic_row["Generic_ID"]
        ]

        if not brand.empty:

            return db.get_complete_medicine(
                brand.iloc[0]["Brand_Name"]
            )

    # =====================================================
    # 9. Fuzzy Gujarati Search
    # =====================================================

    gujarati = db.generic[
        "Generic_Name_Gujarati"
    ].astype(str).tolist()

    match = fuzzy_match(keyword, gujarati)

    if match:

        generic_row = db.generic[
            db.generic["Generic_Name_Gujarati"] == match
        ].iloc[0]

        brand = db.brand[
            db.brand["Generic_ID"] == generic_row["Generic_ID"]
        ]

        if not brand.empty:

            return db.get_complete_medicine(
                brand.iloc[0]["Brand_Name"]
            )

    # =====================================================
    # 10. Fuzzy Company Search
    # =====================================================

    companies = db.company["Company_Name"].astype(str).tolist()

    match = fuzzy_match(keyword, companies)

    if match:

        company_row = db.company[
            db.company["Company_Name"] == match
        ].iloc[0]

        brand = db.brand[
            db.brand["Company_ID"] == company_row["Company_ID"]
        ]

        if not brand.empty:

            return db.get_complete_medicine(
                brand.iloc[0]["Brand_Name"]
            )

    return None