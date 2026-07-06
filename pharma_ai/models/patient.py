from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum
from typing import List, Optional
from datetime import datetime

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

class PregnancyStatus(str, Enum):
    NOT_PREGNANT = "not_pregnant"
    PREGNANT = "pregnant"
    UNKNOWN = "unknown"

class ChildPughClass(str, Enum):
    A = "A"
    B = "B"
    C = "C"

class Patient(BaseModel):
    model_config = ConfigDict(frozen=True)

    # Identity & Demographics
    patient_id: str
    age: int = Field(ge=0)
    gender: Gender
    weight_kg: float = Field(gt=0)
    height_cm: Optional[float] = Field(default=None, gt=0)

    # Clinical Status (Standardized IDs recommended)
    diagnoses: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    
    # Reproductive Status
    pregnancy_status: PregnancyStatus = PregnancyStatus.UNKNOWN
    gestational_age_weeks: Optional[int] = Field(default=None, ge=0, le=42)
    lactation_status: bool = False
    
    # Organ Function
    serum_creatinine: Optional[float] = Field(default=None, ge=0)
    egfr: Optional[float] = Field(default=None, ge=0)
    creatinine_clearance: Optional[float] = Field(default=None, ge=0)
    child_pugh_class: Optional[ChildPughClass] = None
    
    # Metadata
    encounter_date: datetime = Field(default_factory=datetime.now)

    @property
    def age_group(self) -> str:
        if self.age < 1: return "neonate"
        if self.age < 2: return "infant"
        if self.age < 12: return "child"
        if self.age < 18: return "adolescent"
        if self.age < 65: return "adult"
        return "geriatric"

    @field_validator('gestational_age_weeks')
    @classmethod
    def validate_pregnancy_context(cls, v, info):
        if v is not None and info.data.get('pregnancy_status') != PregnancyStatus.PREGNANT:
            raise ValueError("Gestational age can only be set if patient is pregnant.")
        return v