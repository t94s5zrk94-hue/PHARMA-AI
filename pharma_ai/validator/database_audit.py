"""
Pharma AI
Database Integrity Audit

Phase 13.6

Purpose:
    Comprehensive database audit framework.

Author:
    Ravi Varsani
"""

import logging
import os
import time
import datetime
import json
import pandas as pd
from typing import Any, Dict, Final

# Logger setup
logger = logging.getLogger(__name__)

# Constants for Audit Status
STATUS_PASS: Final = "PASS"
STATUS_FAIL: Final = "FAIL"
STATUS_WARN: Final = "WARNING"

# Mapping Rules
MAPPING_RULES: Final = {
    "generic_atc_mapping": {
        "duplicate_keys": ["Generic_ID", "ATC_ID"],
        "primary_group": "Generic_ID",
        "primary_column": "Is_Primary"
    },
    "generic_class_mapping": {
        "duplicate_keys": ["Generic_ID", "Therapeutic_Class_ID", "Pharmacological_Class_ID"],
        "primary_group": "Generic_ID",
        "primary_column": "Is_Primary"
    }
}

# Required columns for schema validation
REQUIRED_SCHEMAS: Final = {
    "generic": [
        "Generic_ID", "Generic_Name", "Standardized_Name", "Generic_Type", "Ingredients",
        "created_at", "updated_at", "catalog_source", "clinical_source", "version", "Status"
    ],
    "brand": [
        "Brand_ID", "Brand_Name", "Generic_ID", "Company_ID", "Strength", "Dosage_Form", "Status"
    ],
    "company": [
        "Company_ID", "Company_Name", "Country", "Company_Type", "Status"
    ],
    "product": [
        "Product_ID", "Generic_ID", "Product_Name", "Strength", "Dosage_Form", "Route", 
        "Pack_Size", "Unit", "Manufacturer", "PMBJK_Code", "HSN_Code", "GST_Rate", 
        "Schedule", "Storage", "Status", "created_at", "updated_at", "source", "version"
    ],
    "atc": [
        "ATC_ID", "ATC_Code", "ATC_Name", "Level_1_Code", "Level_1_Name", "Level_2_Code", 
        "Level_2_Name", "Level_3_Code", "Level_3_Name", "Level_4_Code", "Level_4_Name", 
        "Level_5_Code", "Level_5_Name", "WHO_Version", "created_at", "updated_at", "source", "version", "Status"
    ],
    "therapeutic": [
        "Therapeutic_Class_ID", "Therapeutic_Class_Name", "Therapeutic_Category", "Description", 
        "Parent_Class_ID", "Reference_Source", "created_at", "updated_at", "source", "version", "Status"
    ],
    "pharmacological": [
        "Pharmacological_Class_ID", "Pharmacological_Class_Name", "Mechanism_of_Action", 
        "Parent_Class_ID", "Reference_Source", "created_at", "updated_at", "source", "version", "Status"
    ],
    "generic_atc_mapping": [
        "Mapping_ID", "Generic_ID", "ATC_ID", "Is_Primary", "created_at", "updated_at", "source", "version", "Status"
    ],
    "generic_class_mapping": [
        "Mapping_ID", "Generic_ID", "Therapeutic_Class_ID", "Pharmacological_Class_ID", 
        "Is_Primary", "created_at", "updated_at", "source", "version", "Status"
    ]
}

# Mandatory Fields for Business Logic
MANDATORY_COLUMNS: Final = {
    "generic": ["Generic_ID", "Generic_Name"],
    "brand": ["Brand_ID", "Brand_Name", "Generic_ID", "Company_ID"],
    "company": ["Company_ID", "Company_Name"],
    "product": ["Product_ID", "Generic_ID"],
    "atc": ["ATC_Code", "ATC_Name"],
    "therapeutic": ["Therapeutic_Class_ID", "Therapeutic_Class_Name"],
    "pharmacological": ["Pharmacological_Class_ID", "Pharmacological_Class_Name"],
    "generic_atc_mapping": ["Mapping_ID", "Generic_ID", "ATC_ID"],
    "generic_class_mapping": ["Mapping_ID", "Generic_ID", "Therapeutic_Class_ID", "Pharmacological_Class_ID"]
}

FOREIGN_KEY_RELATIONSHIPS: Final = {

    "brand": [
        ("Generic_ID", "generic", "Generic_ID"),
        ("Company_ID", "company", "Company_ID"),
    ],

    "product": [
        ("Generic_ID", "generic", "Generic_ID"),
    ],

    "generic_atc_mapping": [
        ("Generic_ID", "generic", "Generic_ID"),
        ("ATC_ID", "atc", "ATC_ID"),
    ],

    "generic_class_mapping": [
        ("Generic_ID", "generic", "Generic_ID"),
        ("Therapeutic_Class_ID", "therapeutic", "Therapeutic_Class_ID"),
        ("Pharmacological_Class_ID", "pharmacological", "Pharmacological_Class_ID"),
    ]
}
# File Mapping Registry
FILE_MAP: Final = {
    "generic": ("medicine", "generic_master.csv"),
    "brand": ("medicine", "brand_master.csv"),
    "company": ("medicine", "company_master.csv"),
    "product": ("product", "product_master.csv"),
    "atc": ("medicine", "atc_master.csv"),
    "therapeutic": ("medicine", "therapeutic_class_master.csv"),
    "pharmacological": ("medicine", "pharmacological_class_master.csv"),
    "generic_atc_mapping": ("mapping", "generic_atc_mapping.csv"),
    "generic_class_mapping": ("mapping", "generic_class_mapping.csv")
}

# Directories (Adjusted for Project Root)
BASE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR: Final = os.path.join(BASE_ROOT, "logs")
REPORT_DIR: Final = os.path.join(BASE_ROOT, "reports")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "database_audit.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filemode="w"
)

class DatabaseAudit:
    """Comprehensive Database Audit Framework."""

    def __init__(self):
        self.start_time = time.time()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.logger = logger
        
        self.paths = {
            "medicine": os.path.join(self.base_dir, "database", "medicine"),
            "product": os.path.join(self.base_dir, "database", "product"),
            "mapping": os.path.join(self.base_dir, "database", "mapping")
        }

        self.tables: Dict[str, pd.DataFrame] = {}
        
        self.report = {
            "version": "1.0.0",
            "phase": "13.6",
            "generated_at": datetime.datetime.now().isoformat(),
            "status": STATUS_PASS,
            "health_score": 100,
            "statistics": {category: {} for category in REQUIRED_SCHEMAS.keys()},
            "load_summary": {},
            "errors": [],
            "warnings": []
        }

    def _log_header(self):
        self.logger.info("==========================================")
        self.logger.info("DATABASE INTEGRITY AUDIT STARTED")
        self.logger.info(f"Phase : {self.report['phase']}")
        self.logger.info(f"Version : {self.report['version']}")
        self.logger.info("==========================================")

    def load_tables(self) -> bool:
        self.logger.info("Starting file loading...")
        success = True
        stats = {"loaded": 0, "failed": 0}

        for key, (folder, filename) in FILE_MAP.items():
            file_path = os.path.join(self.paths.get(folder, ""), filename)
            
            if not os.path.exists(file_path):
                msg = f"Missing file: {filename} in {folder}"
                self.logger.error(msg)
                self.report["errors"].append(msg)
                success = False
                stats["failed"] += 1
                continue
            
            try:
                df = pd.read_csv(file_path, encoding="utf-8")
                if df.empty:
                    self.logger.warning(f"File is empty: {filename}")
                    self.report["warnings"].append(f"Empty file: {filename}")
                
                self.tables[key] = df
                stats["loaded"] += 1
                self.logger.info(f"Loaded {filename} ({len(df)} rows)")
            except Exception as e:
                msg = f"Failed to read {filename}: {str(e)}"
                self.logger.error(msg)
                self.report["errors"].append(msg)
                success = False
                stats["failed"] += 1
        
        self.report["load_summary"] = stats
        self.logger.info(f"Load Summary: {stats['loaded']} Loaded, {stats['failed']} Failed.")
        return success

    def generate_statistics(self):
        self.logger.info("Generating database statistics...")
        for key, df in self.tables.items():
            memory_usage = df.memory_usage(deep=True).sum() / 1024
            stats = {
                "rows": int(len(df)),
                "columns": int(len(df.columns)),
                "memory_kb": float(round(memory_usage, 2)),
                "null_values": int(df.isnull().sum().sum()),
                "duplicate_rows": int(df.duplicated().sum())
            }
            self.report["statistics"][key] = stats
            self.logger.info(f"Stats for {key}: Rows={stats['rows']}, Cols={stats['columns']}, "
                        f"Nulls={stats['null_values']}, Dups={stats['duplicate_rows']}")
        self.logger.info("Statistics generation complete.")

    def validate_schema(self):
        self.logger.info("Validating schemas...")
        self.report["schema_validation"] = {}
        for key, required_cols in REQUIRED_SCHEMAS.items():
            if key not in self.tables:
                msg = f"{key}: Table not loaded."
                self.logger.warning(msg)
                self.report["warnings"].append(msg)
                self.report["schema_validation"][key] = {"status": STATUS_WARN, "missing_columns": []}
                continue
            actual_cols = self.tables[key].columns.tolist()
            missing_cols = [col for col in required_cols if col not in actual_cols]
            status = STATUS_PASS if not missing_cols else STATUS_FAIL
            if status == STATUS_FAIL:
                self.report["status"] = STATUS_FAIL
                self.report["errors"].append(f"{key}: Missing columns: {missing_cols}")
            self.report["schema_validation"][key] = {"status": status, "missing_columns": missing_cols}
        self.logger.info("Schema validation complete.")

    def check_duplicates(self):
        self.logger.info("Checking for duplicate records...")
        self.report["duplicate_validation"] = {}
        dupe_config = {
            "generic": ("Generic_ID", "Generic_Name"),
            "brand": ("Brand_ID", "Brand_Name"),
            "company": ("Company_ID", "Company_Name"),
            "product": ("Product_ID", None),
            "atc": ("ATC_Code", "ATC_Name"),
            "therapeutic": ("Therapeutic_Class_ID", "Therapeutic_Class_Name"),
            "pharmacological": ("Pharmacological_Class_ID", "Pharmacological_Class_Name"),
            "generic_atc_mapping": ("Mapping_ID", None),
            "generic_class_mapping": ("Mapping_ID", None)
        }
        for key, (id_col, name_col) in dupe_config.items():
            if key not in self.tables:
                self.logger.warning(f"Skipping duplicate check: {key} not loaded.")
                continue
            df = self.tables[key]
            dup_ids = int(df[id_col].duplicated().sum()) if id_col and id_col in df.columns else 0
            dup_names = int(df[name_col].duplicated().sum()) if name_col and name_col in df.columns else 0
            status = STATUS_PASS if (dup_ids == 0 and dup_names == 0) else STATUS_FAIL
            if status == STATUS_FAIL:
                self.report["status"] = STATUS_FAIL
                self.report["errors"].append(f"{key}: {dup_ids} duplicate IDs, {dup_names} duplicate names found.")
            self.report["duplicate_validation"][key] = {"status": status, "duplicate_ids": dup_ids, "duplicate_names": dup_names}
        self.logger.info("Duplicate validation complete.")

    def check_missing_values(self):
        """Detect missing mandatory fields using a dedicated registry."""
        self.logger.info("Checking for missing mandatory values...")
        self.report["missing_values_validation"] = {}

        for key, mandatory_cols in MANDATORY_COLUMNS.items():
            if key not in self.tables:
                msg = f"Missing mandatory table: {key}"
                self.logger.error(msg)
                self.report["errors"].append(msg)
                self.report["status"] = STATUS_FAIL
                self.report["missing_values_validation"][key] = {"status": STATUS_FAIL, "missing": "TABLE_MISSING"}
                continue

            df = self.tables[key]
            missing_details = {}
            total_missing = 0

            for col in mandatory_cols:
                if col in df.columns:
                    missing_count = int(df[col].replace(r'^\s*$', None, regex=True).isna().sum())
                    if missing_count > 0:
                        missing_details[col] = missing_count
                        total_missing += missing_count
                else:
                    missing_details[col] = "COLUMN_MISSING"
                    total_missing += 1

            status = STATUS_PASS if total_missing == 0 else STATUS_FAIL
            if status == STATUS_FAIL:
                self.report["status"] = STATUS_FAIL
                self.logger.error(f"Missing Value Validation | {key} : {status} | Missing details: {missing_details}")
            else:
                self.logger.info(f"Missing Value Validation | {key} : {status}")

            self.report["missing_values_validation"][key] = {
                "status": status,
                "total_missing": total_missing,
                "checked_columns": mandatory_cols,
                "missing": missing_details
            }
        self.logger.info("Missing value validation complete.")

    def check_foreign_keys(self):
        """
        Validate referential integrity between database tables.
        """
        self.logger.info("=" * 60)
        self.logger.info("Foreign Key Validation")
        self.logger.info("=" * 60)

        self.report["foreign_key_validation"] = {}
        summary = {"checked_relationships": 0, "failed_relationships": 0}

        for table_name, relationships in FOREIGN_KEY_RELATIONSHIPS.items():
            result = {"status": STATUS_PASS, "violations": {}}
            child_df = self.tables.get(table_name)

            if child_df is None:
                msg = f"Missing table: {table_name}"
                self.logger.error(msg)
                self.report["errors"].append(msg)
                self.report["status"] = STATUS_FAIL
                result["status"] = STATUS_FAIL
                result["violations"]["TABLE"] = msg
                self.report["foreign_key_validation"][table_name] = result
                continue

            for fk_column, parent_table, parent_column in relationships:
                summary["checked_relationships"] += 1
                parent_df = self.tables.get(parent_table)

                if parent_df is None:
                    msg = f"Missing parent table: {parent_table}"
                    self.logger.error(msg)
                    self.report["errors"].append(msg)
                    self.report["status"] = STATUS_FAIL
                    result["status"] = STATUS_FAIL
                    result["violations"][fk_column] = msg
                    continue

                # Guard against missing columns
                if fk_column not in child_df.columns:
                    msg = f"Column {fk_column} missing in {table_name}"
                    self.logger.error(msg)
                    self.report["errors"].append(msg) # Consistency improvement
                    self.report["status"] = STATUS_FAIL # Consistency improvement
                    result["status"] = STATUS_FAIL
                    result["violations"][fk_column] = msg
                    continue
                
                if parent_column not in parent_df.columns:
                    msg = f"Column {parent_column} missing in {parent_table}"
                    self.logger.error(msg)
                    self.report["errors"].append(msg)
                    self.report["status"] = STATUS_FAIL # Consistency improvement
                    result["status"] = STATUS_FAIL
                    result["violations"][parent_column] = msg
                    continue

                # Exclude NaNs, validate only non-null references
                valid_child = child_df[fk_column].dropna()
                invalid = ~valid_child.isin(parent_df[parent_column])
                invalid_count = int(invalid.sum())

                if invalid_count > 0:
                    summary["failed_relationships"] += 1
                    result["status"] = STATUS_FAIL
                    self.report["status"] = STATUS_FAIL
                    
                    invalid_values = child_df.loc[valid_child[invalid].index, fk_column].drop_duplicates().tolist()
                    result["violations"][fk_column] = {"count": invalid_count, "invalid_values": invalid_values}
                    
                    self.logger.error(f"{table_name}.{fk_column} -> {parent_table}.{parent_column} : {invalid_count} invalid(s)")
                    self.logger.error(f"Invalid values: {invalid_values}")
                else:
                    self.logger.info(f"{table_name}.{fk_column} -> {parent_table}.{parent_column} : PASS")

            self.report["foreign_key_validation"][table_name] = result

        self.report["foreign_key_summary"] = summary
        self.logger.info(f"Foreign key validation complete. Summary: {summary}")

    def check_mapping_integrity(self):
        """
        Validate business integrity of mapping tables.
        Includes duplicate checks and robust boolean primary key validation.
        """
        self.logger.info("=" * 60)
        self.logger.info("Mapping Integrity Validation")
        self.logger.info("=" * 60)

        self.report["mapping_integrity_validation"] = {}
        total_failed = 0

        for table_name, rules in MAPPING_RULES.items():
            result = {
                "status": STATUS_PASS,
                "duplicate_mappings": 0,
                "multiple_primary": 0,
                "details": {}
            }

            df = self.tables.get(table_name)

            # 1. Graceful check for table existence
            if df is None or df.empty:
                msg = f"Missing or empty mapping table: {table_name}"
                self._handle_validation_failure(table_name, result, msg)
                continue

            # 2. Guard for missing columns
            required_cols = rules["duplicate_keys"] + [rules["primary_column"]]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                msg = f"Missing columns in {table_name}: {missing_cols}"
                self._handle_validation_failure(table_name, result, msg)
                continue

            # 3. Validate Duplicate Keys
            duplicate_rows = df.duplicated(subset=rules["duplicate_keys"], keep=False)
            duplicate_count = int(duplicate_rows.sum())
            if duplicate_count > 0:
                result.update({"status": STATUS_FAIL, "duplicate_mappings": duplicate_count})
                result["details"]["duplicate_rows"] = df.loc[duplicate_rows, rules["duplicate_keys"]].to_dict("records")

            # 4. Robust Boolean Normalization for 'Is_Primary'
            primary_mask = (
                df[rules["primary_column"]]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin(["true", "1", "yes"])
            )
            
            # 5. Validate Primary Constraint
            multiple_primary_counts = df[primary_mask].groupby(rules["primary_group"]).size()
            multiple_groups = multiple_primary_counts[multiple_primary_counts > 1]
            
            if not multiple_groups.empty:
                result.update({"status": STATUS_FAIL, "multiple_primary": int(multiple_groups.sum())})
                result["details"]["multiple_primary_groups"] = multiple_groups.index.tolist()

            if result["status"] == STATUS_FAIL:
                total_failed += 1
                self.report["status"] = STATUS_FAIL
                self.logger.error(f"{table_name}: FAIL")
            else:
                self.logger.info(f"{table_name}: PASS")

            self.report["mapping_integrity_validation"][table_name] = result

        # 6. Summary Section
        self.report["mapping_integrity_summary"] = {
            "checked_tables": len(MAPPING_RULES),
            "failed_tables": total_failed
        }
        self.logger.info("Mapping integrity validation complete.")

    def _handle_validation_failure(self, table_name, result, msg):
        """Helper to update report and log failures."""
        self.logger.error(msg)
        self.report["errors"].append(msg)
        self.report["status"] = STATUS_FAIL
        result["status"] = STATUS_FAIL
        result["details"]["TABLE"] = msg
        self.report["mapping_integrity_validation"][table_name] = result

        # Scoring Weights for Health Calculation
    VALIDATION_WEIGHTS: Final = {
        "load_tables": 10,
        "schema_validation": 20,
        "duplicate_validation": 20,
        "missing_values_validation": 20,
        "foreign_key_validation": 20,
    "mapping_integrity_validation": 10,
    }

    def calculate_health_score(self):
        """
        Calculates overall database health score.
        Uses self.report as the source of truth for all validation states.
        """
           # Defensive Programming: Ensure weights are configured correctly
        if sum(self.VALIDATION_WEIGHTS.values()) != 100:
            raise ValueError(f"self.VALIDATION_WEIGHTS must sum to 100, found: {sum(self.VALIDATION_WEIGHTS.values())}")
        score = 0
        
        # 1. Load Tables Weight
        if self.report.get("load_summary", {}).get("failed", 1) == 0:
            score += self.VALIDATION_WEIGHTS["load_tables"]

        # 2. Map validation sections to weights
        checks = {
            "schema_validation": "schema_validation",
            "duplicate_validation": "duplicate_validation",
            "missing_values_validation": "missing_values_validation",
            "foreign_key_validation": "foreign_key_validation",
            "mapping_integrity_validation": "mapping_integrity_validation"
        }

        for weight_key, report_key in checks.items():
            validation_data = self.report.get(report_key)
            
            if not isinstance(validation_data, dict):
                continue

            # Logic Distinction: Explicitly handle single vs nested results
            if "status" in validation_data:
                # Path A: Single validator result
                if validation_data.get("status") == STATUS_PASS:
                    score += self.VALIDATION_WEIGHTS[weight_key]
            else:
                # Path B: Nested table results (e.g., dictionary of tables)
                # Filter out summary keys to avoid status-missing errors
                table_results = [
                    val for key, val in validation_data.items() 
                    if not key.endswith("_summary") and isinstance(val, dict)
                ]
                
                if table_results and all(item.get("status") == STATUS_PASS for item in table_results):
                    score += self.VALIDATION_WEIGHTS[weight_key]

        # 3. Calculate and store results
        self.report["health_score"] = score
        self.report["health_grade"] = self._get_health_grade(score)
    def _get_health_grade(self, score: int) -> str:
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 40:
            return "Poor"
        return "Critical"    

        self.logger.info(f"Health Score calculated: {score}/100 ({self.report['health_grade']})")
        return score

    def save_report(self):
        """Save audit report as JSON."""
        report_path = os.path.join(
            REPORT_DIR,
            f"audit_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=4, ensure_ascii=False)

        self.logger.info(f"Report saved to {report_path}")


    def build_report(self) -> Dict[str, Any]:
        """Finalize and return audit report."""
        self.report["execution_time"] = round(
            time.time() - self.start_time,
            4
        )

        self.logger.info("DATABASE AUDIT COMPLETE")

        return self.report

def run_database_audit():
    audit = DatabaseAudit()
    audit._log_header()
    if audit.load_tables():
        audit.generate_statistics()
        audit.validate_schema()
        audit.check_duplicates()
        audit.check_missing_values() 
        audit.check_foreign_keys()
        audit.check_mapping_integrity()
        audit.calculate_health_score()
    else:
        audit.report["status"] = STATUS_FAIL
    audit.save_report()
    return audit.build_report()

if __name__ == "__main__":
    print(run_database_audit())