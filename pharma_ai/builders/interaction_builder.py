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

from pharma_ai.builders.clinical_base_builder import ClinicalBaseBuilder
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

class InteractionBuilder(ClinicalBaseBuilder):

    INPUT_FILE = INPUT_FILE

    OUTPUT_FILE = OUTPUT_FILE

    REQUIRED_COLUMNS = REQUIRED_COLUMNS

    OUTPUT_COLUMNS = OUTPUT_COLUMNS

    ID_PREFIX = "INT"

    MASTER_KEY = "Interaction_ID"

    DUPLICATE_COLUMNS = [
        "Generic_A",
        "Generic_B",
    ]

    MERGE_COLUMNS = [
        "Generic_A",
        "Generic_B",
    ]
    
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
    
    def pre_process(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize interaction pairs before validation.
        """

        self.logger.info("Normalizing interaction pairs...")

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

        return df


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    builder = InteractionBuilder()

    summary = builder.build()

    print("\n=== Interaction Builder Summary ===")
    print(summary)