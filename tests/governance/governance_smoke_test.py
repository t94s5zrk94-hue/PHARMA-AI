"""
Governance Smoke Test Script.
Verifies the E2E integration of the Governance Layer:
Loader -> Validator -> Engine -> AuditBuilder.
"""

import sys
from pathlib import Path
from time import perf_counter
import traceback

# Ensure the project root is in sys.path to allow module imports from any directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.governance.loader import PolicyLoader
from modules.governance.validator import PolicyValidator
from modules.governance.engine import PolicyEngine
from modules.governance.report import AuditReportBuilder

def run_smoke_test():
    """
    Executes the End-to-End Governance pipeline validation.
    Flow: Load Config -> Validate -> Evaluate -> Generate Audit Package.
    """
    
    # Setup Paths
    config_path = PROJECT_ROOT / "config" / "quality_config.yaml"
    
    print("====================================")
    print("Governance Smoke Test")
    print("Version : 1.0.0")
    print("====================================")
    
    start_time = perf_counter()
    
    try:
        # 1. Load Configuration: Reads YAML and parses into immutable domain models
        print("1. Loading configuration...", end=" ")
        config = PolicyLoader.load(config_path)
        assert config is not None, "Policy config loading failed."
        print("✓ PASS")

        # 2. Validate Configuration: Orchestrates logic rules against the config
        print("2. Validating policy...", end=" ")
        report = PolicyValidator.validate(config, "TEST-001", "TEST-CORR-001")
        assert report is not None, "Policy validation failed."
        print(f"✓ PASS ({report.summary.passed} Passed)")

        # 3. Evaluate Decision: Determines release status based on validated rules
        print("3. Evaluating policy...", end=" ")
        decision = PolicyEngine.evaluate(report, config)
        assert decision is not None, "Policy evaluation failed."
        print(f"✓ PASS ({decision.release_status.value})")

        # 4. Build Audit Package: Consolidates artifacts for regulatory compliance
        print("4. Building audit...", end=" ")
        audit_pkg = AuditReportBuilder.build_audit_package(report, decision)
        audit_json = AuditReportBuilder.to_json(audit_pkg)
        assert audit_json and len(audit_json) > 0, "Audit serialization failed."
        print(f"✓ PASS ({len(audit_json)} bytes)")

        elapsed = perf_counter() - start_time
        print(f"\nCompleted in {elapsed:.3f}s")
        print("\nAll Governance Tests Passed Successfully.")
        return 0

    except Exception:
        print(f"\n! FAILED")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(run_smoke_test())