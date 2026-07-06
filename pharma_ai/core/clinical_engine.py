from abc import ABC, abstractmethod
from pharma_ai.models.engine_metadata import EngineMetadata
from pharma_ai.models.patient_clinical_context import PatientClinicalContext
from pharma_ai.models.engine_result import EngineResult

class ClinicalEngine(ABC):
    @property
    @abstractmethod
    def metadata(self) -> EngineMetadata:
        """Returns the engine's metadata for registry use."""
        pass

    @abstractmethod
    def execute(self, context: PatientClinicalContext) -> EngineResult:
        """Executes clinical logic and returns a standardized result."""
        pass