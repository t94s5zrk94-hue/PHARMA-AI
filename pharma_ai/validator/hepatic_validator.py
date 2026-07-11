import logging
from pathlib import Path

import pandas as pd


class HepaticValidator:
    """
    Phase 15.8
    Hepatic Dose Adjustment Validator
    """

    REQUIRED_COLUMNS = [
        "Hepatic_ID",
        "Generic_ID",
        "Hepatic_Category",
        "Child_Pugh_Class",
        "Dose_Recommendation",
        "Clinical_Note",
        "Contraindicated",
        "Evidence_Level",
        "Primary_Reference",
        "Status",
        "created_at",
        "updated_at",
        "version",
    ]

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.master_file = Path(
            "pharma_ai/database/clinical/hepatic/hepatic_master.csv"
        )

        self.df = pd.DataFrame()

        self.VALID_HEPATIC_CATEGORY = {
            "Mild",
            "Moderate",
            "Severe",
        }

        self.VALID_CHILD_PUGH = {
            "A",
            "B",
            "C",
        }

        self.VALID_CONTRAINDICATED = {
            "Yes",
            "No",
        }

        self.VALID_EVIDENCE = {
            "High",
            "Moderate",
            "Low",
        }

        self.VALID_STATUS = {
            "Active",
            "Inactive",
        }

        self.statistics = {
            "missing_values": 0,
            "duplicate_ids": 0,
            "duplicate_pairs": 0,
            "total_records": 0,
            "total_columns": 0,
        }

    def load_master(self):

        self.logger.info("Loading Hepatic Master...")

        self.df = pd.read_csv(self.master_file)

        self.statistics["total_records"] = len(self.df)
        self.statistics["total_columns"] = len(self.df.columns)

        self.logger.info(
            "Loaded %d hepatic records.",
            len(self.df),
        )

    def validate_required_columns(self):

        missing = [
            col
            for col in self.REQUIRED_COLUMNS
            if col not in self.df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        self.logger.info(
            "Required column validation passed."
        )

    def validate_missing_values(self):

        missing = self.df.isna().sum().sum()

        self.statistics["missing_values"] = int(missing)

        if missing > 0:
            raise ValueError(
                f"Missing values found: {missing}"
            )

        self.logger.info(
            "Missing value validation passed."
        )

    def validate_duplicate_ids(self):

        duplicates = self.df["Hepatic_ID"].duplicated().sum()

        self.statistics["duplicate_ids"] = int(duplicates)

        if duplicates > 0:
            raise ValueError(
                f"Duplicate Hepatic_ID found: {duplicates}"
            )

        self.logger.info(
            "Hepatic_ID validation passed."
        )

    def validate_duplicate_pairs(self):

        duplicates = self.df.duplicated(
            subset=[
                "Generic_ID",
                "Hepatic_Category",
            ]
        ).sum()

        self.statistics["duplicate_pairs"] = int(duplicates)

        if duplicates > 0:
            raise ValueError(
                f"Duplicate Hepatic pair found: {duplicates}"
            )

        self.logger.info(
            "Hepatic pair validation passed."
        )
        VALID_HEPATIC_CATEGORY = {
        "Mild",
        "Moderate",
        "Severe",
    }

    VALID_CHILD_PUGH = {
        "A",
        "B",
        "C",
    }

    VALID_CONTRAINDICATED = {
        "Yes",
        "No",
    }

    VALID_EVIDENCE = {
        "High",
        "Moderate",
        "Low",
    }

    VALID_STATUS = {
        "Active",
        "Inactive",
    }

    def validate_enum_values(self):

        if not self.df["Hepatic_Category"].isin(
            self.VALID_HEPATIC_CATEGORY
        ).all():
            raise ValueError(
                "Invalid Hepatic_Category found."
            )

        if not self.df["Child_Pugh_Class"].isin(
            self.VALID_CHILD_PUGH
        ).all():
            raise ValueError(
                "Invalid Child_Pugh_Class found."
            )

        if not self.df["Contraindicated"].isin(
            self.VALID_CONTRAINDICATED
        ).all():
            raise ValueError(
                "Invalid Contraindicated value found."
            )

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

        self.logger.info("Enum validation passed.")

    def validate_metadata(self):

        metadata_columns = [
            "created_at",
            "updated_at",
            "version",
        ]

        for column in metadata_columns:

            if self.df[column].isna().any():
                raise ValueError(
                    f"Missing metadata in {column}"
                )

        self.logger.info(
            "Metadata validation passed."
        )

    def generate_statistics(self):

        self.logger.info("")
        self.logger.info("Validation Statistics")

        for key, value in self.statistics.items():

            self.logger.info("%s: %s", key, value)

    def calculate_health_score(self):

        score = 100

        score -= self.statistics["missing_values"] * 5
        score -= self.statistics["duplicate_ids"] * 10
        score -= self.statistics["duplicate_pairs"] * 10

        score = max(score, 0)

        self.logger.info("")
        self.logger.info(
            "Health Score: %d/100",
            score,
        )

        return score

    def build(self):

        self.load_master()

        self.validate_required_columns()

        self.validate_missing_values()

        self.validate_duplicate_ids()

        self.validate_duplicate_pairs()

        self.validate_enum_values()

        self.validate_metadata()

        self.generate_statistics()

        score = self.calculate_health_score()

        self.logger.info("")
        self.logger.info("Validation Complete")

        if score == 100:

            self.logger.info(
                "Status : SUCCESS"
            )

        else:

            self.logger.warning(
                "Status : FAILED"
            )

    @staticmethod
    def main():

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
        )

        validator = HepaticValidator()

        validator.build()


if __name__ == "__main__":
    HepaticValidator.main()    