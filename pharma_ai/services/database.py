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
        clinical_dir = os.path.join(DATABASE_DIR, "clinical")
        interaction_dir = os.path.join(clinical_dir, "interaction")
        contraindication_dir = os.path.join(clinical_dir, "contraindication")
        warning_dir = os.path.join(clinical_dir, "warning")
        side_effect_dir = os.path.join(clinical_dir, "side_effect")
        pregnancy_dir = os.path.join(clinical_dir, "pregnancy")
        lactation_dir = os.path.join(clinical_dir, "lactation")
        renal_dir = os.path.join(clinical_dir, "renal")
        hepatic_dir = os.path.join(clinical_dir, "hepatic") 
        monitoring_dir = os.path.join(clinical_dir, "monitoring")
        evidence_dir = os.path.join(clinical_dir, "evidence")

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
            self.interaction = self._load_csv(
                                os.path.join(interaction_dir, "interaction_master.csv"),
                                ["Interaction_ID","Generic_A", "Generic_B", ],)
            self.contraindication = self._load_csv(
                                os.path.join(contraindication_dir, "contraindication_master.csv"),
                                ["Contraindication_ID","Generic_Name",],)
            self.warning = self._load_csv(
                                os.path.join(warning_dir, "warning_master.csv"),
                                ["Warning_ID","Generic_Name",],)
            self.side_effect = self._load_csv(
                                os.path.join(side_effect_dir, "side_effect_master.csv"),
                                ["SideEffect_ID","Generic_Name",],)
            self.pregnancy = self._load_csv(
                                os.path.join(pregnancy_dir, "pregnancy_master.csv"),
                                ["Pregnancy_ID","Generic_Name",],)
            self.lactation = self._load_csv(
                                os.path.join(lactation_dir, "lactation_master.csv"),
                                ["Lactation_ID","Generic_Name",],)
            self.renal = self._load_csv(
                                os.path.join(renal_dir, "renal_master.csv"),
                                ["Renal_ID","Generic_ID",],)
            self.hepatic = self._load_csv(
                                os.path.join(hepatic_dir, "hepatic_master.csv"),
                                ["Hepatic_ID","Generic_ID", ],)
            self.monitoring = self._load_csv(
                                os.path.join(monitoring_dir, "monitoring_master.csv"),
                                ["Monitoring_ID","Generic_ID",],)
            self.evidence = self._load_csv(
                                os.path.join(evidence_dir, "evidence_master.csv"),
                                ["Evidence_ID","Generic_ID",],)
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
    
    def get_interactions(self) -> pd.DataFrame:
        """Returns Interaction master data."""
        return self.interaction.copy()
 
    def get_contraindications(self) -> pd.DataFrame:
        """Returns Contraindication master data."""
        return self.contraindication.copy()
  
    def get_warnings(self) -> pd.DataFrame:
        """Returns Warning master data."""
        return self.warning.copy()
    
    def get_side_effects(self) -> pd.DataFrame:
        """Returns Side Effect master data."""
        return self.side_effect.copy()
    
    def get_pregnancy(self) -> pd.DataFrame:
        """Returns Pregnancy master data."""
        return self.pregnancy.copy()


    def get_lactation(self) -> pd.DataFrame:
        """Returns Lactation master data."""
        return self.lactation.copy()


    def get_renal(self) -> pd.DataFrame:
        """Returns Renal master data."""
        return self.renal.copy()


    def get_hepatic(self) -> pd.DataFrame:
        """Returns Hepatic master data."""
        return self.hepatic.copy()
    
    def get_monitoring(self) -> pd.DataFrame:
        """Returns Monitoring master data."""
        return self.monitoring.copy()


    def get_evidence(self) -> pd.DataFrame:
        """Returns Evidence master data."""
        return self.evidence.copy()
    
    def get_interactions_by_generic(self, generic_name: str) -> pd.DataFrame:
        """Returns interactions for a generic medicine."""
        return self.interaction[
            (self.interaction["Generic_A"] == generic_name) |
            (self.interaction["Generic_B"] == generic_name)
        ].copy()


    def get_contraindications_by_generic(self, generic_name: str) -> pd.DataFrame:
        """Returns contraindications for a generic medicine."""
        return self.contraindication[
            self.contraindication["Generic_Name"] == generic_name
        ].copy()


    def get_warnings_by_generic(self, generic_name: str) -> pd.DataFrame:
        """Returns warnings for a generic medicine."""
        return self.warning[
            self.warning["Generic_Name"] == generic_name
        ].copy()


    def get_side_effects_by_generic(self, generic_name: str) -> pd.DataFrame:
        """Returns side effects for a generic medicine."""
        return self.side_effect[
            self.side_effect["Generic_Name"] == generic_name
        ].copy()
    
    def get_pregnancy_by_generic(self, generic_name: str) -> pd.DataFrame:
        """Returns pregnancy information for a generic medicine."""
        return self.pregnancy[
            self.pregnancy["Generic_Name"] == generic_name
        ].copy()    
    
    def get_lactation_by_generic(self, generic_name: str) -> pd.DataFrame:
        """Returns lactation information for a generic medicine."""
        return self.lactation[
            self.lactation["Generic_Name"] == generic_name
        ].copy()
    
    def get_renal_by_generic(self, generic_id: str) -> pd.DataFrame:
        """Returns renal information for a generic medicine."""
        return self.renal[
            self.renal["Generic_ID"] == generic_id
        ].copy()
    
    def get_hepatic_by_generic(self, generic_id: str) -> pd.DataFrame:
        """Returns hepatic information for a generic medicine."""
        return self.hepatic[
            self.hepatic["Generic_ID"] == generic_id
        ].copy()
    
    def get_monitoring_by_generic(self, generic_id: str) -> pd.DataFrame:
        """Returns monitoring information for a generic medicine."""
        return self.monitoring[
            self.monitoring["Generic_ID"] == generic_id
        ].copy()
    
    def get_evidence_by_generic(self, generic_id: str) -> pd.DataFrame:
        """Returns evidence information for a generic medicine."""
        return self.evidence[
            self.evidence["Generic_ID"] == generic_id
        ].copy()


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
            # Clinical Data
            # -----------------------------
            generic_name = generic_row.iloc[0]["Generic_Name"]
            generic_id = generic_row.iloc[0]["Generic_ID"]

            interaction_data = self.get_interactions_by_generic(generic_name)
            contraindication_data = self.get_contraindications_by_generic(generic_name)
            print(f"DEBUG Contra: '{generic_name}' -> {len(contraindication_data)} records")
            warning_data = self.get_warnings_by_generic(generic_name)
            side_effect_data = self.get_side_effects_by_generic(generic_name)    
            pregnancy_data = self.get_pregnancy_by_generic(generic_name)
            lactation_data = self.get_lactation_by_generic(generic_name)
            renal_data = self.get_renal_by_generic(generic_id)
            hepatic_data = self.get_hepatic_by_generic(generic_id)
            monitoring_data = self.get_monitoring_by_generic(generic_id)
            evidence_data = self.get_evidence_by_generic(generic_id)

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
                "interaction": interaction_data.to_dict("records"),

                "contraindication": contraindication_data.to_dict("records"),

                "warning": warning_data.to_dict("records"),

                "side_effect": side_effect_data.to_dict("records"),
                "pregnancy": pregnancy_data.to_dict("records"),

                "lactation": lactation_data.to_dict("records"),

                "renal": renal_data.to_dict("records"),

                "hepatic": hepatic_data.to_dict("records"),

                "monitoring": monitoring_data.to_dict("records"),

                "evidence": evidence_data.to_dict("records"),
            }

        except Exception as e:
            logger.error(
                f"Error in get_complete_medicine for {medicine_name}: {e}"
            )
            return None