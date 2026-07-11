import logging
from pathlib import Path

import pandas as pd

from pharma_ai.builders.base_builder import BaseBuilder
from pharma_ai.builders.id_generator import get_next_evidence_id


class EvidenceBuilder(BaseBuilder):
    """
    Phase 15.10
    Evidence & References Builder
    """

    REQUIRED_COLUMNS = [
        "Generic_Name",
        "Clinical_Topic",
        "Evidence_Summary",
        "Evidence_Level",
        "Primary_Reference",
        "Reference_Year",
        "Guideline_Source",
        "Status",
    ]

    VALID_EVIDENCE = {
        "High",
        "Moderate",
        "Low",
    }

    VALID_STATUS = {
        "Active",
        "Inactive",
    }

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.input_file = Path(
            "pharma_ai/database/input/evidence_input.csv"
        )

        self.master_file = Path(
            "pharma_ai/database/clinical/evidence/evidence_master.csv"
        )

        super().__init__(
            input_file=self.input_file,
            output_path=self.master_file,
            required_columns=self.REQUIRED_COLUMNS,
        )

        self.generic_master_file = Path(
            "pharma_ai/database/medicine/generic_master.csv"
        )

        self.df = pd.DataFrame()
        self.master_df = pd.DataFrame()
        self.generic_df = pd.DataFrame()

        self.logger.info("EvidenceBuilder initialized.")

    def _load_input(self):

        self.logger.info("Loading evidence input...")

        self.df = pd.read_csv(self.input_file)

        self.logger.info(
            "Loaded %d evidence records.",
            len(self.df),
        )

    def _validate_schema(self):

        self.logger.info("Validating required columns...")

        missing = [
            col
            for col in self.REQUIRED_COLUMNS
            if col not in self.df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        self.logger.info("Schema validation passed.")

    def _validate_business_rules(self):

        self.logger.info("Validating business rules...")

        if not self.df["Evidence_Level"].isin(
            self.VALID_EVIDENCE
        ).all():
            raise ValueError(
                "Invalid Evidence_Level found."
            )

        if not self.df["Status"].isin(
            self.VALID_STATUS
        ).all():
            raise ValueError(
                "Invalid Status found."
            )

        self.logger.info(
            "Business rule validation passed."
        )

    def _validate_duplicates(self):

        self.logger.info(
            "Checking duplicate evidence records..."
        )

        duplicate_mask = self.df.duplicated(
            subset=[
                "Generic_Name",
                "Clinical_Topic",
            ]
        )

        if duplicate_mask.any():

            duplicates = self.df.loc[
                duplicate_mask,
                [
                    "Generic_Name",
                    "Clinical_Topic",
                ],
            ]

            raise ValueError(
                f"Duplicate evidence records found:\n{duplicates}"
            )

        self.logger.info(
            "Duplicate validation passed."
        )

    def _load_existing_master(self):

        self.logger.info(
            "Loading existing master..."
        )

        if self.master_file.exists():

            self.master_df = pd.read_csv(
                self.master_file
            )

            self.logger.info(
                "Existing master loaded (%d records).",
                len(self.master_df),
            )

        else:

            self.master_df = pd.DataFrame()

            self.logger.info(
                "Master file not found. New master will be created."
            )

        self.logger.info(
            "Loading Generic Master..."
        )

        self.generic_df = pd.read_csv(
            self.generic_master_file
        )

        self.logger.info(
            "Loaded %d generic records.",
            len(self.generic_df),
    
        )
    def _generate_ids(self):

        self.logger.info("Generating Evidence IDs...")

        generic_map = dict(
            zip(
                self.generic_df["Generic_Name"],
                self.generic_df["Generic_ID"],
            )
        )

        self.df["Generic_ID"] = self.df["Generic_Name"].map(
            generic_map
        )

        missing_generic = self.df[
            self.df["Generic_ID"].isna()
        ]

        if not missing_generic.empty:

            raise ValueError(
                "Generic not found in generic_master.csv:\n"
                f"{missing_generic[['Generic_Name']]}"
            )

        last_id = None

        if not self.master_df.empty:
            last_id = self.master_df.iloc[-1]["Evidence_ID"]

        self.df.insert(
            0,
            "Evidence_ID",
            get_next_evidence_id(
                last_id=last_id,
                count=len(self.df),
            ),
        )

        self.df.drop(
            columns=["Generic_Name"],
            inplace=True,
        )

        self.logger.info(
            "Evidence IDs generated successfully."
        )

    def _add_metadata(self):

        self.logger.info("Adding metadata...")

        timestamp = pd.Timestamp.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.df["created_at"] = timestamp
        self.df["updated_at"] = timestamp
        self.df["version"] = "1.0"

        self.logger.info(
            "Metadata added successfully."
        )

    def _merge_master(self):

        self.logger.info("Merging master data...")

        if self.master_df.empty:

            final_df = self.df.copy()

        else:

            final_df = pd.concat(
                [
                    self.master_df,
                    self.df,
                ],
                ignore_index=True,
            )

            final_df.drop_duplicates(
                subset=[
                    "Generic_ID",
                    "Clinical_Topic",
                ],
                keep="last",
                inplace=True,
            )

        final_df.to_csv(
            self.master_file,
            index=False,
        )

        self.logger.info(
            "Evidence master saved successfully (%d records).",
            len(final_df),
        )

    def build(self):

        self.logger.info("=" * 60)
        self.logger.info(
            "Starting Evidence Builder..."
        )

        self._load_input()
        self._validate_schema()
        self._validate_business_rules()
        self._validate_duplicates()
        self._load_existing_master()
        self._generate_ids()
        self._add_metadata()
        self._merge_master()

        self.logger.info(
            "Evidence Builder completed successfully."
        )

    @staticmethod
    def main():

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
        )

        builder = EvidenceBuilder()

        builder.build()


if __name__ == "__main__":
    EvidenceBuilder.main()
