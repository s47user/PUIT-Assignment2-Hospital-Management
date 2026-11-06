# Pentecost University Hospital Management System (PU-HMS)
## Academic Assignment 2: Comprehensive Clinical Information & Electronic Medical Record (EMR) System

**Student Name:** Emmanuel Siaw Asante  
**Student ID / Index:** PYT230047  
**Course Lecturer:** Mr. Harry Attieku-Boateng  
**Academic Institution:** Pentecost University, Faculty of Computing & Information Technology  
**Department:** Information Technology  
**Submission Deadline:** November 30th  

---

## 🌟 Executive Overview
The **Pentecost University Hospital Management System (PU-HMS)** is an enterprise clinical operations and electronic medical record (EMR) platform developed to address real-world healthcare workflow challenges in Ghanaian hospital environments.

Built using an asynchronous **Streamlit** frontend and a normalized **SQLite** relational persistence backend, the platform delivers six core operational modules:
1. **Executive Operational Dashboard:** Real-time throughput indicators, Ghanaian demographic distributions, triage urgency pie charts, and National Health Insurance Scheme (NHIS) claims revenue analysis.
2. **Patient Registration & Medical Record Management:** Captures patient biodata, national NHIS identification numbers, emergency next-of-kin contacts, blood groups, and sickle cell hemoglobin genotypes (AA, AS, SS, AC, SC).
3. **Automated Triage & Clinical Vitals Station:** Captures resting blood pressure, pulse, body temperature, weight, and height; automatically computes WHO-compliant Body Mass Index (BMI); and algorithmically routes patients into color-coded clinical urgency tiers:
   - 🚨 **Emergency (Red):** Systolic BP $\ge$ 160 mmHg, Diastolic BP $\ge$ 100 mmHg, or Temp $\ge$ 38.5°C.
   - ⚠️ **Priority (Yellow):** Systolic BP $\ge$ 140 mmHg, Temp $\ge$ 37.8°C, or BMI $\ge$ 32.0 kg/m².
   - ✅ **Routine (Green):** Stable physiological parameters.
4. **Physician Clinical Encounter & EMR:** Electronic clinical documentation system for Chief Complaints, Definitive Diagnosis, e-Prescriptions with dosage instructions, Laboratory Requests, and Physician Progress Notes.
5. **Outpatient Specialist Clinic Scheduling:** Coordinates specialist appointment queues across Internal Medicine, Cardiology, General OPD, Pediatrics, and Obstetrics/Gynecology.
6. **Billing, Pharmacy & NHIS Claims Management:** Implements the National Health Insurance Scheme copay formula, calculating the 70% state subsidy and generating itemized patient copayment bills.

---

## 📁 Repository File Structure
```
├── app.py                     # Main Interactive Streamlit Hospital Management Application
├── init_db.py                 # Relational schema definition & 20+ authentic Ghanaian clinical records
├── generate_diagrams.py       # Automated architecture, ERD, and operational analytics diagram generator
├── generate_docx_report.py    # Formatted Word (.docx) technical report generator
├── requirements.txt           # Python dependency manifest
├── database/
│   └── hospital.db            # SQLite relational database
└── figures/
    ├── system_architecture.png
    ├── operational_analytics.png
    └── triage_algorithm_flowchart.png
```

---

## 🚀 Running the Web Application Locally

```bash
# 1. Clone this repository
git clone https://github.com/wisabuilds/PUIT-Assignment2-Hospital-Management.git
cd PUIT-Assignment2-Hospital-Management

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed / Initialize Database
python init_db.py

# 4. Launch Streamlit Application
streamlit run app.py
```

---

## 👨‍🏫 Lecturer / Collaborator Notice
As instructed by **Mr. Harry Attieku-Boateng**, this project is tracked under Git version control. The lecturer can be invited as a collaborator directly on GitHub.
