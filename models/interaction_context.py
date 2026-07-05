from dataclasses import dataclass, field
from typing import List, Mapping, Any
from enum import Enum

class InteractionSeverity(Enum):
    NONE = "none"
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    SEVERE = "severe"

@dataclass(frozen=True, slots=True)
class InteractionContext:
    """
    Encapsulates drug-drug interactions with strict Fail-Fast severity parsing.
    """
    interactions: List[str] = field(default_factory=list)
    severity_level: InteractionSeverity = InteractionSeverity.NONE
    clinical_warnings: List[str] = field(default_factory=list)

    @property
    def is_safe(self) -> bool:
        """Derived property: System is unsafe if severity is MAJOR or SEVERE."""
        return self.severity_level not in {InteractionSeverity.MAJOR, InteractionSeverity.SEVERE}

    @staticmethod
    def _parse_string_list(value: Any) -> List[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            return [value.strip()] if value.strip() else []
        return []

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "InteractionContext":
        """Maps interaction data with strict validation."""
        raw_severity = str(data.get("Severity_Level", "none")).lower().strip()
        
        try:
            severity = InteractionSeverity(raw_severity)
        except ValueError:
            # Policy: Fail Fast for invalid clinical data
            raise ValueError(f"Invalid InteractionSeverity: {raw_severity}")

        return cls(
            interactions=cls._parse_string_list(data.get("Interactions")),
            severity_level=severity,
            clinical_warnings=cls._parse_string_list(data.get("Clinical_Warnings"))
        )