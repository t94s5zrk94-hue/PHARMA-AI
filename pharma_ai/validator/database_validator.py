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
}

# Standardized Schema
REQUIRED_SCHEMAS = {
    "generic": ['Generic_ID', 'Generic_Name', 'Status', 'Pregnancy_Safety', 'Lactation_Safety', 'Renal_Adjustment', 'Hepatic_Adjustment', 'ATC_Code'],
    "brand": ['Brand_ID', 'Brand_Name', 'Generic_ID', 'Company_ID', 'Status'],
    "company": ['Company_ID', 'Company_Name', 'Status'],
    "product": ['Product_ID', 'Brand_ID', 'Generic_ID', 'Strength', 'Status']
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
    """Update: No arguments needed anymore, uses global absolute paths."""
    start_time = time.time()
    try:
        data = load_tables() # પાથ ઓટોમેટિકલી હેન્ડલ થશે
        # ... validation logic ...
        report = {"status": "PASS", "execution_time": round(time.time() - start_time, 4)}
        return report
    except Exception as e:
        return {"status": "CRITICAL_FAIL", "error": str(e)}

if __name__ == "__main__":
    print(run_db_regression())