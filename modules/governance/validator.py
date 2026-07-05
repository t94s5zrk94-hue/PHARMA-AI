"""
Policy validator module.
Performs logic validation on PolicyConfig. Adheres to 'Validate Only' principle.
"""

from typing import Tuple, List
from datetime import datetime, timezone
from .models import PolicyConfig, ValidationResult, ValidationSummary, ValidationReport
from .enums import ValidationStage, ValidationStatus, Severity

class PolicyValidator:
    """
    Validates PolicyConfig. Orchestrates validation rules.
    """

    @staticmethod
    def validate(config: PolicyConfig, run_id: str, correlation_id: str) -> ValidationReport:
        """
        Validates PolicyConfig and returns an immutable ValidationReport.
        """
        results: List[ValidationResult] = []

        # Orchestrate validation rules
        results.append(PolicyValidator._validate_weights(config))
        results.append(PolicyValidator._validate_threshold_hierarchy(config))

        summary = PolicyValidator._calculate_summary(tuple(results))

        return ValidationReport(
            run_id=run_id,
            correlation_id=correlation_id,
            validation_timestamp=datetime.now(timezone.utc),
            validation_version="1.0.0",
            policy_version=config.version,
            results=tuple(results),
            summary=summary
        )

    @staticmethod
    def _validate_weights(config: PolicyConfig) -> ValidationResult:
        """Rule: Quality weights must sum to 1.0"""
        weights_sum = sum([config.weights.critical, config.weights.high, 
                           config.weights.medium, config.weights.low])
        
        is_valid = (0.99 <= weights_sum <= 1.01)
        return ValidationResult(
            rule_id="RULE-GOV-001",
            stage=ValidationStage.GOVERNANCE,
            status=ValidationStatus.PASS if is_valid else ValidationStatus.FAIL,
            severity=Severity.CRITICAL,
            message=f"Weights sum to {weights_sum:.2f}",
            recommendation=("Adjust weights to sum to 1.0",) if not is_valid else (),
            component="PolicyValidator"
        )

    @staticmethod
    def _validate_threshold_hierarchy(config: PolicyConfig) -> ValidationResult:
        """Rule: Thresholds must be strictly Prod > Acceptable > NeedsReview"""
        t = config.thresholds
        is_valid = (t.production_ready > t.acceptable > t.needs_review)
        
        return ValidationResult(
            rule_id="RULE-GOV-002",
            stage=ValidationStage.GOVERNANCE,
            status=ValidationStatus.PASS if is_valid else ValidationStatus.FAIL,
            severity=Severity.HIGH,
            message="Threshold hierarchy order check",
            recommendation=("Ensure Prod > Acceptable > NeedsReview",) if not is_valid else (),
            component="PolicyValidator"
        )

    @staticmethod
    def _calculate_summary(results: Tuple[ValidationResult, ...]) -> ValidationSummary:
        """Computes aggregate metrics from ValidationResults."""
        return ValidationSummary(
            total=len(results),
            passed=sum(1 for r in results if r.status == ValidationStatus.PASS),
            failed=sum(1 for r in results if r.status == ValidationStatus.FAIL),
            warnings=sum(1 for r in results if r.status == ValidationStatus.WARN),
            critical=sum(1 for r in results if r.severity == Severity.CRITICAL),
            high=sum(1 for r in results if r.severity == Severity.HIGH),
            medium=sum(1 for r in results if r.severity == Severity.MEDIUM),
            low=sum(1 for r in results if r.severity == Severity.LOW),
            info=sum(1 for r in results if r.severity == Severity.INFO)
        )