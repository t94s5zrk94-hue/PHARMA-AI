"""
Interaction Repository Interfaces.

This module defines the abstract interface for drug-drug interaction (DDI)
data access, adhering to SOLID principles and providing a contract for
concrete interaction repository implementations.

Usage:
    This interface should be implemented by concrete classes providing
    interaction lookup capabilities to ensure decoupled, testable architecture.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional


class InteractionSeverity(Enum):
    """Enumeration of clinical interaction severity levels with string mapping."""
    MAJOR = "Major"
    MODERATE = "Moderate"
    MINOR = "Minor"
    CONTRAINDICATED = "Contraindicated"


class InteractionRepositoryInterface(ABC):
    """
    Abstract Base Class defining the contract for drug interaction operations.

    This interface enforces the implementation of methods required for
    retrieving and validating pharmacological interactions between medications.
    """

    @abstractmethod
    def get_interactions(self, generic_id: int) -> list[dict[str, Any]]:
        """
        Retrieves all known drug interactions for a specific generic medication.

        Args:
            generic_id: The unique integer identifier for the generic drug.

        Returns:
            A list of dictionaries, where each dictionary contains interaction 
            details and associated severity.
        """
        ...

    @abstractmethod
    def check_pair(
        self, drug_a_id: int, drug_b_id: int
    ) -> Optional[dict[str, Any]]:
        """
        Checks for a specific interaction between two distinct drug entities.

        Args:
            drug_a_id: The unique identifier for the first drug.
            drug_b_id: The unique identifier for the second drug.

        Returns:
            An optional dictionary containing interaction clinical details if an
            interaction exists, otherwise None.
        """
        ...

    @abstractmethod
    def get_severity_filtered(
        self, generic_id: int, severity: InteractionSeverity
    ) -> list[dict[str, Any]]:
        """
        Retrieves interactions for a drug, filtered by a specific severity level.

        Args:
            generic_id: The unique integer identifier for the generic drug.
            severity: The InteractionSeverity enum value to filter by.

        Returns:
            A list of interaction dictionaries matching the specified severity.
        """
        ...