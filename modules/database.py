import pandas as pd
import os
import logging

# Logger setup
logger = logging.getLogger(__name__)

# પ્રોજેક્ટ રૂટ અને ડેટાબેઝ ડિરેક્ટરી સેટઅપ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")

class PharmaDatabase:
    def __init__(self):
        """
        માસ્ટર ફાઈલો લોડ કરવા માટેનું કન્સ્ટ્રક્ટર.
        તમામ માસ્ટર ફાઈલો 'database/medicine/' ફોલ્ડરમાંથી લોડ થશે.
        """
        medicine_dir = os.path.join(DATABASE_DIR, "medicine")
        
        try:
            self.brand = pd.read_csv(os.path.join(medicine_dir, "brand_master.csv"))
            self.generic = pd.read_csv(os.path.join(medicine_dir, "generic_master.csv"))
            self.company = pd.read_csv(os.path.join(medicine_dir, "company_master.csv"))
            self.product = pd.read_csv(os.path.join(medicine_dir, "product_master.csv"))
            logger.info("Database loaded successfully from medicine directory.")
        except Exception as e:
            logger.error(f"Error loading database files: {e}")
            raise

    def get_brand_details(self, brand_id):
        """Brand_ID દ્વારા માહિતી મેળવો."""
        return self.brand[self.brand['Brand_ID'] == brand_id]

    def get_generic_details(self, generic_id):
        """Generic_ID દ્વારા માહિતી મેળવો."""
        return self.generic[self.generic['Generic_ID'] == generic_id]

    def get_product_by_brand(self, brand_id):
        """Brand_ID દ્વારા પ્રોડક્ટ માહિતી મેળવો."""
        return self.product[self.product['Brand_ID'] == brand_id]

    def get_complete_medicine(self, medicine_name):
        """
        બ્રાન્ડ અથવા જેનરિક માસ્ટરમાંથી નામ દ્વારા મેડિસિન શોધે છે.
        """
        # બ્રાન્ડમાં શોધો (Brand_Name કોલમ ધારીને)
        brand_match = self.brand[self.brand['Brand_Name'].str.contains(medicine_name, case=False, na=False)]
        if not brand_match.empty:
            return brand_match.iloc[0].to_dict()
        
        # Generic માં શોધો (Generic_Name કોલમ ધારીને)
        generic_match = self.generic[self.generic['Generic_Name'].str.contains(medicine_name, case=False, na=False)]
        if not generic_match.empty:
            return generic_match.iloc[0].to_dict()
            
        return None