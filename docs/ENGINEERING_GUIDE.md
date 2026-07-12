# Pharma AI Engineering Guide
## Official Engineering Manual

---

**Project Name:** Pharma AI

**Document:** Engineering Guide

**Document ID:** PHARMA-ENG-001

**Version:** 1.0.0

**Status:** Official

**Author:** Ravi Varsani

**Last Updated:** July 2026

---

# Document Classification

| Item | Value |
|------|-------|
| Type | Engineering Manual |
| Audience | Developers, AI Engineers, Data Engineers |
| Repository | docs/ENGINEERING_GUIDE.md |

---

# Purpose

This document defines the official engineering workflow followed during Pharma AI development.

Unlike PROJECT_STANDARDS.md, which defines immutable project standards, this guide explains how engineering work should be planned, implemented, tested, reviewed, and released.

It serves as the operational handbook for all contributors.

---

# Relationship with Other Documents

This guide should be read together with:

- PROJECT_STANDARDS.md
- ARCHITECTURE.md
- BUILDER_FRAMEWORK.md
- VALIDATION_FRAMEWORK.md
- GOVERNANCE.md
- CONTRIBUTING.md

PROJECT_STANDARDS.md defines *what* the project standard is.

ENGINEERING_GUIDE.md explains *how* engineers should work within those standards.

---

# Engineering Philosophy

Pharma AI follows an engineering-first approach.

Core principles:

- Patient safety before features
- Deterministic processing before AI
- Validation before release
- Evidence before explanation
- Documentation with implementation

Engineering quality always has higher priority than development speed.

---

# Engineering Lifecycle

Every feature should follow the official engineering lifecycle.

```text
Requirement

↓

Design

↓

Implementation

↓

Builder

↓

Validation

↓

Audit

↓

Testing

↓

Documentation

↓

Git Commit

↓

Release
```

Skipping lifecycle stages is not permitted.

---

# Engineering Goals

Every engineering activity should improve one or more of the following:

- Reliability
- Maintainability
- Performance
- Traceability
- Clinical Safety
- Code Quality

---

# Engineering Principles

## Principle 1

Build once.

Reuse everywhere.

---

## Principle 2

Keep business logic deterministic.

---

## Principle 3

Avoid duplicated implementation.

---

## Principle 4

Every production dataset must be generated.

Never manually maintained.

---

## Principle 5

Every release must be reproducible.

---

# Engineering Layers

Development follows the layered architecture.

```text
Builders

↓

Validators

↓

Repositories

↓

Services

↓

Search

↓

Clinical Engine

↓

AI Layer

↓

UI
```

Each layer has a single responsibility.

---

# Engineering Workflow Overview

The Pharma AI engineering workflow consists of:

1. Design
2. Development
3. Validation
4. Testing
5. Documentation
6. Governance
7. Release

Each stage has independent quality requirements.

---

# Summary

This guide defines the operational engineering practices used throughout Pharma AI development.

All contributors should follow this workflow to ensure consistent, maintainable, and production-ready software.

# Builder Engineering Workflow

The Builder Framework is the foundation of Pharma AI production data generation.

Every production dataset MUST be created through a Builder.

Manual editing of production datasets is prohibited.

---

# Builder Development Lifecycle

Every Builder should follow the official engineering lifecycle.

```text
Requirement

↓

Input Dataset Design

↓

Builder Implementation

↓

Builder Execution

↓

Validation

↓

Audit

↓

Documentation

↓

Git Commit
```

Every stage should complete successfully before moving to the next.

---

# Builder Design Phase

Before writing code, define:

- Builder purpose
- Input dataset
- Output dataset
- Dependencies
- Validation requirements
- Metadata requirements

Design should be documented before implementation begins.

---

# Builder Implementation

Each Builder should focus on a single responsibility.

Typical responsibilities:

- Read input
- Normalize data
- Generate identifiers
- Generate metadata
- Export production dataset

Builders should not perform runtime operations.

---

# Builder Execution

Every Builder execution should produce:

- Production dataset
- Execution log
- Processing statistics
- Error summary (if applicable)

Builder execution should be deterministic.

---

# Validation Workflow

Immediately after Builder execution:

```text
Builder

↓

Validator

↓

Validation Report
```

No Builder output should proceed without successful validation.

---

# Audit Workflow

Validated datasets should enter the Audit Framework.

```text
Validation PASS

↓

Audit

↓

Health Score

↓

Audit Report
```

Audit verifies production readiness.

---

# Builder Debugging Workflow

When a Builder fails:

```text
Identify Failure

↓

Review Logs

↓

Correct Input or Logic

↓

Re-run Builder

↓

Re-run Validation

↓

Re-run Audit
```

Debugging should preserve deterministic behavior.

---

# Builder Testing

Every Builder should be tested using:

- Representative datasets
- Edge cases
- Empty datasets (where applicable)
- Duplicate records
- Invalid records

Testing should confirm expected output.

---

# Builder Quality Checklist

Before approving a Builder verify:

✓ Correct output generated

✓ IDs generated correctly

✓ Metadata complete

✓ Validation PASS

✓ Audit PASS

✓ Documentation updated

Builders should not be merged until all checks pass.

---

# Builder Performance

Builders should optimize:

- Processing speed
- Memory usage
- Duplicate detection
- File generation

Performance improvements must not compromise correctness.

---

# Builder Maintenance

When updating a Builder:

- Preserve backward compatibility where practical
- Document changes
- Update related validators if required
- Verify downstream compatibility

Changes should be regression-tested before release.

---

# Current Implementation

Current Pharma AI Builder ecosystem includes:

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

# Future Enhancements

Planned Builder improvements include:

- Parallel Builder execution
- Incremental builds
- Build dependency graph
- Build caching
- CI/CD integration
- Automated build reports

These enhancements should preserve the official Builder contract.

---

# Part Summary

This chapter defines:

- Builder Development Lifecycle
- Builder Design
- Builder Execution
- Validation Workflow
- Audit Workflow
- Debugging Workflow
- Builder Testing
- Builder Quality Checklist
- Current Implementation
- Future Enhancements

These practices ensure consistent, deterministic, and production-ready Builder development throughout the Pharma AI project.

# Validation Engineering Workflow

Validation is the mandatory quality gate after Builder execution.

Every production dataset MUST successfully pass validation before entering the Audit Framework.

Validation verifies:

- Dataset structure
- Data quality
- Referential integrity
- Business rules
- Metadata consistency

---

# Validation Lifecycle

Every Builder output follows:

```text
Builder

↓

Validator

↓

Validation Report

↓

Audit
```

Validation failures must be corrected before continuing.

---

# Validation Checklist

Every validator should verify:

✓ Required columns

✓ Missing values

✓ Duplicate records

✓ Foreign key integrity

✓ Business rules

✓ Metadata

Validation should be deterministic.

---

# Audit Workflow

After successful validation:

```text
Validation PASS

↓

Audit

↓

Health Score

↓

Audit Report

↓

Governance
```

Audit confirms production readiness.

---

# Clinical Module Development Workflow

Every clinical module follows the official engineering process.

```text
Clinical Research

↓

Input Dataset

↓

Clinical Builder

↓

Clinical Validator

↓

Audit

↓

Repository

↓

Clinical Engine

↓

Testing
```

Each stage must be completed before moving forward.

---

# Clinical Dataset Development

Recommended sequence:

1. Define dataset schema

2. Create import template

3. Populate source data

4. Develop Builder

5. Develop Validator

6. Execute Audit

7. Repository integration

8. Runtime testing

This process should remain consistent across all clinical modules.

---

# Testing Strategy

Every engineering change should be tested.

Testing categories include:

- Unit Testing
- Integration Testing
- Regression Testing
- Streamlit Testing
- AI Testing

Each category verifies a different aspect of the system.

---

# Unit Testing

Unit tests verify individual components.

Examples:

- Builder methods
- Validator rules
- Repository methods
- Search utilities

Unit tests should isolate one logical behavior.

---

# Integration Testing

Integration tests verify communication between modules.

Examples:

```text
Builder

↓

Validator
```

```text
Repository

↓

Clinical Engine
```

Integration testing ensures modules work together correctly.

---

# Regression Testing

Regression testing verifies that existing functionality remains unchanged.

Recommended regression areas:

- Search accuracy
- Builder output
- Validation results
- Audit reports
- Clinical recommendations

Regression failures should block production release.

---

# Streamlit Testing

Every user-facing feature should be tested through the Streamlit interface.

Checklist:

✓ Medicine Search

✓ Medicine Card

✓ Clinical Tabs

✓ Evidence Display

✓ Error Handling

✓ Performance

Streamlit testing validates end-to-end application behavior.

---

# AI Testing

AI testing verifies:

- Prompt stability
- Context correctness
- Evidence preservation
- Explainability
- Safety layer behavior
- Fallback behavior

AI testing complements—but never replaces—deterministic validation.

---

# Debugging Workflow

When defects are identified:

```text
Identify Issue

↓

Reproduce Issue

↓

Collect Logs

↓

Analyze Root Cause

↓

Implement Fix

↓

Re-run Validation

↓

Re-run Audit

↓

Regression Testing
```

Root cause analysis should precede code changes.

---

# Engineering Quality Checklist

Before completing development verify:

✓ Builder PASS

✓ Validation PASS

✓ Audit PASS

✓ Streamlit PASS

✓ AI PASS

✓ Documentation Updated

✓ CHANGELOG Updated

Only then should development proceed to release activities.

---

# Current Implementation

Current Pharma AI engineering workflow includes:

- Builder execution
- Validation
- Database audit
- Streamlit testing
- AI testing
- Documentation review

This workflow represents the current production engineering process.

---

# Future Enhancements

Planned engineering improvements include:

- Automated regression testing
- Continuous Integration (CI)
- Continuous Deployment (CD)
- Test coverage reporting
- Automated quality dashboards
- Engineering analytics

Future improvements should preserve deterministic engineering principles.

---

# Part Summary

This chapter defines:

- Validation Workflow
- Audit Workflow
- Clinical Module Development
- Testing Strategy
- Streamlit Testing
- AI Testing
- Debugging Workflow
- Engineering Quality Checklist
- Current Implementation
- Future Enhancements

These engineering practices ensure that every Pharma AI module is validated, tested, and production-ready before release.

# Git Engineering Workflow

Git is the official version control system for Pharma AI.

Every engineering change must be tracked through Git.

Git history should remain:

- Clean
- Meaningful
- Traceable
- Reproducible

---

# Branch Strategy

Recommended branch structure:

```text
main

↓

development

↓

feature/<feature-name>

↓

bugfix/<issue-name>

↓

hotfix/<release>
```

The `main` branch should always represent a production-ready state.

---

# Feature Development Workflow

Every new feature should follow:

```text
Create Feature Branch

↓

Implement Feature

↓

Builder Execution

↓

Validation

↓

Audit

↓

Testing

↓

Documentation

↓

Commit

↓

Pull Request

↓

Merge
```

Development should never occur directly on the production branch.

---

# Commit Standards

Each commit should represent one logical change.

Recommended commit prefixes:

```text
feat:

fix:

docs:

refactor:

test:

perf:

chore:
```

Examples:

```text
feat: add pregnancy builder

fix: correct renal validator

docs: update governance guide

test: add interaction regression tests
```

Commit messages should be concise and descriptive.

---

# Commit Best Practices

Contributors SHOULD:

- Keep commits focused
- Avoid unrelated changes
- Write meaningful commit messages
- Commit working code only

Large unrelated commits reduce review quality.

---

# Pull Request Workflow

Every Pull Request should include:

✓ Feature summary

✓ Validation results

✓ Audit results

✓ Testing completed

✓ Documentation updated

✓ CHANGELOG updated

Pull Requests should be easy to review.

---

# Merge Policy

Merge only after:

```text
Validation PASS

↓

Audit PASS

↓

Testing PASS

↓

Documentation Updated

↓

Review Approved

↓

Merge
```

No production code should bypass this workflow.

---

# Release Engineering

Official release workflow:

```text
Development

↓

Builder

↓

Validation

↓

Audit

↓

Testing

↓

Documentation

↓

Git Tag

↓

Release
```

Every release should be reproducible.

---

# Version Management

Pharma AI follows Semantic Versioning.

```text
MAJOR.MINOR.PATCH
```

Examples:

```
18.5.0

18.5.1

19.0.0
```

Version updates should be synchronized across:

- Application
- Database
- Documentation
- Release Notes

---

# Git Tag Policy

Every official release should receive a Git tag.

Examples:

```text
v18.5.0

v18.5.1

v19.0.0
```

Tags should identify approved production releases only.

---

# Daily Engineering Workflow

Recommended daily workflow:

```text
Pull Latest Code

↓

Create Feature Branch

↓

Develop

↓

Run Builder

↓

Run Validator

↓

Run Audit

↓

Streamlit Test

↓

AI Test

↓

Update Documentation

↓

Commit Changes

↓

Push Branch
```

Following a consistent routine reduces integration issues.

---

# Engineering Best Practices

Engineers SHOULD:

✓ Follow project standards

✓ Reuse shared components

✓ Keep modules independent

✓ Write deterministic code

✓ Update documentation

✓ Add tests

Engineers MUST NOT:

✗ Skip validation

✗ Modify production datasets manually

✗ Commit broken code

✗ Bypass governance

---

# Current Implementation

Current Pharma AI engineering includes:

- Git-based version control
- Feature-driven development
- Builder-first workflow
- Validation and audit
- Streamlit testing
- AI testing
- Git tagging for releases

This represents the current engineering process.

---

# Future Enhancements

Planned improvements include:

- Protected branches
- Automated CI/CD pipelines
- Commit linting
- Automatic semantic versioning
- Release automation
- Engineering dashboards

Future improvements should strengthen—not replace—the current engineering workflow.

---

# Part Summary

This chapter defines:

- Git Workflow
- Branch Strategy
- Commit Standards
- Pull Request Workflow
- Merge Policy
- Release Engineering
- Version Management
- Daily Engineering Workflow
- Current Implementation
- Future Enhancements

These practices ensure consistent engineering, reproducible releases, and maintainable project history.

# Enterprise Engineering Rules

The following engineering rules are mandatory for all Pharma AI development activities.

These rules preserve software quality, deterministic behavior, maintainability, and clinical safety.

---

## Rule 1 — Follow the Official Architecture

Every implementation MUST follow the approved architecture.

Core architectural layers include:

- Builder Framework
- Validation Framework
- Repository Layer
- Search Engine
- Clinical Engine
- Governance Framework
- AI Layer
- User Interface

Architectural deviations require formal review and approval.

---

## Rule 2 — Deterministic Processing First

Clinical processing MUST remain deterministic.

Artificial Intelligence may enhance presentation but must never replace deterministic clinical logic.

---

## Rule 3 — Validation Before Release

Every production change MUST complete:

✓ Builder Execution

✓ Validation

✓ Audit

✓ Testing

before release approval.

---

## Rule 4 — Documentation is Part of Engineering

Engineering work is incomplete until documentation is updated.

Documentation should evolve together with implementation.

---

## Rule 5 — Maintain Single Responsibility

Each module should perform one primary responsibility.

Examples:

- Builder → Data generation
- Validator → Data verification
- Repository → Data access
- Search → Medicine identification
- Clinical Engine → Clinical processing
- AI Layer → Natural language explanation

Responsibilities should remain clearly separated.

---

## Rule 6 — Preserve Production Integrity

Engineers MUST NOT:

- Edit production master datasets manually
- Bypass validation
- Skip audit
- Introduce undocumented architecture changes

Production integrity has higher priority than development speed.

---

# Daily Engineering Operations

Recommended daily engineering workflow:

```text
Review Current Task

↓

Pull Latest Code

↓

Create Feature Branch

↓

Implement Changes

↓

Run Builder

↓

Run Validator

↓

Run Audit

↓

Run Streamlit Tests

↓

Run AI Tests

↓

Update Documentation

↓

Commit Changes

↓

Push Branch
```

This workflow should be followed consistently.

---

# Daily Engineering Checklist

Before ending a development session verify:

✓ Code committed

✓ Builder executed (if applicable)

✓ Validation passed

✓ Audit passed

✓ Streamlit verified

✓ AI verified

✓ Documentation updated

✓ Working tree clean

A consistent end-of-day routine reduces integration risk.

---

# Engineering Responsibilities

Every engineer is responsible for:

- Writing maintainable code
- Preserving architecture
- Following project standards
- Updating documentation
- Reporting issues early
- Improving code quality

Quality is the responsibility of every contributor.

---

# Engineering Do's

Engineers SHOULD:

✓ Keep modules independent

✓ Write deterministic code

✓ Reuse shared utilities

✓ Prefer clarity over cleverness

✓ Add regression tests

✓ Keep documentation current

---

# Engineering Don'ts

Engineers MUST NOT:

✗ Duplicate business logic

✗ Introduce circular dependencies

✗ Hard-code production data

✗ Commit untested code

✗ Modify generated master files manually

✗ Bypass governance procedures

---

# Current Engineering Process

Current Pharma AI engineering process includes:

- Requirement-driven development
- Builder-first data generation
- Validation-first quality assurance
- Audit verification
- Streamlit integration testing
- AI response testing
- Documentation synchronization
- Governance-controlled release

This represents the official engineering workflow.

---

# Engineering Vision

The long-term engineering vision of Pharma AI is to build:

- Reliable software
- Explainable clinical systems
- Maintainable architecture
- Enterprise-quality tooling
- Scalable healthcare technology

Every engineering decision should support this vision.

---

# Related Documents

This guide should be used together with:

- PROJECT_STANDARDS.md
- ARCHITECTURE.md
- DATABASE.md
- BUILDER_FRAMEWORK.md
- VALIDATION_FRAMEWORK.md
- GOVERNANCE.md
- AI_DESIGN.md
- CONTRIBUTING.md

Together these documents define the complete Pharma AI engineering ecosystem.

---

# Engineering Guide Summary

The Engineering Guide defines how Pharma AI should be designed, developed, validated, tested, documented, and released.

Its objectives are to ensure:

- Deterministic engineering
- High software quality
- Clinical safety
- Long-term maintainability
- Consistent engineering practices
- Reproducible production releases

These principles apply to all current and future development.

---

# Approval

Document

ENGINEERING_GUIDE.md

Status

Approved

Version

1.0.0

Project

Pharma AI

Owner

Pharma AI Project

Location

docs/ENGINEERING_GUIDE.md

Approval Date

July 2026

This document serves as the official engineering operations manual for Pharma AI.