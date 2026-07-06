from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

# Importing existing contracts
from pharma_ai.models.finding import Finding, RecommendationStatus

class Recommendation(BaseModel):
    model_config = ConfigDict(frozen=True)

    # Identifiers - Standardized to REC000001 format
    # In production, replace the default_factory with a sequence generator
    recommendation_id: str = Field(default_factory=lambda: f"REC{uuid4().hex[:6].upper()}")
    evaluation_id: str 
    patient_id: str
    target_drug_id: str
    
    # Decision Core
    status: RecommendationStatus
    recommended_dose: Optional[str] = None
    recommendation_summary: str
    findings: List[Finding] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    
    # Metadata
    confidence_score: float = Field(ge=0, le=100)
    engine_version: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def aggregated_references(self) -> List[str]:
        """
        Extracts unique references from all findings for a summary view.
        """
        refs = set()
        for finding in self.findings:
            refs.update(finding.references)
        return sorted(list(refs))