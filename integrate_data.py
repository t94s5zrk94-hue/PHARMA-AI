import pandas as pd

# ૧. ફાઈલો લોડ કરો
product_list = pd.read_csv('Product List_4_7_2026 @ 8_20_15.csv')
generic_master = pd.read_csv('database/medicine/generic_master.csv')

# ૨. Data Cleaning: Generic Name ના આધારે મેપિંગ માટે
# આપણે Generic Name માંથી માત્ર મુખ્ય નામ લઈશું જેથી મેચિંગ સરળ રહે
product_list['Match_Key'] = product_list['Generic Name'].str.split().str[0].str.lower()
generic_master['Match_Key'] = generic_master['Generic_Name'].str.split().str[0].str.lower()

# ૩. મર્જ (Join) કરો
final_df = pd.merge(
    product_list, 
    generic_master[['Match_Key', 'Pregnancy_Safety', 'Lactation_Safety', 'Renal_Adjustment', 'Hepatic_Adjustment', 'Contraindications']], 
    on='Match_Key', 
    how='left'
)

# ૪. ફાઈલ સેવ કરો
final_df.drop(columns=['Match_Key'], inplace=True)
final_df.to_csv('final_product_inventory.csv', index=False)

print("સફળતા! 'final_product_inventory.csv' તૈયાર છે જેમાં ક્લિનિકલ ડેટા પણ છે.")