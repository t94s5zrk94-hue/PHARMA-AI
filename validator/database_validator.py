import pandas as pd
import os
import time
import logging

# Logger setup
logger = logging.getLogger(__name__)

# Constants
FILES = {
    "generic": "database/medicine/generic_master.csv",
    "brand": "database/medicine/brand_master.csv",
    "company": "database/medicine/company_master.csv",
    "product": "database/medicine/product_master.csv"
}

# Standardized Schema
REQUIRED_SCHEMAS = {
    "generic": ['Generic_ID', 'Generic_Name', 'Status', 'Pregnancy_Safety', 'Lactation_Safety', 'Renal_Adjustment', 'Hepatic_Adjustment', 'ATC_Code'],
    "brand": ['Brand_ID', 'Brand_Name', 'Generic_ID', 'Company_ID', 'Status'],
    "company": ['Company_ID', 'Company_Name', 'Status'],
    "product": ['Product_ID', 'Brand_ID', 'Generic_ID', 'Strength', 'Status']
}

# Clinical Enums
ALLOWED_SAFETY = {"Safe", "Use with Caution", "Avoid", "Specialist Advice", "Unknown"}
ALLOWED_ADJUSTMENT = {"No Adjustment", "Dose Reduction", "Contraindicated", "Specialist Advice"}
ALLOWED_STATUS = {"Active", "Deprecated", "Draft"}

def load_tables():
    data = {}
    for key, path in FILES.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Critical Error: {path} missing.")
        data[key] = pd.read_csv(path)
    return data

def validate_data_quality(data):
    errors = {"schema": 0, "duplicates": 0, "empty": 0, "clinical": 0}
    for key, df in data.items():
        if not all(col in df.columns for col in REQUIRED_SCHEMAS[key]):
            errors["schema"] += 1
        id_col = f"{key.capitalize()}_ID" if key != "generic" else "Generic_ID"
        if df[id_col].duplicated().any():
            errors["duplicates"] += 1
        if df[REQUIRED_SCHEMAS[key]].isnull().values.any():
            errors["empty"] += 1
    
    gen_df = data['generic']
    if not (gen_df['Pregnancy_Safety'].isin(ALLOWED_SAFETY).all() and 
            gen_df['Renal_Adjustment'].isin(ALLOWED_ADJUSTMENT).all()):
        errors["clinical"] += 1
    return errors

def validate_foreign_keys(data):
    fk_errors = 0
    master_generic_ids = set(data['generic']['Generic_ID'])
    print(f"DEBUG: Master માં કુલ {len(master_generic_ids)} Unique Generic IDs છે.")
    
    # 1. Product ટેબલ ચેક
    product_ids = data['product']['Generic_ID'].unique()
    for gid in product_ids:
        if gid not in master_generic_ids:
            print(f"ભૂલ: આ Generic_ID Product માં છે પણ Master માં નથી: {gid}")
            fk_errors += 1
            
    # 2. Brand ટેબલ ચેક
    brand_ids = data['brand']['Generic_ID'].unique()
    for gid in brand_ids:
        if gid not in master_generic_ids:
            print(f"ભૂલ: આ Generic_ID Brand માં છે પણ Master માં નથી: {gid}")
            fk_errors += 1
            
    return fk_errors

def run_db_regression():
    start_time = time.time()
    try:
        data = load_tables()
        data_errors = validate_data_quality(data)
        fk_errors = validate_foreign_keys(data)
    except Exception as e:
        return {"status": "CRITICAL_FAIL", "error": str(e)}

    report = {
        "status": "PASS" if sum(data_errors.values()) + fk_errors == 0 else "FAIL",
        "rows_checked": sum(len(df) for df in data.values()),
        **data_errors,
        "fk_errors": fk_errors,
        "execution_time": round(time.time() - start_time, 4)
    }
    return report

if __name__ == "__main__":
    print(run_db_regression())