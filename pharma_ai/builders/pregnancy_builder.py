"""
Pregnancy Builder
Phase 15 - Clinical Knowledge Engine
"""

from datetime import datetime
from pathlib import Path
import time

import pandas as pd

from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import (
    get_next_pregnancy_id,
)

INPUT_FILE = (
    "pharma_ai/database/input/pregnancy_input.csv"
)

OUTPUT_FILE = (
    "pharma_ai/database/clinical/"
    "pregnancy/"
    "pregnancy_master.csv"
)

REQUIRED_COLUMNS = [
    "Generic_Name",
    "Pregnancy_Risk",
    "Trimester",
    "Recommendation",
    "Clinical_Notes",
    "Evidence_Level",
    "Primary_Reference",
    "Status",
]

OUTPUT_COLUMNS = [
    "Pregnancy_ID",
    "Generic_Name",
    "Pregnancy_Risk",
    "Trimester",
    "Recommendation",
    "Clinical_Notes",
    "Evidence_Level",
    "Primary_Reference",
    "Status",
    "created_at",
    "updated_at",
    "version",
]


class PregnancyBuilder(BaseBuilder):
    """Production Pregnancy Builder."""

    def __init__(self):

        super().__init__(
            input_file=INPUT_FILE,
            output_path=OUTPUT_FILE,
            required_columns=REQUIRED_COLUMNS,
        )
    def _load_input(self) -> pd.DataFrame:
        """Load pregnancy input."""

        df = self.load_csv()

        print(f"Loaded {len(df)} input records.")

        return df


    def _validate_schema(
        self,
        df: pd.DataFrame,
    ) -> None:
        """Validate schema."""

        self.validate_columns(df)

        print("Schema validation passed.")


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

        df["Pregnancy_Risk"] = (
            df["Pregnancy_Risk"]
            .astype(str)
            .str.strip()
        )

        df = df.drop_duplicates()

        print("Business validation passed.")

        return df


    def _validate_duplicates(
            self,
            df: pd.DataFrame,
        ) -> pd.DataFrame:
            """Remove duplicate pregnancy records."""

            before = len(df)

            df = df.drop_duplicates(
                subset=[
                    "Generic_Name",
                    "Trimester",
                ]
            )

            removed = before - len(df)

            print(
                f"Duplicate records removed: {removed}"
            )

            return df  
    def _load_existing_master(
        self,
    ) -> pd.DataFrame:
        """Load existing pregnancy master."""

        output_path = Path(OUTPUT_FILE)

        if output_path.exists():

            print("Loading existing pregnancy master...")

            return pd.read_csv(output_path)

        print("No existing pregnancy master found.")

        return pd.DataFrame(columns=OUTPUT_COLUMNS)


    def _generate_ids(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Generate Pregnancy IDs."""

        master_df = self._load_existing_master()

        if master_df.empty:
            last_id = None
        else:
            last_id = master_df["Pregnancy_ID"].iloc[-1]

        ids = get_next_pregnancy_id(
            last_id,
            len(df),
        )

        df.insert(
            0,
            "Pregnancy_ID",
            ids,
        )

        print("Pregnancy IDs generated.")

        return df


    def _add_metadata(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Add metadata."""

        timestamp = datetime.now().isoformat()

        df["created_at"] = timestamp
        df["updated_at"] = timestamp
        df["version"] = "1.0"

        print("Metadata added.")

        return df   
    def _merge_master(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Merge with existing pregnancy master."""

        master_df = self._load_existing_master()

        final_df = pd.concat(
            [
                master_df,
                df,
            ],
            ignore_index=True,
        )

        final_df = final_df.drop_duplicates(
            subset=[
                "Generic_Name",
                "Trimester",
            ],
            keep="first",
        )

        final_df = final_df[
            OUTPUT_COLUMNS
        ]

        print(
            f"Master contains {len(final_df)} records."
        )

        return final_df
    def build(self) -> dict:
        """Build pregnancy master."""

        start_time = time.time()

        print("\nStarting Pregnancy Builder...")

        df = self._load_input()

        input_records = len(df)

        self._validate_schema(df)

        df = self._validate_business_rules(df)

        df = self._validate_duplicates(df)

        df = self._generate_ids(df)

        df = self._add_metadata(df)

        final_df = self._merge_master(df)

        self.save_csv(final_df)

        summary = self.get_summary(
            start_time=start_time,
            input_count=input_records,
            output_count=len(final_df),
            dups_removed=input_records - len(df),
            skipped=0,
            failed=0,
            status="SUCCESS",
        )

        print("\nPregnancy Builder Completed Successfully.")

        return summary
def main() -> None:
    """Run Pregnancy Builder."""

    builder = PregnancyBuilder()

    summary = builder.build()

    print("\nBuild Summary")
    print("=" * 60)

    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()    