import pandas as pd
import os

def fix_master_header():
    file_path = "database/medicine/generic_master.csv"
    
    if not os.path.exists(file_path):
        print(f"Error: ફાઈલ {file_path} મળી નથી!")
        return

    # 1. માસ્ટર ફાઈલ લોડ કરો
    df = pd.read_csv(file_path)

    # 2. જો 'Product_Name' કોલમ નથી, તો તે બનાવો
    if 'Product_Name' not in df.columns:
        if 'Generic_Name' in df.columns:
            df['Product_Name'] = df['Generic_Name']
            print("સફળ! 'Product_Name' કોલમ ઉમેરવામાં આવી છે.")
        else:
            print("Error: ફાઈલમાં 'Generic_Name' કોલમ પણ નથી!")
            return
    else:
        print("માહિતી: 'Product_Name' કોલમ પહેલેથી જ અસ્તિત્વમાં છે.")
        
    # 3. ફાઈલ ફરીથી સેવ કરો
    df.to_csv(file_path, index=False)
    print("તમારી માસ્ટર ફાઈલ હવે પાઈપલાઈન માટે તૈયાર છે.")

if __name__ == "__main__":
    fix_master_header()