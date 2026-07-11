import logging
from pathlib import Path

import pandas as pd


class MonitoringValidator:
    """
    Phase 15.9
    Monitoring Parameters Validator
    """

    REQUIRED_COLUMNS = [
        "Monitoring_ID",
        "Generic_ID",
        "Monitoring_Parameter",
        "Monitoring_Frequency",
        "Target_Range",
        "Clinical_Action",
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
            "pharma_ai/database/clinical/monitoring/monitoring_master.csv"
        )

        self.df = pd.DataFrame()

        self.statistics = {
            "missing_values": 0,
            "duplicate_ids": 0,
            "duplicate_pairs": 0,
            "total_records": 0,
            "total_columns": 0,
        }

    def load_master(self):

        self.logger.info("Loading Monitoring Master...")

        self.df = pd.read_csv(self.master_file)

        self.statistics["total_records"] = len(self.df)
        self.statistics["total_columns"] = len(self.df.columns)

        self.logger.info(
            "Loaded %d monitoring records.",
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

        missing = self.df.isnull().sum()

        total_missing = int(missing.sum())

        self.statistics["missing_values"] = total_missing

        if total_missing > 0:

            self.logger.error("Missing Values Summary")

            for column, count in missing.items():

                if count > 0:
                    self.logger.error(
                        "%s : %d",
                        column,
                        count,
                    )

            raise ValueError(
                f"Missing values found: {total_missing}"
            )

        self.logger.info(
            "Missing value validation passed."
        )

    def validate_duplicate_ids(self):

        duplicates = self.df["Monitoring_ID"].duplicated().sum()

        self.statistics["duplicate_ids"] = int(duplicates)

        if duplicates > 0:
            raise ValueError(
                f"Duplicate Monitoring_ID found: {duplicates}"
            )

        self.logger.info(
            "Monitoring_ID validation passed."
        )

    def validate_duplicate_pairs(self):

        duplicates = self.df.duplicated(
            subset=[
                "Generic_ID",
                "Monitoring_Parameter",
            ]
        ).sum()

        self.statistics["duplicate_pairs"] = int(duplicates)

        if duplicates > 0:
            raise ValueError(
                f"Duplicate Monitoring pair found: {duplicates}"
            )

        self.logger.info(
            "Monitoring pair validation passed."
        )

    def validate_enum_values(self):

        self.VALID_EVIDENCE = {
            "High",
            "Moderate",
            "Low",
        }

        self.VALID_STATUS = {
            "Active",
            "Inactive",
        }

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
            self.logger.info("Status : SUCCESS")
        else:
            self.logger.warning("Status : FAILED")

    @staticmethod
    def main():

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
        )

        validator = MonitoringValidator()

        validator.build()


if __name__ == "__main__":
    MonitoringValidator.main()    