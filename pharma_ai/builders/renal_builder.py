import logging
from pathlib import Path

import pandas as pd

from pharma_ai.builders.clinical_base_builder import ClinicalBaseBuilder
from pharma_ai.builders.id_generator import get_next_renal_id

class RenalBuilder(ClinicalBaseBuilder):    
    """
    Phase 15.7
    Renal Dose Adjustment Builder
    """
    INPUT_FILE = "pharma_ai/database/input/renal_input.csv"

    OUTPUT_FILE = (
        "pharma_ai/database/clinical/"
        "renal/renal_master.csv"
    )

    ID_PREFIX = "REN"

    MASTER_KEY = "Renal_ID"

    DUPLICATE_COLUMNS = [
        "Generic_Name",
        "Renal_Category",
    ]

    MERGE_COLUMNS = [
        "Generic_ID",
        "Renal_Category",
    ]
    REQUIRED_COLUMNS = [
        "Generic_Name",
        "Renal_Category",
        "eGFR_Min",
        "eGFR_Max",
        "Dose_Recommendation",
        "Clinical_Note",
        "Dialysis",
        "Evidence_Level",
        "Primary_Reference",
        "Status",
    ]

    VALID_RENAL_CATEGORY = {
        "Mild",
        "Moderate",
        "Severe",
        "ESRD",
    }

    VALID_DIALYSIS = {
        "Yes",
        "No",
    }

    VALID_EVIDENCE = {
        "High",
        "Moderate",
        "Low",
    }

    VALID_STATUS = {
        "Active",
        "Inactive",
    }

    
    def _validate_business_rules(self):

        self.logger.info("Validating business rules...")

        if not self.df["Renal_Category"].isin(
            self.VALID_RENAL_CATEGORY
        ).all():
            raise ValueError("Invalid Renal_Category found.")

        if not self.df["Dialysis"].isin(
            self.VALID_DIALYSIS
        ).all():
            raise ValueError("Invalid Dialysis value found.")

        if not self.df["Evidence_Level"].isin(
            self.VALID_EVIDENCE
        ).all():
            raise ValueError("Invalid Evidence_Level found.")

        if not self.df["Status"].isin(
            self.VALID_STATUS
        ).all():
            raise ValueError("Invalid Status found.")

        invalid_egfr = self.df[
            self.df["eGFR_Min"] > self.df["eGFR_Max"]
        ]

        if not invalid_egfr.empty:
            raise ValueError(
                "eGFR_Min cannot be greater than eGFR_Max."
            )

        self.logger.info("Business rule validation passed.")

    
    def _load_existing_master(self):

        self.logger.info("Loading existing master...")

        if self.master_file.exists():

            self.master_df = pd.read_csv(
                self.master_file
            )

            self.logger.info(
                "Existing master loaded (%d records).",
                len(self.master_df),
            )

        else:

            self.master_df = pd.DataFrame()

            self.logger.info(
                "Master file not found. New master will be created."
            )

        self.logger.info("Loading Generic Master...")

        self.generic_df = pd.read_csv(
            self.generic_master_file
        )

        self.logger.info(
            "Loaded %d generic records.",
            len(self.generic_df),
        )
    def _generate_ids(self):

        self.logger.info("Generating Renal IDs...")

        # Generic_Name -> Generic_ID Mapping
        generic_map = dict(
            zip(
                self.generic_df["Generic_Name"],
                self.generic_df["Generic_ID"],
            )
        )

        self.df["Generic_ID"] = self.df["Generic_Name"].map(generic_map)

        missing_generic = self.df[
            self.df["Generic_ID"].isna()
        ]

        if not missing_generic.empty:
            raise ValueError(
                "Generic not found in generic_master.csv:\n"
                f"{missing_generic[['Generic_Name']]}"
            )

       # Get last generated ID
        last_id = None

        if not self.master_df.empty:
            last_id = self.master_df.iloc[-1]["Renal_ID"]

        # Generate new IDs
        self.df.insert(
            0,
            "Renal_ID",
            get_next_renal_id(
                last_id=last_id,
                count=len(self.df),
            ),
        )

        # Generic_Name હવે Master માં નહીં રાખીએ
        self.df.drop(columns=["Generic_Name"], inplace=True)

        self.logger.info("Renal IDs generated successfully.")


    def _merge_master(self):

        self.logger.info("Merging master data...")

        if self.master_df.empty:

            final_df = self.df.copy()

        else:

            final_df = pd.concat(
                [self.master_df, self.df],
                ignore_index=True,
            )

            final_df.drop_duplicates(
                subset=["Generic_ID", "Renal_Category"],
                keep="last",
                inplace=True,
            )

        final_df.to_csv(
            self.master_file,
            index=False,
        )

        self.logger.info(
            "Renal master saved successfully (%d records).",
            len(final_df),
        )

    def build(self):

        self.logger.info(
            "=" * 60
        )
        self.logger.info(
            "Starting Renal Builder..."
        )

        self._load_input()
        self._validate_schema()
        self._validate_business_rules()
        self._validate_duplicates()
        self._load_existing_master()
        self._generate_ids()
        self._add_metadata()
        self._merge_master()

        self.logger.info(
            "Renal Builder completed successfully."
        )

    @staticmethod
    def main():

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
        )

        builder = RenalBuilder()
        builder.build()


if __name__ == "__main__":
    RenalBuilder.main()    