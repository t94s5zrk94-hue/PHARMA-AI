import pandas as pd
import os
import re
import logging
import time
from datetime import datetime

# ૧. Logging અને Error handling માટે સુધારાઓ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MasterBuilder:
    def __init__(self):
        self.staging_path = 'database/staging/classified_data.csv'
        self.output_dir = 'database/medicine'
        self.version = f"BUILD_{datetime.now().strftime('%Y_%m_%d')}_001"
        self.report = {"total": 0, "generic": 0, "combination": 0, "duplicates": 0, "errors": 0}
        os.makedirs(self.output_dir, exist_ok=True)

    def standardize_name(self, name):
        """વધુ મજબૂત નામ સ્ટાન્ડર્ડાઈઝેશન."""
        name = str(name).lower()
        # Dosage forms અને strength ને હટાવવાના કમ્પ્રિહેન્સિવ રૂલ્સ
        patterns = [
            r'\d+\s*(mg|g|ml|%|w/w|iu)', r'tablets?', r'capsules?', r'syrup', 
            r'injection', r'ip', r'bp', r'usp', r'dry syrup', r'oral suspension',
            r'softgel', r'drops', r'cream', r'ointment', r'gel', r'lotion', 
            r'spray', r'powder', r'plus', r'forte', r'ds', r'er', r'xr', r'mr', r'cr'
        ]
        for p in patterns:
            name = re.sub(p, '', name, flags=re.IGNORECASE)
        # Whitespace અને special characters ક્લીનઅપ
        return re.sub(r'\s+', ' ', name).strip().title()

    def validate_input(self, df):
        required = ['Product_Name', 'Mapped_Category', 'Processing_Status']
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    def generate_ids(self, df, prefix, filename):
        """સુરક્ષિત ID જનરેશન."""
        last_id = 0
        file_path = os.path.join(self.output_dir, filename)
        if os.path.exists(file_path):
            existing = pd.read_csv(file_path)
            # કોલમ નામ સુરક્ષિત રીતે શોધવું
            id_col = [c for c in existing.columns if 'ID' in c]
            if id_col:
                ids = existing[id_col[0]].str.replace(prefix, '', regex=False)
                last_id = pd.to_numeric(ids, errors='coerce').fillna(0).max()
        return [f"{prefix}{str(int(last_id) + i + 1).zfill(6)}" for i in range(len(df))]

    def build_generic_master(self, df):
        logger.info("Building Generic Master...")
        df_gen = df[df['Mapped_Category'] == 'generic'].copy()
        df_gen['Generic_Name'] = df_gen['Product_Name'].apply(self.standardize_name)
        
        before = len(df_gen)
        df_gen = df_gen.drop_duplicates(subset=['Generic_Name'])
        self.report['duplicates'] = before - len(df_gen)
        
        df_gen['Generic_ID'] = self.generate_ids(df_gen, 'GEN', 'generic_master.csv')
        
        # Schema Initialization (Blank/NaN fields)
        clinical_cols = ['Therapeutic_Class', 'Pharmacological_Class', 'ATC_Code', 'Pregnancy_Safety', 'Lactation_Safety']
        for col in clinical_cols: df_gen[col] = None
        
        df_gen.to_csv(os.path.join(self.output_dir, 'generic_master.csv'), index=False, encoding='utf-8-sig')
        self.report['generic'] = len(df_gen)
        logger.info("Generic Master built successfully.")

    def run(self):
        try:
            logger.info("Master Builder started.")
            start_time = time.time()
            df = pd.read_csv(self.staging_path)
            self.validate_input(df)
            
            self.build_generic_master(df)
            
            logger.info(f"Build complete in {time.time() - start_time:.2f} seconds.")
        except Exception as e:
            logger.exception("Build failed: %s", e)

if __name__ == "__main__":
    builder = MasterBuilder()
    builder.run()