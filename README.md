# 💊 Pharma AI

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red)
![Google Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-green)
![Version](https://img.shields.io/badge/Version-v1.0-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

## 🚀 Advanced Clinical Decision Support System

**Pharma AI** is an AI-powered Clinical Decision Support System (CDSS) designed to assist pharmacists and healthcare professionals in providing accurate medicine information, clinical decision support, and patient counselling.

The application combines a local medicine database with Google Gemini AI to deliver intelligent pharmaceutical assistance while maintaining a clean and user-friendly interface.

---

# ✨ Features

## 🔍 Smart Medicine Search

- Fast medicine search
- Brand & Generic search
- Fuzzy spelling correction
- Alternative medicine suggestions
- Detailed medicine information

---

## 🤖 AI Clinical Pharmacist

Powered by Google Gemini AI

Provides:

- Clinical counselling
- Indications
- Dosage information
- Side effects
- Contraindications
- Patient counselling
- Clinical recommendations

---

## 💊 Drug Interaction Checker

Analyze interactions between two medicines.

Provides:

- Severity Classification
    - 🔴 Major
    - 🟡 Moderate
    - 🟢 Minor
    - ✅ No Known Interaction
- Clinical mechanism
- Management recommendations
- Patient counselling

---

## ⚖️ Brand Comparison

Compare medicines based on:

- Generic Name
- Strength
- Dosage Form
- Price
- Manufacturer
- Therapeutic Class

---

## 🧪 Clinical QA Engine

Built-in Quality Assurance Engine for regression testing.

Features:

- Automated Clinical Validation
- Regression Test Suite
- CSV-based Test Cases
- Performance Measurement
- PASS / FAIL Report
- JSON Report Export

---

# 🛠 Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.12 |
| UI | Streamlit |
| AI Engine | Google Gemini 2.5 Flash |
| Data Processing | Pandas |
| Environment | Python Virtual Environment |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
PHARMA-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .env
│
├── assets/
│
├── data/
│   ├── medicine_database.xlsx
│   └── clinical_test_cases.csv
│
├── modules/
│   ├── ai_engine.py
│   ├── comparison.py
│   ├── clinical_validator.py
│   ├── database.py
│   ├── interaction.py
│   ├── medicine_card.py
│   ├── smart_search.py
│   └── styles.py
│
└── pages/
```

---

# 📸 Screenshots

Add screenshots here.

### 🏠 Home Dashboard

```
Screenshot Here
```

---

### 💊 Drug Interaction Checker

```
Screenshot Here
```

---

### 🤖 AI Clinical Pharmacist

```
Screenshot Here
```

---

### 🧪 Clinical QA Engine

```
Screenshot Here
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/PHARMA-AI.git
```

```bash
cd PHARMA-AI
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a **.env** file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📋 Clinical Validation

Pharma AI includes a Clinical QA Engine.

Example regression suite:

| Medicine 1 | Medicine 2 | Expected |
|------------|------------|----------|
| Warfarin | Aspirin | Major |
| Warfarin | Ibuprofen | Major |
| Sildenafil | Nitroglycerin | Major |
| Paracetamol | Amlodipine | No Known Interaction |
| Crocin | Paracetamol | Duplicate Therapy |

---

# 📈 Current Project Status

| Module | Status |
|----------|--------|
| Smart Search | ✅ Stable |
| AI Clinical Pharmacist | ✅ Stable |
| Drug Interaction | ✅ Stable |
| Brand Comparison | ✅ Stable |
| Clinical QA Engine | ✅ Stable |
| UI | ✅ Stable |

Overall Progress

**Version 1.0 Release Candidate**

---

# 🗺 Roadmap

## Version 1.0

- ✅ Smart Medicine Search
- ✅ AI Clinical Pharmacist
- ✅ Drug Interaction Checker
- ✅ Brand Comparison
- ✅ Clinical QA Engine

---

## Version 1.1

- OCR Prescription Reader
- Drug-Food Interaction
- Drug-Alcohol Interaction
- PDF Report Export

---

## Version 1.2

- Pregnancy Risk Checker
- Lactation Safety
- Renal Dose Adjustment
- Hepatic Dose Adjustment
- QT Prolongation Alerts

---

# ⚠️ Medical Disclaimer

**Pharma AI** is intended for educational purposes and as a Clinical Decision Support (CDS) tool.

It **does not replace** the clinical judgment of physicians or pharmacists.

All recommendations should be verified using standard clinical references and institutional guidelines before making patient care decisions.

---

# 🤝 Contributing

Contributions are welcome.

Please:

- Fork the repository
- Create a feature branch
- Commit your changes
- Submit a Pull Request

---

# 📜 License

This project is licensed under the **MIT License**.

See the LICENSE file for details.

---

# 👨‍💻 Author

**Ravi Varsani**

Clinical Pharmacist • Python Developer • AI in Healthcare

GitHub:
https://github.com/your-username

---

# ⭐ Support

If you found this project useful,

⭐ Star this repository on GitHub.
## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 💙 Built with Python, Streamlit & Google Gemini AI for Better Clinical Decision Support.