"""
Governance domain exceptions.

Provides a unified error hierarchy for the Governance Layer.
All exceptions inherit from GovernanceError, ensuring consistent 
error handling across the Policy Engine and supporting modules.
"""

from typing import Any, Optional, Dict

class GovernanceError(Exception):
    """Base exception for all Governance layer errors."""
    def __init__(self, message: str, error_code: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}

class ConfigurationError(GovernanceError):
    """Base class for configuration related errors."""
    pass

class PolicyLoadError(ConfigurationError):
    """Raised when the policy file cannot be loaded."""
    pass

class ConfigurationParseError(ConfigurationError):
    """Raised when the configuration schema is invalid."""
    pass

class ValidationError(GovernanceError):
    """Base class for governance validation errors."""
    pass

class InvalidRuleError(ValidationError):
    """Raised when a validation rule is logically invalid."""
    pass

class InvalidThresholdError(ValidationError):
    """Raised when a threshold value is out of bounds."""
    pass

class PolicyEvaluationError(GovernanceError):
    """Raised when the Policy Engine fails to reach a deterministic decision."""
    pass

class GovernanceDecisionError(GovernanceError):
    """Raised when a decision transition is invalid."""
    pass

class ReportGenerationError(GovernanceError):
    """Raised when the Audit Report or JSON/CSV serialization fails."""
    pass