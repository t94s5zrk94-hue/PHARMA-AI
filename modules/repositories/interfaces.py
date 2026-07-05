from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from enum import Enum

class InteractionSeverity(Enum):
    MAJOR = "Major"
    MODERATE = "Moderate"
    MINOR = "Minor"
    CONTRAINDICATED = "Contraindicated"

class InteractionRepositoryInterface(ABC):
    @abstractmethod
    def get_interactions(self, generic_id: int) -> List[Dict]: 
        """Fetch all unique interactions for a specific generic drug."""
        pass
    
    @abstractmethod
    def check_pair(self, drug_a_id: int, drug_b_id: int) -> Optional[Dict]: 
        """
        Check interaction between two specific drugs. 
        Note: This lookup is bidirectional (Order-independent, A-B is same as B-A).
        """
        pass

    @abstractmethod
    def get_severity_filtered(self, generic_id: int, severity: InteractionSeverity) -> List[Dict]:
        """Filter interactions by Enum severity."""
        pass