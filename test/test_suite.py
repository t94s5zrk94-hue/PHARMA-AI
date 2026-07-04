import logging
from engine.generic_resolver import GenericResolver
from engine.combination_parser import CombinationParser
from engine.validation_gate import ValidationGate

class PharmaTestSuite:
    def __init__(self):
        self.resolver = GenericResolver()
        self.parser = CombinationParser()
        # API Fixed: ValidationGate હવે માત્ર stats લે છે
        self.gate = ValidationGate({"max_errors": 0, "max_review_records": 100, "min_success_rate": 80.0})
        self.results = {"passed": 0, "failed": 0}

    def assert_test(self, condition, message):
        if condition:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            logging.error(f"Test Failed: {message}")

    def run_all(self):
        print("--- [RC1] Regression Suite Started ---")
        self.test_generic_resolver()
        self.test_combination_parser()
        self.test_validation_gate()
        print(f"--- Testing Complete. Passed: {self.results['passed']}, Failed: {self.results['failed']} ---")

    def test_generic_resolver(self):
        # 1. Exact Match with Metadata Assertion
        res = self.resolver.resolve("Paracetamol")
        self.assert_test(res['generic_id'] == "GEN000001", "Exact Match Logic")
        self.assert_test(res['confidence'] == 1.0, "Exact Match Confidence")
        
        # 2. Unknown Case
        res_unk = self.resolver.resolve("FakeDrug123")
        self.assert_test(res_unk['match_type'] == "unknown", "Unknown Detection")

    def test_combination_parser(self):
        # Combination Detection
        res = self.parser.parse("Amoxicillin + Clavulanic Acid")
        self.assert_test(res['is_combination'] == True, "Combo Detection")
        self.assert_test(len(res['components']) == 2, "Component Count")

    def test_validation_gate(self):
        # Policy Threshold Check
        stats = {"input": 100, "success": 90, "review": 5, "errors": 0}
        result = self.gate.validate(stats)
        self.assert_test(result['passed'] == True, "Validation Pass Logic")

if __name__ == "__main__":
    suite = PharmaTestSuite()
    suite.run_all()