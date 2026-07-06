from typing import List
from pharma_ai.models.engine_result import EngineResult, ExecutionStatus
from pharma_ai.models.finding import Finding

class FindingAggregator:
    """
    Collects Findings from successful engine executions.
    Responsibilities:
    - Flatten results into a single list.
    - Filter for only successful execution states.
    - Preserve order and data integrity.
    """
    
    @staticmethod
    def aggregate(results: List[EngineResult]) -> List[Finding]:
        collected_findings: List[Finding] = []
        
        # Define statuses that are eligible for aggregation
        valid_statuses = {ExecutionStatus.SUCCESS, ExecutionStatus.PARTIAL_SUCCESS}
        
        for result in results:
            if result.status in valid_statuses:
                # Extend the list with findings from valid engines
                if result.findings:
                    collected_findings.extend(result.findings)
                    
        return collected_findings