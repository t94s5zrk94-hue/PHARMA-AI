"""
Repository Interfaces Package.

This module exposes the abstract repository interfaces for the Pharma AI
domain models, ensuring a clean and consistent API for dependency injection
and implementation.
"""

from .medicine import MedicineRepositoryInterface
from .clinical import ClinicalRepositoryInterface
from .interaction import (
    InteractionRepositoryInterface,
    InteractionSeverity,
)

__all__ = [
    "MedicineRepositoryInterface",
    "ClinicalRepositoryInterface",
    "InteractionRepositoryInterface",
    "InteractionSeverity",
]