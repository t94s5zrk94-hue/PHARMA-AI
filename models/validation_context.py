from dataclasses import dataclass, field
from typing import List, Mapping, Any
from enum import Enum

class ValidationStatus(Enum):
    VALID = "valid"
    WARNING = "warning"
    INVALID = "invalid"

@dataclass(frozen=True, slots=True)
class ValidationContext:
    """
    Tracks clinical data audit results and validity status.
    """
    missing_fields: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    confidence_score: float = 1.0

    def __post_init__(self):
        """Range validation for confidence score."""
        if not (0.0 <= self.confidence_score <= 1.0):
            raise ValueError("Confidence score must be between 0.0 and 1.0")

    @property
    def status(self) -> ValidationStatus:
        """Derived status based on validation rules."""
        if self.missing_fields:
            return ValidationStatus.INVALID
        if len(self.warnings) >= 3:
            return ValidationStatus.INVALID
        if len(self.warnings) > 0:
            return ValidationStatus.WARNING
        return ValidationStatus.VALID

    @property
    def is_valid(self) -> bool:
        """Derived property indicating usability of the context."""
        return self.status != ValidationStatus.INVALID

    @staticmethod
    def _parse_string_list(value: Any) -> List[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            return [value.strip()] if value.strip() else []
        return []

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ValidationContext":
        """Maps audit results with list and range parsing."""
        return cls(
            missing_fields=cls._parse_string_list(data.get("Missing_Fields")),
            warnings=cls._parse_string_list(data.get("Warnings")),
            confidence_score=float(data.get("Confidence_Score", 1.0))
        )