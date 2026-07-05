from dataclasses import dataclass
from models.medicine_context import MedicineContext
from models.clinical_data import ClinicalData
from models.interaction_context import InteractionContext
from models.validation_context import ValidationContext
from models.metadata import Metadata

@dataclass(frozen=True, slots=True)
class ClinicalContext:
    medicine: MedicineContext
    clinical: ClinicalData
    interaction: InteractionContext
    validation: ValidationContext
    metadata: Metadata