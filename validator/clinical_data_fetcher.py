import os
import requests
import pandas as pd
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Logger setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Security: .env ફાઈલને સાચા પાથથી લોડ કરો (રૂટ ફોલ્ડરમાંથી)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
API_KEY = os.getenv("OPENFDA_API_KEY")
BASE_URL = "https://api.fda.gov/drug/label.json"

def clean_drug_name(name):
    """દવાના નામમાંથી Strength અને Form દૂર કરીને માત્ર મુખ્ય Generic નામ મેળવે છે."""
    return str(name).split(' ')[0]

def fetch_fda_data(drug_name):
    """API થી ડેટા ફેચ કરવાનું ફંક્શન."""
    if not API_KEY: return None
    params = {'api_key': API_KEY, 'search': f'openfda.generic_name:"{drug_name.strip()}"', 'limit': 1}
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        results = response.json().get('results', [])
        return results[0] if results else None
    except requests.RequestException as e:
        logger.error(f"API Error for {drug_name}: {e}")
        return "ERROR"

def main():
    if not API_KEY:
        logger.error("OPENFDA_API_KEY not configured in .env file.")
        return

    try:
        df = pd.read_csv('database/medicine/generic_master.csv')
        
        # FIX: બધી ક્લિનિકલ કોલમ્સને string ફોર્મેટમાં કન્વર્ટ કરો જેથી TypeError ન આવે
        clinical_cols = ['Pregnancy_Safety', 'Lactation_Safety', 'Renal_Adjustment', 
                         'Hepatic_Adjustment', 'Common_Side_Effects', 'Contraindications',
                         'Data_Source', 'Last_Updated']
        
        for col in clinical_cols:
            if col not in df.columns:
                df[col] = 'Unknown'
            df[col] = df[col].astype(str)
                
    except FileNotFoundError:
        logger.error("Database file not found at database/medicine/generic_master.csv")
        return

    stats = {"updated": 0, "errors": 0, "not_found": 0, "skipped": 0}
    logger.info("Clinical Enrichment Engine શરૂ થઈ રહ્યું છે...")

    for index, row in df.iterrows():
        # Status check: જો ડેટા પહેલેથી ભરેલો હોય તો સ્કીપ કરો
        if row.get('Pregnancy_Safety') != 'Unknown' and row.get('Pregnancy_Safety') != 'nan':
            stats["skipped"] += 1
            continue

        raw_name = str(row['Generic_Name'])
        drug_name = clean_drug_name(raw_name) 
        
        logger.info(f"Searching for: {drug_name} (Original: {raw_name})")
        data = fetch_fda_data(drug_name)
        
        if data == "ERROR":
            stats["errors"] += 1
        elif data:
            df.at[index, 'Pregnancy_Safety'] = data.get('pregnancy', ['Unknown'])[0][:50]
            df.at[index, 'Lactation_Safety'] = data.get('nursing_mothers', ['Unknown'])[0][:50]
            df.at[index, 'Renal_Adjustment'] = data.get('renal_impairment', ['Unknown'])[0][:50]
            df.at[index, 'Hepatic_Adjustment'] = data.get('hepatic_impairment', ['Unknown'])[0][:50]
            df.at[index, 'Common_Side_Effects'] = data.get('adverse_reactions', ['Unknown'])[0][:100]
            df.at[index, 'Contraindications'] = data.get('contraindications', ['Unknown'])[0][:100]
            
            df.at[index, 'Data_Source'] = 'OpenFDA'
            df.at[index, 'Last_Updated'] = datetime.now().strftime("%Y-%m-%d")
            
            stats["updated"] += 1
            logger.info(f"✓ Updated: {drug_name}")
        else:
            stats["not_found"] += 1
            
        time.sleep(1)

    # Final Save
    df.to_csv('database/medicine/generic_master.csv', index=False)
    
    # Summary Report
    print("\n==================================")
    print("      Clinical Fetch Report       ")
    print("==================================")
    print(f"Total Updated : {stats['updated']}")
    print(f"Not Found     : {stats['not_found']}")
    print(f"API Errors    : {stats['errors']}")
    print(f"Skipped       : {stats['skipped']}")
    print("==================================")

if __name__ == "__main__":
    main()