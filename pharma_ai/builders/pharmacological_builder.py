from __future__ import annotations

import logging
import time
import pandas as pd
from datetime import datetime

from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import get_next_pharmacological_id
from pharma_ai.core.constants import BUILDER_VERSION


logger = logging.getLogger(__name__)


class PharmacologicalBuilder(BaseBuilder):
    """
    Production-ready builder for Pharmacological Class Master.
    """
    REQUIRED_COLUMNS = [
        "Pharmacological_Class_Name",
        "Description",
        "WHO_Reference",
        "Status",
    ]

    OUTPUT_COLUMNS = [
        "Pharmacological_Class_ID",
        "Pharmacological_Class_Name",
        "Description",
        "WHO_Reference",
        "Status",
        "created_at",
        "updated_at",
        "version",
    ]

    def __init__(self):
        super().__init__(
            input_file="pharma_ai/database/input/pharmacological_input.csv",
            output_path="pharma_ai/database/pharmacological/pharmacological_master.csv",
            required_columns=self.REQUIRED_COLUMNS,
        )

    def build(self) -> dict:
        start_time = time.time()

        logger.info("Starting Pharmacological Builder...")

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
        master_df = self._load_master()

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

        logger.info("Pharmacological Builder completed successfully.")

        return self.get_summary(
            start_time,
            len(new_df),
            len(final_df),
            duplicates_removed,
            0,
            0,
            "SUCCESS",
        )

    def _validate_business_rules(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate Pharmacological business rules.
        """
        logger.info("Validating Pharmacological business rules...")

        # Remove leading/trailing spaces
        df = df.apply(
            lambda col: col.str.strip() if col.dtype == "object" else col
        )

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

    def _validate_duplicates(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate duplicate Pharmacological Class records within the input file.
        """
        logger.info("Checking duplicate Pharmacological Class records...")

        if df["Pharmacological_Class_Name"].str.lower().duplicated().any():
            raise ValueError(
                "Duplicate Pharmacological_Class_Name found in input."
            )

        logger.info("Duplicate validation passed.")
        return df

    def _load_master(self) -> pd.DataFrame:
        """
        Load existing Pharmacological master if available.
        """
        if self.output_path.exists():
            logger.info("Loading existing Pharmacological master...")
            return pd.read_csv(self.output_path, dtype=str)

        logger.info("No existing Pharmacological master found. Creating new master.")
        return pd.DataFrame(columns=self.OUTPUT_COLUMNS)

    def _generate_ids(
        self,
        df: pd.DataFrame,
        master_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate sequential Pharmacological Class IDs.
        """
        logger.info("Generating Pharmacological Class IDs...")
        
        last_id = None
        df["Pharmacological_Class_ID"] = get_next_pharmacological_id(
            last_id,
            count=len(df),
        )

        logger.info("Pharmacological Class IDs generated.")
        return df

    def _add_metadata(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Add metadata to newly created Pharmacological Class records.
        """
        logger.info("Adding metadata...")

        current_time = datetime.now().isoformat()

        df["created_at"] = current_time
        df["updated_at"] = current_time
        df["version"] = BUILDER_VERSION

        logger.info("Metadata added.")
        return df

    def _merge_master(
        self,
        master_df: pd.DataFrame,
        new_df: pd.DataFrame,
        subset_cols: list[str] = ["Pharmacological_Class_Name"],
    ) -> pd.DataFrame:
        """
        Merge Pharmacological master records.
        """
        logger.info("Merging Pharmacological master...")
        return new_df.drop_duplicates(
            subset=subset_cols,
            keep="first",
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    builder = PharmacologicalBuilder()
    summary = builder.build()

    print("\n=== Pharmacological Builder Summary ===")
    print(summary)