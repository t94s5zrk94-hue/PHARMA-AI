import pandas as pd
import os
import time
import logging

# Logger setup (Library friendly)
logger = logging.getLogger(__name__)

# Constants
FILES = {
    "generic": "database/medicine/generic_master.csv",
    "brand": "database/medicine/brand_master.csv",
    "company": "database/medicine/company_master.csv",
    "product": "database/medicine/product_master.csv"
}

# Standardized Schema (Using Pregnancy_Safety)
REQUIRED_SCHEMAS = {
    "generic": ['Generic_ID', 'Generic_Name', 'Status', 'Pregnancy_Safety', 'Lactation_Safety', 'Renal_Adjustment', 'Hepatic_Adjustment', 'ATC_Code'],
    "brand": ['Brand_ID', 'Brand_Name', 'Generic_ID', 'Company_ID', 'Status'],
    "company": ['Company_ID', 'Company_Name', 'Status'],
    "product": ['Product_ID', 'Brand_ID', 'Strength', 'Status']
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
    """Schema, Duplicates, Nulls અને Clinical Enums ચેક કરે છે."""
    errors = {"schema": 0, "duplicates": 0, "empty": 0, "clinical": 0}
    
    for key, df in data.items():
        # Schema Check
        if not all(col in df.columns for col in REQUIRED_SCHEMAS[key]):
            errors["schema"] += 1
            
        # Duplicate Check
        id_col = f"{key.capitalize()}_ID" if key != "generic" else "Generic_ID"
        if df[id_col].duplicated().any():
            errors["duplicates"] += 1
            
        # Null Check (Required columns only)
        if df[REQUIRED_SCHEMAS[key]].isnull().values.any():
            errors["empty"] += 1
            
    # Clinical Enum Check (Generic table only)
    gen_df = data['generic']
    if not (gen_df['Pregnancy_Safety'].isin(ALLOWED_SAFETY).all() and 
            gen_df['Renal_Adjustment'].isin(ALLOWED_ADJUSTMENT).all()):
        errors["clinical"] += 1
        
    return errors

def validate_foreign_keys(data):
    errors = 0
    if not data['brand']['Generic_ID'].isin(data['generic']['Generic_ID']).all(): errors += 1
    if not data['brand']['Company_ID'].isin(data['company']['Company_ID']).all(): errors += 1
    return errors

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