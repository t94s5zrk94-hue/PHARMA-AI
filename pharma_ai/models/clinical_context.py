from dataclasses import dataclass
from pharma_ai.models.medicine_context import MedicineContext
from pharma_ai.models.clinical_data import ClinicalData
from pharma_ai.models.interaction_context import InteractionContext
from pharma_ai.models.validation_context import ValidationContext
from pharma_ai.models.metadata import Metadata

@dataclass(frozen=True, slots=True)
class ClinicalContext:
    medicine: MedicineContext
    clinical: ClinicalData
    interaction: InteractionContext
    validation: ValidationContext
    metadata: Metadata