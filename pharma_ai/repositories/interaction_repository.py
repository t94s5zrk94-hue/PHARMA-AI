from typing import List, Dict, Optional
from pharma_ai.repositories.base_repository import BaseRepository
from pharma_ai.repositories.interfaces import (
    InteractionRepositoryInterface,
    InteractionSeverity,
)

class InteractionRepository(BaseRepository, InteractionRepositoryInterface):
    """
    Production-ready Interaction Repository with bidirectional lookup and deduplication.
    """

    def __init__(self, db_instance):
        super().__init__(db_instance)
        if not hasattr(self.db, 'interactions'):
            raise AttributeError("Interactions table not initialized.")

    def get_interactions(self, generic_id: int) -> List[Dict]:
        """Fetches all unique interactions for a given generic drug."""
        res1 = self.find_by_column(self.db.interactions, "Generic_ID_1", generic_id) or []
        res2 = self.find_by_column(self.db.interactions, "Generic_ID_2", generic_id) or []
        
        # Deduplication using Interaction_ID as unique key
        combined = res1 + res2
        unique_interactions = {item['Interaction_ID']: item for item in combined}.values()
        return list(unique_interactions)

    def check_pair(self, drug_a_id: int, drug_b_id: int) -> Optional[Dict]:
        """
        Bidirectional check for specific drug pair interaction.
        Checks both A->B and B->A directions.
        """
        # Direction 1: A -> B
        mask_ab = (self.db.interactions["Generic_ID_1"] == drug_a_id) & \
                  (self.db.interactions["Generic_ID_2"] == drug_b_id)
        
        # Direction 2: B -> A
        mask_ba = (self.db.interactions["Generic_ID_1"] == drug_b_id) & \
                  (self.db.interactions["Generic_ID_2"] == drug_a_id)
        
        result = self.db.interactions[mask_ab | mask_ba]
        return result.to_dict('records')[0] if not result.empty else None

    def get_severity_filtered(self, generic_id: int, severity: InteractionSeverity) -> List[Dict]:
        all_data = self.get_interactions(generic_id)
        return [i for i in all_data if i.get("Severity") == severity.value]