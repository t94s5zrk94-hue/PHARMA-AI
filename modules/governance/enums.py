from enum import Enum

class ValidationStage(str, Enum):
    SCHEMA = "SCHEMA"
    STRUCTURE = "STRUCTURE"
    REFERENTIAL = "REFERENTIAL"
    CLINICAL = "CLINICAL"
    GOVERNANCE = "GOVERNANCE"

class ValidationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class ReleaseStatus(str, Enum):
    PRODUCTION_READY = "PRODUCTION_READY"
    ACCEPTABLE = "ACCEPTABLE"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    FAILED = "FAILED"