"""
Contraindication Validator
Phase 15 - Clinical Knowledge Engine
"""

from pathlib import Path
from typing import Dict

import pandas as pd
class ContraindicationValidator:
    """Production validator for contraindication_master.csv."""

    REQUIRED_COLUMNS = [
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

    SEVERITY_VALUES = {
        "Absolute",
        "Relative",
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
            "contraindication/"
            "contraindication_master.csv"
        )

        self.df = pd.DataFrame()

        self.statistics: Dict[str, int] = {}

    def load_master(self) -> None:
        """Load contraindication master."""

        if not self.master_path.exists():
            raise FileNotFoundError(f"Master file not found: {self.master_path}" )
        self.df = pd.read_csv(self.master_path)
        print(f"Loaded {len(self.df)} contraindication records." )   
    
    def validate_required_columns(self) -> bool:
        """Validate required columns."""

        missing_columns = [
        column
        for column in self.REQUIRED_COLUMNS
        if column not in self.df.columns
        ]

        if missing_columns:

            print("\nMissing Columns:")

        for column in missing_columns:
            print(f" - {column}")

            return False

        print("Required column validation passed.")
        return True
    
    def validate_missing_values(self) -> bool:
        """Validate missing values."""

        missing_found = False
        total_missing = 0

        for column in self.REQUIRED_COLUMNS:

            missing_count = (
               self.df[column]
               .fillna("")
               .astype(str)
               .str.strip()
               .eq("")
               .sum()
            )

            total_missing += int(missing_count)

            if missing_count > 0:
               print(f"{column}: {missing_count} missing values")
               missing_found = True

            self.statistics["missing_values"] = total_missing

        if missing_found:
            return False

        print("Missing value validation passed.")
        return True
    
    def validate_duplicate_ids(self) -> bool:
        """Validate duplicate Contraindication_ID values."""

        duplicate_count = (
            self.df["Contraindication_ID"]
            .duplicated()
            .sum()
        )

        if duplicate_count > 0:

            print(f"Duplicate Contraindication_ID found: " f"{duplicate_count}")
            return False

        print("Contraindication_ID validation passed.")

        return True
    
    def validate_duplicate_pairs(self) -> bool:
        """Validate duplicate contraindication records."""

        duplicate_count = (
            self.df.duplicated(
            subset=[
                "Generic_Name",
                "Contraindication",]
            ).sum()
            )

        if duplicate_count > 0:

            print(
            f"Duplicate contraindications found: "
            f"{duplicate_count}"
        )

            return False

        print("Contraindication pair validation passed.")
        return True
    
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
        return passed
    
    def generate_statistics(self) -> None:
        """Generate validation statistics."""

        self.statistics = {
            "total_records": len(self.df),
            "total_columns": len(self.df.columns),
            "duplicate_ids": int(
            self.df["Contraindication_ID"]
            .duplicated()
            .sum()
            ),
            "duplicate_pairs": int(
            self.df.duplicated(
                subset=[
                    "Generic_Name",
                    "Contraindication",
                ]
            ).sum()
            ),
            "missing_values": self.statistics.get("missing_values", 0),}

        print("\nValidation Statistics")

        for key, value in self.statistics.items():
            print(f"{key}: {value}")

    def calculate_health_score(self) -> int:
        """Calculate health score."""

        score = 100

        score -= self.statistics["duplicate_ids"] * 10
        score -= self.statistics["duplicate_pairs"] * 10
        score -= self.statistics["missing_values"]

        score = max(score, 0)

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
    """Run Contraindication Validator."""

    validator = ContraindicationValidator()

    report = validator.build()

    print("\nFinal Report")
    print("=" * 60)

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()