import logging

class ValidationGate:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config 

    def validate(self, stats):
        """Pipeline metrics પરથી Release Decision લે છે."""
        passed = True
        reasons = []
        
        # 1. Defensive Stats Check (KeyError protection)
        errors = stats.get("errors", 0)
        review = stats.get("review", 0)
        total = stats.get("input", 0)
        success = stats.get("success", 0)
        
        # 2. Validation Rules
        if errors > self.config.get("max_errors", 0):
            passed = False
            reasons.append(f"Errors threshold exceeded: {errors}")
            
        if review > self.config.get("max_review_records", 500):
            passed = False
            reasons.append(f"Review queue threshold exceeded: {review}")
            
        success_rate = (success / max(1, total)) * 100
        if success_rate < self.config.get("min_success_rate", 98.0):
            passed = False
            reasons.append(f"Success rate too low: {success_rate:.2f}%")
            
        # 3. Logging & Reporting
        if passed:
            self.logger.info(f"Validation Passed. Success Rate: {success_rate:.2f}%")
        else:
            self.logger.critical(f"Validation Failed. Reasons: {', '.join(reasons)}")
            
        return {
            "passed": passed,
            "reasons": reasons,
            "stats_snapshot": stats
        }