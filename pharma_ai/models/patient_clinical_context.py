from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from typing import List

# Importing existing models
from pharma_ai.models.patient import Patient
from pharma_ai.models.clinical_context import ClinicalContext

class ExecutionMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)
    evaluation_id: str
    # Using UTC for consistent audit logs
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    engine_version: str

class PatientClinicalContext(BaseModel):
    """
    The immutable container passed to all Clinical Rule Engines.
    
    Attributes:
        patient: The frozen patient record.
        knowledge_context: Aggregated clinical data (e.g., drug contraindications).
        target_drug_id: Standardized generic_id of the medication being evaluated.
        metadata: Audit and versioning information.
    """
    model_config = ConfigDict(frozen=True)

    patient: Patient
    knowledge_context: ClinicalContext
    target_drug_id: str
    metadata: ExecutionMetadata

    @property
    def is_valid(self) -> bool:
        """
        High-level check to ensure the context has the minimal 
        information required for engine execution.
        """
        return all([
            self.patient is not None,
            self.knowledge_context is not None,
            bool(self.target_drug_id)
        ])