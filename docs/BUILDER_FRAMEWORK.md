# Pharma AI Builder Framework
## Enterprise Data Builder Architecture Documentation

---

**Project Name:** Pharma AI

**Document:** Builder Framework Documentation

**Document ID:** PHARMA-BUILDER-001

**Version:** 1.0.0

**Status:** Official

**Author:** Ravi Varsani

**Last Updated:** July 2026

---

# Document Classification

| Item | Value |
|------|-------|
| Type | Enterprise Technical Documentation |
| Module | Builder Framework |
| Audience | Developers, Data Engineers |
| Repository | docs/BUILDER_FRAMEWORK.md |

---

# Purpose

This document defines the official Builder Framework architecture used by Pharma AI.

It explains:

- Builder philosophy
- Builder lifecycle
- Builder architecture
- Standard interfaces
- ID generation
- Data normalization
- Metadata generation
- Builder standards

This document serves as the authoritative reference for all Builder implementations.

---

# Builder Philosophy

The Builder Framework transforms raw datasets into validated production datasets.

Builders are responsible for:

- Importing data
- Cleaning data
- Normalizing values
- Generating identifiers
- Creating production master CSV files

Builders never perform runtime operations.

---

# Builder Design Goals

The framework is designed to provide:

- Reproducible output
- Deterministic processing
- Reusable components
- Consistent metadata
- Stable identifiers
- Validation-ready datasets

---

# Builder Architecture

```text
Input CSV

↓

Builder

↓

Normalization

↓

ID Generation

↓

Metadata

↓

Master CSV

↓

Validation

↓

Audit
```

Builders always execute offline.

---

# Builder Responsibilities

Builders are responsible for:

- Reading input files
- Data normalization
- Duplicate removal
- Metadata generation
- Master dataset creation

Builders are NOT responsible for:

- UI rendering
- Runtime search
- Clinical decision support
- User interaction

---

# Builder Categories

Current Builder Framework includes:

| Builder | Purpose |
|----------|---------|
| Generic Builder | Generic master generation |
| Company Builder | Company master generation |
| Brand Builder | Brand master generation |
| Product Builder | Product master generation |
| ATC Builder | WHO ATC master generation |
| Generic ATC Mapping Builder | Generic ↔ ATC mapping |
| Generic Class Mapping Builder | Generic ↔ Class mapping |
| Clinical Builders | Clinical master generation |

Future builders should follow the same framework.

---

# Builder Lifecycle

```text
Import

↓

Normalize

↓

Validate Internal Data

↓

Generate IDs

↓

Generate Metadata

↓

Export Master CSV

↓

Validator

↓

Audit
```

Each stage must complete successfully before proceeding.

---

# Standard Builder Workflow

Every Builder should follow the same processing sequence.

1. Load Input Dataset

↓

2. Validate Required Columns

↓

3. Normalize Data

↓

4. Generate IDs

↓

5. Remove Duplicates

↓

6. Generate Metadata

↓

7. Export Master CSV

↓

8. Return Processing Report

This workflow should remain consistent across all builders.

---

# BaseBuilder

All builders should inherit from a common BaseBuilder.

Responsibilities of BaseBuilder:

- Logging
- Common validation
- Metadata generation
- Export utilities
- Error handling

This minimizes duplicate implementation across builders.

---

# Builder Independence

Every Builder should remain independent.

Example

Generic Builder

↓

Produces Generic Master

↓

Stops

It must never invoke Product Builder or Clinical Builders directly.

Pipeline orchestration belongs to higher-level workflows.

---

# Builder Output

Every Builder produces:

- Production CSV
- Processing statistics
- Log entries
- Optional report

Builders should never directly modify existing production data.

# BaseBuilder Architecture

The BaseBuilder is the foundation of the Pharma AI Builder Framework.

Every production builder should inherit common functionality from BaseBuilder.

The objective is to eliminate duplicate code and provide consistent behavior across all builders.

---

# BaseBuilder Responsibilities

The BaseBuilder provides common infrastructure for all builders.

Typical responsibilities include:

- Input loading
- Logging
- Error handling
- Metadata generation
- Export utilities
- Common validation
- Statistics collection

Individual builders should only implement business-specific logic.

---

# Builder Inheritance

```text
                    BaseBuilder
                         │
 ┌───────────────────────┼────────────────────────┐
 │                       │                        │
 ▼                       ▼                        ▼
GenericBuilder     CompanyBuilder         BrandBuilder
 │                       │                        │
 ▼                       ▼                        ▼
ProductBuilder      ATCBuilder        Clinical Builders
```

Every builder follows the same lifecycle while implementing its own transformation logic.

---

# Builder Contract

Every Builder should implement the following logical workflow.

```text
Load

↓

Validate

↓

Normalize

↓

Transform

↓

Generate IDs

↓

Generate Metadata

↓

Export

↓

Return Report
```

This contract ensures consistency throughout the project.

---

# Standard Builder Interface

Every builder should expose a consistent public interface.

Conceptually:

```python
builder.build()
```

Expected Result

```python
BuilderResult
```

The internal implementation may vary while preserving the public contract.

---

# BuilderResult

Every builder should produce structured execution information.

Typical information includes:

- Builder Name
- Status
- Records Read
- Records Generated
- Records Skipped
- Processing Time
- Output File
- Warnings
- Errors

Builder results improve automation and release reporting.

---

# ID Generation Framework

Every production entity requires a permanent identifier.

ID generation must be:

- Deterministic
- Collision-free
- Sequential
- Immutable

Identifiers should never depend on row order after release.

---

# Standard ID Prefixes

| Entity | Prefix |
|----------|---------|
| Generic | GEN |
| Company | CMP |
| Brand | BRD |
| Product | PRD |
| ATC | ATC |
| Mapping | MAP |

Clinical entity prefixes should follow the official project standard defined in the database documentation.

---

# ID Generation Rules

Every generated identifier must satisfy:

✓ Unique

✓ Stable

✓ Permanent

✓ Never reused

Example

```
GEN000001

GEN000002

GEN000003
```

Deleted identifiers remain retired.

---

# Metadata Framework

Every production record should include standard metadata.

Recommended fields:

- Status
- created_at
- updated_at
- source
- version

This metadata enables:

- Traceability
- Auditing
- Version control
- Release management

---

# Timestamp Policy

Builders generate timestamps during dataset creation.

Typical metadata:

```
created_at

updated_at
```

Runtime components must never modify these values.

---

# Source Policy

Every production record should identify its origin.

Example

```
source = Pharma AI
```

Future integrations may introduce additional approved source values.

---

# Version Policy

Every Builder assigns the dataset version.

Example

```
version = 1.0
```

Version values should remain synchronized with the project release process.

---

# Builder Logging

Builders should generate structured logs.

Recommended log events:

INFO

- Builder started
- Input loaded
- Output generated

WARNING

- Duplicate removed
- Missing optional field

ERROR

- Required column missing
- Invalid data
- Export failure

Logging should support debugging without exposing sensitive information.

---

# Builder Statistics

Every Builder should report execution statistics.

Recommended metrics:

- Input Records
- Output Records
- Duplicate Records
- Invalid Records
- Processing Time

Statistics support engineering monitoring and release reporting.

---

# Error Handling

Expected Builder failures include:

- Missing input file
- Missing required column
- Invalid format

Unexpected failures should:

- Stop processing safely
- Preserve diagnostic information
- Produce a structured error report

Partial production output should never be released.

---

# Builder Independence

Builders should never invoke other builders directly.

Correct architecture:

```
Workflow Manager

↓

Generic Builder

↓

Company Builder

↓

Brand Builder
```

Incorrect architecture:

```
Generic Builder

↓

Brand Builder
```

Builder orchestration belongs outside the individual builder implementation.

---

# Part Summary

This chapter defines:

- BaseBuilder architecture
- Builder contract
- Standard interface
- BuilderResult
- ID generation
- Metadata framework
- Logging
- Statistics
- Error handling
- Builder independence

These standards provide a consistent engineering foundation for all current and future Pharma AI builders.

# Data Normalization Framework

Normalization is the process of converting raw input data into a consistent production format.

Every Builder MUST normalize data before generating production datasets.

Normalization improves:

- Data consistency
- Search accuracy
- Mapping integrity
- Clinical reliability

---

# Normalization Pipeline

```text
Raw Input

↓

Trim Whitespace

↓

Normalize Case

↓

Standardize Values

↓

Validate Format

↓

Normalize Relationships

↓

Production Object
```

Normalization MUST occur before ID generation.

---

# Normalization Rules

The following normalization rules apply across all builders.

## Text Fields

Builders MUST:

- Remove leading spaces
- Remove trailing spaces
- Collapse multiple spaces
- Preserve meaningful punctuation

Example

```
"  Paracetamol  "

↓

"Paracetamol"
```

---

## Case Normalization

Medicine names SHOULD follow project naming standards.

Example

```
PARACETAMOL

↓

Paracetamol
```

---

## Combination Medicines

Combination medicines MUST preserve component order.

Example

```
Aceclofenac + Paracetamol
```

Builders MUST NOT reorder medicine components unless an approved normalization rule exists.

---

## Empty Values

Builders MUST distinguish between:

- Missing value
- Empty string
- Unknown value

These values should not be treated as identical.

---

## Duplicate Handling

Builders MUST detect duplicate records before export.

Duplicate policy:

```
Duplicate

↓

Evaluate

↓

Keep Valid Record

↓

Discard Duplicate

↓

Log Event
```

Duplicate removal must be deterministic.

---

# Validation Integration

Every Builder integrates with the Validation Framework.

Builder processing sequence:

```text
Input

↓

Normalization

↓

Builder Validation

↓

Export

↓

Validator

↓

Audit
```

Builders MUST NOT bypass the Validator.

---

# Internal Builder Validation

Builders should perform lightweight validation before export.

Examples:

- Required fields present
- Mandatory relationships available
- Invalid values detected
- Empty identifiers rejected

Comprehensive validation belongs to the Validator Framework.

---

# Business Rule Validation

Builders should verify project-specific business rules before export.

Examples:

- Approved dosage forms
- Approved routes
- Approved status values
- Approved schedules

Business rule violations should be reported clearly.

---

# Export Pipeline

After successful processing, the Builder exports production datasets.

Pipeline:

```text
Validated Objects

↓

Generate CSV

↓

Write Metadata

↓

Save Master File

↓

Return Builder Result
```

Export must be atomic whenever possible.

---

# Export Standards

Every exported production file MUST:

✓ Use UTF-8 encoding

✓ Include official header

✓ Preserve column order

✓ Include metadata

✓ Contain validated records only

---

# Output File Rules

Production datasets MUST be:

- Builder generated
- Version controlled
- Immutable during runtime

Manual editing is prohibited.

---

# File Naming Standard

Recommended naming convention:

```
generic_master.csv

company_master.csv

brand_master.csv

product_master.csv

atc_master.csv
```

Naming should remain stable across releases.

---

# Processing Report

Every Builder SHOULD produce a processing report.

Recommended contents:

- Builder Name
- Input Records
- Output Records
- Duplicate Records
- Invalid Records
- Warnings
- Errors
- Processing Time

Processing reports improve release traceability.

---

# Failure Handling

If a Builder encounters a critical failure:

```text
Stop Processing

↓

Log Error

↓

Return Failure Result

↓

Do Not Export
```

Partial master datasets MUST NOT be released.

---

# Recovery Strategy

Builders SHOULD support rerunning from the same input dataset.

Repeated execution using identical input SHOULD produce identical output.

This deterministic behavior simplifies testing and auditing.

---

# Integration with Governance

Builder output enters the Governance Pipeline only after:

✓ Successful Export

✓ Validation PASS

✓ Audit PASS

↓

Governance Review

↓

Production Approval

Builders are responsible only for generating production-ready datasets.

Governance is responsible for release approval.

---

# Part Summary

This chapter defines:

- Data Normalization
- Duplicate Handling
- Validation Integration
- Export Pipeline
- Processing Reports
- Failure Handling
- Recovery Strategy
- Governance Integration

These standards ensure that every Pharma AI Builder produces consistent, reproducible, and production-ready datasets.

# Builder Testing Strategy

Every Builder MUST be independently testable.

Testing ensures that production datasets remain reliable, reproducible, and regression-free.

Builders should never be released without successful testing.

---

# Testing Pyramid

```text
           End-to-End Tests

                 ▲

         Integration Tests

                 ▲

            Unit Tests
```

Each Builder should have test coverage at all three levels.

---

# Unit Testing

Unit tests verify individual Builder behavior.

Recommended unit tests:

- Input loading
- Required column validation
- Data normalization
- ID generation
- Metadata generation
- Duplicate detection
- Export generation

Each unit test should validate one logical behavior.

---

# Integration Testing

Integration tests verify Builder interaction with the framework.

Typical integration tests:

- Builder → Validator
- Builder → Export
- Builder → Logging
- Builder → Governance Pipeline

Integration tests should use representative production datasets.

---

# Regression Testing

Regression tests ensure that previously correct behavior remains unchanged.

Regression verification should include:

- Output consistency
- ID stability
- Metadata consistency
- Duplicate handling
- Export format

Regression failures must block release.

---

# Golden Dataset Verification

Every Builder SHOULD be tested using the approved Golden Dataset.

Verification includes:

- Record count
- ID consistency
- Metadata correctness
- Schema validation
- Referential integrity

Golden Dataset tests provide production confidence.

---

# Builder Logging Standards

Builders MUST produce structured logs.

Recommended log levels:

INFO

- Builder started
- Records loaded
- Export completed

WARNING

- Duplicate removed
- Optional value missing
- Deprecated value detected

ERROR

- Missing required column
- Invalid relationship
- Export failure

DEBUG

- Normalization details
- Internal processing
- ID generation

Production releases should disable verbose debug logging.

---

# Performance Guidelines

Builder optimization should focus on:

- Efficient file reading
- Minimal memory duplication
- Deterministic processing
- Efficient duplicate detection

Performance improvements must never reduce correctness.

---

# Performance Metrics

Recommended Builder metrics:

- Input record count
- Output record count
- Processing duration
- Duplicate count
- Invalid record count
- Export duration

Metrics support benchmarking and release monitoring.

---

# Memory Management

Builders SHOULD process datasets efficiently.

Recommended practices:

- Avoid unnecessary object duplication
- Release temporary resources promptly
- Reuse shared normalization utilities

Large datasets should remain processable without excessive memory usage.

---

# Best Practices

Builders SHOULD:

✓ Follow the BaseBuilder contract

✓ Produce deterministic output

✓ Use shared utilities

✓ Generate complete metadata

✓ Log important events

✓ Remain independent

Builders MUST NOT:

✗ Access UI components

✗ Perform runtime search

✗ Execute clinical recommendations

✗ Modify production datasets after export

---

# Maintainability

Builders should prioritize readability over unnecessary optimization.

Recommended practices:

- Small functions
- Clear variable names
- Explicit processing steps
- Shared helper utilities
- Minimal code duplication

Maintainability supports long-term project growth.

---

# Documentation Requirements

Every Builder should include:

- Purpose
- Input
- Output
- Dependencies
- Processing Steps
- Error Conditions

Builder documentation should remain synchronized with implementation.

---

# Continuous Improvement

Builder quality should improve through:

- Code review
- Benchmarking
- Regression testing
- Documentation updates
- Architecture review

Engineering improvements should preserve backward compatibility whenever possible.

---

# Current Implementation

Current Pharma AI Builders:

- Generic Builder
- Company Builder
- Brand Builder
- Product Builder
- ATC Builder
- Generic ATC Mapping Builder
- Generic Class Mapping Builder
- Clinical Builders

All production datasets are Builder-generated.

---

# Architecture Standard

The Builder Framework defines the official method for producing production datasets.

No alternative generation mechanism is approved.

All future Builders MUST conform to the BaseBuilder architecture.

---

# Future Enhancements

Planned improvements include:

- Parallel Builder execution
- Incremental builds
- Dependency-aware build orchestration
- Build caching
- Automated quality dashboards
- CI/CD integration

Future enhancements should preserve deterministic output.

---

# Part Summary

This chapter defines:

- Testing Strategy
- Logging Standards
- Performance Guidelines
- Best Practices
- Maintainability
- Documentation Requirements
- Current Implementation
- Architecture Standard
- Future Enhancements

These standards ensure consistent engineering quality across the entire Builder Framework.

# Enterprise Builder Rules

The following rules are mandatory for every Builder implementation within Pharma AI.

These rules ensure consistency, reproducibility, and production quality.

---

## Rule 1 — Single Responsibility

Each Builder MUST produce one logical dataset only.

Examples:

- Generic Builder → Generic Master
- Company Builder → Company Master
- ATC Builder → ATC Master

A Builder MUST NOT generate multiple unrelated datasets.

---

## Rule 2 — Offline Processing

Builders MUST execute offline.

Builders are development tools.

They are never executed during application runtime.

---

## Rule 3 — Immutable Production Data

Builders generate production datasets.

They MUST NOT modify production datasets after successful export.

Production changes require a new Builder execution.

---

## Rule 4 — Deterministic Output

Given:

- Same input
- Same Builder version
- Same configuration

The generated output MUST be identical.

---

## Rule 5 — Validation Required

Every Builder output MUST pass:

- Validation
- Audit
- Governance Review

before becoming production data.

---

# Builder Lifecycle

The complete Builder lifecycle is:

```text
Import Template

↓

Input Dataset

↓

Builder

↓

Normalization

↓

ID Generation

↓

Metadata Generation

↓

Master CSV

↓

Validation

↓

Audit

↓

Governance

↓

Production Release
```

Every stage is mandatory.

---

# Builder Dependency Rules

Builders MUST remain independent.

Correct dependency flow:

```text
Builder

↓

Validator

↓

Audit

↓

Governance
```

Incorrect flow:

```text
Builder

↓

Clinical Engine
```

```text
Builder

↓

Search Engine
```

Builders never communicate with runtime modules.

---

# Builder Governance

Builder execution is governed by the following principles:

- Controlled execution
- Version tracking
- Structured logging
- Release approval
- Audit traceability

Every production dataset should have a complete build history.

---

# Release Requirements

A Builder release is approved only when:

✓ Build Successful

✓ Validation PASS

✓ Audit PASS

✓ Health Score Acceptable

✓ Documentation Updated

✓ CHANGELOG Updated

✓ Git Commit

✓ Git Tag

---

# Builder Checklist

Before approving Builder output verify:

- Schema correct
- IDs generated
- Metadata complete
- No duplicate records
- Referential integrity maintained
- Output file generated
- Validation passed
- Audit passed

---

# Builder Versioning

Builders should follow Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Examples:

```
2.0.0

1.4.0

1.4.2
```

Builder versions should remain compatible with the project release process.

---

# Builder Documentation Standard

Every Builder should include:

- Overview
- Purpose
- Input Dataset
- Output Dataset
- Dependencies
- Processing Steps
- Validation Rules
- Error Conditions
- Example Execution

This documentation simplifies onboarding and maintenance.

---

# Current Implementation

Current Pharma AI Builder Framework includes:

- BaseBuilder
- Generic Builder
- Company Builder
- Brand Builder
- Product Builder
- ATC Builder
- Generic ATC Mapping Builder
- Generic Class Mapping Builder
- Clinical Builders

All production datasets are generated through this framework.

---

# Architecture Standard

The Builder Framework is the official production data generation mechanism.

Alternative approaches require architectural review and approval.

The Builder Framework remains the only approved path for generating production master datasets.

---

# Future Enhancements

Planned Builder Framework improvements:

- Dependency-aware build execution
- Incremental dataset generation
- Parallel build pipeline
- Build manifest generation
- Automatic validation triggering
- CI/CD pipeline integration
- Build quality dashboard

These enhancements should preserve the existing Builder contract.

---

# Related Documents

This document should be read together with:

- ARCHITECTURE.md
- DATABASE.md
- VALIDATION_FRAMEWORK.md
- GOVERNANCE.md

These documents collectively define the complete production data lifecycle.

---

# Builder Framework Summary

The Pharma AI Builder Framework is responsible for transforming raw datasets into validated production datasets.

Core characteristics:

- Offline execution
- Deterministic processing
- Stable identifiers
- Standard metadata
- Validation-first workflow
- Audit-ready output

The framework is designed for long-term maintainability and enterprise-scale data management.

---

# Approval

Document Status

Approved

Version

1.0.0

Owner

Pharma AI Project

Location

docs/BUILDER_FRAMEWORK.md

This document serves as the official Builder Framework reference for all current and future Pharma AI development.