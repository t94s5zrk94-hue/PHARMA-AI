Day 2 – Functional Requirements (SRS)

Document Version: 1.0

1. Introduction

આ Document Pharma AI ના તમામ Functional Requirements Define કરે છે.

દરેક Feature ને એક Unique Requirement Number આપવામાં આવશે.

Format:

FR-001

FR-002

FR-003
FR-001 Medicine Search
Description

User કોઈપણ Medicine નું

Generic Name
Brand Name
Product Name

Search કરી શકે.

Input
Paracetamol

Dolo

Crocin

PCM
Output

Medicine Profile

Priority

⭐⭐⭐⭐⭐

Critical

FR-002 Smart Search

System નીચેના Search Support કરશે.

Exact Search
Dolo
Partial Search
Dol
Fuzzy Search
Paracetamol

↓

Correct

Paracetamol
Gujarati Search
પેરાસિટામોલ
Hindi Search (Future)
पैरासिटामोल

Priority

⭐⭐⭐⭐⭐

FR-003 Medicine Information

દરેક Medicine માટે નીચેની માહિતી ઉપલબ્ધ રહેશે.

Basic

Generic
Brand
Company
Strength
Dosage Form
Pack Size
Schedule

Clinical

Uses
Dosage (General Educational Information)
Mechanism
Side Effects
Contraindications

Priority

⭐⭐⭐⭐⭐

FR-004 Multiple Brand Selection

જો એક Generic માટે અનેક Brands હોય

User Dropdown માંથી પસંદ કરી શકે.

Example

Paracetamol

↓

Dolo

Crocin

Calpol

Priority

⭐⭐⭐⭐⭐

FR-005 Brand Comparison

User

Dolo

VS

Crocin

Compare કરી શકે.

Comparison

Company
Strength
Pack Size
Schedule
Jan Aushadhi

Priority

⭐⭐⭐⭐⭐

FR-006 Generic Finder

Brand

↓

Generic

Example

Crocin

↓

Paracetamol

Priority

⭐⭐⭐⭐⭐

FR-007 Jan Aushadhi Alternative

Brand

↓

Equivalent Generic

↓

Jan Aushadhi Medicine

Priority

⭐⭐⭐⭐⭐

FR-008 Drug Interaction

Medicine A

Medicine B

↓

Interaction

Types

Major
Moderate
Minor

Priority

⭐⭐⭐⭐⭐

FR-009 Contraindications

દરેક Medicine માટે

Liver Disease
Kidney Disease
Allergy
Pregnancy
Lactation

Priority

⭐⭐⭐⭐⭐

FR-010 Side Effects

દરેક Medicine માટે

Common

Serious

Rare

Priority

⭐⭐⭐⭐⭐

FR-011 Patient Counselling

Supported Languages

Gujarati
Hindi
English

Topics

How to Take
Food
Storage
Missed Dose
Overdose

Priority

⭐⭐⭐⭐⭐

FR-012 AI Clinical Pharmacist

AI

Database First
Explain Information
Multilingual
Safety First

AI will never

Diagnose
Prescribe

Priority

⭐⭐⭐⭐⭐

FR-013 OCR Prescription

Upload Prescription

↓

Medicine Detection

↓

Database Search

Priority

⭐⭐⭐⭐

FR-014 Barcode Scanner

Scan Medicine

↓

Medicine Profile

Priority

⭐⭐⭐⭐

FR-015 Stock Management

Store Owner

can manage

Stock
Batch
Expiry
Quantity

Priority

⭐⭐⭐⭐

FR-016 Voice Assistant

User

Speak

↓

Medicine Search

Priority

⭐⭐⭐

FR-017 Multilingual Support

Auto Detect

Gujarati
Hindi
English

Priority

⭐⭐⭐⭐⭐

FR-018 Offline Mode

Database Search

without Internet

Priority

⭐⭐⭐

FR-019 Evidence Reference

Clinical Information

↓

Reference

CDSCO
NFI
WHO

Priority

⭐⭐⭐⭐⭐

FR-020 Security

API Key

Protected

Database

Protected

Priority

⭐⭐⭐⭐⭐

Functional Requirements Summary
Module	Status
Medicine Search	Planned
Smart Search	Completed
Medicine Card	Completed
Brand Comparison	Planned
Drug Interaction	Planned
Patient Counselling	Planned
OCR	Planned
Barcode	Planned
Voice	Planned
Stock	Planned