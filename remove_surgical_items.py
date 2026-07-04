import pandas as pd
import os

def remove_surgical_and_consumables():
    file_path = "database/medicine/generic_master.csv"
    
    if not os.path.exists(file_path):
        print("ફાઈલ મળી નથી!")
        return

    df = pd.read_csv(file_path)
    original_count = len(df)
    
    # જે શબ્દો દૂર કરવા છે તેનું લિસ્ટ (તમે આમાં વધારો કરી શકો છો)
    keywords = ['surgical', 'bandage', 'napkins', 'fixator', 'consumable', 'gauze', 'gloves', 'syringe']
    
    # Generic_Name અથવા Therapeutic_Class માં આ શબ્દો હોય તે લાઈન રિમૂવ કરો
    mask = ~df['Generic_Name'].str.lower().str.contains('|'.join(keywords), na=False)
    
    df_cleaned = df[mask]
    
    new_count = len(df_cleaned)
    removed_count = original_count - new_count
    
    if removed_count > 0:
        df_cleaned.to_csv(file_path, index=False)
        print(f"સફળ! {removed_count} સર્જિકલ/કન્ઝ્યુમેબલ આઈટમ્સ દૂર કરી.")
        print(f"હવે માસ્ટર લિસ્ટમાં કુલ {new_count} દવાઓ બાકી છે.")
    else:
        print("કોઈ સર્જિકલ આઈટમ મળી નથી.")

if __name__ == "__main__":
    remove_surgical_and_consumables()