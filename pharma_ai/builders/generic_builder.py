import time
import datetime
import pandas as pd
from pathlib import Path
from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.services.normalization import NormalizationEngine
from pharma_ai.services.combination_parser import CombinationParser
# ID Generator માં સુધારો: હવે તે file path લેશે અને છેલ્લો ID parse કરશે
from pharma_ai.builders.id_generator import get_next_generic_id 

class GenericBuilder(BaseBuilder):
    VERSION = "1.0"
    VALID_TYPES = ["Single", "Combination", "Device", "Vaccine", "Biological", "Herbal"]
    VALID_STATUS = ["Active", "Inactive"]

    def __init__(self, input_file: str, output_path: str):
        required_cols = ["Generic_Name", "Generic_Type", "Ingredients", "Catalog_Source", "Clinical_Source", "Status"]
        super().__init__(input_file, output_path, required_cols)
        # BaseBuilder ના output_path પરથી જ Master File નો Path derive કરો
        self.master_path = self.output_path
        self.normalizer = NormalizationEngine()
        self.parser = CombinationParser()

    def validate_business_rules(self, df: pd.DataFrame):
        print(df.columns.tolist())
        print(self.required_columns)
        """Perform robust business validation."""
        # 1. Clean strings and handle whitespace-only values
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
        
        # 2. Check for empty strings
        if (df[self.required_columns] == "").any().any():
            raise ValueError("Required fields contain empty values.")

        # 3. Status and Type Validation
        if not df['Status'].isin(self.VALID_STATUS).all():
            raise ValueError(f"Invalid Status. Allowed: {self.VALID_STATUS}")
        if not df['Generic_Type'].isin(self.VALID_TYPES).all():
            raise ValueError(f"Invalid Generic_Type. Allowed: {self.VALID_TYPES}")
           
        return df

    def build(self):
        start_time = time.time()
        
        # 1. Load and Transform Input
        self.validate_input()
        new_df = self.load_csv()
        self.validate_columns(new_df)
        new_df = self.validate_business_rules(new_df)
        
        new_df = new_df.rename(columns={"Catalog_Source": "catalog_source", "Clinical_Source": "clinical_source"})
        new_df["Standardized_Name"] = new_df["Generic_Name"].apply(
            lambda x: self.normalizer.normalize(x)["normalized_name"]
        )
        new_df["Ingredients"] = new_df["Ingredients"].apply(
            lambda x: self.parser.parse(x)
        )
        # 4. Duplicate Check (Within template)
        if new_df['Standardized_Name'].str.lower().duplicated().any():
            raise ValueError("Duplicate entries detected within input template.")

        # 3. Merge Strategy
        if self.master_path.exists():
            master_df = pd.read_csv(
                self.master_path,
                encoding="utf-8",
                dtype=str
            )
            
            # Duplicate Check against Master
            if new_df['Standardized_Name'].str.lower().isin(master_df['Standardized_Name'].str.lower()).any():
                raise ValueError("Some records already exist in the master database.")
            
            # Correct ID Generation using last ID parse
            last_id = master_df['Generic_ID'].iloc[-1] if not master_df.empty else None
            new_df['Generic_ID'] = get_next_generic_id(last_id, count=len(new_df))
            
            # Concat
            final_df = pd.concat([master_df, new_df], ignore_index=True)
            self.logger.info(f"Merging: Existing={len(master_df)}, New={len(new_df)}, Final={len(final_df)}")
        else:
            new_df['Generic_ID'] = get_next_generic_id(None, count=len(new_df))
            final_df = new_df
        
        # 4. Correct Metadata Assignment
        curr_time = datetime.datetime.now().isoformat()
        final_df["created_at"] = curr_time
        final_df["updated_at"] = curr_time
        final_df["version"] = self.VERSION
        
        # 5. Schema Ordering
        schema_order = [
            "Generic_ID", "Generic_Name", "Standardized_Name", "Generic_Type", "Ingredients",
            "created_at", "updated_at", "catalog_source", "clinical_source", "version", "Status"
        ]
        final_df = final_df[schema_order]
        
        # 6. Save
        self.save_csv(final_df)
        return self.get_summary(start_time, len(new_df), len(final_df), 0, 0, 0, "SUCCESS")