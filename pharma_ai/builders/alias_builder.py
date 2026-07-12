"""
Alias Builder

Builds the production Alias Master database from
alias_input.csv.

Phase 18 – Smart Search Engine
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from pharma_ai.builders.clinical_base_builder import ClinicalBaseBuilder

LOGGER = logging.getLogger(__name__)

INPUT_FILE = Path(
    "pharma_ai/database/search/alias_input.csv"
)

OUTPUT_FILE = Path(
    "pharma_ai/database/search/alias_master.csv"
)

REQUIRED_COLUMNS = [
    "Alias",
    "Generic_Name",
    "Alias_Type",
    "Priority",
    "Status",
]

OUTPUT_COLUMNS = [
    "Alias_ID",
    "Alias",
    "Generic_Name",
    "Alias_Type",
    "Priority",
    "Status",
    "created_at",
    "updated_at",
    "source",
    "version",
]
class AliasBuilder(ClinicalBaseBuilder):

    INPUT_FILE = INPUT_FILE

    OUTPUT_FILE = OUTPUT_FILE

    REQUIRED_COLUMNS = REQUIRED_COLUMNS

    OUTPUT_COLUMNS = OUTPUT_COLUMNS

    ID_PREFIX = "ALS"

    MASTER_KEY = "Alias_ID"

    DUPLICATE_COLUMNS = [
        "Alias",
    ]

    MERGE_COLUMNS = [
        "Alias",
    ]
    def pre_process(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize alias records before validation.
        """

        self.logger.info("Normalizing alias records...")

        df = df.copy()

        df["Alias"] = (
            df["Alias"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        df["Generic_Name"] = (
            df["Generic_Name"]
            .astype(str)
            .str.strip()
        )

        df["Alias_Type"] = (
            df["Alias_Type"]
            .astype(str)
            .str.strip()
        )

        df["Priority"] = (
            df["Priority"]
            .astype(str)
            .str.strip()
        )

        df["Status"] = (
            df["Status"]
            .astype(str)
            .str.strip()
        )

        return df
    
    def _validate_business_rules(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate alias business rules.
        """

        self.logger.info(
            "Validating alias business rules..."
        )

        # Required values
        if df[self.REQUIRED_COLUMNS].isnull().any().any():
            raise ValueError(
                "Required fields contain empty values."
            )

        # Alias cannot be empty
        if (df["Alias"] == "").any():
            raise ValueError(
                "Alias cannot be empty."
            )

        # Generic cannot be empty
        if (df["Generic_Name"] == "").any():
            raise ValueError(
                "Generic_Name cannot be empty."
            )

        # Alias Type validation
        valid_types = {
            "Generic",
            "Brand",
            "Abbreviation",
            "Short_Name",
            "Synonym",
        }

        invalid = df[
            ~df["Alias_Type"].isin(valid_types)
        ]

        if not invalid.empty:
            raise ValueError(
                "Invalid Alias_Type found."
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
if __name__ == "__main__":

    builder = AliasBuilder()

    summary = builder.build()

    print("\n=== Alias Builder Summary ===")
    print(summary)    