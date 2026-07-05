"""
Policy engine module.

The central decision-making component of the Governance Layer.
Calculates quality scores and determines release status based on
validated reports and policy configuration.
"""

from datetime import datetime, timezone
from typing import List, Tuple
from .models import PolicyConfig, ValidationReport, GovernanceDecision
from .enums import ReleaseStatus, ValidationStatus, Severity
from .exceptions import PolicyEvaluationError

class PolicyEngine:
    """
    Evaluates ValidationReport against PolicyConfig to produce GovernanceDecision.
    Adheres to 'Stateless' and 'Deterministic' principles.
    """

    @staticmethod
    def evaluate(report: ValidationReport, config: PolicyConfig) -> GovernanceDecision:
        """
        Evaluates the governance state and returns an immutable decision.
        Scale used: 0.0 to 1.0 (float).
        """
        try:
            # 1. Calculate Score
            score = PolicyEngine._calculate_score(report, config)
            
            # 2. Determine Status
            status = PolicyEngine._determine_release_status(score, config)
            
            # 3. Aggregate Rules and Warnings (Deterministic order)
            passed = tuple(r.rule_id for r in report.results if r.status == ValidationStatus.PASS)
            failed = tuple(r.rule_id for r in report.results if r.status == ValidationStatus.FAIL)
            warnings = tuple(r.rule_id for r in report.results if r.status == ValidationStatus.WARN)
            
            # 4. Generate Recommendations (Unique and Deterministic)
            recs = PolicyEngine._generate_recommendations(report)

            reason = (f"Quality score: {score:.4f} | "
                      f"Status: {status.value} | "
                      f"Policy version: {config.version}")

            return GovernanceDecision(
                run_id=report.run_id,
                correlation_id=report.correlation_id,
                quality_score=score,
                release_status=status,
                passed_rules=passed,
                failed_rules=failed,
                warnings=warnings,
                recommendation=recs,
                decision_reason=reason,
                policy_version=config.version,
                decision_timestamp=datetime.now(timezone.utc)
            )
        except Exception as e:
            raise PolicyEvaluationError(
                f"Policy evaluation failed: {str(e)}",
                "GOV-004",
                {"exception": type(e).__name__}
            ) from e

    @staticmethod
    def _calculate_score(report: ValidationReport, config: PolicyConfig) -> float:
        """Calculates weighted quality score on 0.0 - 1.0 scale."""
        penalty = 0.0
        for r in report.results:
            if r.status == ValidationStatus.FAIL:
                if r.severity == Severity.CRITICAL: penalty += config.weights.critical
                elif r.severity == Severity.HIGH: penalty += config.weights.high
                elif r.severity == Severity.MEDIUM: penalty += config.weights.medium
                elif r.severity == Severity.LOW: penalty += config.weights.low
        
        # Ensures score is clamped between 0.0 and 1.0
        return max(0.0, min(1.0, 1.0 - penalty))

    @staticmethod
    def _determine_release_status(score: float, config: PolicyConfig) -> ReleaseStatus:
        """Maps score to release status based on 0.0-1.0 thresholds."""
        if score >= config.thresholds.production_ready:
            return ReleaseStatus.PRODUCTION_READY
        if score >= config.thresholds.acceptable:
            return ReleaseStatus.ACCEPTABLE
        if score >= config.thresholds.needs_review:
            return ReleaseStatus.NEEDS_REVIEW
        return ReleaseStatus.FAILED

    @staticmethod
    def _generate_recommendations(report: ValidationReport) -> Tuple[str, ...]:
        """Extracts unique recommendations in deterministic order."""
        recs = []
        for r in report.results:
            if r.status == ValidationStatus.FAIL:
                recs.extend(list(r.recommendation))
        
        # Maintains order and uniqueness
        return tuple(dict.fromkeys(recs))