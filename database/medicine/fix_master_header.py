import pandas as pd

# 1. માસ્ટર ફાઈલ લોડ કરો
file_path = "database/medicine/generic_master.csv"
df = pd.read_csv(file_path)

# 2. જો 'Product_Name' નથી, તો 'Generic_Name' ની કોપી કરીને 'Product_Name' બનાવો
if 'Product_Name' not in df.columns:
    df['Product_Name'] = df['Generic_Name']
    
# 3. ફાઈલ ફરીથી સેવ કરો
df.to_csv(file_path, index=False)
print("Header fixed! 'Product_Name' column added successfully.")