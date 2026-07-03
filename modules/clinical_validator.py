"""Clinical QA Engine for Pharma AI - v3.0 (Production Ready)."""
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class ClinicalValidator:
    def __init__(self):
        from modules.interaction import DrugInteraction
        self.interaction_engine = DrugInteraction()
        self.test_history = [] 
        self.total_tests = 0
        self.passed_tests = 0

    def _record_result(self, name: str, passed: bool):
        self.total_tests += 1
        if passed: self.passed_tests += 1
        self.test_history.append({"test": name, "status": "PASS" if passed else "FAIL"})
        return passed

    def validate_interaction(self, row):
        """નવા schema અને robust validation સાથે."""
        m1 = row.get("medicine_1", "")
        m2 = row.get("medicine_2", "")
        expected = row.get("expected_severity", "")
        
        result = self.interaction_engine.check_interaction(m1, m2)
        
        # Robust validation: Severity + Success + Non-empty interaction
        passed = (
            result.get("severity", "").lower() == str(expected).lower() and
            result.get("success", False) and
            bool(result.get("interaction"))
        )
        
        self._record_result(f"INT:{row.get('test_id')}", passed)
        return passed

    def run_regression_suite(self, csv_path: str):
        """Runs bulk test cases with error handling for UI integration."""
        import pandas as pd
        try:
            df = pd.read_csv(csv_path)
            required = ["test_id", "category", "medicine_1", "medicine_2", "expected_severity"]
            if not all(col in df.columns for col in required):
                raise ValueError(f"CSV missing columns. Required: {required}")
            
            for _, row in df.iterrows():
                if row['category'] == 'Interaction':
                    self.validate_interaction(row)
            
            return {"success": True, "summary": self.get_report_summary()}
        except Exception as e:
            logger.error(f"Regression Suite failed: {e}")
            return {"success": False, "error": str(e)}

    def get_report_summary(self) -> dict:
        pass_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        return {
            "total": self.total_tests,
            "passed": self.passed_tests,
            "failed": self.total_tests - self.passed_tests,
            "pass_rate": round(pass_rate, 2)
        }

    def export_report(self, folder="reports"):
        """Clean report export to specified folder."""
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        filename = f"{folder}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump({"summary": self.get_report_summary(), "history": self.test_history}, f, indent=4)
        logger.info(f"Report exported to {filename}")