# ADR-002: Tiered Validation Strategy

**Status:** Accepted  
**Date:** 2026-07-05  
**Owner:** Engineering Governance  
**Version:** 1.0.0  
**Review Frequency:** Annual or upon major governance cycle update  
**Next Review:** 2027-07-05  

---

## 1. Context
Pharma AI is a safety-critical Enterprise-Grade Clinical Decision Support System (CDSS). Ingesting, transforming, and presenting clinical data involves inherent risks of data corruption, conceptual logical gaps, and omission of vital safety instructions. To ensure absolute clinical safety without paralyzing the integration pipeline during non-critical updates, a multi-tiered risk-based validation infrastructure is mandatory.

## 2. Problem Statement
How can Pharma AI enforce absolute medical safety guardrails, detect clinical logical inconsistencies, and track minor data quality degradation without resulting in a brittle ingestion system that uniformly hard-fails on minor informational gaps?

## 3. Decision Statement (Binding)
**Pharma AI SHALL implement a Risk-Based Tiered Validation Strategy that classifies data validation checks into three distinct levels: Critical (Hard Fail), Clinical Consistency (Soft Fail / High Severity), and Informational. The system SHALL programmatically calculate a weighted Quality Score for every data ingest execution run and evaluate it against a strict configuration-driven Quality Gate before permitting any production release. Validation SHALL be deterministic.**

## 4. Validation Tier Specifications

### Level 1 — Critical (Hard Fail) 🚫
Failures at this level represent structural breakdowns or missing vital identifiers that prevent safe execution or parsing.
*   **Examples:** Orphan foreign keys, invalid ATC hierarchy links, missing `Generic_ID`, duplicate primary mapping records, corrupted CSV schemas, invalid Enum values, or missing mandatory safety-critical fields.
*   **Action:** Immediately raise an exception, abort the pipeline run, log a critical error, and prevent the generation of a `ClinicalContext`.

### Level 2 — Clinical Consistency (Soft Fail + High Severity) ⚠️
Data structure is intact, but a logical contradiction exists within the clinical knowledge domain, creating potential medical risk.
*   **Examples:** A drug marked as 'Pregnancy Category X' but missing an accompanying Contraindication mapping, a severe drug-drug interaction missing an explicit clinical warning note, or a renal/hepatic adjustment entry missing standardized dosage guidance.
*   **Action:** Log as high-severity anomalies, append detailed entries to the `ValidationReport`, allow the compilation run to complete for auditing purposes, but block the Quality Gate release phase.

### Level 3 — Informational 📝
Minor documentation or data completeness discrepancies that do not compromise patient safety or logical evaluation.
*   **Examples:** Empty entity description text fields, missing chemical synonyms, absent non-critical WHO references.
*   **Action:** Record as warnings/informational entries within the reporting logs for continuous quality improvement cycles.

---

## 5. Decision Rationale
*   **Safety Isolation:** Isolates critical structural breaking points from medical logic discrepancies, preventing corrupted formats from infiltrating downstream engines.
*   **Granular Governance:** Quantifies data health, allowing clinical reviewers to see exactly where clinical inconsistencies lie.
*   **Policy Decoupling:** Decouples policy thresholds from code execution logic via external configuration integration.

## 6. Validation Architecture & Order
All data will be validated in the following deterministic sequence:
1. **Schema Validation** (Structural integrity)
2. **Structure Validation** (Format correctness)
3. **Referential Validation** (Relationship checks)
4. **Clinical Validation** (Logical safety checks)
5. **Governance Validation** (Policy adherence)
6. **Quality Gate** (Final release decision)

## 7. Non-Functional Requirements
*   **Auditability:** Every validation run must generate an immutable audit trail.
*   **Determinism:** Same Input -> Same Output -> Same Quality Score -> Same Report.
*   **Extensibility:** Adding new rules must not modify core execution logic.

## 8. Success Criteria
* 100% of pipeline data ingestion passes through all defined validation layers.
* Critical failures block execution before any export artifacts are modified.
* A structured report containing the explicit weighted quality score is generated on every run.

---

## 9. Technical Metrics & Schema Contracts

### Quality Score Formulation
$$\text{Quality Score} = 100 - (\text{CriticalCount} \times 20) - (\text{HighCount} \times 5) - (\text{MediumCount} \times 2) - (\text{LowCount} \times 0.5)$$

### Build Status Threshold Matrix
| Score Range | Release Status | Action Requirements |
| :--- | :--- | :--- |
| **98 – 100** | `PRODUCTION_READY` | Automated transition allowed. |
| **90 – 97** | `ACCEPTABLE` | Requires automated tracking logs and Data Steward sign-off. |
| **80 – 89** | `NEEDS_REVIEW` | Pipeline blocks; requires manual clinical panel review. |
| **< 80** | `FAILED` | Build rejected; immediate remediation required. |

### Validation Result Contract Schema
Every generated error event must follow this strict model definition:
```json
{
  "run_id": "string (UUID)",
  "validator": "string",
  "rule_id": "string (Pattern: [A-Z]{3,4}\\d{3})",
  "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO",
  "status": "FAIL | WARN | PASS",
  "entity_type": "string",
  "entity_id": "string",
  "message": "string",
  "timestamp": "string (ISO 8601)"
}