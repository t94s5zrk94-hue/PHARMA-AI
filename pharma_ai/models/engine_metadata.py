from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime, timezone
from typing import List, Optional

class EngineCategory(str, Enum):
    RENAL = "renal"
    HEPATIC = "hepatic"
    INTERACTION = "interaction"
    CONTRAINDICATION = "contraindication"
    PREGNANCY = "pregnancy"
    LACTATION = "lactation"
    DOSAGE = "dosage"
    MONITORING = "monitoring"
    ADVERSE_EFFECT = "adverse_effect"

class EngineStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    DEPRECATED = "deprecated"

class EngineMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    # Identification
    engine_id: str  # e.g., ENG000001
    engine_name: str
    engine_category: EngineCategory
    description: str
    version: str  # Semantic versioning, e.g., "1.0.0"
    
    # Execution Control
    status: EngineStatus = EngineStatus.ENABLED
    execution_priority: int = Field(ge=0)  # Lower number = higher priority
    dependencies: List[str] = Field(default_factory=list) # List of engine_ids
    
    # Capabilities (Future-proofing)
    supports_parallel_execution: bool = False
    requires_patient_labs: bool = False
    produces_findings: bool = True
    
    # Audit
    author: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))