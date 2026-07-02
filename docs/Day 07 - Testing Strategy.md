Day 7 – System Architecture & Project Structure

Project: Pharma AI – Digital Clinical Pharmacist Platform
Document Version: 1.0
Status: Approved

1. Purpose

આ Document Pharma AI નું સંપૂર્ણ Software Architecture Define કરે છે.

આ Architecture ના મુખ્ય હેતુ:

Modular Development
Scalability
Maintainability
High Performance
Clinical Data Integrity
2. Architecture Philosophy

Pharma AI નું Architecture નીચેના સિદ્ધાંતો પર આધારિત રહેશે:

Modular Design
Database First
AI-Assisted
Separation of Concerns
Reusable Components
Secure Configuration
Easy Testing
3. High-Level Architecture
                    USER
                      │
                      ▼
              Streamlit User Interface
                      │
──────────────────────────────────────────────
                      │
                      ▼
              Search Controller
                      │
──────────────────────────────────────────────
          │                    │
          ▼                    ▼
   Database Engine        AI Engine
          │                    │
          ▼                    ▼
     Clinical Database    AI Explanation
          │                    │
          └──────────┬─────────┘
                     ▼
              Final Response
4. Project Folder Structure
PHARMA AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── modules/
│   ├── database.py
│   ├── smart_search.py
│   ├── medicine_card.py
│   ├── ai_engine.py
│   ├── styles.py
│   ├── validator.py
│   ├── interaction.py
│   ├── counselling.py
│   ├── jan_aushadhi.py
│   ├── barcode.py
│   ├── ocr.py
│   └── utilities.py
│
├── database/
│   ├── generic.csv
│   ├── brands.csv
│   ├── company.csv
│   ├── product.csv
│   ├── interaction.csv
│   ├── counselling.csv
│   ├── pregnancy.csv
│   ├── lactation.csv
│   ├── storage.csv
│   ├── references.csv
│   └── inventory.csv
│
├── assets/
│   ├── logo.png
│   ├── icons/
│   └── css/
│
├── docs/
│   ├── Day 01.md
│   ├── Day 02.md
│   ├── Day 03.md
│   ├── Day 04.md
│   ├── Day 05.md
│   ├── Day 06.md
│   ├── Day 07.md
│   ├── ROADMAP.md
│   ├── CHANGELOG.md
│   └── SRS_v1.0.md
│
├── tests/
│   ├── test_search.py
│   ├── test_database.py
│   ├── test_ai.py
│   └── test_interactions.py
│
└── backups/
5. Module Responsibilities
app.py

Main Application

Responsibilities:

Streamlit UI
Session Management
Navigation
Module Integration
database.py

Responsibilities

Load CSV Files
Search Database
Database Relationships
smart_search.py

Responsibilities

Exact Search
Partial Search
Fuzzy Search
Gujarati Search
Hindi Search
ai_engine.py

Responsibilities

Prompt Generation
AI Communication
Language Detection
Response Formatting
medicine_card.py

Responsibilities

Medicine Card UI
Product Information
Responsive Display
interaction.py

Responsibilities

Drug Interaction Engine
Severity Detection
Clinical Notes
counselling.py

Responsibilities

Gujarati Counselling
Hindi Counselling
English Counselling
jan_aushadhi.py

Responsibilities

Generic Mapping
PMBI Information
Alternative Suggestions
ocr.py

Responsibilities

Prescription Reading
Medicine Extraction
barcode.py

Responsibilities

Barcode Lookup
Product Identification
6. Data Flow
User Input
     │
     ▼
Smart Search
     │
     ▼
Database Search
     │
     ▼
Clinical Information
     │
     ▼
AI Explanation
     │
     ▼
Final Response
7. AI Architecture
User
   │
Language Detection
   │
Intent Detection
   │
Database Context
   │
Prompt Builder
   │
Gemini API
   │
Response Formatter
   │
User
8. Database Layer

Database Layer માત્ર Data Store તરીકે કાર્ય કરશે.

તે કોઈ Clinical Decision નહીં લે.

Responsibilities

Data Retrieval
Validation
Relationships
9. Business Logic Layer

આ Layer

Clinical Logic સંભાળશે.

Examples

Brand Comparison
Drug Interaction
Jan Aushadhi Mapping
Contraindications
10. Presentation Layer

UI

Medicine Card

Tables

Alerts

Patient Counselling

11. Security Architecture

Environment Variables

.env

માં રહેશે

Gemini API Key
Future API Keys

ક્યારેય GitHub પર Commit નહીં કરવાના.

12. Logging Strategy

ભવિષ્યમાં

Logs

Search Logs
Error Logs
AI Logs
13. Testing Strategy

દરેક Module માટે Unit Tests

Database
Search
AI
Interaction
Counselling
14. Deployment Plan
Development
VS Code
Git
Streamlit
Production
Cloud Server
PostgreSQL (Future)
Secure API Keys
HTTPS
15. Scalability Plan

Current

CSV Database

↓

SQLite

↓

PostgreSQL

↓

Cloud Database

આ બદલાવથી Modules બદલવાના નહીં પડે.

16. Coding Standards
Python PEP 8
Type Hints (જ્યાં શક્ય હોય)
Functions ≤ 100 lines (ભલામણ)
Reusable Modules
Meaningful Variable Names
Docstrings for Public Functions
17. Git Workflow

દરેક Feature પછી

git add .

git commit -m "Feature: Brand Comparison"

git push
18. Error Handling

જો

Database Missing
API Error
Internet Failure

તો

Graceful Error બતાવવો.

Application Crash ન થવી જોઈએ.

19. Future Architecture

Future Modules

Mobile App
REST API
Admin Dashboard
Analytics
Voice Assistant
OCR Service

હાલના Architecture માં મોટા ફેરફાર વગર ઉમેરવા યોગ્ય હોવા જોઈએ.

20. Technical Vision

Pharma AI નું Architecture એવું હોવું જોઈએ કે:

નવા Modules સરળતાથી ઉમેરાય
Database વધે તો Performance જળવાય
AI Provider બદલવો સરળ રહે
Web, Mobile અને API ત્રણેય માટે આધાર તૈયાર રહે
21. Architecture Principles
Database First
Modular Design
Clean Code
Reusable Components
AI as Assistant
Security by Design
Scalability
Testability
Documentation First
Clinical Safety
22. Day 7 Outcome

આજે Pharma AI માટે સંપૂર્ણ Technical Architecture તૈયાર થયું.

આ Architecture આગામી તમામ Development માટે Blueprint તરીકે ઉપયોગમાં લેવામાં આવશે.

📅 Day 8 Preview
Development Standards & Coding Guidelines

આ Document માં હશે:

Python Coding Standards
Naming Convention
File Naming Rules
Database Naming Rules
Git Branch Strategy
Commit Message Standards
Versioning Policy
Code Review Checklist
Documentation Standards
Release Process