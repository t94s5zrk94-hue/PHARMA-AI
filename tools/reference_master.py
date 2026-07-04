import pandas as pd
import uuid
import os
import logging
from datetime import datetime

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def initialize_reference_master():
    metadata_dir = 'database/metadata'
    os.makedirs(metadata_dir, exist_ok=True)
    ref_path = os.path.join(metadata_dir, 'reference_master.csv')
    
    try:
        df_generic = pd.read_csv('database/medicine/generic_master.csv')
    except FileNotFoundError:
        logger.error("Generic Master not found!")
        return {"new_records": 0, "total_records": 0}

    # Load existing or create new
    if os.path.exists(ref_path):
        df_ref = pd.read_csv(ref_path)
    else:
        df_ref = pd.DataFrame(columns=[
            'Reference_ID', 'Generic_ID', 'Clinical_Field', 'Source', 
            'Version', 'Last_Reviewed', 'Reviewer', 'Confidence', 'Notes'
        ])

    clinical_fields = [
        'Pregnancy_Safety', 'Lactation_Safety', 'Renal_Adjustment', 
        'Hepatic_Adjustment', 'Contraindications', 'Common_Side_Effects'
    ]

    new_records_count = 0
    updated_records_count = 0

    for _, row in df_generic.iterrows():
        g_id = row['Generic_ID']
        
        for field in clinical_fields:
            value = row.get(field)
            if pd.notna(value) and str(value).strip() not in ['Unknown', 'nan', '']:
                
                # Check for existing
                mask = (df_ref['Generic_ID'] == g_id) & (df_ref['Clinical_Field'] == field)
                
                if mask.any():
                    # Update Existing Record
                    idx = df_ref.index[mask][0]
                    df_ref.at[idx, 'Last_Reviewed'] = datetime.now().strftime("%Y-%m-%d")
                    df_ref.at[idx, 'Source'] = row.get('Data_Source', 'OpenFDA')
                    updated_records_count += 1
                else:
                    # Create New Record
                    new_rec = {
                        'Reference_ID': f"REF-{uuid.uuid4().hex[:8].upper()}",
                        'Generic_ID': g_id,
                        'Clinical_Field': field,
                        'Source': row.get('Data_Source', 'OpenFDA'),
                        'Version': 'v1',
                        'Last_Reviewed': datetime.now().strftime("%Y-%m-%d"),
                        'Reviewer': 'AI',
                        'Confidence': 'Medium',
                        'Notes': ''
                    }
                    df_ref = pd.concat([df_ref, pd.DataFrame([new_rec])], ignore_index=True)
                    new_records_count += 1

    df_ref.to_csv(ref_path, index=False)
    logger.info(f"Process Complete: {new_records_count} new, {updated_records_count} updated.")
    
    return {"new_records": new_records_count, "total_records": len(df_ref)}

if __name__ == "__main__":
    initialize_reference_master()