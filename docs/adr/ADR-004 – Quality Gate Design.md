# ADR-004: Quality Gate Design

**Status:** Accepted (Baseline v1.0)  
**Date:** 2026-07-05  
**Owner:** Engineering Governance  
**Version:** 1.0.0  
**Review Frequency:** Annual or upon major architectural change  
**Next Review:** 2027-07-05  

---

## 1. Context & Problem Statement
Pharma AI operates as a safety-critical CDSS. Ensuring that clinical data ingestion, configuration changes, and logic updates do not compromise system integrity is paramount. We require a mathematical and deterministic enforcement point to prevent non-compliant builds from reaching production without error-prone manual intervention.

## 2. Decision Statement (Binding)
**Pharma AI SHALL implement a mandatory, configuration-driven Quality Gate as the final enforcement point in the deployment pipeline. Every clinical release SHALL be evaluated against a weighted Quality Score derived from the Policy Engine. No release SHALL proceed to production if the status is lower than `ACCEPTABLE` or if any `CRITICAL` severity validation rule is triggered. Manual overrides SHALL NOT bypass the mandatory validation pipeline.**

## 3. Quality Gate Principles
* **Safety over Deployment Speed:** Patient safety is non-negotiable.
* **No Validation Bypass:** Automated validation is mandatory for all release types (including hotfixes).
* **Deterministic Decision:** Same input must yield the same release decision.
* **Configuration-Driven:** Logic thresholds are defined in external governance files.
* **Fully Auditable:** Every decision must be traceable to a specific audit report.

## 4. Gate Inputs & Outputs
* **Inputs:** `Validation Report`, `quality_config.yaml`, `validation_rules.yaml`, `release_policy.md`, `clinical_policy.md`.
* **Outputs:** `Quality Score`, `Release Status`, `JSON/CSV Audit Report`, `Release Decision`, `Recommendations`.

## 5. Decision Matrix
| Build Score | Status | Release Action |
| :--- | :--- | :--- |
| **98 – 100** | `PRODUCTION_READY` | Automated transition allowed. |
| **90 – 97** | `ACCEPTABLE` | Automated transition subject to policy-defined reviews. |
| **80 – 89** | `NEEDS_REVIEW` | Pipeline blocked; requires manual clinical panel review. |
| **< 80** | `FAILED` | Build rejected; immediate remediation required. |

## 6. Architecture & Execution Flow
```mermaid
graph TD
    VE[Validation Engine] --> VR[Validation Report]
    VR --> QG[Quality Gate]
    subgraph QG [Quality Gate Internal]
        TE[Threshold Evaluation]
        PE[Policy Evaluation]
        RD[Release Decision]
    end
    QG --> TE
    TE --> PE
    PE --> RD
    RD --> Audit[Generate Immutable Audit Report]
    Audit --> RP[Release Package]