import pandas as pd
import logging
import json
import os
import time
from datetime import datetime
from pharma_ai.services.normalization import NormalizationEngine
from services.combination_parser import CombinationParser
from services.generic_resolver import GenericResolver
from builders.combination_builder import CombinationBuilder
from services.validation_gate import ValidationGate

class PharmaPipeline:
    def __init__(self):
        # 1. Directory Setup
        for d in ["logs", "reports", "database/medicine", "database/raw"]: 
            os.makedirs(d, exist_ok=True)
        
        # 2. Logging Setup
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler('logs/pipeline.log'),
                                logging.StreamHandler()
                            ])
        self.logger = logging.getLogger(__name__)
        
        # 3. Engine Initialization
        self.norm = NormalizationEngine()
        self.parser = CombinationParser()
        self.resolver = GenericResolver()
        self.builder = CombinationBuilder(self.resolver)
        self.gate = ValidationGate({"max_errors": 0, "max_review_records": 100, "min_success_rate": 80.0})
        
        self.stats = {"input": 0, "success": 0, "review": 0, "errors": 0}
        self.review_queue = []

    def run(self, input_file):
        start_time = time.time()
        self.logger.info(f"--- Pipeline Starting: {input_file} ---")
        
        try:
            # Force Mapping logic for raw data header
            df = pd.read_csv(input_file)
            if 'Product_Name' not in df.columns:
                if 'Generic Name' in df.columns:
                    df = df.rename(columns={'Generic Name': 'Product_Name'})
                    self.logger.info("Mapped 'Generic Name' to 'Product_Name'.")
                else:
                    raise ValueError("Column 'Product_Name' or 'Generic Name' not found in raw data.")
            
            # Rest of the pipeline...
            processed_data = []
            self.stats['input'] = len(df)
            
            for _, row in df.iterrows():
                product_name = row['Product_Name']
                # Pipeline processing continues...
                # ... (તમારો બાકીનો કોડ અહીં જેવો હતો તેવો જ રહેશે)
            
            # ... validate and build ...
            
        except Exception as e:
            self.logger.critical(f"Pipeline Fatal Error: {e}")

    # (બાકીના ફંક્શન્સ અહીં જ રાખો...)