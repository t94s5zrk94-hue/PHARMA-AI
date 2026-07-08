import pandas as pd
import time
from datetime import datetime
from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import get_next_brand_id
from pharma_ai.services.normalization import (
    NormalizationEngine,
    normalize_company_name
)

class BrandBuilder(BaseBuilder):
    def __init__(self, input_file, output_path):
        required_cols = ["Brand_Name", "Generic_Name", "Company_Name", "Strength", "Dosage_Form", "Status"]
        super().__init__(input_file, output_path, required_cols)
        self.normalizer = NormalizationEngine()
        self.schema = [
            "Brand_ID", "Brand_Name", "Standardized_Brand_Name", "Generic_ID", "Generic_Name", 
            "Standardized_Generic_Name", "Company_ID", "Company_Name", "Standardized_Company_Name",
            "Strength", "Dosage_Form", "Status", "Record_Status", "Catalog_Source", 
            "Clinical_Source", "created_at", "updated_at", "version"
        ]
    def run(self):
        start_time = time.time()
        self.logger.info("Starting BrandBuilder execution.")
        
        self.validate_input()
        df = self.load_csv()
        self.validate_columns(df)
        self.validate_business_rules(df)
        
        initial_count = len(df)
        df = self._normalize(df)
        df = df.drop_duplicates(subset=["Standardized_Brand_Name"])
        
        df = self._lookup_foreign_keys(df)
        df = self._merge_with_existing(df)
        df = self._assign_brand_ids(df)
        final_df = self._finalize_metadata(df)
        
        # Final Pre-Save Integrity Gate
        self._pre_save_integrity_check(final_df)
        self.save_csv(final_df[self.schema])
        
        return self.get_summary(start_time, initial_count, len(final_df), initial_count - len(df), 0, 0, "SUCCESS")
    
    def validate_business_rules(self, df):
        required = [
            "Brand_Name",
            "Generic_Name",
            "Company_Name",
            "Strength",
            "Dosage_Form",
            "Status",
        ]
        blank_mask = (
            df[required]
            .apply(lambda col: col.astype(str).str.strip())
            .eq("")
        )

        if df[required].isnull().any().any() or blank_mask.any().any():
            raise ValueError(
            "Business Rule Violation: Blank or null values found."
        )

        if not df["Status"].isin(["Active", "Inactive"]).all():
            raise ValueError(
            "Invalid Status: Only 'Active' or 'Inactive' allowed."
        )
    def _normalize(self, df):
        """
        Brand અને Generic માટે NormalizationEngine નો ઉપયોગ કરે છે,
        અને Company માટે અગાઉથી નિર્ધારિત ફંક્શન વાપરે છે.
        """
        df = df.copy()
        
        # Brand અને Generic માટે સેન્ટ્રલ નોર્મલાઇઝરનો ઉપયોગ
        df["Standardized_Brand_Name"] = df["Brand_Name"].apply(
            lambda x: self.normalizer.normalize(x)["normalized_name"]
        )

        df["Standardized_Generic_Name"] = df["Generic_Name"].apply(
            lambda x: self.normalizer.normalize(x)["normalized_name"]
        )

        # Company માટે પ્રોડક્શન-રેડી નોર્મલાઇઝરનો ઉપયોગ
        df["Standardized_Company_Name"] = df["Company_Name"].apply(
            normalize_company_name
        )

        return df    
    def _lookup_foreign_keys(self, df):
        # FIXED: Using DATABASE_CONFIG for master paths
        generic_master = pd.read_csv(
                           "pharma_ai/database/medicine/generic_master.csv",
                            dtype=str
                    )

        company_master = pd.read_csv(
                        "pharma_ai/database/medicine/company_master.csv",
                        dtype=str
                    )
        df = df.merge(generic_master[["Standardized_Name", "Generic_ID"]].rename(columns={"Standardized_Name": "Standardized_Generic_Name"}), on="Standardized_Generic_Name", how="left")
        df = df.merge(company_master[["Standardized_Name", "Company_ID"]].rename(columns={"Standardized_Name": "Standardized_Company_Name"}), on="Standardized_Company_Name", how="left")
        
        if df[["Generic_ID", "Company_ID"]].isnull().any().any():
            raise ValueError("Foreign Key Lookup Failed.")
        return df
    
    def _merge_with_existing(self, new_df):
        try:
            existing = pd.read_csv(
                        self.output_path,
                        dtype=str
            )
            if not all(col in existing.columns for col in self.schema):
                raise ValueError("Master file schema mismatch.")
        except FileNotFoundError:
            return new_df.assign(Record_Status="New", version=1)
            
        mutable_cols = ["Strength", "Dosage_Form", "Status", "Catalog_Source", "Clinical_Source"]
        merged = pd.merge(new_df, existing, on="Standardized_Brand_Name", how="left", suffixes=("_new", ""))
        
        # FIXED: Explicit Column-by-Column Comparison
        mask_changed = pd.Series(False, index=merged.index)
        for col in mutable_cols:
            mask_changed |= merged[f"{col}_new"].ne(merged[col])
        
        merged["Record_Status"] = merged["Brand_ID"].apply(lambda x: "Existing" if pd.notnull(x) else "New")
        
        for col in mutable_cols:
            merged[col] = merged[f"{col}_new"].combine_first(merged[col])
            
        merged["version"] = merged["version"].fillna(1).astype(int)
        
        # FIXED: Valid Pandas Indexing for Version Increment
        condition = (merged["Record_Status"] == "Existing") & mask_changed
        merged.loc[condition, "version"] += 1
        
        return merged    
    def _assign_brand_ids(self, df):
        """
        નવા રેકોર્ડ્સને સિક્વન્શિયલ Brand_ID અસાઇન કરે છે.
        """
        # First-run support
        if "Brand_ID" not in df.columns:
            df["Brand_ID"] = None

        if "Record_Status" not in df.columns:
            raise ValueError("Record_Status column is missing.")

        new_mask = df["Record_Status"] == "New"

        if new_mask.any():
            existing_ids = df["Brand_ID"].dropna()
            last_id = existing_ids.max() if not existing_ids.empty else None

            df.loc[new_mask, "Brand_ID"] = get_next_brand_id(
                last_id,
                count=new_mask.sum()
            )

            self.logger.info(f"Assigned {new_mask.sum()} new Brand_ID(s).")

        return df
    
    def _finalize_metadata(self, df):
        now = datetime.now().isoformat()

        if "created_at" not in df.columns:
            df["created_at"] = now
        else:
            df["created_at"] = df["created_at"].fillna(now)
        
        df["updated_at"] = now

        if "version" not in df.columns:
            df["version"] = 1
        return df
    
    def _pre_save_integrity_check(self, df):
        if df["Brand_ID"].duplicated().any(): raise ValueError("Integrity Gate: Duplicate Brand_ID found.")
        if df["Standardized_Brand_Name"].isnull().any(): raise ValueError("Integrity Gate: Missing Brand Name.")
        if df[["Generic_ID", "Company_ID"]].isnull().any().any(): raise ValueError("Integrity Gate: FK violation.")

if __name__ == "__main__":

        builder = BrandBuilder(
            input_file="pharma_ai/database/import_templates/brand_import_template.csv",
            output_path="pharma_ai/database/medicine/brand_master.csv"
        )
        summary = builder.run()
        print(summary)

   