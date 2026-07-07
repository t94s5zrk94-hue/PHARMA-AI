import pandas as pd
import os

def clean_master_thoroughly():
    file_path = "database/medicine/generic_master.csv"
    
    if not os.path.exists(file_path):
        print("ફાઈલ મળી નથી!")
        return

    df = pd.read_csv(file_path)
    original_count = len(df)
    
    # જે શબ્દો દૂર કરવા છે તેનું કમ્બાઈન્ડ લિસ્ટ
    # આમાં સર્જિકલ, આયુર્વેદિક, મોસ્કીટો રિપેલન્ટ વગેરે બધું આવી જાય છે
    drop_keywords = [
        'surgical', 'bandage', 'napkins', 'fixator', 'consumable', 'gauze', 
        'gloves', 'syringe', 'ayurvedic', 'mosquito', 'repellant', 'janaushadhi'
    ]
    
    # પૂરું લિસ્ટ સ્ટ્રિંગ તરીકે
    pattern = '|'.join(drop_keywords)
    
    # 'Generic_Name' અને 'Therapeutic_Class' બંનેમાં ચેક કરો
    # જો આમાંથી કોઈ પણ કોલમમાં આ શબ્દો હોય, તો તે રો (Row) દૂર કરો
    mask = (
        df['Generic_Name'].str.lower().str.contains(pattern, na=False) | 
        df['Therapeutic_Class'].str.lower().str.contains(pattern, na=False)
    )
    
    # માસ્કને ઉલટાવો જેથી આપણે તે આઈટમ્સ રાખીએ જે આ શબ્દો ધરાવતી નથી
    df_cleaned = df[~mask]
    
    new_count = len(df_cleaned)
    removed_count = original_count - new_count
    
    if removed_count > 0:
        df_cleaned.to_csv(file_path, index=False)
        print(f"સફળ! કુલ {removed_count} બિન-જેનરિક આઈટમ્સ દૂર કરવામાં આવી.")
        print(f"માસ્ટર લિસ્ટમાં હવે શુદ્ધ {new_count} રેકોર્ડ્સ બાકી છે.")
    else:
        print("કોઈ બિન-જેનરિક આઈટમ મળી નથી, ડેટા ક્લીન છે!")

if __name__ == "__main__":
    clean_master_thoroughly()