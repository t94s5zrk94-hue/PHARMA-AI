"""
Warning Validator
Phase 15 - Clinical Knowledge Engine
"""

from pathlib import Path

import pandas as pd

class WarningValidator:
    """Production validator for warning_master.csv."""

    REQUIRED_COLUMNS = [
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

    SEVERITY_VALUES = {
        "Major",
        "Moderate",
        "Minor",
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
            "warning/"
            "warning_master.csv"
        )

        self.df = pd.DataFrame()

        self.validation_results = {}

        self.statistics = {}

    def load_master(self) -> None:
        """Load warning master."""

        if not self.master_path.exists():
            raise FileNotFoundError(
                f"Master file not found: {self.master_path}"
            )

        self.df = pd.read_csv(self.master_path)

        print(
            f"Loaded {len(self.df)} warning records."
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
            print("\nMissing Columns:")

            for column in missing:
                print(f" - {column}")

        self.validation_results["required_columns"] = passed

        return passed     
    
    def validate_missing_values(self) -> bool:
        """Validate missing values."""

        missing = 0

        for column in self.REQUIRED_COLUMNS:

            missing_count = self.df[column].isna().sum()

            if missing_count > 0:

                print(f"{column}: {missing_count} missing values")

                missing += missing_count

        self.statistics["missing_values"] = missing

        passed = (missing == 0)

        if passed:
            print("Missing value validation passed.")

        self.validation_results["missing_values"] = passed

        return passed
    
    def validate_duplicate_ids(self) -> bool:
        """Validate Warning_ID uniqueness."""

        duplicates = int(
            self.df["Warning_ID"]
            .duplicated()
            .sum()
        )

        self.statistics["duplicate_ids"] = duplicates

        passed = duplicates == 0

        if passed:
            print("Warning_ID validation passed.")
        else:
            print(f"Duplicate Warning_ID found: {duplicates}")

        self.validation_results["duplicate_ids"] = passed

        return passed
    
    def validate_duplicate_pairs(self) -> bool:
        """Validate duplicate warning pairs."""

        duplicates = int(
            self.df.duplicated(
                subset=[
                    "Generic_Name",
                    "Warning",
                ]
            ).sum()
        )

        self.statistics["duplicate_pairs"] = duplicates

        passed = duplicates == 0

        if passed:
            print("Warning pair validation passed.")
        else:
            print(f"Duplicate warning pairs: {duplicates}")

        self.validation_results["duplicate_pairs"] = passed

        return passed
    
    def validate_enum_values(self) -> bool:
        """Validate enum fields."""

        enum_checks = {
            "Severity": self.SEVERITY_VALUES,
            "Evidence_Level": self.EVIDENCE_LEVELS,
            "Status": self.STATUS_VALUES,
        }

        passed = True

        for column, allowed_values in enum_checks.items():

            invalid = (
                self.df.loc[
                    ~self.df[column]
                    .astype(str)
                    .str.strip()
                    .isin(allowed_values),
                    column,
                ]
                .dropna()
                .unique()
            )

            if len(invalid) > 0:

                print(f"\nInvalid values in {column}")

                for value in invalid:
                    print(f" - {value}")

                passed = False

        if passed:
            print("Enum validation passed.")

        self.validation_results["enum_values"] = passed

        return passed
    
    def validate_metadata(self) -> bool:
        """Validate metadata."""

        metadata_columns = [
            "created_at",
            "updated_at",
            "version",
        ]

        passed = True

        for column in metadata_columns:

            missing = self.df[column].isna().sum()

            if missing > 0:

                print(f"{column}: {missing} missing values")

                passed = False

        if passed:
            print("Metadata validation passed.")

        self.validation_results["metadata"] = passed

        return passed
    
    def generate_statistics(self) -> None:
        """Generate validation statistics."""

        self.statistics.update({
            "total_records": len(self.df),
            "total_columns": len(self.df.columns),
        })

        print("\nValidation Statistics")

        for key, value in self.statistics.items():
            print(f"{key}: {value}")
    
    def calculate_health_score(self) -> int:
        """Calculate validation health score."""

        score = 100

        for result in self.validation_results.values():
            if not result:
                score -= 20

        score = max(score, 0)

        self.statistics["health_score"] = score

        print(f"\nHealth Score: {score}/100")

        return score
    
    def build(self) -> dict:
        """Run the complete contraindication validation workflow."""

        self.load_master()

        required_ok = self.validate_required_columns()

        if not required_ok:
            return {
            "status": "FAILED",
            "message": "Required column validation failed.",
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

        health_score = self.calculate_health_score()

        status = (
            "SUCCESS"
            if all(validation_results.values())
            else "FAILED"
        )

        report = {
            "status": status,
            "health_score": health_score,
            "statistics": self.statistics,
            "validation_results": validation_results,
        }

        print("\nValidation Complete")
        print(f"Status : {status}")
        print(f"Health : {health_score}/100")
        return report
    
def main() -> None:

    validator = WarningValidator()

    report = validator.build()

    print("\nFinal Report")
    print("=" * 60)

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()    

    