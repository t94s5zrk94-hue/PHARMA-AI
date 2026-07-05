# ADR-003: Repository Pattern & Immutable Domain Model Strategy

**Status:** Accepted  
**Date:** 2026-07-05  
**Owner:** Engineering Governance  
**Version:** 1.0.0  
**Review Frequency:** Annual or upon major architectural change  
**Next Review:** 2027-07-05  

---

## 1. Context
Pharma AI functions as an Enterprise-Grade Clinical Decision Support System (CDSS). Direct coupling between data persistence layers (CSV/SQL/API) and the clinical intelligence logic (ClinicalContext) introduces significant risks of data mutation, tight coupling, and testing complexities.

## 2. Problem Statement
How can we ensure that business logic remains agnostic of the underlying data source while guaranteeing that clinical entities cannot be accidentally modified during the lifecycle of a request, thereby ensuring absolute clinical truth and deterministic evaluation?

## 3. Decision Statement (Binding)
**Pharma AI SHALL implement the Repository Pattern to decouple data access logic from clinical business logic. Furthermore, all repositories SHALL return Immutable Domain Models (Frozen Objects). Under no circumstances SHALL raw data entities (e.g., mutable dictionaries or raw ORM objects) be exposed to the business layer. Repository implementations SHALL NOT contain business/clinical logic.**

## 4. Decision Rationale
* **Decoupling:** Business logic remains agnostic of the data source, allowing infrastructure changes without affecting clinical intelligence.
* **Integrity (Immutability):** Frozen domain models prevent accidental mutation of critical clinical data during execution.
* **Testability:** Decoupled interfaces allow for the injection of high-fidelity Mocks/Stubs, enabling isolated testing of clinical business rules.
* **Auditability:** Centralized access via the Repository layer provides a single point to hook logging, auditing, and performance metrics.

## 5. Repository Contract
* **Repository SHALL:** Read, Search, Filter, Map, and Return Immutable Objects.
* **Repository SHALL NOT:** Execute AI logic, Build prompts, Apply clinical decisions, or Modify Domain Objects.
* **Dependency Rule:** Business Layer depends only on Repository Interfaces. Storage implementations NEVER depend on the Business Layer.

## 6. Architecture & Runtime Flow
```mermaid
graph TD
    BL[Clinical Business Layer] --> Interface[Repository Interface]
    Interface --> Impl[Repository Implementation]
    Impl --> Mapper[Mapper]
    Mapper --> Model[Immutable Domain Model]
    Model --> Persistence[Persistence Layer]