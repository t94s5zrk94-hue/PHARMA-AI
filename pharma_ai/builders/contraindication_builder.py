"""
Contraindication Builder
Phase 15 - Clinical Knowledge Engine

Builds:
- contraindication_master.csv

Input:
- contraindication_input.csv

Output:
- contraindication_master.csv
"""

from datetime import datetime
from pathlib import Path
import time

import pandas as pd

from pharma_ai.builders.clinical_base_builder import ClinicalBaseBuilder

INPUT_FILE = (
    "pharma_ai/database/input/contraindication_input.csv"
)

OUTPUT_FILE = (
    "pharma_ai/database/clinical/"
    "contraindication/contraindication_master.csv"
)

REQUIRED_COLUMNS = [
    "Generic_Name",
    "Contraindication",
    "Severity",
    "Reason",
    "Recommendation",
    "Primary_Reference",
    "Evidence_Level",
    "Status",
]

OUTPUT_COLUMNS = [
    "Contraindication_ID",
    "Generic_Name",
    "Contraindication",
    "Severity",
    "Reason",
    "Recommendation",
    "Primary_Reference",
    "Evidence_Level",
    "Status",
    "created_at",
    "updated_at",
    "version",
]
class ContraindicationBuilder(ClinicalBaseBuilder):

    INPUT_FILE = INPUT_FILE

    OUTPUT_FILE = OUTPUT_FILE

    REQUIRED_COLUMNS = REQUIRED_COLUMNS

    OUTPUT_COLUMNS = OUTPUT_COLUMNS

    ID_PREFIX = "CON"

    MASTER_KEY = "Contraindication_ID"

    DUPLICATE_COLUMNS = [
        "Generic_Name",
        "Contraindication",
    ]

    MERGE_COLUMNS = [
        "Generic_Name",
        "Contraindication",
    ]

    def _validate_business_rules(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Validate business rules."""

        df = df.copy()

        df["Generic_Name"] = (
        df["Generic_Name"]
        .astype(str)
        .str.strip()
        )

        df["Contraindication"] = (
        df["Contraindication"]
        .astype(str)
        .str.strip()
        )

        df = df.drop_duplicates()

        print("Business validation passed.")

        return df
    

def main() -> None:
    """Run Contraindication Builder."""

    builder = ContraindicationBuilder()

    summary = builder.build()

    print("\nBuild Summary")
    print("=" * 60)

    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()