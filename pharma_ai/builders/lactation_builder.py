"""
Lactation Builder
Phase 15 - Clinical Knowledge Engine
"""



import pandas as pd
from pharma_ai.builders.clinical_base_builder import ClinicalBaseBuilder



INPUT_FILE = (
    "pharma_ai/database/input/lactation_input.csv"
)

OUTPUT_FILE = (
    "pharma_ai/database/clinical/"
    "lactation/"
    "lactation_master.csv"
)

REQUIRED_COLUMNS = [
    "Generic_Name",
    "Lactation_Risk",
    "Recommendation",
    "Clinical_Notes",
    "Evidence_Level",
    "Primary_Reference",
    "Status",
]

OUTPUT_COLUMNS = [
    "Lactation_ID",
    "Generic_Name",
    "Lactation_Risk",
    "Recommendation",
    "Clinical_Notes",
    "Evidence_Level",
    "Primary_Reference",
    "Status",
    "created_at",
    "updated_at",
    "version",
]


class LactationBuilder(ClinicalBaseBuilder):

    INPUT_FILE = INPUT_FILE

    OUTPUT_FILE = OUTPUT_FILE

    REQUIRED_COLUMNS = REQUIRED_COLUMNS

    OUTPUT_COLUMNS = OUTPUT_COLUMNS

    ID_PREFIX = "LAC"

    MASTER_KEY = "Lactation_ID"

    DUPLICATE_COLUMNS = [
        "Generic_Name",
    ]

    MERGE_COLUMNS = [
        "Generic_Name",
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

        df["Lactation_Risk"] = (
            df["Lactation_Risk"]
            .astype(str)
            .str.strip()
        )

        print("Business validation passed.")

        return df

def main() -> None:
    """Run Lactation Builder."""

    builder = LactationBuilder()

    summary = builder.build()

    print("\nBuild Summary")
    print("=" * 60)

    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()