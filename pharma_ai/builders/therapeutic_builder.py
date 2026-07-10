from __future__ import annotations

import logging
import pandas as pd
from datetime import datetime

from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import get_next_therapeutic_id
from pharma_ai.core.constants import BUILDER_VERSION

logger = logging.getLogger(__name__)


class TherapeuticBuilder(BaseBuilder):
    """
    Production-ready builder for Therapeutic Class Master.
    """
    REQUIRED_COLUMNS = [
        "Therapeutic_Class_Name",
        "Description",
        "WHO_Reference",
        "Status",
    ]

    OUTPUT_COLUMNS = [
        "Therapeutic_Class_ID",
        "Therapeutic_Class_Name",
        "Description",
        "WHO_Reference",
        "Status",
        "created_at",
        "updated_at",
        "version",
    ]

    def __init__(self):
        super().__init__(
            input_file="pharma_ai/database/input/therapeutic_input.csv",
            output_path="pharma_ai/database/therapeutic/therapeutic_master.csv",
            required_columns=self.REQUIRED_COLUMNS,
        )

    def build(self) -> dict:
        """
        Build Therapeutic Master.
        """

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

        # Step 10
        final_df = final_df[self.OUTPUT_COLUMNS]

        # Step 11
        self.save_csv(final_df)

        return {}

    def _validate_business_rules(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate Therapeutic business rules.
        """

        logger.info("Validating Therapeutic business rules...")

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
        Validate duplicate Therapeutic Class records within the input file.
        """

        logger.info("Checking duplicate Therapeutic Class records...")

        if df["Therapeutic_Class_Name"].str.lower().duplicated().any():
            raise ValueError(
                "Duplicate Therapeutic_Class_Name found in input."
            )

        logger.info("Duplicate validation passed.")

        return df

    def _load_master(self) -> pd.DataFrame:
        """
        Load existing Therapeutic master if available.
        """

        if self.output_path.exists():
            logger.info("Loading existing Therapeutic master...")
            return pd.read_csv(self.output_path, dtype=str)

        logger.info("No existing Therapeutic master found. Creating new master.")
        return pd.DataFrame(columns=self.OUTPUT_COLUMNS)

    def _generate_ids(
        self,
        df: pd.DataFrame,
        master_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate sequential Therapeutic Class IDs.
        """

        logger.info("Generating Therapeutic Class IDs...")

        # Production Rebuild Mode
        # Always generate fresh IDs starting from THR000001
        last_id = None

        df["Therapeutic_Class_ID"] = get_next_therapeutic_id(
            last_id,
            count=len(df),
        )

        logger.info("Therapeutic Class IDs generated.")

        return df

    def _add_metadata(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Add metadata to newly created Therapeutic Class records.
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
        subset_cols: list[str] = ["Therapeutic_Class_Name"],
    ) -> pd.DataFrame:
        """
        Merge Therapeutic master records.

        In Production Rebuild mode, the existing master is ignored and
        the newly generated master is returned after removing duplicates.
        """

        logger.info("Merging Therapeutic master...")

        return new_df.drop_duplicates(
            subset=subset_cols,
            keep="first",
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    builder = TherapeuticBuilder()
    summary = builder.build()

    print("\n=== Therapeutic Builder Summary ===")
    print(summary)