"""
Clinical Domain Models.
Core immutable domain objects for the Canonical Generic Builder.
"""

from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class CanonicalDrug:
    """
    Immutable representation of a canonical clinical drug concept.
    Designed for high-precision clinical data transformation.
    """
    source_text: str
    normalized_name: str
    ingredients: Tuple[str, ...]
    strengths: Tuple[str, ...]
    dosage_form: str
    route: str
    category: str
    is_combination: bool

    def __post_init__(self):
        """
        Governance Validation: Ensures integrity before object instantiation.
        """
        # Validate Ingredients
        if not self.ingredients:
            raise ValueError("Ingredients list cannot be empty.")

        # Validate Invariants: Strengths must map to ingredients
        if len(self.ingredients) != len(self.strengths):
            raise ValueError("Count mismatch: Ingredients and Strengths must be 1:1 mapped.")

        # Validate Combination Logic
        expected_combination = len(self.ingredients) > 1
        if self.is_combination != expected_combination:
            raise ValueError(f"is_combination flag {self.is_combination} inconsistent with ingredients count.")

        # Validate Meta Fields
        if not all([self.dosage_form, self.route, self.category]):
            raise ValueError("dosage_form, route, and category are mandatory.")

        if not self.source_text or not self.normalized_name:
            raise ValueError("source_text and normalized_name are mandatory for traceability.")