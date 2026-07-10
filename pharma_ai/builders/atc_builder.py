from __future__ import annotations
import re
import time
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import get_next_atc_id
from pharma_ai.core.constants import BUILDER_VERSION

logger = logging.getLogger(__name__)

class ATCBuilder(BaseBuilder):
    """
    Production-ready builder for ATC Master.
    Handles validation, ID generation, and metadata for ATC records.
    """

    REQUIRED_COLUMNS = [
        "ATC_Code", "ATC_Name", "Level_1_Code", "Level_1_Name",
        "Level_2_Code", "Level_2_Name", "Level_3_Code", "Level_3_Name",
        "Level_4_Code", "Level_4_Name", "Level_5_Code", "Level_5_Name",
        "WHO_Version", "Status",
    ]
    ATC_REGEX = re.compile(r"^[A-Z][0-9]{2}[A-Z]{2}[0-9]{2}$")

    OUTPUT_COLUMNS = [
        "ATC_ID", "ATC_Code", "ATC_Name", "Level_1_Code", "Level_1_Name",
        "Level_2_Code", "Level_2_Name", "Level_3_Code", "Level_3_Name",
        "Level_4_Code", "Level_4_Name", "Level_5_Code", "Level_5_Name",
        "WHO_Version", "Status", "created_at", "updated_at", "version",
    ]

    def __init__(self):
        super().__init__(
            input_file="pharma_ai/database/input/atc_input.csv",
            output_path="pharma_ai/database/atc/atc_master.csv",
            required_columns=self.REQUIRED_COLUMNS,
)

    def build(self) -> dict: 
        start_time = time.time()

        logger.info("Starting ATC Builder...")

    # Step 1
        self.validate_input()

    # Step 2
        new_df = self.load_csv()

    # Step 3
        self.validate_columns(new_df)
    # Step 4
        new_df = self._validate_business_rules(new_df)

    # Step 5
        new_df = self._validate_duplicates(new_df)

    # Step 6
        master_df = pd.DataFrame(columns=self.OUTPUT_COLUMNS)
    # Step 7
        new_df = self._generate_ids(new_df, master_df)

    # Step 8
        new_df = self._add_metadata(new_df)

    # Step 9
        final_df = self._merge_master(master_df, new_df)

        duplicates_removed = len(master_df) + len(new_df) - len(final_df)

    # Step 10
        final_df = final_df[self.OUTPUT_COLUMNS]

    # Step 11
        self.save_csv(final_df)

        logger.info("ATC Builder completed successfully.")

        return self.get_summary(
        start_time,
        len(new_df),        
        len(final_df),        
        duplicates_removed,
        0,
        0,
        "SUCCESS",
    )

    def get_last_id(self, column_name: str) -> str:
        """Helper to retrieve the last existing ID for sequence continuation."""
        if self.master_df is not None and not self.master_df.empty:
            return str(self.master_df[column_name].iloc[-1])
        return ""
    
    def _validate_business_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate ATC business rules.
        """

        logger.info("Validating ATC business rules...")

    # Remove leading/trailing spaces
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Required values
        if df[self.REQUIRED_COLUMNS].isnull().any().any():
            raise ValueError("Required fields contain empty values.")

    # Status validation
        valid_status = {"Active", "Inactive"}

        invalid = df[~df["Status"].isin(valid_status)]

        if not invalid.empty:
           raise ValueError("Invalid Status found.")

        logger.info("Business validation completed.")

        return df
    
    def _validate_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate duplicate ATC records within the input file.
        """

        logger.info("Checking duplicate ATC records...")

        if df["ATC_Code"].duplicated().any():
            raise ValueError("Duplicate ATC_Code found in input.")

        if df["ATC_Name"].str.lower().duplicated().any():
            raise ValueError("Duplicate ATC_Name found in input.")

        logger.info("Duplicate validation passed.")

        return df

    def _load_master(self) -> pd.DataFrame:
        """
        Load existing ATC master if available.
        """
        if self.output_path.exists():
            logger.info("Loading existing ATC master...")
            return pd.read_csv(self.output_path, dtype=str)

        logger.info("No existing ATC master found. Creating new master.")
        return pd.DataFrame(columns=self.OUTPUT_COLUMNS)

    def _generate_ids(
        self,
        df: pd.DataFrame,
        master_df: pd.DataFrame,
        ) -> pd.DataFrame:
        """
        Generate sequential ATC IDs.
        """

        logger.info("Generating ATC IDs...")

        if master_df.empty:
            last_id = None
        else:
            last_id = master_df["ATC_ID"].iloc[-1]

        df["ATC_ID"] = get_next_atc_id(
        last_id,
        count=len(df),
        )

        logger.info("ATC IDs generated.")

        return df
    
    def _add_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add metadata only to newly created records.
        """
        logger.info("Adding metadata...")

        current_time = datetime.now().isoformat()

        df["created_at"] = current_time
        df["updated_at"] = current_time
        df["version"] = BUILDER_VERSION

        return df
    
    def _merge_master(
        self,
        master_df: pd.DataFrame,
        new_df: pd.DataFrame,
        subset_cols: list[str] = ["ATC_Code"]    ) -> pd.DataFrame:
        """
        Merge new ATC records into existing master, ensuring no duplicates.
        """
        logger.info("Merging ATC master...")

        if master_df.empty:
            return new_df.drop_duplicates(subset=subset_cols)

    # 1. Concatenate
        final_df = pd.concat([master_df, new_df], ignore_index=True)

    # 2. Remove duplicates, keeping the latest entry if applicable
    # We use 'last' to ensure new data overwrites old data if there's a conflict
        final_df = final_df.drop_duplicates(subset=subset_cols, keep='last')

        logger.info(
        f"Existing={len(master_df)} | "
        f"New={len(new_df)} | "
        f"Final={len(final_df)} | "
        f"Duplicates removed={len(master_df) + len(new_df) - len(final_df)}"
        )

        return final_df
    
if __name__ == "__main__":
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
    )

        builder = ATCBuilder()
        summary = builder.build()

        print("\n=== ATC Builder Summary ===")
        print(summary)