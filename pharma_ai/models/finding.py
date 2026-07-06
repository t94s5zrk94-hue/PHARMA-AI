from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime, timezone
from typing import List, Optional

# Assuming Evidence will be defined in its own file
from pharma_ai.models.evidence import Evidence 

class FindingCategory(str, Enum):
    RENAL = "renal"
    HEPATIC = "hepatic"
    INTERACTION = "interaction"
    CONTRAINDICATION = "contraindication"
    PREGNANCY = "pregnancy"
    LACTATION = "lactation"
    DOSAGE = "dosage"
    MONITORING = "monitoring"
    ADVERSE_EFFECT = "adverse_effect"

class ClinicalSeverity(str, Enum):
    NONE = "none"
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    LIFE_THREATENING = "life_threatening"

class RecommendationStatus(str, Enum):
    APPROVED = "approved"
    CAUTION = "caution"
    MODIFIED = "modified"
    REJECTED = "rejected"
    INSUFFICIENT_DATA = "insufficient_data"

class Finding(BaseModel):
    model_config = ConfigDict(frozen=True)

    # Core Identifiers
    finding_id: str
    engine_name: str
    rule_id: str  # e.g., REN-001
    category: FindingCategory
    
    # Content
    title: str
    description: str
    
    # Clinical Status
    severity: ClinicalSeverity
    priority: int  # 1 (Low) to 10 (Critical)
    recommendation: str
    recommendation_status: RecommendationStatus
    
    # Evidence & Traceability
    evidence: Evidence
    references: List[str] = Field(default_factory=list)
    
    # Execution Metadata
    engine_version: str
    rule_version: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))