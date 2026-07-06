"""
Medicine Repository Interfaces.

This module defines the abstract interface for medicine-related data access,
adhering to SOLID principles and providing a contract for concrete repository
implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class MedicineRepositoryInterface(ABC):
    """
    Abstract Base Class defining the contract for medicine data operations.
    """

    @abstractmethod
    def list_brand_names(self) -> list[str]:
        """
        Retrieves a complete list of all available brand names in the system.

        Returns:
            A list of all unique brand name strings.
        """
        ...

    @abstractmethod
    def get_brand(self, brand_name: str) -> Optional[dict[str, Any]]:
        """
        Retrieves detailed information for a specific brand name.

        Args:
            brand_name: The unique string identifier for the brand.

        Returns:
            An optional dictionary containing brand details, or None if not found.
        """
        ...

    @abstractmethod
    def get_generic(self, generic_id: int) -> Optional[dict[str, Any]]:
        """
        Retrieves detailed information for a specific generic identifier.

        Args:
            generic_id: The integer identifier for the generic drug.

        Returns:
            An optional dictionary containing generic drug details, or None if not found.
        """
        ...

    @abstractmethod
    def get_generic_by_name(self, generic_name: str) -> Optional[dict[str, Any]]:
        """
        Retrieves detailed information for a specific generic name.

        Args:
            generic_name: The string name of the generic drug.

        Returns:
            An optional dictionary containing generic drug details, or None if not found.
        """
        ...

    @abstractmethod
    def get_complete_medicine(self, brand_name: str) -> Optional[dict[str, Any]]:
        """
        Retrieves the complete clinical and product composition for a brand.

        Args:
            brand_name: The unique string identifier for the brand.

        Returns:
            An optional dictionary containing the full medicine composition,
            or None if the brand is not found.
        """
        ...