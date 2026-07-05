"""
Governance domain models.

All models in this module are immutable and represent the canonical
objects exchanged between the Validation Engine, Policy Engine,
Quality Gate, and Audit Layer.
"""

from dataclasses import dataclass
from typing import Tuple
from datetime import datetime
from .enums import ValidationStage, ValidationStatus, Severity, ReleaseStatus

__all__ = [
    "ValidationResult",
    "ValidationSummary",
    "ValidationReport",
    "QualityWeights",
    "Thresholds",
    "PolicyConfig",
    "GovernanceDecision",
]

@dataclass(frozen=True)
class ValidationResult:
    """Represents the result of a single validation rule."""
    rule_id: str
    stage: ValidationStage
    status: ValidationStatus
    severity: Severity
    message: str
    recommendation: Tuple[str, ...]
    component: str  # TODO: Refactor to ComponentType Enum later

@dataclass(frozen=True)
class ValidationSummary:
    """Aggregated metrics from a validation run."""
    total: int
    passed: int
    failed: int
    warnings: int
    critical: int
    high: int
    medium: int
    low: int
    info: int

@dataclass(frozen=True)
class ValidationReport:
    """Immutable validation results produced by the Validation Engine."""
    run_id: str
    correlation_id: str
    validation_timestamp: datetime
    validation_version: str
    policy_version: str
    results: Tuple[ValidationResult, ...]
    summary: ValidationSummary

@dataclass(frozen=True)
class QualityWeights:
    """Configurable weights for scoring logic."""
    critical: float
    high: float
    medium: float
    low: float

@dataclass(frozen=True)
class Thresholds:
    """Release quality thresholds."""
    production_ready: float
    acceptable: float
    needs_review: float

@dataclass(frozen=True)
class PolicyConfig:
    """Governance policy configuration."""
    version: str
    weights: QualityWeights
    thresholds: Thresholds
    effective_date: datetime
    config_hash: str

@dataclass(frozen=True)
class GovernanceDecision:
    """The final decision produced by the Policy Engine."""
    run_id: str
    correlation_id: str
    quality_score: float
    release_status: ReleaseStatus
    passed_rules: Tuple[str, ...]
    failed_rules: Tuple[str, ...]
    warnings: Tuple[str, ...]
    recommendation: Tuple[str, ...]
    decision_reason: str
    policy_version: str
    decision_timestamp: datetime