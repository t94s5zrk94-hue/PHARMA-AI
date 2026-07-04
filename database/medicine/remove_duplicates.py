import pandas as pd
import os

def clean_master_file():
    file_path = "database/medicine/generic_master.csv"
    
    if not os.path.exists(file_path):
        print("ફાઈલ મળી નથી!")
        return

    # ફાઈલ લોડ કરો
    df = pd.read_csv(file_path)
    original_count = len(df)
    
    # Generic_ID ના આધારે ડુપ્લીકેટ્સ દૂર કરો
    df = df.drop_duplicates(subset=['Generic_ID'], keep='first')
    
    new_count = len(df)
    
    if original_count > new_count:
        df.to_csv(file_path, index=False)
        print(f"સફાઈ સફળ! {original_count - new_count} ડુપ્લીકેટ રેકોર્ડ્સ દૂર કર્યા.")
        print(f"હવે કુલ {new_count} યુનિક રેકોર્ડ્સ છે.")
    else:
        print("કોઈ ડુપ્લીકેટ મળ્યા નથી, ડેટા એકદમ ક્લીન છે!")

if __name__ == "__main__":
    clean_master_file()