from typing import List, Dict, Optional
from modules.repositories.base_repository import BaseRepository
from modules.repositories.interfaces import ClinicalRepositoryInterface

class ClinicalRepository(BaseRepository, ClinicalRepositoryInterface):
    """
    Production-ready Clinical Repository implementation.
    Acts as a Domain Service for all clinical knowledge queries.
    """

    def __init__(self, db_instance):
        super().__init__(db_instance)
        # Ensure database has the required clinical table
        if not hasattr(self.db, 'clinical_data'):
            raise AttributeError("Clinical data table not initialized in database.")

    def get_clinical_data(self, generic_id: int) -> Optional[Dict]:
        """Fetches raw clinical data object for a given Generic ID."""
        return self.find_one(self.db.clinical_data, "Generic_ID", generic_id)

    def get_contraindications(self, generic_id: int) -> List[str]:
        """Returns a cleaned list of contraindications."""
        data = self.get_clinical_data(generic_id)
        raw = data.get("Contraindications", "") if data else ""
        return [item.strip() for item in raw.split(',')] if raw else []

    def get_pregnancy_risk(self, generic_id: int) -> str:
        """Returns pregnancy safety category."""
        data = self.get_clinical_data(generic_id)
        return data.get("Pregnancy_Category", "Data Unavailable") if data else "Data Unavailable"

    def get_patient_counselling(self, generic_id: int) -> List[str]:
        """Returns a cleaned list of actionable patient counselling points."""
        data = self.get_clinical_data(generic_id)
        raw = data.get("Counselling_Points", "") if data else ""
        return [item.strip() for item in raw.split('|')] if raw else []

    # Placeholder for future expansion - Ready to implement as per roadmap
    def get_renal_adjustment(self, generic_id: int) -> str:
        data = self.get_clinical_data(generic_id)
        return data.get("Renal_Adjustment", "Not specified") if data else "Not specified"