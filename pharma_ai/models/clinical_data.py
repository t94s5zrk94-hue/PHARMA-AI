from dataclasses import dataclass, field
from typing import List, Optional, Mapping, Any, Union

@dataclass(frozen=True, slots=True)
class ClinicalData:
    """
    Encapsulates core clinical information with strict list and boolean parsing.
    """
    contraindications: List[str] = field(default_factory=list)
    pregnancy_category: Optional[str] = None
    lactation_safety: str = "unknown"
    renal_adjustment: bool = False
    hepatic_adjustment: bool = False
    side_effects: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    patient_counselling: List[str] = field(default_factory=list)

    @staticmethod
    def _parse_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return str(value).lower() in ("true", "1", "yes", "y")

    @staticmethod
    def _parse_string_list(value: Any) -> List[str]:
        """Ensures input is always returned as a list of strings."""
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value]
        if isinstance(value, str):
            return [value.strip()] if value.strip() else []
        return []

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ClinicalData":
        """Maps repository clinical data with strict field parsing."""
        return cls(
            contraindications=cls._parse_string_list(data.get("Contraindications")),
            pregnancy_category=str(data.get("Pregnancy_Category", "")).strip().upper() or None,
            lactation_safety=str(data.get("Lactation_Safety", "unknown")).lower().strip(),
            renal_adjustment=cls._parse_bool(data.get("Renal_Adjustment", False)),
            hepatic_adjustment=cls._parse_bool(data.get("Hepatic_Adjustment", False)),
            side_effects=cls._parse_string_list(data.get("Side_Effects")),
            warnings=cls._parse_string_list(data.get("Warnings")),
            patient_counselling=cls._parse_string_list(data.get("Patient_Counselling"))
        )