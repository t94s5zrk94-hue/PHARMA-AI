import pandas as pd
import os
import time
import logging

# Logger setup
logger = logging.getLogger(__name__)

# --- FIX: Absolute Path Construction ---
# આ કોડ ફાઈલ જે ફોલ્ડરમાં છે તેનાથી બે લેવલ ઉપર જઈને (validator -> PHARMA AI) રૂટ સેટ કરશે
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = {
    "generic": os.path.join(BASE_DIR, "database", "medicine", "generic_master.csv"),
    "brand": os.path.join(BASE_DIR, "database", "medicine", "brand_master.csv"),
    "company": os.path.join(BASE_DIR, "database", "medicine", "company_master.csv"),
    "product": os.path.join(BASE_DIR, "database", "product", "product_master.csv"),
    "atc": os.path.join(BASE_DIR, "database", "atc", "atc_master.csv"),
    "therapeutic": os.path.join(BASE_DIR,"database","therapeutic","therapeutic_master.csv",),
    "pharmacological": os.path.join(BASE_DIR,"database","pharmacological","pharmacological_master.csv",),
    "generic_atc_mapping": os.path.join(BASE_DIR,"database","mapping","generic_atc_mapping.csv",),
    "generic_class_mapping": os.path.join(BASE_DIR,"database","mapping","generic_class_mapping.csv",),
   }

# Standardized Schema
REQUIRED_SCHEMAS = {
        "generic": ["Generic_ID", "Generic_Name","Standardized_Name","Generic_Type","Ingredients","created_at","updated_at","catalog_source","clinical_source","version","Status",],
        "brand": ["Brand_ID","Brand_Name","Generic_ID","Company_ID","Strength","Dosage_Form","Status",],
        "company": ["Company_ID","Company_Name","Country","Company_Type","Status",],
        "product": ["Product_ID","Generic_ID","Product_Name","Strength","Dosage_Form","Route","Pack_Size","Unit","Manufacturer","PMBJK_Code","HSN_Code","Schedule", "Storage","Status",],
        "atc": ["ATC_ID","ATC_Code","ATC_Name","Status",],
        "therapeutic": ["Therapeutic_Class_ID","Therapeutic_Class_Name","Description","WHO_Reference","Status",],
        "pharmacological": ["Pharmacological_Class_ID","Pharmacological_Class_Name","Description","WHO_Reference","Status",],
        "generic_atc_mapping": ["Mapping_ID","Generic_ID","ATC_ID",],
        "generic_class_mapping": ["Mapping_ID","Generic_ID","Therapeutic_Class_ID","Pharmacological_Class_ID",],
        }

def load_tables():
    """Update: Now uses the global FILES dictionary with absolute paths."""
    data = {}
    for key, full_path in FILES.items():
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Critical Error: {full_path} missing.")
        data[key] = pd.read_csv(full_path)
    return data

def run_db_regression():
    start_time = time.time()

    try:
        data = load_tables()

        # Schema Validation
        for table_name, required_columns in REQUIRED_SCHEMAS.items():

            df = data[table_name]

            missing = [
                col
                for col in required_columns
                if col not in df.columns
            ]

            if missing:
                raise ValueError(
                    f"{table_name}: Missing columns -> {missing}"
                )
        # Duplicate Validation
        for table_name, df in data.items():

            duplicate_rows = df.duplicated().sum()

            if duplicate_rows > 0:
                raise ValueError(
                f"{table_name}: {duplicate_rows} duplicate rows found."
            )
        report = {
            "status": "PASS",
            "execution_time": round(time.time() - start_time, 4),
        }

        return report

    except Exception as e:
        return {
            "status": "CRITICAL_FAIL",
            "error": str(e),
        }