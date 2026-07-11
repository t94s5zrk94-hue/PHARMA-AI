"""
Warning Builder
Phase 15 - Clinical Knowledge Engine

Builds:
- warning_master.csv

Input:
- warning_input.csv

Output:
- warning_master.csv
"""

import pandas as pd

from pharma_ai.builders.clinical_base_builder import ClinicalBaseBuilder

INPUT_FILE = (
    "pharma_ai/database/input/warning_input.csv"
)

OUTPUT_FILE = (
    "pharma_ai/database/clinical/"
    "warning/warning_master.csv"
)

REQUIRED_COLUMNS = [
    "Generic_Name",
    "Warning",
    "Severity",
    "Reason",
    "Recommendation",
    "Primary_Reference",
    "Evidence_Level",
    "Status",
]

OUTPUT_COLUMNS = [
    "Warning_ID",
    "Generic_Name",
    "Warning",
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
class WarningBuilder(ClinicalBaseBuilder):
    INPUT_FILE = INPUT_FILE

    OUTPUT_FILE = OUTPUT_FILE

    REQUIRED_COLUMNS = REQUIRED_COLUMNS

    OUTPUT_COLUMNS = OUTPUT_COLUMNS

    ID_PREFIX = "WRN"

    MASTER_KEY = "Warning_ID"

    DUPLICATE_COLUMNS = [
        "Generic_Name",
        "Warning",
    ]

    MERGE_COLUMNS = [
        "Generic_Name",
        "Warning",
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

        df["Warning"] = (
            df["Warning"]
            .astype(str)
            .str.strip()
        )

        df = df.drop_duplicates()

        print("Business validation passed.")

        return df    

    
def main() -> None:
    """Run Warning Builder."""

    builder = WarningBuilder()

    summary = builder.build()

    print("\nBuild Summary")
    print("=" * 60)

    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()    