import pandas as pd
import os

# ૧. ફાઈલ લોડ કરો
input_file = 'Product List_4_7_2026 @ 8_20_15.csv'
df = pd.read_csv(input_file)

# ૨. ડેટા મેપિંગ (Schema Mapping)
# નોંધ: આપણી પાસે અત્યારે Generic_ID છે, Brand/Company આઈડી આપણે ડિફોલ્ટ સેટ કરીશું
product_df = pd.DataFrame({
    'Product_ID': ['PROD' + str(i).zfill(6) for i in range(1, len(df) + 1)],
    'Brand_ID': 'BRD' + df['Drug Code'].astype(str).str.zfill(6), # Generic Code પરથી મેપિંગ
    'Generic_ID': 'GEN' + df['Drug Code'].astype(str).str.zfill(6),
    'Company_ID': 'COMP000001', # ડિફોલ્ટ કંપની ID
    'Strength': 'Standard',      # ફાઈલમાંથી એક્સટ્રેક્ટ કરી શકાય (હાલ ડિફોલ્ટ)
    'Unit_Size': df['Unit Size'],
    'MRP': df['MRP'],
    'Status': 'Active'
})

# ૩. સેવ કરો
os.makedirs('database/medicine', exist_ok=True)
product_df.to_csv('database/medicine/product_master.csv', index=False)

print("સફળતા! 'database/medicine/product_master.csv' ફાઈલ તૈયાર છે.")