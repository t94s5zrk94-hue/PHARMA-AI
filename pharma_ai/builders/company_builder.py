import pandas as pd
import time
from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import get_next_company_id
from pharma_ai.services.normalization import normalize_company_name

class CompanyBuilder(BaseBuilder):
    def __init__(self, input_file, output_path):
        required_cols = ["Company_Name"]
        super().__init__(input_file, output_path, required_cols)

    def run(self):
        start_time = time.time()
        try:
            self.logger.info("Starting CompanyBuilder execution.")

            # 1. Pipeline: Load & Validation
            self.validate_input()
            df = self.load_csv()
            self.validate_business_rules(df)

            # 2. Normalize and Deduplicate
            df["Standardized_Name"] = df["Company_Name"].apply(normalize_company_name)
            df = df.drop_duplicates(subset=["Standardized_Name"])
            self.logger.info(f"Normalization: {len(df)} unique companies identified.")
            
            # 3. Merge with existing master
            master_df = self._load_existing_master()
            merged_df = self._merge_data(df, master_df)
            
            # 4. Assign IDs to New records
            final_df = self._assign_company_ids(merged_df)
            
            # 5. Save and Audit
            final_df.to_csv(self.output_path, index=False)
            self.logger.info(f"Saved company_master.csv with {len(final_df)} records.")
            
            execution_time = time.time() - start_time
            self.logger.info(f"CompanyBuilder completed in {execution_time:.2f}s.")
            
            return {
                "status": "success",
                "input_rows": len(df),
                "existing_matches": len(merged_df[merged_df['Status'] == 'Existing']),
                "new_companies": len(merged_df[merged_df['Status'] == 'New']),
                "execution_time": execution_time
            }

        except Exception as e:
            self.logger.error(f"Error in CompanyBuilder: {str(e)}")
            raise

    def validate_business_rules(self, df):
        if df["Company_Name"].isnull().any() or (df["Company_Name"].str.strip() == "").any():
            raise ValueError("Company_Name contains null or blank values.")

    def _load_existing_master(self):
        try:
            df = pd.read_csv(self.output_path)
            # Schema Validation
            required = ["Company_ID", "Company_Name", "Standardized_Name"]
            if not all(col in df.columns for col in required):
                raise ValueError("Master schema mismatch")
            
            # Duplicate Key Audit Check
            if df["Standardized_Name"].duplicated().any():
                self.logger.error("Critical: Master file contains duplicate Standardized_Name keys.")
                raise ValueError("Data corruption detected: Duplicate keys in master file.")
                
            return df
        except (FileNotFoundError, ValueError):
            return pd.DataFrame(columns=["Company_ID", "Company_Name", "Standardized_Name", "Status"])

    def _merge_data(self, new_df, master_df):
        merged = pd.merge(new_df, master_df, on="Standardized_Name", how="left", suffixes=("_new", "_master"))
        merged["Status"] = merged["Company_ID"].apply(lambda x: "Existing" if pd.notnull(x) else "New")
        merged["Company_Name"] = merged["Company_Name_master"].combine_first(merged["Company_Name_new"])
        
        self.logger.info(f"Merge: {len(merged[merged['Status'] == 'Existing'])} matched, {len(merged[merged['Status'] == 'New'])} new.")
        return merged[["Company_ID", "Company_Name", "Standardized_Name", "Status"]]

    def _assign_company_ids(self, df):
        new_mask = df["Status"] == "New"
        if new_mask.any():
            # IDGenerator ને last_id આપવા માટે numeric/lexical sorting ની જરૂર નથી, 
            # get_next_company_id તે internally સંભાળશે.
            existing_ids = df["Company_ID"].dropna()
            last_id = existing_ids.max() if not existing_ids.empty else None
            
            new_ids = get_next_company_id(last_id, count=new_mask.sum())
            df.loc[new_mask, "Company_ID"] = new_ids
            self.logger.info(f"IDs assigned: {new_mask.sum()} new IDs generated.")
        return df