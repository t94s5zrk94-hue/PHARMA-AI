from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping, Any
from enum import Enum
from pharma_ai.models.search_result import SearchStrategy  # Reused Enum

class DataSource(Enum):
    INTERNAL = "internal_repo"
    OPENFDA = "openfda"
    MANUAL = "manual"
    HYBRID = "hybrid"

@dataclass(frozen=True, slots=True)
class Metadata:
    """
    Audit and Traceability for ClinicalContext.
    Standardized with robust Enum parsing and Fail-Fast policy.
    """
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: DataSource = DataSource.INTERNAL
    version: str = "1.0.0"
    builder_version: str = "1.0.0"
    search_strategy: SearchStrategy = SearchStrategy.DEFAULT

    @staticmethod
    def _parse_datetime(value: Any) -> datetime:
        """Parses datetime with Fail-Fast policy."""
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(str(value))
        except (ValueError, TypeError):
            raise ValueError(f"Invalid timestamp format: {value}")

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Metadata":
        """Maps audit data with strict Enum and Type parsing."""
        
        # 1. Source Parsing (Fail-Fast)
        try:
            source = DataSource(str(data.get("Source", "internal_repo")).lower())
        except ValueError:
            raise ValueError(f"Invalid DataSource: {data.get('Source')}")

        # 2. Strategy Parsing (Fail-Fast)
        raw_strategy = data.get("Search_Strategy", SearchStrategy.DEFAULT)
        if isinstance(raw_strategy, SearchStrategy):
            strategy = raw_strategy
        else:
            try:
                strategy = SearchStrategy(str(raw_strategy).lower())
            except ValueError:
                raise ValueError(f"Invalid SearchStrategy: {raw_strategy}")

        return cls(
            timestamp=cls._parse_datetime(data.get("Timestamp", datetime.utcnow())),
            source=source,
            version=str(data.get("Version", "1.0.0")).strip() or "1.0.0",
            builder_version=str(data.get("Builder_Version", "1.0.0")).strip() or "1.0.0",
            search_strategy=strategy
        )