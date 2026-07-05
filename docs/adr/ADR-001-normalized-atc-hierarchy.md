# ADR-001: Normalized ATC Hierarchy

**Status:** Accepted  
**Date:** 2026-07-05  
**Owner:** Engineering Governance  
**Version:** 1.0.0  
**Review Frequency:** Annual or upon major architectural change  
**Next Review:** 2027-07-05  

---

## 1. Context
Pharma AI requires a robust and internationally recognized standard for drug classification to support clinical decision-making. The World Health Organization (WHO) Anatomical Therapeutic Chemical (ATC) classification system is the industry standard for this purpose.

## 2. Problem Statement
How to structure the ATC hierarchy within our data architecture to minimize redundancy, ensure referential integrity, and facilitate complex clinical mappings (e.g., interactions, contraindications) without incurring high maintenance costs?

## 3. Decision Statement (Binding)
**Pharma AI SHALL adopt a fully normalized WHO ATC hierarchy as the canonical classification model for all ATC-related clinical data. All future ATC integrations SHALL conform to this architecture unless superseded by a future approved ADR.**

## 4. Decision Rationale
* **Maintenance:** Lowest long-term maintenance cost through normalized structure.
* **Integrity:** Strong referential integrity via foreign key relationships.
* **Validation:** Simplifies the validation framework by isolating hierarchical levels.
* **Interoperability:** Facilitates future integration with the Evidence Layer and international clinical databases.
* **Auditability:** Provides a clear, traceable path from the WHO source to the clinical context.

## 5. Alternatives Considered
* **Option A (Single CSV):** Rejected due to high data redundancy, poor maintenance, and higher update costs.
* **Option B (Normalized Hierarchy):** **Accepted.** Balances scalability, integrity, and WHO compatibility.
* **Option C (SQLite/SQL DB only):** Rejected for current development phase; prefers CSV-first strategy to maintain Git diff visibility and simpler auditing.

## 6. Assumptions
* The WHO ATC dataset is the authoritative source.
* Generic drug master data is available.
* Each Generic Drug may map to one or more ATC codes (Many-to-Many).
* CSV files are the primary storage during the development phase.

## 7. Scope & Out of Scope
* **In Scope:** ATC Levels 1-5, Master Tables, Mapping Tables.
* **Out of Scope:** Therapeutic Class, Pharmacological Class, Evidence Repository, Clinical Guidelines, Repository/Builder implementation details.

## 8. Non-Functional Requirements
* **Referential Integrity:** Enforced at the schema level.
* **Deterministic Mapping:** Mapping rules must be consistent and reproducible.
* **Traceability:** Every mapping must be linked to a source and version.
* **Extensibility:** Must support future clinical classification expansions.

## 9. Success Criteria
* Levels 1-5 hierarchy are fully normalized.
* Zero orphan hierarchies or duplicate ATC codes.
* Generic-to-ATC mapping validation passes 100%.

## 10. Migration Strategy
1. Raw WHO Data Ingestion
2. Parsing & Normalization
3. Validation via Tiered Framework
4. Repository Sync
5. Clinical Context Consumption

## 11. Architecture Diagram
```mermaid
graph TD
    WHO[WHO Dataset] --> Pipe[ATC Pipeline]
    Pipe --> Master[Normalized Masters L1-L5]
    Master --> Valid[Validation Engine]
    Valid --> Repo[ATC Repository]
    Repo --> Context[Clinical Context]
    Context --> Prompt[Prompt Builder]