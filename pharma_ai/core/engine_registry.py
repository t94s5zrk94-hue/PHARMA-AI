from typing import Dict, List, Deque
from collections import deque
from pharma_ai.core.clinical_engine import ClinicalEngine
from pharma_ai.models.engine_result import EngineResult, ExecutionStatus, EngineError
from pharma_ai.models.engine_metadata import EngineStatus
from pharma_ai.models.patient_clinical_context import PatientClinicalContext
import time

class EngineRegistry:
    def __init__(self):
        self._engines: Dict[str, ClinicalEngine] = {}

    def register(self, engine: ClinicalEngine):
        # Enforce unique IDs and Names
        if engine.metadata.engine_id in self._engines:
            raise ValueError(f"Duplicate engine ID: {engine.metadata.engine_id}")
        
        if any(e.metadata.engine_name == engine.metadata.engine_name for e in self._engines.values()):
            raise ValueError(f"Duplicate engine name: {engine.metadata.engine_name}")
            
        self._engines[engine.metadata.engine_id] = engine

    def validate(self):
        """Validates the dependency graph and returns a sorted execution order."""
        in_degree = {eid: 0 for eid in self._engines}
        adj = {eid: [] for eid in self._engines}

        for eid, engine in self._engines.items():
            for dep in engine.metadata.dependencies:
                if dep not in self._engines:
                    raise ValueError(f"Missing dependency: {dep} for engine {eid}")
                adj[dep].append(eid)
                in_degree[eid] += 1

        # Kahn's Algorithm for Topological Sort
        queue: Deque[str] = deque([eid for eid in in_degree if in_degree[eid] == 0])
        sorted_order = []
        
        while queue:
            u = queue.popleft()
            sorted_order.append(u)
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        
        if len(sorted_order) != len(self._engines):
            raise ValueError("Circular dependency detected in clinical engines.")
            
        return sorted_order

    def execute(self, context: PatientClinicalContext) -> List[EngineResult]:
        # Validate and get topologically sorted order
        execution_order = self.validate()
        results = []
        
        for eid in execution_order:
            engine = self._engines[eid]
            
            if engine.metadata.status != EngineStatus.ENABLED:
                continue
            
            start_time = time.perf_counter()
            try:
                results.append(engine.execute(context))
            except Exception as e:
                elapsed = (time.perf_counter() - start_time) * 1000
                results.append(self._build_failed_result(engine, e, elapsed))
        
        return results

    def _build_failed_result(self, engine: ClinicalEngine, e: Exception, elapsed: float) -> EngineResult:
        return EngineResult(
            engine_metadata=engine.metadata,
            status=ExecutionStatus.FAILED,
            errors=[EngineError(code="EXEC_FAIL", message=str(e), severity="high")],
            execution_time_ms=elapsed
        )