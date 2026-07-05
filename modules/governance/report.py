"""
Audit report builder module.

Consolidates ValidationReport and GovernanceDecision into an immutable 
Audit Package (JSON). This provides the final clinical traceability artifact.
"""

import json
from dataclasses import asdict
from typing import Any, Dict
from .models import ValidationReport, GovernanceDecision
from .exceptions import ReportGenerationError

class AuditReportBuilder:
    """
    Builds structured audit artifacts from governance outcomes.
    Adheres to the traceability requirements of ADR-005.
    """

    @staticmethod
    def build_audit_package(report: ValidationReport, decision: GovernanceDecision) -> Dict[str, Any]:
        """
        Consolidates reports and decisions into a single audit artifact.
        """
        try:
            return {
                "metadata": {
                    "audit_version": "1.0.0",
                    "governance_version": "1.0.0",
                    "run_id": decision.run_id,
                    "correlation_id": decision.correlation_id,
                    "timestamp": decision.decision_timestamp.isoformat(),
                    "policy_version": decision.policy_version,
                    "integrity_hash": "placeholder_hash" 
                },
                "validation": asdict(report),
                "decision": asdict(decision)
            }
        except Exception as e:
            raise ReportGenerationError(
                f"Failed to build audit package: {str(e)}",
                "GOV-006"
            ) from e

    @staticmethod
    def to_json(audit_package: Dict[str, Any], pretty: bool = True) -> str:
        """Serializes the audit package to JSON string."""
        try:
            return json.dumps(audit_package, indent=4 if pretty else None, default=str)
        except (TypeError, ValueError) as e:
            raise ReportGenerationError(
                f"JSON serialization failed: {str(e)}",
                "GOV-006"
            ) from e