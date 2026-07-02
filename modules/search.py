from modules.database import PharmaDatabase

db = PharmaDatabase()


def search_medicine(query):

    query = query.strip().lower()

    # ---------------- Product Search ----------------

    product = db.products()

    result = product[
        product["Product_Name"].astype(str).str.lower().str.contains(query)
    ]

    if not result.empty:
        return result, "Product"

    # ---------------- Brand Search ----------------

    brand = db.brands()

    result = brand[
        brand["Brand_Name"].astype(str).str.lower().str.contains(query)
    ]

    if not result.empty:
        return result, "Brand"

    # ---------------- Generic Search ----------------

    generic = db.generics()

    result = generic[
        generic["Generic_Name"].astype(str).str.lower().str.contains(query)
    ]

    if not result.empty:
        return result, "Generic"

    # ---------------- Company Search ----------------

    company = db.companies()

    result = company[
        company["Company_Name"].astype(str).str.lower().str.contains(query)
    ]

    if not result.empty:
        return result, "Company"

    return None, None