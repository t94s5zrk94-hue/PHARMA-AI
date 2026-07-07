import pandas as pd
import os

# ૧. ફાઈલનું નામ જે તમારા ફોલ્ડરમાં છે
file_name = 'Product List_4_7_2026 @ 8_20_15.csv'

# ૨. ફાઈલનું લોકેશન મેળવો
if os.path.exists(file_name):
    input_file = file_name
    print(f"ફાઈલ મળી ગઈ: {input_file}")
else:
    print(f"ભૂલ: આ ફોલ્ડરમાં '{file_name}' નામની ફાઈલ નથી.")
    print("કૃપા કરીને ચેક કરો કે ફાઈલનું નામ બરાબર આ જ છે કે નહીં.")
    exit()

# ૩. ડેટા પ્રોસેસ કરો
df = pd.read_csv(input_file)

ready_df = pd.DataFrame({
    'Generic_ID': 'GEN' + df['Drug Code'].astype(str).str.zfill(6),
    'Generic_Name': df['Generic Name'],
    'Therapeutic_Class': df['Group Name'],
    'Pharmacological_Class': 'Unknown',
    'ATC_Code': 'A00AA00',
    'Pregnancy_Safety': 'Unknown',
    'Lactation_Safety': 'Unknown',
    'Renal_Adjustment': 'No Adjustment',
    'Hepatic_Adjustment': 'No Adjustment',
    'Contraindications': 'None',
    'Status': 'Active'
})

# ૪. ફાઈલ સેવ કરો (ડિરેક્ટરી ચેક સાથે)
os.makedirs('database/medicine', exist_ok=True)
ready_df.to_csv('database/medicine/generic_master.csv', index=False)
print("સફળતા! 'database/medicine/generic_master.csv' તૈયાર થઈ ગઈ છે.")