Day 3 – Database Design & Architecture

Document Version: 1.0

1. Database Philosophy
Database First

દરેક જવાબનો પ્રથમ આધાર

Pharma AI Database

હશે.

AI માત્ર સમજાવશે.

Database હંમેશા Source of Truth રહેશે.

2. Database Architecture
                 Pharma AI Database

                        │
────────────────────────────────────────────────────

Generic

Brand

Company

Product

Composition

Classification

Drug Interaction

Contraindication

Side Effects

Pregnancy

Lactation

Renal Dose

Hepatic Dose

Food Interaction

Alcohol Interaction

Storage

Patient Counselling

Jan Aushadhi

Stock

References
3. Database Tables
Table 1
Generic

Purpose

Store generic medicine information.

Columns

Generic_ID

Generic_Name

Gujarati_Name

Hindi_Name

Category

Therapeutic_Class

Pharmacological_Class

ATC_Code

WHO_Essential

Description
Table 2
Brand

Purpose

Store all brands.

Columns

Brand_ID

Brand_Name

Generic_ID

Company_ID

Strength

Dosage_Form
Table 3
Company

Columns

Company_ID

Company_Name

Country

Website

Manufacturer

License
Table 4
Product

Columns

Product_ID

Brand_ID

Pack_Size

MRP

GST

Schedule

Barcode
Table 5
Composition

Example

PCM 325

+

Caffeine 30

+

Phenylephrine

Columns

Composition_ID

Brand_ID

Ingredient

Strength

Unit
Table 6
Classification
Medicine

↓

NSAID

Analgesic

Antibiotic

Antihypertensive

Antidiabetic

Columns

Class_ID

Generic_ID

System

Class

Subclass
Table 7
Drug Interaction

Columns

Interaction_ID

Drug_A

Drug_B

Severity

Mechanism

Recommendation
Table 8
Contraindications

Columns

Generic_ID

Condition

Severity

Reason
Table 9
Side Effects

Columns

Generic_ID

Common

Serious

Rare

Frequency
Table 10
Pregnancy

Columns

Generic_ID

Risk

Recommendation

Reference
Table 11
Lactation

Columns

Generic_ID

Safe

Recommendation

Reference
Table 12
Renal Dose

Columns

Generic_ID

Creatinine_Clearance

Dose_Adjustment

Reference
Table 13
Hepatic Dose

Columns

Generic_ID

Liver_Status

Dose_Adjustment
Table 14
Food Interaction

Columns

Generic_ID

Food

Effect

Recommendation
Table 15
Alcohol Interaction

Columns

Generic_ID

Alcohol

Severity

Advice
Table 16
Storage

Columns

Generic_ID

Temperature

Humidity

Light

Shelf_Life
Table 17
Patient Counselling

Columns

Generic_ID

Gujarati

Hindi

English
Table 18
Jan Aushadhi

Columns

Generic_ID

Jan_Aushadhi_Name

PMBI_Code

Availability
Table 19
Store Inventory

Columns

Product_ID

Batch

Expiry

Quantity

Rack

Location
Table 20
Clinical References

Columns

Reference_ID

Generic_ID

Source

Edition

URL

Last_Update
4. Database Relationships
Generic

↓

Brand

↓

Product

↓

Inventory

↓

Patient
5. Database Priority

Priority 1

Generic
Brand
Company
Product

Priority 2

Interaction
Side Effects
Contraindications

Priority 3

Pregnancy
Lactation
Counselling

Priority 4

Stock
OCR
Barcode
6. Database Rules
Rule 1

Every Generic must have

Generic_ID

Rule 2

Every Brand must belong to one Generic.

Rule 3

Every Product belongs to one Brand.

Rule 4

No duplicate Generic.

Rule 5

No duplicate Brand.

Rule 6

Every Clinical Information must have a Reference.

Rule 7

Every Patient Counselling must be available in

Gujarati

Hindi

English

7. Future Database Size

Target

Generic

5,000+

Brands

50,000+

Companies

5,000+

Products

100,000+

Interactions

500,000+

Counselling

5,000+

References

100,000+
8. Master Database Workflow
Medicine Search

↓

Generic Table

↓

Brand Table

↓

Clinical Tables

↓

AI Engine

↓

Patient
9. Current Status
Table	Status
Generic	✅ Started
Brand	✅ Started
Company	✅ Started
Product	✅ Started
Interaction	📋 Planned
Side Effects	📋 Planned
Counselling	📋 Planned
References	📋 Planned
10. Long-Term Database Goal

Build the largest structured Indian Clinical Pharmacy Database to support multilingual medicine information, patient counselling, Jan Aushadhi services, and AI-assisted pharmacy workflows.