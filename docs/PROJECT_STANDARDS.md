# Contributing to Pharma AI
## Official Contributor Guide

---

**Project Name:** Pharma AI

**Document:** Contributor Guide

**Document ID:** PHARMA-CONTRIB-001

**Version:** 1.0.0

**Status:** Official

**Author:** Ravi Varsani

**Last Updated:** July 2026

---

# Welcome

Thank you for your interest in contributing to Pharma AI.

Pharma AI is an enterprise-grade Clinical Decision Support System (CDSS) focused on deterministic, evidence-based medicine information.

Every contribution should improve the platform while preserving:

- Clinical safety
- Code quality
- Data integrity
- Architectural consistency

---

# Purpose

This document explains:

- Development workflow
- Coding standards
- Documentation standards
- Builder workflow
- Validation workflow
- Git workflow
- Pull request process
- Review process

---

# Core Engineering Principles

Every contributor must understand these principles before making changes.

## Principle 1

Patient safety comes first.

---

## Principle 2

Evidence is the source of truth.

---

## Principle 3

Deterministic engines have higher priority than AI.

---

## Principle 4

Every production change must be validated.

---

## Principle 5

Architecture consistency is more important than short-term convenience.

---

# Project Architecture

Contributors should understand the project structure before modifying code.

```text
pharma_ai/

├── builders/
├── validator/
├── repositories/
├── services/
├── search/
├── clinical/
├── governance/
├── ui/
├── database/
└── docs/
```

Every module has a clearly defined responsibility.

---

# Before You Start

Before contributing:

✓ Read ARCHITECTURE.md

✓ Read DATABASE.md

✓ Read BUILDER_FRAMEWORK.md

✓ Read VALIDATION_FRAMEWORK.md

✓ Read GOVERNANCE.md

Contributors should understand the architecture before writing code.

---

# Contribution Types

Examples of accepted contributions:

- Bug fixes
- Performance improvements
- Documentation improvements
- New Builders
- New Validators
- Clinical dataset improvements
- Unit tests
- Integration tests

---

# Contributions That Require Design Review

The following changes require architectural review before implementation:

- Database schema changes
- Repository interface changes
- Search Engine changes
- Clinical Engine changes
- AI architecture changes
- Governance workflow changes

These components are considered core architecture.

---

# Development Workflow

Every contribution should follow the official workflow.

```text
Design

↓

Implementation

↓

Validation

↓

Testing

↓

Documentation

↓

Review

↓

Merge
```

Skipping workflow stages is not permitted.

---

# Branch Strategy

Recommended Git branches:

```
main

development

feature/<feature-name>

bugfix/<bug-name>

hotfix/<release>
```

Development should never occur directly on the production branch.

---

# Coding Standards

All code should:

- Be readable
- Be modular
- Follow project naming conventions
- Avoid unnecessary duplication
- Include meaningful comments where appropriate

Consistency is preferred over personal coding style.

---

# Documentation Requirement

Every architectural or functional change should include corresponding documentation updates.

Code and documentation should evolve together.

---

# Summary

Every contribution should improve the project without compromising:

- Quality
- Safety
- Maintainability
- Traceability

These principles apply to all contributors.

# Development Standards

Every contribution must follow the official Pharma AI engineering standards.

Consistency across the project has higher priority than individual coding preferences.

---

# Development Workflow

The official development workflow is:

```text
Planning

↓

Implementation

↓

Builder Execution

↓

Validation

↓

Audit

↓

Streamlit Testing

↓

AI Testing

↓

Documentation Update

↓

Git Commit

↓

Git Tag
```

Every production feature should follow this workflow.

---

# Builder Development Workflow

Every new Builder should follow the same engineering process.

```text
Design

↓

Implementation

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

Builders should never be merged without successful validation.

---

# Validator Development Workflow

Validators should be developed independently from Builders.

Workflow:

```text
Design Validation Rules

↓

Implementation

↓

Unit Testing

↓

Validation Execution

↓

Regression Testing

↓

Documentation
```

Validators must remain deterministic.

---

# Clinical Module Workflow

Clinical modules should follow the official sequence.

```text
Clinical Dataset

↓

Builder

↓

Validator

↓

Audit

↓

Repository

↓

Clinical Engine

↓

Testing
```

Clinical modules must never bypass validation.

---

# Streamlit Testing

Every user-facing feature should be verified using the Streamlit interface.

Suggested checklist:

✓ Medicine Search

✓ Medicine Card

✓ Clinical Findings

✓ Recommendations

✓ Evidence Display

✓ Error Handling

UI testing verifies runtime integration.

---

# AI Testing

AI testing should verify:

- Response consistency
- Structured explanations
- Evidence preservation
- Safety behavior
- Fallback behavior

AI testing should never replace deterministic validation.

---

# Git Commit Standards

Every commit should represent one logical change.

Recommended commit format:

```
feat: add renal builder

fix: correct interaction validator

docs: update architecture

refactor: improve repository layer

test: add validation tests
```

Commit messages should be concise and descriptive.

---

# Git Tag Policy

Official releases should be tagged.

Example:

```
v18.5.0

v18.5.1

v19.0.0
```

Tags should correspond to approved production releases.

---

# Code Review Standards

Every code review should verify:

- Architecture compliance
- Coding standards
- Validation impact
- Documentation updates
- Test coverage

Code review should focus on correctness before optimization.

---

# Coding Guidelines

Code should:

- Follow project naming conventions
- Use descriptive identifiers
- Avoid unnecessary complexity
- Minimize duplication
- Keep functions focused on one responsibility

Readable code is preferred over clever code.

---

# Naming Conventions

Examples:

Classes

```
GenericBuilder

InteractionValidator

ClinicalEngine
```

Methods

```
build()

validate()

search()

evaluate()
```

Variables

```
generic_id

health_score

validation_result
```

Naming should remain consistent across the project.

---

# Folder Ownership

Each module should remain responsible for its own functionality.

Examples:

```
builders/

↓

Builder Logic
```

```
validator/

↓

Validation Logic
```

```
clinical/

↓

Clinical Logic
```

Cross-module responsibility should be avoided.

---

# Dependency Rules

Allowed dependency flow:

```text
Builder

↓

Validator

↓

Audit

↓

Repository

↓

Runtime
```

Avoid reverse dependencies between runtime and development tools.

---

# Current Implementation

Current Pharma AI development workflow includes:

- Builder execution
- Validator execution
- Audit execution
- Streamlit testing
- AI testing
- Documentation updates
- Git commits
- Git tags

This workflow represents the current engineering standard.

---

# Future Enhancements

Future improvements may include:

- Automated code formatting
- Static analysis
- CI/CD pipelines
- Automated code review
- Automated release generation

These enhancements should preserve the existing development workflow.

---

# Part Summary

This chapter defines:

- Development Workflow
- Builder Workflow
- Validator Workflow
- Clinical Module Workflow
- Streamlit Testing
- AI Testing
- Git Standards
- Coding Guidelines
- Naming Conventions
- Current Implementation
- Future Enhancements

These standards ensure consistent and maintainable development across the Pharma AI project.
# Testing Standards

Testing is a mandatory part of every contribution.

No production change should be merged without appropriate testing.

Testing protects:

- Clinical safety
- Data integrity
- Architecture stability
- Regression prevention

---

# Testing Pyramid

```text
          End-to-End Tests

                 ▲

         Integration Tests

                 ▲

            Unit Tests
```

Every contribution should include testing at the appropriate level.

---

# Unit Testing

Unit tests verify individual components.

Examples:

- Builder methods
- Validator rules
- Repository methods
- Search algorithms
- Clinical engines

Each unit test should validate one behavior.

---

# Integration Testing

Integration testing verifies communication between modules.

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

```text
Search Engine

↓

Clinical Engine
```

Integration testing ensures correct module interaction.

---

# Regression Testing

Regression testing ensures existing functionality remains unchanged.

Regression testing should verify:

- Search accuracy
- Builder output
- Validator behavior
- Clinical recommendations
- Repository results

Regression failures block production release.

---

# Streamlit Testing

Every UI-related feature should be verified manually.

Checklist:

✓ Search

✓ Medicine Card

✓ Clinical Tabs

✓ Evidence Display

✓ Error Handling

✓ Performance

Streamlit testing verifies end-to-end user experience.

---

# AI Testing

AI testing should verify:

- Prompt consistency
- Context correctness
- Structured explanations
- Evidence preservation
- Safety layer behavior
- Fallback behavior

AI responses should remain explainable.

---

# Documentation Standards

Documentation is part of the source code.

Every architectural or functional change should update:

- Architecture documentation
- Builder documentation
- Validation documentation
- Clinical documentation
- CHANGELOG

Documentation should accurately reflect implementation.

---

# Documentation Quality

Documentation should be:

- Accurate
- Complete
- Versioned
- Easy to understand
- Technically correct

Outdated documentation should be corrected before release.

---

# Code Review Process

Every production contribution should undergo review.

Review should verify:

✓ Architecture compliance

✓ Coding standards

✓ Validation impact

✓ Documentation updates

✓ Test coverage

✓ Performance impact

---

# Review Checklist

Before approving a contribution verify:

- Code readability
- Correct module ownership
- No duplicated logic
- Error handling present
- Logging appropriate
- Tests passed
- Documentation updated

The checklist should be completed for every production contribution.

---

# Review Responsibilities

Reviewers should focus on:

- Correctness
- Maintainability
- Safety
- Consistency

Review is an engineering quality activity,

not a personal evaluation.

---

# Continuous Improvement

Contributors are encouraged to improve:

- Documentation
- Testing
- Code quality
- Performance
- Maintainability

Incremental improvements are preferred over large unreviewed changes.

---

# Current Implementation

Current Pharma AI quality workflow includes:

- Builder testing
- Validator testing
- Audit verification
- Streamlit testing
- AI testing
- Documentation review

These activities form the current engineering quality process.

---

# Future Enhancements

Potential improvements include:

- Automated regression testing
- Test coverage reporting
- Continuous Integration (CI)
- Continuous Deployment (CD)
- Automated documentation validation
- AI-assisted code review

Future improvements should strengthen—not replace—engineering review.

---

# Part Summary

This chapter defines:

- Testing Standards
- Unit Testing
- Integration Testing
- Regression Testing
- Streamlit Testing
- AI Testing
- Documentation Standards
- Code Review Process
- Current Implementation
- Future Enhancements

These practices ensure that every Pharma AI contribution meets enterprise engineering quality standards.

# Pull Request Workflow

Every production change should be submitted through a Pull Request (PR).

The Pull Request provides:

- Technical review
- Architecture review
- Quality verification
- Documentation verification

Direct commits to the production branch are discouraged.

---

# Pull Request Lifecycle

```text
Feature Branch

↓

Implementation

↓

Builder Execution

↓

Validation

↓

Audit

↓

Testing

↓

Documentation Update

↓

Pull Request

↓

Review

↓

Merge
```

Every stage should be completed before merge approval.

---

# Pull Request Requirements

Every Pull Request should include:

- Clear title
- Description of the change
- Reason for the change
- Testing performed
- Documentation updated
- Related issue (if applicable)

The description should help reviewers understand the contribution.

---

# Pull Request Checklist

Before creating a Pull Request verify:

✓ Code completed

✓ Validation PASS

✓ Audit PASS

✓ Streamlit testing completed

✓ AI testing completed

✓ Documentation updated

✓ CHANGELOG updated

✓ No merge conflicts

Every Pull Request should satisfy this checklist.

---

# Review Process

Every Pull Request should undergo technical review.

Review should verify:

- Architecture compliance
- Coding standards
- Module boundaries
- Test coverage
- Documentation updates
- Performance impact

Review should focus on engineering quality.

---

# Merge Policy

A Pull Request may be merged only after:

✓ Review completed

✓ Required tests passed

✓ Documentation approved

✓ Governance requirements satisfied

Merge should represent a production-quality change.

---

# Release Contribution Workflow

Contributions intended for production releases should follow:

```text
Feature Development

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

Pull Request

↓

Review

↓

Merge

↓

Release
```

This workflow aligns with the official Pharma AI release process.

---

# Commit Hygiene

Contributors should:

- Keep commits small
- Use meaningful commit messages
- Avoid unrelated changes
- Squash trivial fix commits before merge (when appropriate)

Clean history simplifies maintenance.

---

# Best Practices

Contributors SHOULD:

✓ Write readable code

✓ Reuse shared utilities

✓ Follow architecture

✓ Preserve deterministic behavior

✓ Add tests for new functionality

✓ Update documentation

Contributors MUST NOT:

✗ Bypass validation

✗ Modify production datasets manually

✗ Introduce undocumented architecture changes

✗ Skip required testing

---

# Common Mistakes

Avoid the following:

- Mixing unrelated features in one Pull Request
- Large unreviewed changes
- Missing documentation updates
- Missing validation results
- Ignoring regression failures
- Direct production branch commits

These practices increase project risk.

---

# Current Implementation

Current Pharma AI development includes:

- Feature-based development
- Builder execution
- Validation
- Audit
- Streamlit testing
- AI testing
- Documentation updates
- Git commit
- Git tag

These activities form the recommended contribution workflow.

---

# Future Enhancements

Future improvements may include:

- Protected branches
- Mandatory Pull Request templates
- Automated code quality checks
- CI/CD validation
- Automatic release notes generation
- Reviewer assignment automation

These enhancements should strengthen the review process.

---

# Part Summary

This chapter defines:

- Pull Request Workflow
- Pull Request Requirements
- Review Process
- Merge Policy
- Release Contribution Workflow
- Commit Hygiene
- Best Practices
- Common Mistakes
- Current Implementation
- Future Enhancements

These practices ensure that every contribution maintains the engineering quality expected by the Pharma AI project.

# Enterprise Contribution Rules

The following rules are mandatory for every contributor to the Pharma AI project.

These rules ensure long-term maintainability, engineering quality, and clinical safety.

---

## Rule 1 — Patient Safety First

Every contribution must preserve patient safety.

Engineering convenience must never override clinical correctness.

---

## Rule 2 — Follow the Architecture

All contributors MUST follow the approved architecture.

Core architectural components include:

- Search Engine
- Clinical Engine
- Builder Framework
- Validation Framework
- Governance Framework
- AI Layer

Architectural changes require formal design review.

---

## Rule 3 — Validation is Mandatory

Every production change MUST successfully complete:

- Validation
- Audit
- Required Testing

No production contribution may bypass these quality gates.

---

## Rule 4 — Documentation is Required

Code changes affecting functionality or architecture MUST include corresponding documentation updates.

Documentation and implementation should remain synchronized.

---

## Rule 5 — Small, Focused Contributions

Each contribution should solve one logical problem.

Avoid combining unrelated features in a single contribution.

---

## Rule 6 — Preserve Deterministic Behavior

Contributors MUST NOT introduce non-deterministic behavior into:

- Search Engine
- Clinical Engine
- Validation Framework
- Builder Framework

Deterministic processing remains the foundation of Pharma AI.

---

# Code of Conduct

Every contributor should:

- Respect reviewers
- Accept constructive feedback
- Discuss technical decisions objectively
- Prioritize project quality over personal preference

Professional communication is expected throughout the project.

---

# Engineering Values

The Pharma AI project values:

- Correctness
- Simplicity
- Maintainability
- Transparency
- Traceability
- Clinical Safety
- Continuous Improvement

These values guide all engineering decisions.

---

# Contribution Lifecycle

The official contribution lifecycle is:

```text
Idea

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

Pull Request

↓

Review

↓

Merge

↓

Release
```

Every official contribution follows this lifecycle.

---

# Contributor Checklist

Before submitting a contribution verify:

✓ Architecture followed

✓ Code reviewed

✓ Validation passed

✓ Audit passed

✓ Tests completed

✓ Documentation updated

✓ CHANGELOG updated

✓ Git history clean

---

# Current Implementation

Current Pharma AI engineering process includes:

- Builder-driven development
- Validation-first workflow
- Audit verification
- Streamlit testing
- AI testing
- Documentation updates
- Git commits
- Git tags

This represents the official development workflow for the project.

---

# Architecture Standard

The Contributor Guide is based on the following principles:

- Builder-generated production data
- Validation-first quality assurance
- Governance-controlled releases
- Deterministic clinical processing
- Evidence-based AI assistance

All future contributions should preserve these principles.

---

# Future Contributor Roadmap

Future improvements may include:

- Contributor onboarding guide
- Development environment automation
- Coding style automation
- Contributor dashboards
- Automated architecture validation
- CI/CD contribution pipelines

These improvements should simplify contribution without reducing engineering quality.

---

# Related Documents

Contributors should become familiar with:

- ARCHITECTURE.md
- DATABASE.md
- SEARCH_ENGINE.md
- CLINICAL_ENGINE.md
- BUILDER_FRAMEWORK.md
- VALIDATION_FRAMEWORK.md
- GOVERNANCE.md
- AI_DESIGN.md

These documents collectively define the Pharma AI engineering standards.

---

# Contributor Guide Summary

The Pharma AI Contributor Guide establishes the official engineering workflow for the project.

Every contribution should be:

- Safe
- Validated
- Audited
- Tested
- Documented
- Reviewed
- Traceable

These principles ensure the long-term success and maintainability of Pharma AI.

---

# Approval

Document Status

Approved

Version

1.0.0

Owner

Pharma AI Project

Location

docs/CONTRIBUTING.md

This document serves as the official contributor guide for all current and future Pharma AI development.