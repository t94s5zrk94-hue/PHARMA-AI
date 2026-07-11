"""
Contraindication Audit
Phase 15 - Clinical Knowledge Engine
"""

from pathlib import Path
import json

import pandas as pd
class ContraindicationAudit:
    """Production audit for contraindication_master.csv."""

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

        self.report_path = Path(
            "reports/contraindication_audit.json"
        )

        self.df = pd.DataFrame()

        self.audit_results = {}

        self.statistics = {}

    def load_master(self) -> None:
        """Load contraindication master."""

        if not self.master_path.exists():
            raise FileNotFoundError(
                f"Master file not found: {self.master_path}"
            )

        self.df = pd.read_csv(self.master_path)

        print(
            f"Loaded {len(self.df)} contraindication records."
        )
    def audit_schema(self) -> bool:
        """Audit schema."""

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in self.df.columns
        ]

        passed = len(missing) == 0

        if passed:
            print("Schema Audit Passed")
        else:
            print("\nMissing Columns:")

        for column in missing:
            print(f" - {column}")

        self.audit_results["schema"] = passed

        return passed    
    
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
        """Audit duplicate records."""

        duplicate_ids = int(
            self.df["Contraindication_ID"]
            .duplicated()
            .sum()
        )

        duplicate_pairs = int(
            self.df.duplicated(
                subset=[
                    "Generic_Name",
                    "Contraindication",
                ]
            ).sum()
        )

        self.statistics["duplicate_ids"] = duplicate_ids
        self.statistics["duplicate_pairs"] = duplicate_pairs

        passed = (
            duplicate_ids == 0
            and duplicate_pairs == 0
        )

        if passed:
            print("Duplicate Audit Passed")
        else:
            print(
                f"Duplicate IDs: {duplicate_ids}"
            )
            print(
                f"Duplicate Pairs: {duplicate_pairs}"
            )

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
            print("Enum Audit Passed")

        self.audit_results["enum"] = passed

        return passed
    
    def audit_metadata(self) -> bool:
        """Audit metadata."""

        metadata_columns = [
            "created_at",
            "updated_at",
            "version",
        ]

        passed = True

        for column in metadata_columns:

            missing = self.df[column].isna().sum()

            if missing > 0:

                print(
                    f"{column}: {missing} missing values"
                )

                passed = False

        if passed:
            print("Metadata Audit Passed")

        self.audit_results["metadata"] = passed

        return passed
    
    def generate_statistics(self) -> None:
        """Generate audit statistics."""

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

        print("\nContraindication Statistics")

        for key, value in self.statistics.items():
            print(f"{key}: {value}")
        
    def calculate_health_score(self) -> None:
        """Calculate audit health score."""

        score = 100

        for passed in self.audit_results.values():
            if not passed:
                score -= 20

        score = max(score, 0)

        if score >= 90:
            grade = "A+"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"

        self.statistics["health_score"] = score
        self.statistics["health_grade"] = grade

        print(f"\nHealth Score: {score}/100")
        print(f"Health Grade: {grade}")

    def save_report(self) -> None:
        """Save audit report."""

        report = {
            "status": (
                "SUCCESS"
                if all(self.audit_results.values())
                else "FAILED"
            ),
            "audit_results": self.audit_results,
            "statistics": self.statistics,
        }

        self.report_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.report_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                report,
                file,
                indent=4,
            )

        print(
            f"\nAudit report saved to {self.report_path}"
        )    

    def build(self) -> dict:
        """Run complete audit."""

        self.load_master()

        self.audit_schema()
        self.audit_missing_values()
        self.audit_duplicates()
        self.audit_enum_values()
        self.audit_metadata()

        self.generate_statistics()

        self.calculate_health_score()

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
    """Run Contraindication Audit."""

    audit = ContraindicationAudit()

    report = audit.build()

    print("\nFinal Audit Report")
    print("=" * 60)

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()    