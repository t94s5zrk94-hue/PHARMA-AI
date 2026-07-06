"""
Clinical Repository Interfaces.

This module defines the abstract interface for clinical decision support data access,
adhering to SOLID principles and providing a contract for concrete clinical
repository implementations.

Usage:
    This interface should be implemented by concrete classes interacting with
    clinical knowledge bases or database layers to ensure decoupled, 
    testable architecture.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class ClinicalRepositoryInterface(ABC):
    """
    Abstract Base Class defining the contract for clinical data operations.

    This interface enforces the implementation of methods required for
    retrieving clinical safety, adjustment, and patient counselling information
    for pharmaceutical products.
    """

    @abstractmethod
    def get_clinical_data(self, generic_id: int) -> Optional[dict[str, Any]]:
        """
        Retrieves the core clinical profile for a specific generic medication.

        Args:
            generic_id: The unique integer identifier for the generic drug.

        Returns:
            An optional dictionary containing clinical attributes, 
            or None if the record is not found.
        """
        ...

    @abstractmethod
    def get_contraindications(self, generic_id: int) -> list[str]:
        """
        Retrieves a list of contraindications for a specific medication.

        Args:
            generic_id: The unique integer identifier for the generic drug.

        Returns:
            A list of strings describing clinical contraindications.
        """
        ...

    @abstractmethod
    def get_pregnancy_risk(self, generic_id: int) -> str:
        """
        Retrieves the pregnancy safety category for a specific medication.

        Args:
            generic_id: The unique integer identifier for the generic drug.

        Returns:
            A string representing the pregnancy risk classification (e.g., FDA category).
        """
        ...

    @abstractmethod
    def get_patient_counselling(self, generic_id: int) -> list[str]:
        """
        Retrieves standard patient counselling points for a specific medication.

        Args:
            generic_id: The unique integer identifier for the generic drug.

        Returns:
            A list of patient-friendly clinical counselling instructions.
        """
        ...

    @abstractmethod
    def get_renal_adjustment(self, generic_id: int) -> str:
        """
        Retrieves renal function adjustment guidelines for a specific medication.

        Args:
            generic_id: The unique integer identifier for the generic drug.

        Returns:
            A string detailing the required renal dose adjustments or safety notes.
        """
        ...