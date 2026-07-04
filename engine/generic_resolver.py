import pandas as pd
import logging
import os

class GenericResolver:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.master_path = 'database/medicine/generic_master.csv'
        self.lookup = self._load_master(self.master_path)

    def _load_master(self, path):
        try:
            if not os.path.exists(path):
                self.logger.error(f"Master file not found: {path}")
                return pd.DataFrame(columns=['Product_Name'])

            # ફાઈલ લોડ કરો
            df = pd.read_csv(path)
            
            # સૌથી મહત્વનો સુધારો: જો Generic_Name હોય તો તેને Product_Name બનાવી દો
            if 'Generic_Name' in df.columns:
                df = df.rename(columns={'Generic_Name': 'Product_Name'})
            
            # ખાતરી કરો કે 'Product_Name' કોલમ અસ્તિત્વમાં છે
            if 'Product_Name' not in df.columns:
                self.logger.error("Master file does not contain 'Generic_Name' or 'Product_Name' column.")
                return pd.DataFrame(columns=['Product_Name'])

            # ડુપ્લીકેટ્સ દૂર કરો
            df = df.drop_duplicates(subset=['Product_Name'], keep='first')
            
            return df
        except Exception as e:
            self.logger.error(f"Error loading master data: {e}")
            return pd.DataFrame(columns=['Product_Name'])

    def resolve(self, name):
        # સિમ્પલ લુકઅપ લોજિક
        if self.lookup.empty:
            return {}
            
        result = self.lookup[self.lookup['Product_Name'].str.lower() == name.lower()]
        if not result.empty:
            return result.iloc[0].to_dict()
        return {}