"""
Medicine Repository Implementation.

Provides concrete implementation for medicine data access using Pandas,
adhering to the Repository Pattern and Clean Architecture principles.
"""

from typing import Any, Optional
import pandas as pd
from pharma_ai.repositories.base_repository import BaseRepository
from pharma_ai.repositories.interfaces.medicine import MedicineRepositoryInterface


class MedicineRepository(BaseRepository, MedicineRepositoryInterface):
    """
    Concrete implementation of MedicineRepositoryInterface.
    
    Provides read-only access to master medicine and generic data frames
    injected via dependency injection.
    """

    def __init__(self, brand_df: pd.DataFrame, generic_df: pd.DataFrame) -> None:
        """
        Initializes the repository with validated data frames.
        
        Args:
            brand_df: Pandas DataFrame containing brand master data.
            generic_df: Pandas DataFrame containing generic master data.
            
        Raises:
            ValueError: If provided data frames are None.
        """
        if brand_df is None or generic_df is None:
            raise ValueError("DataFrames cannot be None.")
            
        self._brand_df = brand_df
        self._generic_df = generic_df

    def list_brand_names(self) -> list[str]:
        """Returns a unique, cleaned list of brand names."""
        if self._brand_df.empty or "Brand_Name" not in self._brand_df.columns:
            return []

        return (
            self._brand_df["Brand_Name"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

    def get_brand(self, brand_name: str) -> Optional[dict[str, Any]]:
        """Retrieves brand details via case-insensitive lookup."""
        query = brand_name.strip().lower()
        mask = self._brand_df["Brand_Name"].str.strip().str.lower() == query
        return self._find_first(self._brand_df[mask])

    def get_generic(self, generic_id: int) -> Optional[dict[str, Any]]:
        """Retrieves generic details via ID lookup."""
        mask = self._generic_df["Generic_ID"] == generic_id
        return self._find_first(self._generic_df[mask])

    def get_generic_by_name(self, generic_name: str) -> Optional[dict[str, Any]]:
        """Retrieves generic details via name case-insensitive lookup."""
        query = generic_name.strip().lower()
        mask = self._generic_df["Generic_Name"].str.strip().str.lower() == query
        return self._find_first(self._generic_df[mask])

    def get_complete_medicine(self, brand_name: str) -> Optional[dict[str, Any]]:
        """Retrieves merged brand and generic data."""
        brand_data = self.get_brand(brand_name)
        if not brand_data:
            return None

        generic_id = brand_data.get("Generic_ID")
        if generic_id is not None:
            generic_data = self.get_generic(int(generic_id))
            if generic_data:
                return {**generic_data, **brand_data}
        
        return brand_data

    def _find_first(self, df: pd.DataFrame) -> Optional[dict[str, Any]]:
        """Helper to return the first record as a dictionary."""
        if df.empty:
            return None
        return df.iloc[0].to_dict()