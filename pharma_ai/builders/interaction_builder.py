"""
Interaction Builder

Builds the production Drug Interaction Master database from
interaction_input.csv.

Phase 15.2 – Clinical Knowledge Engine
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd

from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import IDGenerator
from pharma_ai.builders.id_generator import (get_next_interaction_id,)

# =============================================================================
# Configuration
# =============================================================================

LOGGER = logging.getLogger(__name__)

INPUT_FILE = Path(
    "pharma_ai/database/input/interaction_input.csv"
)

OUTPUT_FILE = Path(
    "pharma_ai/database/clinical/interaction/interaction_master.csv"
)

REQUIRED_COLUMNS = [
    "Generic_A",
    "Generic_B",
    "Severity",
    "Mechanism",
    "Clinical_Effect",
    "Management",
    "Evidence_Level",
    "Primary_Reference",
    "Status",
]

OUTPUT_COLUMNS = [
    "Interaction_ID",
    "Generic_A",
    "Generic_B",
    "Severity",
    "Mechanism",
    "Clinical_Effect",
    "Management",
    "Evidence_Level",
    "Primary_Reference",
    "Status",
    "created_at",
    "updated_at",
    "version",
]

# =============================================================================
# Interaction Builder
# =============================================================================

class InteractionBuilder(BaseBuilder):
    """
    Builds the production Drug Interaction Master database.
    """

    def __init__(self):
        super().__init__(
            input_file="pharma_ai/database/input/interaction_input.csv",
            output_path="pharma_ai/database/clinical/interaction/interaction_master.csv",
            required_columns=REQUIRED_COLUMNS,
        )

        self.logger.info("InteractionBuilder initialized.")

    def _load_input(self) -> pd.DataFrame:
        """
        Load the interaction input CSV.

        Returns
        -------
        pd.DataFrame
        Input interaction data.

        Raises
        ------
        FileNotFoundError
        If the input file does not exist.

        ValueError
        If the input file is empty.
        """

        LOGGER.info("Loading interaction input...")

        if not self.input_file.exists():
            raise FileNotFoundError(
                f"Input file not found: {self.input_file}"
            )

        df = pd.read_csv(self.input_file)

        if df.empty:
            raise ValueError(
                "Interaction input file is empty."
            )

        LOGGER.info("Loaded %d interaction records.", len(df))

        return df

    def _validate_schema(self, df: pd.DataFrame) -> None:
        """
        Validate the input schema.

        Parameters
        ----------
        df : pd.DataFrame
        Input interaction data.

        Raises
        ------
        ValueError
        If required columns are missing.
        """

        LOGGER.info("Validating interaction schema...")

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_columns)}"
            )

        LOGGER.info("Interaction schema validation passed.")

    def _validate_business_rules(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate interaction business rules.
        """

        self.logger.info("Validating interaction business rules...")

    # Remove leading/trailing spaces
        df = df.apply(
            lambda col: col.str.strip() if col.dtype == "object" else col
        )

    # Required values
        if df[REQUIRED_COLUMNS].isnull().any().any():
            raise ValueError(
            "Required fields contain empty values."
        )

    # Severity validation
        valid_severity = {
        "Minor",
        "Moderate",
        "Major",
        "Contraindicated",
        }

        invalid = df[
            ~df["Severity"].isin(valid_severity)
        ]

        if not invalid.empty:
            raise ValueError(
            "Invalid Severity found."
        )

    # Status validation
        valid_status = {
        "Active",
        "Inactive",
        }

        invalid = df[
            ~df["Status"].isin(valid_status)
        ]

        if not invalid.empty:
            raise ValueError(
            "Invalid Status found."
        )

        self.logger.info(
            "Business validation passed."
        )

        return df    
    
    def _validate_duplicates(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate duplicate interaction pairs.
        """
        self.logger.info("Checking duplicate interaction records...")

        duplicate_mask = df.duplicated(
            subset=["Generic_A", "Generic_B"],
            keep=False,
        )

        if duplicate_mask.any():

            duplicates = df.loc[
            duplicate_mask,
            ["Generic_A", "Generic_B"],
        ]

            raise ValueError(
                f"Duplicate interaction pairs found:\n{duplicates}"
        )

        self.logger.info(
            "Duplicate validation passed."
        )

        return df

    def _generate_ids(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate unique Interaction IDs.

        Parameters
        ----------
        df : pd.DataFrame
        Interaction dataframe.

        Returns
        -------
        pd.DataFrame
        DataFrame with Interaction_ID column.
        """

        LOGGER.info("Generating Interaction IDs...")

        df = df.copy()

        generator = IDGenerator(prefix="INT")

        df["Interaction_ID"] = [
            generator.generate()
            for _ in range(len(df))
        ]

        LOGGER.info(
            "Generated %d Interaction IDs.",
            len(df),
        )

        return df

    def _add_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add standard metadata columns.

        Parameters
        ----------
        df : pd.DataFrame
        Interaction dataframe.

        Returns
        -------
        pd.DataFrame
        DataFrame with metadata columns.
        """

        LOGGER.info("Adding metadata...")

        df = df.copy()

        timestamp = pd.Timestamp.now()

        df["created_at"] = timestamp
        df["updated_at"] = timestamp
        df["version"] = "1.0"

        LOGGER.info("Metadata added.")

        return df

    def _normalize_pairs(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize interaction pairs.

        Ensures:
        Aspirin + Warfarin
        and
        Warfarin + Aspirin

        are stored as the same interaction.
        """

        LOGGER.info("Normalizing interaction pairs...")

        df = df.copy()

        normalized = df.apply(
            lambda row: sorted(
                [
                    str(row["Generic_A"]).strip(),
                    str(row["Generic_B"]).strip(),
                ]
            ),
            axis=1,
        )

        df["Generic_A"] = normalized.str[0]
        df["Generic_B"] = normalized.str[1]

        LOGGER.info("Interaction normalization completed.")

        return df

    def _load_existing_master(
        self,
    ) -> pd.DataFrame:
        """
        Load existing Interaction Master.

        Returns
        -------
        pd.DataFrame
        Existing interaction master or an empty DataFrame.
        """

        LOGGER.info("Loading existing Interaction Master...")

        if self.output_path.exists():
            existing_df = pd.read_csv(
                self.output_path,
                dtype=str,
            )


            LOGGER.info(
                "Loaded %d existing interactions.",
                len(existing_df),
            )

            return existing_df

        LOGGER.info("No existing Interaction Master found.")

        return pd.DataFrame(
            columns=OUTPUT_COLUMNS,
        )

    def _assign_interaction_ids(
        self,
        existing_df: pd.DataFrame,
        new_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Preserve existing Interaction_ID values and assign
        IDs only to newly discovered interactions.
        """

        LOGGER.info("Assigning Interaction IDs...")

        # First build
        if existing_df.empty:
            # Assuming get_next_interaction_id is accessible via self
            new_df["Interaction_ID"] = get_next_interaction_id(
            None,
            count=len(new_df),
            )

            return new_df

        # Existing interaction keys
        existing_keys = existing_df[
            ["Generic_A", "Generic_B", "Interaction_ID"]
        ]

        merged = new_df.merge(
            existing_keys,
            on=["Generic_A", "Generic_B"],
            how="left",
        )

        # Find new interactions
        new_mask = merged["Interaction_ID"].isna()

        if not new_mask.any():
            LOGGER.info("No new interactions found.")
            return merged

        last_id = existing_df["Interaction_ID"].dropna().iloc[-1]

        new_ids = get_next_interaction_id(
            last_id,
             count=int(new_mask.sum()),
        )

        merged.loc[new_mask, "Interaction_ID"] = new_ids

        LOGGER.info(
            "Existing=%d | New=%d",
            (~new_mask).sum(),
            new_mask.sum(),
        )

        return merged

    def _merge_master(
        self,
        existing_df: pd.DataFrame,
        new_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Merge Interaction Master.

        Existing Interaction_ID values are preserved.
        Latest clinical information overwrites older data.
        """

        LOGGER.info("Merging Interaction Master...")

        if existing_df.empty:
            return new_df

        final_df = pd.concat(
            [existing_df, new_df],
            ignore_index=True,
        )

        final_df = final_df.drop_duplicates(
            subset=["Generic_A", "Generic_B"],
            keep="last",
        )

        LOGGER.info(
            "Existing=%d | New=%d | Final=%d",
            len(existing_df),
            len(new_df),
            len(final_df),
        )

        return final_df

    def build(self) -> dict:
        """
        Build the production Interaction Master.
        """

        start_time = time.time()

        LOGGER.info("Starting Interaction Builder...")

        # Step 1
        self.validate_input()

        # Step 2
        new_df = self.load_csv()

        input_count = len(new_df)

        # Step 3
        self.validate_columns(new_df)

        # Step 4
        new_df = self._validate_business_rules(new_df)

        # Step 5
        new_df = self._normalize_pairs(new_df)

        # Step 6
        new_df = self._validate_duplicates(new_df)

        # Step 7
        existing_df = self._load_existing_master()

        # Step 8
        new_df = self._assign_interaction_ids(
            existing_df,
            new_df,
        )

        # Step 9
        new_df = self._add_metadata(new_df)

        # Step 10
        final_df = self._merge_master(
            existing_df,
            new_df,
        )

        # Step 11
        final_df = final_df[OUTPUT_COLUMNS]

        self.save_csv(final_df)

        LOGGER.info(
            "Interaction Builder completed successfully."
        )

        return self.get_summary(
            start_time,
            input_count,
            len(final_df),
            0,
            0,
            0,
            "SUCCESS",
        )

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    builder = InteractionBuilder()

    summary = builder.build()

    print("\n=== Interaction Builder Summary ===")
    print(summary)