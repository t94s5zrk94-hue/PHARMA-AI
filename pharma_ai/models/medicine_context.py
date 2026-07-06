from dataclasses import dataclass
from typing import Mapping, Any
from enum import Enum

class MedicineStatus(Enum):
    ACTIVE = "active"
    DISCONTINUED = "discontinued"
    SUSPENDED = "suspended"
    UNKNOWN = "unknown"

@dataclass(frozen=True, slots=True)
class MedicineContext:
    """
    Represents the identity and core characteristics of a medicine.
    Ensures data integrity for the ClinicalContext pipeline.
    """
    brand_id: int
    generic_id: int
    company_id: int
    brand_name: str
    generic_name: str
    company_name: str
    strength: str
    dosage_form: str
    status: MedicineStatus = MedicineStatus.ACTIVE

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MedicineContext":
        """Maps repository data to MedicineContext with strict validation."""
        
        # 1. Critical Field Validation (Presence and Content)
        required_fields = ["Brand_ID", "Generic_ID", "Brand_Name", "Generic_Name"]
        for field in required_fields:
            val = data.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                raise ValueError(f"Missing or empty critical field: {field}")

        # 2. Integer Validation
        try:
            brand_id = int(data["Brand_ID"])
            generic_id = int(data["Generic_ID"])
            company_id = int(data.get("Company_ID", 0))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid numeric ID format: {e}")

        # 3. Status Handling (Fail fast)
        raw_status = data.get("Status", "active").lower()
        try:
            status = MedicineStatus(raw_status)
        except ValueError:
            raise ValueError(f"Invalid status value: {raw_status}")

        return cls(
            brand_id=brand_id,
            generic_id=generic_id,
            company_id=company_id,
            brand_name=data["Brand_Name"].strip(),
            generic_name=data["Generic_Name"].strip(),
            company_name=data.get("Company_Name", "Unknown").strip() or "Unknown",
            strength=data.get("Strength", "N/A").strip(),
            dosage_form=data.get("Dosage_Form", "N/A").strip(),
            status=status
        )