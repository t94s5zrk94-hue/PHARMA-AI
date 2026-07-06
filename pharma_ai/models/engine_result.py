from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime, timezone
from typing import List, Optional

from pharma_ai.models.finding import Finding
from pharma_ai.models.engine_metadata import EngineMetadata

class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    PARTIAL_SUCCESS = "partial_success"

class EngineError(BaseModel):
    model_config = ConfigDict(frozen=True)
    code: str
    message: str
    severity: str

class EngineResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    # Contextual Metadata
    engine_metadata: EngineMetadata
    
    # Execution Outcome
    status: ExecutionStatus
    findings: List[Finding] = Field(default_factory=list)
    errors: List[EngineError] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    
    # Performance Metrics
    execution_time_ms: float = Field(ge=0)
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Optional execution-specific context
    metadata: Optional[dict] = None