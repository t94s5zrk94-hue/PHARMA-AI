"""
Interaction Audit
Phase 15 - Clinical Knowledge Engine

Production audit for interaction_master.csv
"""

from pathlib import Path
from typing import Any

import json
import pandas as pd
class InteractionAudit:
    """Production audit for interaction_master.csv."""

    REQUIRED_COLUMNS = [
        "Interaction_ID",
        "Generic_A",
        "Generic_B",
        "Severity",
        "Mechanism",
        "Clinical_Effect",
        "Management",
        "Evidence_Level",
        "Primary_Reference",
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

        self.report_path = Path(
            "reports/interaction_audit.json"
        )

        self.df = pd.DataFrame()

        self.statistics: dict[str, Any] = {}

        self.audit_results: dict[str, bool] = {}

    class InteractionAudit:
        """Production audit for interaction_master.csv."""

    REQUIRED_COLUMNS = [
        "Interaction_ID",
        "Generic_A",
        "Generic_B",
        "Severity",
        "Mechanism",
        "Clinical_Effect",
        "Management",
        "Evidence_Level",
        "Primary_Reference",
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

        self.report_path = Path(
            "reports/interaction_audit.json"
        )

        self.df = pd.DataFrame()

        self.statistics: dict[str, Any] = {}

        self.audit_results: dict[str, bool] = {}

    def load_master(self) -> None:
        """Load interaction_master.csv."""

        if not self.master_path.exists():
            raise FileNotFoundError(
            f"Interaction master not found: {self.master_path}"
        )

        self.df = pd.read_csv(self.master_path)

        print(f"Loaded {len(self.df)} interaction records.")    

    def audit_schema(self) -> bool:
        """Audit interaction master schema."""

        missing_columns = [
        column
        for column in self.REQUIRED_COLUMNS
        if column not in self.df.columns
        ]

        if missing_columns:
            print("\nSchema Audit Failed")

        for column in missing_columns:
            print(f"Missing: {column}")

            self.audit_results["schema"] = False
            return False

        print("Schema Audit Passed")

        self.audit_results["schema"] = True
        return True    
    def audit_missing_values(self) -> bool:
        """Audit missing values."""

        missing = int(
        self.df[self.REQUIRED_COLUMNS]
        .isna()
        .sum()
        .sum()
        )

        self.statistics["missing_values"] = missing

        if missing > 0:
            print(f"Missing Values: {missing}")

            self.audit_results["missing_values"] = False
            return False

        print("Missing Value Audit Passed")

        self.audit_results["missing_values"] = True
        return True
    
    def audit_duplicates(self) -> bool:
        """Audit duplicate Interaction_IDs and interaction pairs."""

        duplicate_ids = int(
        self.df["Interaction_ID"].duplicated().sum()
        )

        duplicate_pairs = int(
        (
            self.df["Generic_A"].astype(str).str.strip().str.lower()
            + "|"
            + self.df["Generic_B"].astype(str).str.strip().str.lower()
        ).duplicated().sum()
        )

        self.statistics["duplicate_ids"] = duplicate_ids
        self.statistics["duplicate_pairs"] = duplicate_pairs

        if duplicate_ids > 0:
            print(f"Duplicate IDs: {duplicate_ids}")

        if duplicate_pairs > 0:
            print(f"Duplicate Pairs: {duplicate_pairs}")

        passed = duplicate_ids == 0 and duplicate_pairs == 0

        if passed:
            print("Duplicate Audit Passed")

        self.audit_results["duplicates"] = passed

        return passed
    
    def audit_enum_values(self) -> bool:
        """Audit enum fields."""

        enum_checks = {
        "Severity": self.SEVERITY_VALUES,
        "Evidence_Level": self.EVIDENCE_LEVELS,
        "Status": self.STATUS_VALUES,
       }

        passed = True

        for column, allowed_values in enum_checks.items():

            invalid = (
            self.df.loc[
                ~self.df[column].isin(allowed_values),
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
           print("Enum Audit Passed")

        self.audit_results["enum"] = passed

        return passed
    
    def audit_metadata(self) -> bool:
        """Audit metadata fields."""

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
            print("Metadata Audit Passed")

        self.audit_results["metadata"] = passed

        return passed
    
    def generate_statistics(self) -> None:
        """Generate interaction audit statistics."""

        self.statistics.update({
        "total_records": len(self.df),
        "total_columns": len(self.df.columns),
        "active_records": int(
            (self.df["Status"] == "Active").sum()
        ),
        "inactive_records": int(
            (self.df["Status"] == "Inactive").sum()
        ),
        "severity_distribution": (
            self.df["Severity"]
            .value_counts()
            .to_dict()
        ),
        "evidence_distribution": (
            self.df["Evidence_Level"]
            .value_counts()
            .to_dict()
        ),
        })

        print("\nInteraction Statistics")

        for key, value in self.statistics.items():
           print(f"{key}: {value}")
    
    def calculate_health_score(self) -> int:
        """Calculate interaction audit health score."""

        score = 100

        for passed in self.audit_results.values():
            if not passed:
                score -= 20

        score = max(score, 0)

        self.statistics["health_score"] = score

        print(f"\nHealth Score: {score}/100")

        return score
    
    def calculate_health_grade(self) -> str:
        """Calculate health grade."""

        score = self.statistics["health_score"]

        if score >= 95:
           grade = "A+"
        elif score >= 90:
           grade = "A"
        elif score >= 80:
           grade = "B"
        elif score >= 70:
           grade = "C"
        else:
            grade = "F"

        self.statistics["health_grade"] = grade

        print(f"Health Grade: {grade}")

        return grade
    
    def save_report(self) -> None:
        """Save audit report as JSON."""

        self.report_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        report = {
        "audit_results": self.audit_results,
        "statistics": self.statistics,
        }

        with open(
            self.report_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
        )

        print(f"\nAudit report saved to {self.report_path}")

    def build(self) -> dict:
        """Run the complete interaction audit."""

        self.load_master()

        schema_ok = self.audit_schema()

        if not schema_ok:
            report = {
            "status": "FAILED",
            "message": "Schema audit failed.",
        }

            print("\nAudit Complete")
            print("Status : FAILED")

            return report

        self.audit_missing_values()
        self.audit_duplicates()
        self.audit_enum_values()
        self.audit_metadata()

        self.generate_statistics()
        self.calculate_health_score()
        self.calculate_health_grade()

        self.save_report()

        status = (
            "SUCCESS"
        if all(self.audit_results.values())
        else "FAILED"
        )

        report = {
        "status": status,
        "audit_results": self.audit_results,
        "statistics": self.statistics,
        }

        print("\nAudit Complete")
        print(f"Status : {status}")
        print(
            f"Health : "
            f"{self.statistics['health_score']}/100"
        )

        return report    
def main() -> None:
    """Run the Interaction Audit."""

    audit = InteractionAudit()

    report = audit.build()

    print("\nFinal Audit Report")
    print("=" * 60)

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()