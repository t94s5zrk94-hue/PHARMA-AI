from typing import List, Dict, Optional
from modules.repositories.interfaces import MedicineRepositoryInterface
from modules.repositories.base_repository import BaseRepository

class MedicineRepository(BaseRepository, MedicineRepositoryInterface):
    """
    Refactored Repository Layer with explicit interfaces and type hinting.
    """

    def get_brand(self, brand_name: str) -> Optional[Dict]:
        return self.find_one(self.db.brand, "Brand_Name", brand_name)

    def get_generic(self, generic_id: int) -> Optional[Dict]:
        return self.find_one(self.db.generic, "Generic_ID", generic_id)

    def get_complete_medicine(self, brand_name: str) -> Optional[Dict]:
        return self.db.get_complete_medicine(brand_name)

    def get_brands_by_generic(self, generic_id: int) -> List[Dict]:
        # Using BaseRepository's find_by_column for consistency
        results = self.find_by_column(self.db.brand, "Generic_ID", generic_id)
        return results if results is not None else []

    def search_brand(self, query: str) -> List[Dict]:
        """Reusable search strategy."""
        mask = self.db.brand["Brand_Name"].fillna("").astype(str).str.contains(query, case=False, na=False)
        return self.db.brand[mask].to_dict('records')

    def exists_brand(self, brand_name: str) -> bool:
        return self.get_brand(brand_name) is not None