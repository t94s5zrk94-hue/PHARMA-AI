# 💊 Pharma AI

> **Enterprise Clinical Decision Support System (CDSS) for Pharmacists and Healthcare Professionals**

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red)
![License](https://img.shields.io/badge/License-MIT-brightgreen)
![Status](https://img.shields.io/badge/Status-Release_Candidate-orange)
![Architecture](https://img.shields.io/badge/Architecture-Enterprise-success)

---

# Overview

**Pharma AI** is an enterprise-grade **Clinical Decision Support System (CDSS)** designed to provide reliable, deterministic, and evidence-based medicine information for pharmacists, healthcare professionals, and clinical decision support applications.

Unlike traditional AI chatbots, Pharma AI follows a **deterministic, builder-driven architecture**, where validated production datasets, clinical knowledge, and governance processes form the foundation of every clinical recommendation.

Artificial Intelligence is used only to enhance explanations and usability—it never replaces validated clinical logic.

---

# Key Objectives

Pharma AI is designed to:

- Provide accurate medicine information
- Support evidence-based clinical decisions
- Improve medicine search and identification
- Assist pharmacists during dispensing and counselling
- Deliver deterministic clinical recommendations
- Maintain explainable AI-assisted responses
- Ensure production-grade data quality through Builders, Validation, and Governance

---

# Core Principles

The project is built on the following engineering principles:

- 🛡 Patient Safety First
- 📚 Evidence Before AI
- ⚙ Deterministic Clinical Processing
- 🧱 Builder-Driven Production Data
- ✅ Validation-First Quality Assurance
- 📊 Governance-Controlled Releases
- 🤖 Explainable AI Assistance
- 📖 Comprehensive Engineering Documentation

---

# Current Project Status

| Item | Status |
|------|--------|
| Project Stage | Release Candidate |
| Architecture | Enterprise |
| Development Model | Builder-Driven |
| Clinical Engine | Active Development |
| Documentation | Complete |
| AI Layer | Architecture Ready |
| Quality Framework | Production Ready |

---

# Project Vision

The long-term vision of Pharma AI is to become a modular, explainable, and enterprise-ready Clinical Decision Support Platform capable of supporting:

- Community Pharmacy
- Hospital Pharmacy
- Clinical Pharmacy
- Academic Training
- Healthcare Research
- Future Hospital Information System (HIS) Integration

---

# Why Pharma AI?

Pharma AI is different from general-purpose AI tools because it is built around structured clinical knowledge rather than free-form text generation.

The platform emphasizes:

- Deterministic processing
- Evidence-based recommendations
- Structured clinical datasets
- Explainable outputs
- Enterprise software engineering practices

This approach improves reliability, maintainability, and future scalability.

---

# High-Level Architecture

```text
                User
                  │
                  ▼
          Search Engine
                  │
                  ▼
         Clinical Engine
                  │
                  ▼
         Evidence Engine
                  │
                  ▼
            AI Layer
                  │
                  ▼
          Presentation Layer
```

The AI Layer enhances presentation but does not replace deterministic clinical processing.

---
# ✨ Enterprise Features

Pharma AI is designed as a modular Clinical Decision Support System (CDSS).

Each module has a clearly defined responsibility and follows deterministic engineering principles.

---

# 🔍 Smart Search Engine

Fast and intelligent medicine search with structured normalization.

Features include:

- Brand Search
- Generic Search
- Alias Resolution
- Combination Medicine Search
- Typo Tolerance
- Smart Ranking
- Structured Search Results

---

# 💊 Clinical Decision Support

The Clinical Engine provides evidence-based clinical information.

Supported modules include:

- Drug Interactions
- Contraindications
- Warnings & Precautions
- Side Effects
- Pregnancy Safety
- Lactation Safety
- Renal Dose Adjustment
- Hepatic Dose Adjustment
- Monitoring Parameters
- Clinical Evidence & References

All recommendations are generated from validated clinical datasets.

---

# 🏗 Builder Framework

All production datasets are generated through the Builder Framework.

Current Builders include:

- Generic Builder
- Company Builder
- Brand Builder
- Product Builder
- ATC Builder
- Generic ATC Mapping Builder
- Generic Class Mapping Builder
- Clinical Data Builders

Builders generate standardized production datasets with metadata.

---

# ✅ Validation Framework

Every production dataset passes through the Validation Framework.

Validation includes:

- Required Column Validation
- Missing Value Validation
- Duplicate Detection
- Foreign Key Validation
- Business Rule Validation
- Metadata Validation

Only validated datasets proceed to production.

---

# 📊 Governance Framework

The Governance Framework controls production readiness.

Quality gates include:

- Builder Execution
- Validation
- Audit
- Streamlit Testing
- AI Testing
- Documentation Review
- Release Approval

No production release bypasses governance.

---

# 🤖 AI-Assisted Clinical Support

Artificial Intelligence is used to improve explanation—not decision making.

Planned AI capabilities include:

- Clinical Summaries
- Natural Language Explanations
- Explainable AI (XAI)
- Context Engine
- Prompt Engine
- Safety Layer
- Response Validation

Clinical recommendations always originate from deterministic clinical engines.

---

# ⚙ Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python 3.14 |
| UI | Streamlit |
| Data Processing | Pandas |
| Version Control | Git |
| Documentation | Markdown |
| Architecture | Modular Package Architecture |
| AI Integration | Provider Independent |
| Development Model | Builder Driven |

---

# 🧱 Enterprise Architecture

The application follows a layered architecture.

```text
User Interface

↓

Search Engine

↓

Clinical Engine

↓

Repository Layer

↓

Production Database
```

Development infrastructure:

```text
Input Data

↓

Builder Framework

↓

Validation Framework

↓

Audit Framework

↓

Production Database
```

This separation ensures that runtime operations remain independent from data generation.

---

# 🎯 Key Advantages

Pharma AI provides:

- Deterministic clinical processing
- Evidence-based recommendations
- Builder-generated production data
- Validation-first quality assurance
- Explainable AI architecture
- Enterprise governance
- Modular software architecture
- Comprehensive engineering documentation

These principles support long-term maintainability and production readiness.

---

# 📂 Project Structure

The project follows a modular enterprise architecture.

```text
PHARMA AI/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .env.example
│
├── pharma_ai/
│   ├── builders/
│   ├── validator/
│   ├── repositories/
│   ├── services/
│   ├── search/
│   ├── clinical/
│   ├── governance/
│   ├── ui/
│   ├── database/
│   └── core/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATABASE.md
│   ├── SEARCH_ENGINE.md
│   ├── CLINICAL_ENGINE.md
│   ├── BUILDER_FRAMEWORK.md
│   ├── VALIDATION_FRAMEWORK.md
│   ├── GOVERNANCE.md
│   ├── AI_DESIGN.md
│   ├── PROJECT_STANDARDS.md
│   ├── ENGINEERING_GUIDE.md
│   ├── CONTRIBUTING.md
│   └── CHANGELOG.md
│
├── tests/
│
└── logs/
```

---

# ⚙️ System Requirements

Minimum Requirements

- Python 3.14+
- Git
- Streamlit
- Virtual Environment (venv)

Recommended

- Visual Studio Code
- GitHub Desktop (Optional)

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/pharma-ai.git
```

---

## Change Directory

```bash
cd pharma-ai
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Linux / macOS

```bash
python3 -m venv .venv
```

---

## Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

Additional configuration options may be added in future releases.

---

# ▶ Running Pharma AI

Start the Streamlit application.

```bash
streamlit run app.py
```

The application will launch in your default web browser.

---

# 🧪 Running Builders

Example:

```bash
python -m pharma_ai.builders.generic_builder
```

---

# ✅ Running Validators

Example:

```bash
python -m pharma_ai.validator.generic_validator
```

---

# 📊 Running Database Audit

Example:

```bash
python -m pharma_ai.validator.database_audit
```

---

# 📋 Recommended Development Workflow

For every new feature follow:

```text
Develop

↓

Builder

↓

Validation

↓

Audit

↓

Streamlit Test

↓

AI Test

↓

Documentation

↓

Git Commit
```

This workflow ensures production-quality development.

---

# 📈 Expected Output

Successful development should produce:

- Production datasets
- Validation reports
- Audit reports
- Updated documentation
- Git commit
- Git tag (for releases)

---

# 🔧 Troubleshooting

Common issues:

### Virtual Environment Not Activated

Ensure the correct virtual environment is activated before running any command.

---

### Missing Dependencies

Run:

```bash
pip install -r requirements.txt
```

---

### Streamlit Not Found

Install Streamlit:

```bash
pip install streamlit
```

---

### Builder Errors

Verify:

- Input datasets
- CSV headers
- Required metadata
- Validation rules

---

### Validation Failures

Review the validation report and correct the dataset before proceeding.

---

# 💡 Development Recommendation

Always follow the official engineering workflow.

Never modify production master datasets manually.

Always generate production datasets using the Builder Framework.

---
# 📚 Documentation

Pharma AI includes a comprehensive enterprise documentation suite.

| Document | Description |
|----------|-------------|
| ARCHITECTURE.md | Overall system architecture |
| DATABASE.md | Database design and schema |
| SEARCH_ENGINE.md | Search engine architecture |
| CLINICAL_ENGINE.md | Clinical decision support architecture |
| BUILDER_FRAMEWORK.md | Production Builder Framework |
| VALIDATION_FRAMEWORK.md | Validation architecture |
| GOVERNANCE.md | Release governance and quality gates |
| AI_DESIGN.md | AI architecture and explainable AI |
| PROJECT_STANDARDS.md | Official engineering standards |
| ENGINEERING_GUIDE.md | Engineering operations manual |
| CONTRIBUTING.md | Contributor guide |
| CHANGELOG.md | Official release history |

Complete documentation is available in the **`docs/`** directory.

---

# 🔄 Development Workflow

Pharma AI follows a deterministic engineering workflow.

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

Streamlit Testing

↓

AI Testing

↓

Documentation

↓

Git Commit

↓

Git Tag

↓

Release
```

Every production feature follows this workflow.

---

# 🏗 Engineering Workflow

Production datasets are created using the following pipeline.

```text
Input Data

↓

Builder Framework

↓

Validation Framework

↓

Audit Framework

↓

Production Database

↓

Repository

↓

Clinical Engine

↓

AI Layer

↓

Presentation
```

This separation ensures reliable and reproducible production data.

---

# 🧪 Quality Assurance

Every production release includes:

- Builder Verification
- Dataset Validation
- Database Audit
- Streamlit Testing
- AI Testing
- Documentation Review
- Governance Approval

Quality assurance is mandatory before every production release.

---

# 🗺 Project Roadmap

## Current Release

**Phase 18.5 — Release Candidate**

Completed:

- Enterprise Architecture
- Builder Framework
- Validation Framework
- Governance Framework
- Clinical Knowledge Engine
- Enterprise Documentation

---

## Upcoming Phases

### Phase 19

- AI Context Engine
- Prompt Engine
- Explainable AI
- AI Safety Layer

---

### Phase 20

- Knowledge Graph
- Clinical Relationships
- Therapeutic Intelligence

---

### Phase 21

- REST API
- Authentication
- External Integration

---

### Phase 22+

- Enterprise Search
- Hospital Integration
- Mobile Applications
- Analytics Dashboard
- Enterprise Deployment

---

# 🤝 Contributing

Contributions are welcome.

Please read the following documents before contributing:

- CONTRIBUTING.md
- ENGINEERING_GUIDE.md
- PROJECT_STANDARDS.md

Every contribution should follow the official engineering workflow.

---

# 🧭 Project Principles

Pharma AI is developed according to the following principles:

- Patient Safety First
- Deterministic Clinical Processing
- Evidence-Based Recommendations
- Validation-First Engineering
- Builder-Driven Production Data
- Explainable AI
- Enterprise Governance

These principles guide all engineering decisions.

---

# 📊 Current Project Status

| Area | Status |
|------|--------|
| Architecture | ✅ Complete |
| Production Database | ✅ Active |
| Search Engine | ✅ Stable |
| Clinical Engine | ✅ Active Development |
| Builder Framework | ✅ Stable |
| Validation Framework | ✅ Stable |
| Governance | ✅ Complete |
| AI Architecture | ✅ Ready |
| Documentation | ✅ Complete |

---

# 🌟 Why This Project?

Pharma AI combines modern software engineering practices with evidence-based clinical knowledge to build a reliable Clinical Decision Support System.

The platform is designed for:

- Community Pharmacists
- Hospital Pharmacists
- Clinical Pharmacists
- Healthcare Organizations
- Academic Institutions
- Future Healthcare Integrations

---

# 💬 Community

Questions, suggestions, and improvements are always welcome.

Please use GitHub Issues or Pull Requests to report bugs, request features, or contribute improvements.

---

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for complete license information.

---

# ⚠️ Medical Disclaimer

Pharma AI is intended to function as a **Clinical Decision Support System (CDSS)**.

The platform is designed to assist pharmacists and healthcare professionals by providing structured, evidence-based clinical information.

Pharma AI **does not replace**:

- Physician judgment
- Pharmacist professional judgment
- Institutional clinical guidelines
- Official prescribing information

Clinical decisions should always be made by qualified healthcare professionals using appropriate clinical judgment and verified references.

---

# 🔒 Data & Privacy

Pharma AI is designed with an **offline-first architecture**.

Core clinical processing is performed using locally validated production datasets.

Future cloud-based AI integrations will follow applicable security and privacy requirements.

---

# 📖 Citation

If you use Pharma AI in academic work, research, or educational material, please cite the project appropriately.

Example:

```text
Ravi Varsani

Pharma AI

Enterprise Clinical Decision Support System (CDSS)

GitHub Repository
```

---

# 🙏 Acknowledgements

The development of Pharma AI has been inspired by:

- Evidence-Based Medicine
- Clinical Pharmacy Practice
- Enterprise Software Engineering
- Open Source Software Community
- Modern Artificial Intelligence Research

Special appreciation goes to healthcare professionals and developers who contribute to safer medication practices.

---

# 🚀 Future Vision

The long-term vision of Pharma AI includes:

- Enterprise Clinical Decision Support
- Explainable Artificial Intelligence (XAI)
- Knowledge Graph Integration
- REST API Platform
- Hospital Information System (HIS) Integration
- FHIR & HL7 Compatibility
- Mobile Applications
- Enterprise Deployment
- Clinical Analytics
- Global Healthcare Collaboration

---

# 📬 Support

If you encounter issues or have improvement suggestions:

- Open a GitHub Issue
- Submit a Pull Request
- Review the documentation in the `docs/` directory

Constructive feedback and contributions are welcome.

---

# 👨‍💻 Project Maintainer

**Ravi Varsani**

Clinical Pharmacist

Python Developer

Healthcare Technology Enthusiast

---

# 🏆 Project Highlights

Pharma AI combines:

- Enterprise Software Architecture
- Deterministic Clinical Decision Support
- Builder-Driven Production Data
- Validation-First Quality Assurance
- Governance-Controlled Releases
- Explainable AI Architecture
- Comprehensive Technical Documentation

The project is engineered for long-term maintainability, reliability, and scalability.

---

# 📌 Repository Summary

| Category | Status |
|----------|--------|
| Architecture | ✅ Enterprise |
| Documentation | ✅ Complete |
| Builder Framework | ✅ Complete |
| Validation Framework | ✅ Complete |
| Governance | ✅ Complete |
| Clinical Engine | ✅ Active |
| AI Architecture | ✅ Ready |
| Release Status | 🚧 Release Candidate |

---

# ⭐ Support the Project

If Pharma AI is useful to you:

- ⭐ Star the repository
- 🍴 Fork the project
- 📝 Share feedback
- 🤝 Contribute improvements

Community participation helps improve the project.

---

# 📚 Documentation Index

Refer to the `docs/` directory for detailed technical documentation covering:

- System Architecture
- Database Design
- Search Engine
- Clinical Engine
- Builder Framework
- Validation Framework
- Governance
- AI Design
- Engineering Guide
- Project Standards
- Contribution Guide
- Release History

---

# End of README

Thank you for your interest in **Pharma AI**.

Together, we can build a reliable, evidence-based, and explainable Clinical Decision Support System for the healthcare community.