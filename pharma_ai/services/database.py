import pandas as pd
import os
import logging
from typing import Any, Optional

# Logger setup
logger = logging.getLogger(__name__)

# Dynamic path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")

class PharmaDatabase:
    """
    Centralized database service providing clean, read-only access to 
    medicine master data.
    """

    def __init__(self) -> None:
        """Loads master CSV files into memory with schema validation."""
        medicine_dir = os.path.join(DATABASE_DIR, "medicine")
        product_dir = os.path.join(DATABASE_DIR, "product")

        try:
            self.brand = self._load_csv(os.path.join(medicine_dir, "brand_master.csv"), 
                                        ["Brand_ID", "Brand_Name", "Generic_ID", "Company_ID"])
            self.generic = self._load_csv(os.path.join(medicine_dir, "generic_master.csv"), 
                                          ["Generic_ID", "Generic_Name"])
            self.company = self._load_csv(os.path.join(medicine_dir, "company_master.csv"), 
                                          ["Company_ID", "Company_Name"])
            self.product = self._load_csv(os.path.join(product_dir, "product_master.csv"), 
                                          ["Product_ID", "Generic_ID"])
            atc_dir = os.path.join(DATABASE_DIR, "atc") 
            self.atc = self._load_csv(os.path.join(atc_dir, "atc_master.csv"),
                                      ["ATC_ID", "ATC_Code", "ATC_Name"])  
            self.generic_atc_mapping = self._load_csv(
                                     os.path.join(DATABASE_DIR, "mapping", "generic_atc_mapping.csv"),
                                     ["Generic_ID", "ATC_ID"])
            self.generic_class_mapping = self._load_csv(
                                     os.path.join(DATABASE_DIR, "mapping", "generic_class_mapping.csv"),
                                    ["Generic_ID","Therapeutic_Class_ID","Pharmacological_Class_ID",],)
            self.therapeutic = self._load_csv(
                                     os.path.join(DATABASE_DIR, "therapeutic", "therapeutic_master.csv"),
                                     ["Therapeutic_Class_ID", "Therapeutic_Class_Name"],)
            self.pharmacological = self._load_csv(
                                    os.path.join(DATABASE_DIR, "pharmacological", "pharmacological_master.csv"),
                                    ["Pharmacological_Class_ID", "Pharmacological_Class_Name"],)
            
            logger.info("Database loaded successfully.")
        except Exception as e:
            logger.error(f"Critical error loading database files: {e}")
            raise

    def _load_csv(self, path: str, required_columns: list[str]) -> pd.DataFrame:
        """Loads CSV and validates schema."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Database file not found: {path}")
        
        df = pd.read_csv(path)
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing column '{col}' in {os.path.basename(path)}")
        return df

    # --- Backward Compatible Methods ---
    def get_brand_details(self, brand_id: Any) -> pd.DataFrame:
        return self.brand[self.brand['Brand_ID'] == brand_id]

    def get_generic_details(self, generic_id: Any) -> pd.DataFrame:
        return self.generic[self.generic['Generic_ID'] == generic_id]

    def get_product_by_brand(self, brand_id: Any) -> pd.DataFrame:
        """Lookup by Generic_ID derived from Brand_ID."""
        brand_row = self.get_brand(brand_id)
        if brand_row:
            return self.product[self.product['Generic_ID'] == brand_row['Generic_ID']]
        return pd.DataFrame()

    # --- New Repository-Ready Methods ---
    def get_brand(self, brand_id: Any) -> Optional[dict[str, Any]]:
        row = self.brand[self.brand["Brand_ID"] == brand_id]
        return row.iloc[0].to_dict() if not row.empty else None

    def get_generic(self, generic_id: Any) -> Optional[dict[str, Any]]:
        row = self.generic[self.generic["Generic_ID"] == generic_id]
        return row.iloc[0].to_dict() if not row.empty else None

    def get_company(self, company_id: Any) -> Optional[dict[str, Any]]:
        row = self.company[self.company["Company_ID"] == company_id]
        return row.iloc[0].to_dict() if not row.empty else None

    def get_product(self, product_id: Any) -> Optional[dict[str, Any]]:
        row = self.product[self.product["Product_ID"] == product_id]
        return row.iloc[0].to_dict() if not row.empty else None

    # --- Core Pipeline Method ---
    def get_complete_medicine(self, medicine_name: str) -> Optional[dict[str, Any]]:
        """Retrieves comprehensive data by brand or generic name."""
        try:
            # -----------------------------
            # Brand Search
            # -----------------------------
            brand_match = self.brand[
                self.brand["Brand_Name"].str.contains(
                    medicine_name,
                    case=False,
                    na=False,
                )
            ]

            if not brand_match.empty:
                brand_row = brand_match.iloc[0]
            else:
                # -----------------------------
                # Generic Search
                # -----------------------------
                generic_match = self.generic[
                    self.generic["Generic_Name"].str.contains(
                        medicine_name,
                        case=False,
                        na=False,
                    )
                ]

                if generic_match.empty:
                    return None

                generic_row = generic_match.iloc[0]

                brand_match = self.brand[
                    self.brand["Generic_ID"] == generic_row["Generic_ID"]
                ]

                if brand_match.empty:
                    return None

                brand_row = brand_match.iloc[0]

            # -----------------------------
            # Related Master Records
            # -----------------------------
            generic_row = self.generic[
                self.generic["Generic_ID"] == brand_row["Generic_ID"]
            ]

            company_row = self.company[
                self.company["Company_ID"] == brand_row["Company_ID"]
            ]

            product_row = self.product[
                self.product["Generic_ID"] == brand_row["Generic_ID"]
            ]

            # -----------------------------
            # ATC Mapping
            # -----------------------------
            mapping_row = self.generic_atc_mapping[
                self.generic_atc_mapping["Generic_ID"] == brand_row["Generic_ID"]
            ]

            if not mapping_row.empty:
                atc_row = self.atc[
                    self.atc["ATC_ID"] == mapping_row.iloc[0]["ATC_ID"]
                ]
            else:
                atc_row = pd.DataFrame()

            # -----------------------------
            # Therapeutic & Pharmacological Mapping
            # -----------------------------
            class_mapping_row = self.generic_class_mapping[
                self.generic_class_mapping["Generic_ID"] == brand_row["Generic_ID"]
            ]

            if not class_mapping_row.empty:
                therapeutic_row = self.therapeutic[
                    self.therapeutic["Therapeutic_Class_ID"]
                    == class_mapping_row.iloc[0]["Therapeutic_Class_ID"]
                ]

                pharmacological_row = self.pharmacological[
                    self.pharmacological["Pharmacological_Class_ID"]
                    == class_mapping_row.iloc[0]["Pharmacological_Class_ID"]
                ]
            else:
                therapeutic_row = pd.DataFrame()
                pharmacological_row = pd.DataFrame()

            # -----------------------------
            # Final Response
            # -----------------------------
            return {
                "brand": brand_row.to_dict(),
                "generic": (
                    generic_row.iloc[0].to_dict()
                    if not generic_row.empty
                    else {}
                ),
                "company": (
                    company_row.iloc[0].to_dict()
                    if not company_row.empty
                    else {}
                ),
                "product": (
                    product_row.iloc[0].to_dict()
                    if not product_row.empty
                    else {}
                ),
                "atc": (
                    atc_row.iloc[0].to_dict()
                    if not atc_row.empty
                    else {}
                ),
                "therapeutic": (
                    therapeutic_row.iloc[0].to_dict()
                    if not therapeutic_row.empty
                    else {}
                ),
                "pharmacological": (
                    pharmacological_row.iloc[0].to_dict()
                    if not pharmacological_row.empty
                    else {}
                ),
            }

        except Exception as e:
            logger.error(
                f"Error in get_complete_medicine for {medicine_name}: {e}"
            )
            return None