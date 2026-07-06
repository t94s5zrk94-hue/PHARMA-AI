from typing import Mapping, Any
from pharma_ai.repositories.interfaces import (
    MedicineRepositoryInterface, 
    ClinicalRepositoryInterface, 
    InteractionRepositoryInterface
)
from pharma_ai.models.clinical_context import ClinicalContext
from pharma_ai.models.medicine_context import MedicineContext
from pharma_ai.models.clinical_data import ClinicalData
from pharma_ai.models.interaction_context import InteractionContext
from pharma_ai.models.validation_context import ValidationContext
from pharma_ai.models.metadata import Metadata, DataSource
from pharma_ai.models.search_result import SearchResult
from pharma_ai.context.validator import ContextValidator

class ContextBuilder:
    """
    Orchestrates the assembly of ClinicalContext with strict type safety.
    """
    
    def __init__(
        self,
        medicine_repository: MedicineRepositoryInterface,
        clinical_repository: ClinicalRepositoryInterface,
        interaction_repository: InteractionRepositoryInterface,
        validator: ContextValidator
    ):
        self.med_repo = medicine_repository
        self.clin_repo = clinical_repository
        self.int_repo = interaction_repository
        self.validator = validator

    def build(self, search_result: SearchResult) -> ClinicalContext:
        # 1. Identity
        medicine = MedicineContext.from_dict(search_result.data)
        
        # 2. Clinical & Interaction Data
        clin_data = self.clin_repo.get_clinical_data(medicine.generic_id) or {}
        clinical = ClinicalData.from_dict(clin_data)
        
        int_data = self.int_repo.get_interactions(medicine.brand_id) or {}
        interaction = InteractionContext.from_dict(int_data)
        
        # 3. Validation
        validation = self.validator.validate(medicine, clinical, interaction)
        
        # 4. Metadata (Using Enum and proper construction)
        metadata = Metadata(
            source=DataSource.INTERNAL,
            search_strategy=search_result.search_strategy
        )
        
        # 5. Composition
        return ClinicalContext(
            medicine=medicine,
            clinical=clinical,
            interaction=interaction,
            validation=validation,
            metadata=metadata
        )