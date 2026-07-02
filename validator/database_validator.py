import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")


generic = pd.read_csv(
    os.path.join(DATABASE_DIR, "generic_master.csv")
)

brand = pd.read_csv(
    os.path.join(DATABASE_DIR, "brand_master.csv")
)

company = pd.read_csv(
    os.path.join(DATABASE_DIR, "company_master.csv")
)

product = pd.read_csv(
    os.path.join(DATABASE_DIR, "product_master.csv")
)
print("="*60)
print("PHARMA AI DATABASE VALIDATOR")
print("="*60)

print()

print("Generic :", len(generic))
print("Brand   :", len(brand))
print("Company :", len(company))
print("Product :", len(product))

print()
# =====================================================
# Duplicate Checker
# =====================================================

def check_duplicate(df, column_name, table_name):

    duplicate = df[df[column_name].duplicated()]

    if duplicate.empty:

        print(f"✅ {table_name} : No Duplicate {column_name}")

    else:

        print(f"❌ {table_name} : Duplicate {column_name}")

        print(
            duplicate[
                [column_name]
            ]
        )

print()

check_duplicate(
    generic,
    "Generic_ID",
    "Generic"
)

check_duplicate(
    brand,
    "Brand_ID",
    "Brand"
)

check_duplicate(
    company,
    "Company_ID",
    "Company"
)

check_duplicate(
    product,
    "Product_ID",
    "Product"
)
# =====================================================
# Smart Foreign Key Validator
# =====================================================

def validate_foreign_key(
    child_df,
    child_column,
    parent_df,
    parent_column,
    title
):

    # Empty Values
    empty = child_df[
        child_df[child_column].isna()
    ]

    if not empty.empty:

        print(f"⚠ {title}")

        print(
            f"Missing {child_column} : {len(empty)} Rows"
        )

        return

    # Invalid Values

    invalid = child_df[
        ~child_df[child_column].isin(
            parent_df[parent_column]
        )
    ]

    if invalid.empty:

        print(f"✅ {title}")

    else:

        print(f"❌ {title}")

        print(
            invalid[
                [child_column]
            ]
        )
        print()

validate_foreign_key(
    brand,
    "Generic_ID",
    generic,
    "Generic_ID",
    "Brand → Generic Mapping OK"
)

validate_foreign_key(
    brand,
    "Company_ID",
    company,
    "Company_ID",
    "Brand → Company Mapping OK"
)

validate_foreign_key(
    product,
    "Brand_ID",
    brand,
    "Brand_ID",
    "Product → Brand Mapping OK"
)

print()
print("=" * 60)
print("DATABASE HEALTH REPORT")
print("=" * 60)

total = (
    len(generic)
    + len(brand)
    + len(company)
    + len(product)
)

print(f"Total Records : {total}")
print("Status : 🟢 Database Loaded Successfully")
print("=" * 60)
# =====================================================
# Empty Field Validator
# =====================================================

def check_empty_fields(df, table_name):

    print()
    print("=" * 60)
    print(f"{table_name.upper()} EMPTY FIELD REPORT")
    print("=" * 60)

    for column in df.columns:

        empty = df[column].isna().sum()

        if empty == 0:

            print(f"✅ {column:<30} : OK")

        else:

            print(f"⚠ {column:<30} : {empty} Empty")

check_empty_fields(
    generic,
    "Generic"
)

check_empty_fields(
    brand,
    "Brand"
)

check_empty_fields(
    company,
    "Company"
)

check_empty_fields(
    product,
    "Product"
)