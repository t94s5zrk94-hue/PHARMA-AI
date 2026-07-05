from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class MedicineRepositoryInterface(ABC):
    @abstractmethod
    def get_brand(self, brand_name: str) -> Optional[Dict]: pass
    
    @abstractmethod
    def get_generic(self, generic_id: int) -> Optional[Dict]: pass
    
    @abstractmethod
    def get_complete_medicine(self, brand_name: str) -> Optional[Dict]: pass

class ClinicalRepositoryInterface(ABC):
    """
    Interface for Clinical Domain Services.
    All implementations must provide these evidence-based parameters.
    """
    
    @abstractmethod
    def get_clinical_data(self, generic_id: int) -> Optional[Dict]: 
        """Fetches raw clinical data object."""
        pass
    
    @abstractmethod
    def get_contraindications(self, generic_id: int) -> List[str]: 
        """Returns a list of contraindications."""
        pass
    
    @abstractmethod
    def get_pregnancy_risk(self, generic_id: int) -> str: 
        """Returns the pregnancy safety category."""
        pass

    @abstractmethod
    def get_patient_counselling(self, generic_id: int) -> List[str]:
        """Returns actionable patient counselling points."""
        pass