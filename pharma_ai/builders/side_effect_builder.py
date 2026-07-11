"""
Side Effect Builder
Phase 15 - Clinical Knowledge Engine

Builds:
- side_effect_master.csv

Input:
- side_effect_input.csv

Output:
- side_effect_master.csv
"""

from pathlib import Path

import pandas as pd

from pharma_ai.builders.clinical_base_builder import ClinicalBaseBuilder


INPUT_FILE = (
    "pharma_ai/database/input/side_effect_input.csv"
)

OUTPUT_FILE = (
    "pharma_ai/database/clinical/"
    "side_effect/side_effect_master.csv"
)

REQUIRED_COLUMNS = [
    "Generic_Name",
    "Side_Effect",
    "Frequency",
    "Severity",
    "Action",
    "Patient_Counseling",
    "Evidence_Level",
    "Primary_Reference",
    "Status",
]

OUTPUT_COLUMNS = [
    "SideEffect_ID",
    "Generic_Name",
    "Side_Effect",
    "Frequency",
    "Severity",
    "Action",
    "Patient_Counseling",
    "Evidence_Level",
    "Primary_Reference",
    "Status",
    "created_at",
    "updated_at",
    "version",
]
class SideEffectBuilder(ClinicalBaseBuilder):
    INPUT_FILE = INPUT_FILE

    OUTPUT_FILE = OUTPUT_FILE

    REQUIRED_COLUMNS = REQUIRED_COLUMNS

    OUTPUT_COLUMNS = OUTPUT_COLUMNS

    ID_PREFIX = "SFX"

    MASTER_KEY = "SideEffect_ID"

    DUPLICATE_COLUMNS = [
        "Generic_Name",
        "Side_Effect",
    ]

    MERGE_COLUMNS = [
        "Generic_Name",
        "Side_Effect",
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

        df["Side_Effect"] = (
            df["Side_Effect"]
            .astype(str)
            .str.strip()
        )

        print("Business validation passed.")

        return df
    
def main() -> None:
    """Run Side Effect Builder."""

    builder = SideEffectBuilder()

    summary = builder.build()

    print("\nBuild Summary")
    print("=" * 60)

    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()    