from typing import List
from pharma_ai.models.patient_clinical_context import PatientClinicalContext
from pharma_ai.models.finding import Finding, RecommendationStatus
from pharma_ai.models.recommendation import Recommendation

class RecommendationBuilder:
    """
    Composes a final, immutable Recommendation from resolved Findings.
    """

    def build(
        self, 
        context: PatientClinicalContext, 
        findings: List[Finding]
    ) -> Recommendation:
        
        # 1. Determine overall recommendation status
        # If any finding is REJECTED, the whole recommendation is REJECTED
        overall_status = RecommendationStatus.APPROVED
        if any(f.recommendation_status == RecommendationStatus.REJECTED for f in findings):
            overall_status = RecommendationStatus.REJECTED
        elif any(f.recommendation_status == RecommendationStatus.MODIFIED for f in findings):
            overall_status = RecommendationStatus.MODIFIED

        # 2. Generate deterministic summary
        summary = self._generate_summary(findings)
        
        # 3. Aggregate unique references
        # Logic is defined in the Recommendation model, but we ensure findings are passed
        
        # 4. Calculate Execution Confidence (0-100)
        # Based on data completeness and successful execution count
        confidence = self._calculate_confidence(context, findings)

        return Recommendation(
            evaluation_id=context.metadata.evaluation_id,
            patient_id=context.patient.patient_id,
            target_drug_id=context.target_drug_id,
            status=overall_status,
            recommendation_summary=summary,
            findings=findings,
            confidence_score=confidence,
            engine_version=context.metadata.engine_version
        )

    def _generate_summary(self, findings: List[Finding]) -> str:
        if not findings:
            return "No clinical findings generated."
        
        lines = []
        for f in findings:
            lines.append(f"{f.title}: {f.recommendation}")
        return "\n".join(lines)

    def _calculate_confidence(self, context: PatientClinicalContext, findings: List[Finding]) -> float:
        # Simple baseline: 100 if all inputs (e.g., eGFR, etc) are present
        score = 100.0
        if context.patient.egfr is None:
            score -= 20.0
        if context.patient.pregnancy_status == "unknown":
            score -= 20.0
        return max(0.0, score)