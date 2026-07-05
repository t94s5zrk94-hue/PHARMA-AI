"""
Repository Layer for Pharma AI.
Provides abstracted data access for Medicine, Clinical, and Interaction domains.
"""

from .medicine_repository import MedicineRepository
from .clinical_repository import ClinicalRepository
from .interaction_repository import InteractionRepository
from .interfaces import (
    MedicineRepositoryInterface, 
    ClinicalRepositoryInterface, 
    InteractionRepositoryInterface,
    InteractionSeverity
)

__all__ = [
    "MedicineRepository",
    "ClinicalRepository",
    "InteractionRepository",
    "MedicineRepositoryInterface",
    "ClinicalRepositoryInterface",
    "InteractionRepositoryInterface",
    "InteractionSeverity"
]