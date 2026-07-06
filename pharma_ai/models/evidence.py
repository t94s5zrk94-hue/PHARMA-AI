from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from enum import Enum
from datetime import datetime, timezone
from typing import Optional

class EvidenceLevel(str, Enum):
    A = "A"  # High quality, RCTs or Meta-analysis
    B = "B"  # Moderate quality, observational studies
    C = "C"  # Low quality, consensus or expert opinion

class RecommendationStrength(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    EXPERT_CONSENSUS = "expert_consensus"

class SourceType(str, Enum):
    FDA = "fda"
    WHO = "who"
    KDIGO = "kdigo"
    NICE = "nice"
    EMA = "ema"
    LEXICOMP = "lexicomp"
    MICROMEDEX = "micromedex"
    MANUAL = "manual"
    INTERNAL = "internal"

class Evidence(BaseModel):
    model_config = ConfigDict(frozen=True)

    evidence_id: str
    source: SourceType
    guideline: str
    publication_year: int = Field(ge=1900, le=datetime.now().year + 1)
    
    # Clinical Quality Metrics
    evidence_level: EvidenceLevel
    recommendation_strength: RecommendationStrength
    
    # Bibliographic Details
    reference_title: str
    reference_identifier: str  # DOI, PMID, or Internal ID
    citation: str
    url: Optional[HttpUrl] = None
    
    # Auditability
    version: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))