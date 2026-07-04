import pandas as pd
import os

def migrate_data():
    # 1. ફાઈલો લોડ કરો
    input_file = "Product List_4_7_2026 @ 8_20_15.csv"
    output_file = "database/medicine/generic_master.csv"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} મળતી નથી.")
        return

    df_source = pd.read_csv(input_file)
    
    # 2. નવા સ્ટ્રક્ચર મુજબ ખાલી DataFrame બનાવો
    # તમારા જૂના master ફોર્મેટ મુજબની કોલમ્સ
    columns = [
        'Generic_ID', 'Generic_Name', 'Secondary_Name/Ingredients', 'Combination_Class', 
        'Therapeutic_Class', 'Pharmacological_Class', 'ATC_Code', 'Pregnancy_Safety', 
        'Lactation_Safety', 'Renal_Adjustment', 'Hepatic_Adjustment', 'Contraindications', 
        'Common_Side_Effects', 'Serious_Side_Effects', 'Status'
    ]
    
    df_new = pd.DataFrame(columns=columns)
    
    # 3. ડેટા મેપિંગ (Source -> Target)
    df_new['Generic_Name'] = df_source['Generic Name']
    df_new['Therapeutic_Class'] = df_source['Group Name']
    
    # Generic_ID જનરેટ કરો
    df_new['Generic_ID'] = ['GEN' + str(i+1).zfill(6) for i in range(len(df_source))]
    
    # બાકીની કોલમ્સ ખાલી (NaN) રહેશે જે પછીથી ભરી શકાય
    df_new['Status'] = 'Active'
    
    # 4. સેવ કરો
    df_new.to_csv(output_file, index=False)
    print(f"Migration Success! {len(df_new)} દવાઓ {output_file} માં ટ્રાન્સફર થઈ ગઈ છે.")

if __name__ == "__main__":
    migrate_data()