from dataclasses import dataclass, field
from typing import Dict
from datetime import datetime
from enum import Enum

class MatchType(Enum):
    EXACT_BRAND = "Exact Brand"
    EXACT_GENERIC = "Exact Generic"
    FUZZY_BRAND = "Fuzzy Brand"
    FUZZY_GENERIC = "Fuzzy Generic"
    COMPANY = "Company"

class SearchStrategy(Enum):
    DEFAULT = "default"
    SEMANTIC = "semantic"
    AI_SEARCH = "ai_search"
    VECTOR = "vector"

@dataclass(frozen=True, slots=True)
class SearchResult:
    data: Dict
    match_type: MatchType
    confidence: float
    matched_value: str
    query: str
    timestamp: datetime = field(default_factory=datetime.now)
    execution_time_ms: float = 0.0
    search_strategy: SearchStrategy = SearchStrategy.DEFAULT

    def __post_init__(self):
        # Validation for clinical data integrity
        if not self.query.strip():
            raise ValueError("Query cannot be empty.")
        if not self.matched_value:
            raise ValueError("Matched value cannot be empty.")
        if not (0 <= self.confidence <= 100):
            raise ValueError(f"Confidence {self.confidence} must be between 0 and 100.")
        if self.execution_time_ms < 0:
            raise ValueError("Execution time cannot be negative.")
        
        # Coerce confidence to float
        object.__setattr__(self, "confidence", float(self.confidence))