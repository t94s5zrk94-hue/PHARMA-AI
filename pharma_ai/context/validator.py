from pharma_ai.models.medicine_context import MedicineContext
from pharma_ai.models.clinical_data import ClinicalData
from pharma_ai.models.interaction_context import InteractionContext
from pharma_ai.models.validation_context import ValidationContext


class ContextValidator:
    """
    Validates the completeness and quality of a ClinicalContext.
    """

    def validate(
        self,
        medicine: MedicineContext,
        clinical: ClinicalData,
        interaction: InteractionContext,
    ) -> ValidationContext:

        missing_fields = []
        warnings = []

        # Medicine validation
        if not medicine.generic_id:
            missing_fields.append("generic_id")

        if not medicine.brand_id:
            missing_fields.append("brand_id")

        # Confidence score
        confidence = 1.0

        if missing_fields:
            confidence -= 0.3

        if warnings:
            confidence -= 0.1 * len(warnings)

        confidence = max(0.0, min(confidence, 1.0))

        return ValidationContext(
            missing_fields=missing_fields,
            warnings=warnings,
            confidence_score=confidence,
        )