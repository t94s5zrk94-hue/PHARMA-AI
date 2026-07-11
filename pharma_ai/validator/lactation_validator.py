"""
Lactation Validator
Phase 15 - Clinical Knowledge Engine
"""

from pathlib import Path

import pandas as pd


class LactationValidator:
    """Production validator for lactation_master.csv."""

    REQUIRED_COLUMNS = [
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

    LACTATION_RISK_VALUES = {
        "Compatible",
        "Use with Caution",
        "Contraindicated",
        "Unknown",
    }

    RECOMMENDATION_VALUES = {
        "Continue",
        "Monitor Infant",
        "Avoid",
        "Consult Doctor",
    }

    EVIDENCE_LEVELS = {
        "High",
        "Moderate",
        "Low",
    }

    STATUS_VALUES = {
        "Active",
        "Inactive",
    }

    def __init__(self):

        self.master_path = Path(
            "pharma_ai/database/clinical/"
            "lactation/"
            "lactation_master.csv"
        )

        self.df = pd.DataFrame()

        self.validation_results = {}

        self.statistics = {}

    def load_master(self) -> None:
        """Load lactation master."""

        if not self.master_path.exists():
            raise FileNotFoundError(
                f"Master file not found: {self.master_path}"
            )

        self.df = pd.read_csv(self.master_path)

        print(
            f"Loaded {len(self.df)} lactation records."
        )


    def validate_required_columns(self) -> bool:
        """Validate required columns."""

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in self.df.columns
        ]

        passed = len(missing) == 0

        if passed:
            print("Required column validation passed.")

        else:

            print("\nMissing Columns")

            for column in missing:
                print(f" - {column}")

        self.validation_results["required_columns"] = passed

        return passed


    def validate_missing_values(self) -> bool:
        """Validate missing values."""

        missing = 0

        for column in self.REQUIRED_COLUMNS:

            missing_count = (
                self.df[column]
                .astype(str)
                .str.strip()
                .replace("", pd.NA)
                .isna()
                .sum()
            )

            if missing_count > 0:

                print(
                    f"{column}: {missing_count}"
                )

                missing += missing_count

        self.statistics["missing_values"] = missing

        passed = missing == 0

        if passed:
            print("Missing value validation passed.")

        self.validation_results["missing_values"] = passed

        return passed


    def validate_duplicate_ids(self) -> bool:
        """Validate Lactation_ID."""

        duplicates = int(
            self.df["Lactation_ID"]
            .duplicated()
            .sum()
        )

        self.statistics["duplicate_ids"] = duplicates

        passed = duplicates == 0

        if passed:
            print("Lactation_ID validation passed.")

        self.validation_results["duplicate_ids"] = passed

        return passed
    
    def validate_duplicate_pairs(self) -> bool:
        """Validate duplicate lactation records."""

        duplicates = int(
            self.df.duplicated(
                subset=[
                    "Generic_Name",
                ]
            ).sum()
        )

        self.statistics["duplicate_pairs"] = duplicates

        passed = duplicates == 0

        if passed:
            print("Lactation pair validation passed.")

        self.validation_results["duplicate_pairs"] = passed

        return passed


    def validate_enum_values(self) -> bool:
        """Validate enum values."""

        enum_checks = {
            "Lactation_Risk": self.LACTATION_RISK_VALUES,
            "Recommendation": self.RECOMMENDATION_VALUES,
            "Evidence_Level": self.EVIDENCE_LEVELS,
            "Status": self.STATUS_VALUES,
        }

        passed = True

        for column, allowed in enum_checks.items():

            invalid = (
                self.df.loc[
                    ~self.df[column]
                    .astype(str)
                    .str.strip()
                    .isin(allowed),
                    column,
                ]
                .dropna()
                .unique()
            )

            if len(invalid) > 0:

                print(f"\nInvalid values in {column}")

                for value in invalid:
                    print(value)

                passed = False

        if passed:
            print("Enum validation passed.")

        self.validation_results["enum_values"] = passed

        return passed


    def validate_metadata(self) -> bool:
        """Validate metadata."""

        passed = True

        for column in [
            "created_at",
            "updated_at",
            "version",
        ]:

            if self.df[column].isna().sum() > 0:
                passed = False

        if passed:
            print("Metadata validation passed.")

        self.validation_results["metadata"] = passed

        return passed


    def generate_statistics(self):

        self.statistics.update({
            "total_records": len(self.df),
            "total_columns": len(self.df.columns),
        })

        print("\nValidation Statistics")

        for k, v in self.statistics.items():
            print(f"{k}: {v}")


    def calculate_health_score(self):

        score = 100

        for result in self.validation_results.values():

            if not result:
                score -= 20

        score = max(score, 0)

        self.statistics["health_score"] = score

        print(f"\nHealth Score: {score}/100")

        return score
    
    def build(self):

        self.load_master()

        required_ok = self.validate_required_columns()

        if not required_ok:

            return {
                "status": "FAILED"
            }

        validation_results = {
            "required_columns": required_ok,
            "missing_values": self.validate_missing_values(),
            "duplicate_ids": self.validate_duplicate_ids(),
            "duplicate_pairs": self.validate_duplicate_pairs(),
            "enum_values": self.validate_enum_values(),
            "metadata": self.validate_metadata(),
        }

        self.generate_statistics()

        health = self.calculate_health_score()

        status = (
            "SUCCESS"
            if all(validation_results.values())
            else "FAILED"
        )

        report = {
            "status": status,
            "health_score": health,
            "statistics": self.statistics,
            "validation_results": validation_results,
        }

        print("\nValidation Complete")
        print(f"Status : {status}")

        return report


def main():

    validator = LactationValidator()

    report = validator.build()

    print("\nFinal Report")
    print("=" * 60)

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()