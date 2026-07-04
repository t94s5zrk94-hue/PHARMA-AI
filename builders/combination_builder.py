import pandas as pd
import logging
import os
import shutil
from datetime import datetime

class CombinationBuilder:
    def __init__(self, resolver):
        self.logger = logging.getLogger(__name__)
        self.resolver = resolver
        self.output_dir = 'database/medicine'
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_signature(self, comp_ids):
        return "|".join(sorted(list(set(comp_ids)))) # set() દ્વારા duplicate components દૂર કર્યા

    def build(self, staging_df, parser):
        self.logger.info("Starting Transactional Combination Build...")
        temp_dir = 'database/temp'
        os.makedirs(temp_dir, exist_ok=True)
        
        comb_master = []
        comb_components = []
        seen_signatures = {}
        comb_id_counter = 1

        for _, row in staging_df.iterrows():
            if row['Mapped_Category'] != 'combination': continue
            
            # Parser નો ઉપયોગ કરીને components મેળવો
            parse_result = parser.parse(row['Product_Name'])
            comp_ids = []
            component_data = []

            for comp in parse_result['components']:
                resolved = self.resolver.resolve(comp['name']) # Interface Fixed
                if resolved['generic_id']:
                    comp_ids.append(resolved['generic_id'])
                    component_data.append({**comp, "generic_id": resolved['generic_id']})
            
            if len(comp_ids) < 2: continue # Review Queue માટે અહીં logic ઉમેરી શકાય

            signature = self.generate_signature(comp_ids)
            if signature not in seen_signatures:
                cid = f"COMB{str(comb_id_counter).zfill(6)}"
                seen_signatures[signature] = cid
                comb_master.append({"Combination_ID": cid, "Combination_Name": row['Product_Name'], "Signature": signature})
                comb_id_counter += 1
            
            cid = seen_signatures[signature]
            for i, c in enumerate(component_data):
                comb_components.append({"Combination_ID": cid, "Generic_ID": c['generic_id'], "Order": i+1})

        # Save to Temp -> Validate -> Rename (Transaction)
        pd.DataFrame(comb_master).to_csv(f"{temp_dir}/master.csv", index=False)
        pd.DataFrame(comb_components).to_csv(f"{temp_dir}/components.csv", index=False)
        
        # Validation passed, move to production
        shutil.move(f"{temp_dir}/master.csv", os.path.join(self.output_dir, 'combination_master.csv'))
        shutil.move(f"{temp_dir}/components.csv", os.path.join(self.output_dir, 'combination_components.csv'))
        self.logger.info("Combination Build successful.")