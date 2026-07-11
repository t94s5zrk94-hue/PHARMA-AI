"""
Interaction Validator
Phase 15 - Clinical Knowledge Engine

Validates:
- interaction_master.csv
- Schema
- Required Columns
- Missing Values
- Duplicate IDs
- Duplicate Generic Pairs
- Enum Values
- Metadata
"""

from pathlib import Path
from typing import Dict

import pandas as pd


class InteractionValidator:
    """Production validator for interaction_master.csv."""

    REQUIRED_COLUMNS = [
        "Interaction_ID",
        "Generic_A",
        "Generic_B",
        "Severity",
        "Clinical_Effect",
        "Mechanism",
        "Management",
        "Primary_Reference",
        "Evidence_Level",
        "Status",
        "created_at",
        "updated_at",
        "version",
    ]

    SEVERITY_VALUES = {
        "Contraindicated",
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

    def __init__(self) -> None:

        
        self.master_path = Path(
            "pharma_ai/database/clinical/interaction/interaction_master.csv"
        )

        self.df = pd.DataFrame()

        self.statistics: Dict[str, int] = {}

        #self.logger.info("InteractionValidator initialized.")

    def load_master(self) -> None:
        """Load interaction_master.csv."""

        if not self.master_path.exists():
            raise FileNotFoundError(
                f"Interaction master not found: {self.master_path}"
        )

        self.df = pd.read_csv(self.master_path)

        print(f"Loaded {len(self.df)} interaction records.")    

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
        """Validate missing values in required columns."""

        missing_found = False

        for column in self.REQUIRED_COLUMNS:

            missing_count = self.df[column].isna().sum()

        if missing_count > 0:
            print(f"{column}: {missing_count} missing values")
            missing_found = True

        if missing_found:
            return False

        print("Missing value validation passed.")
        return True
    
    def validate_duplicate_ids(self) -> bool:
        """Validate duplicate Interaction_ID values."""

        duplicate_count = self.df["Interaction_ID"].duplicated().sum()

        if duplicate_count > 0:
            print(f"Duplicate Interaction_ID found: {duplicate_count}")
            return False

        print("Interaction_ID validation passed.")
        return True
    
    def validate_duplicate_pairs(self) -> bool:
        """Validate duplicate Generic_A + Generic_B pairs."""

        pairs = (
            self.df["Generic_A"].astype(str).str.strip().str.lower()
            + "|"
            + self.df["Generic_B"].astype(str).str.strip().str.lower()
        )

        duplicate_count = pairs.duplicated().sum()

        if duplicate_count > 0:
            print(f"Duplicate interaction pairs found: {duplicate_count}")
            return False

        print("Interaction pair validation passed.")
        return True
    def validate_enum_values(self) -> bool:
        """Validate enum fields."""

        validation_passed = True

        enum_checks = {
            "Severity": self.SEVERITY_VALUES,
            "Evidence_Level": self.EVIDENCE_LEVELS,
            "Status": self.STATUS_VALUES,
        }

        for column, allowed_values in enum_checks.items():

            invalid_values = (
                self.df.loc[
                ~self.df[column].isin(allowed_values),
                column,
            ]
            .dropna()
            .unique()
        )

        if len(invalid_values) > 0:
            print(f"\nInvalid values found in '{column}':")

            for value in invalid_values:
                print(f"  - {value}")

            validation_passed = False

        if validation_passed:
           print("Enum validation passed.")

        return validation_passed
    def validate_metadata(self) -> bool:
        """Validate metadata columns."""

        metadata_columns = [
            "created_at",
            "updated_at",
            "version",
        ]

        validation_passed = True

        for column in metadata_columns:

            if self.df[column].isna().any():
                print(f"{column} contains missing values.")
                validation_passed = False

        if validation_passed:
            print("Metadata validation passed.")

        return validation_passed
    def generate_statistics(self) -> None:
        """Generate validation statistics."""

        self.statistics = {
            "total_records": len(self.df),
            "total_columns": len(self.df.columns),
            "duplicate_ids": int(
            self.df["Interaction_ID"].duplicated().sum()
        ),
        "duplicate_pairs": int(
            (
                self.df["Generic_A"].astype(str).str.strip().str.lower()
                + "|"
                + self.df["Generic_B"].astype(str).str.strip().str.lower()
            ).duplicated().sum()
        ),
        "missing_values": int(
            self.df[self.REQUIRED_COLUMNS]
            .isna()
            .sum()
            .sum()
        ),
        }

        print("\nValidation Statistics")

        for key, value in self.statistics.items():
            print(f"{key}: {value}")

    def calculate_health_score(self) -> int:
        """Calculate interaction database health score."""

        score = 100

        score -= self.statistics["duplicate_ids"] * 10
        score -= self.statistics["duplicate_pairs"] * 10
        score -= self.statistics["missing_values"]

        if score < 0:
           score = 0

        print(f"\nHealth Score: {score}/100")

        return score        
    
    def build(self) -> dict:
        """Run the complete interaction validation workflow."""

        self.load_master()

        required_ok = self.validate_required_columns()

        if not required_ok:
            return {
               "status": "FAILED",
                "message": "Required column validation failed."
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
        """Run the Interaction Validator."""

        validator = InteractionValidator()

        report = validator.build()

        print("\nFinal Report")
        print("=" * 50)

        for key, value in report.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
        main()