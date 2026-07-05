"""
Clinical Domain Models.
Core immutable domain objects for the Pharma AI Resolution Layer.
"""

from dataclasses import dataclass
from typing import Tuple
from .enums import MatchType

@dataclass(frozen=True)
class ResolvedDrug:
    """
    Immutable representation of a resolved clinical drug concept.
    Designed to handle single, combination, and alias-based drug resolution.
    """
    generic_ids: Tuple[str, ...]
    canonical_names: Tuple[str, ...]
    matched_value: str
    confidence: float
    match_type: MatchType
    is_combination: bool
    strengths: Tuple[str, ...]
    aliases: Tuple[str, ...]

    def __post_init__(self):
        """
        Governance Validation: Ensures the integrity of the clinical concept 
        before object instantiation.
        """
        # Ensure structural integrity for combinations
        if len(self.generic_ids) != len(self.canonical_names):
            raise ValueError("generic_ids and canonical_names must have equal length.")

        # Ensure confidence score bounds
        if not (0.0 <= self.confidence <= 100.0):
            raise ValueError(f"Confidence score {self.confidence} must be between 0 and 100.")

        # Ensure consistency for combination logic
        if self.is_combination and len(self.generic_ids) < 2:
            raise ValueError("is_combination=True requires multiple generic_ids.")