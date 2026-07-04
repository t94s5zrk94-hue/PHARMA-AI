import requests
import pandas as pd
import time
import os

# તમારી API કી અહીં સેટ કરો
API_KEY = "KIHP1kaOz2T430cwB0GVSj1Gir7oicZhr9sEOciw"
BASE_URL = "https://api.fda.gov/drug/label.json"
FILE_PATH = 'database/medicine/generic_master.csv'

def get_fda_data(generic_name):
    """OpenFDA API માંથી ડેટા ફેચ કરો"""
    params = {
        'api_key': API_KEY,
        'search': f'openfda.generic_name:"{generic_name}"',
        'limit': 1
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()['results'][0]
        return None
    except Exception as e:
        return None

# 1. ફાઈલ લોડ કરો
df = pd.read_csv(FILE_PATH)

# 2. કઈ કોલમ્સ અપડેટ કરવી છે તેનું લિસ્ટ
target_columns = {
    'Pregnancy_Safety': 'pregnancy',
    'Lactation_Safety': 'lactation',
    'Contraindications': 'contraindications',
    'Common_Side_Effects': 'adverse_reactions'
}

print("ડેટાબેઝ અપડેટ કરવાનું શરૂ થઈ રહ્યું છે...")

# 3. દરેક રો ચેક કરો
for index, row in df.iterrows():
    # ચેક કરો કે કોઈ પણ ટાર્ગેટ કોલમ ખાલી (NaN) છે કે કેમ
    needs_update = any(pd.isna(row.get(col)) or str(row.get(col)).lower() == 'unknown' for col in target_columns.keys())
    
    if needs_update:
        print(f"[{index+1}/{len(df)}] Updating: {row['Generic_Name']}...")
        fda_result = get_fda_data(row['Generic_Name'])
        
        if fda_result:
            for csv_col, fda_key in target_columns.items():
                if pd.isna(row[csv_col]) or str(row[csv_col]).lower() == 'unknown':
                    # API માંથી ડેટા મેળવો (જો ઉપલબ્ધ હોય)
                    data = fda_result.get(fda_key, ["Not Found"])[0] if isinstance(fda_result.get(fda_key), list) else fda_result.get(fda_key, "Not Found")
                    df.at[index, csv_col] = data
            
            # API પર વધુ લોડ ન આવે તે માટે વિરામ
            time.sleep(1.1) 
        else:
            print("  -> ડેટા મળ્યો નથી (Skipping).")

# 4. ફાઈલ સેવ કરો
df.to_csv(FILE_PATH, index=False)
print("પ્રોસેસ પૂર્ણ! બધી ખાલી કોલમ્સ અપડેટ થઈ ગઈ છે.")