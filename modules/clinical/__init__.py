"""
Clinical Resolution Layer.

Public API for all clinical normalization and generic resolution
components used throughout Pharma AI.

Architecture:
    User Input
        ↓
    ClinicalNormalizer
        ↓
    GenericResolver
        ↓
    ResolvedDrug
"""

from .enums import MatchType
from .models import ResolvedDrug
from .normalizer import ClinicalNormalizer
from .resolver import GenericResolver

__all__ = [
    "MatchType",
    "ResolvedDrug",
    "ClinicalNormalizer",
    "GenericResolver",
]

__version__ = "1.0.0"