import os
import sqlite3
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIGS_DIR = os.path.join(BASE_DIR, "figures")
DB_PATH = os.path.join(BASE_DIR, "database", "hospital.db")
OUTPUT_DOCX = os.path.join(BASE_DIR, "Emmanuel_Siaw_Asante_PYT230047_Assignment2.docx")

doc = Document()

# Set standard 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Helper styling functions
def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_header_block():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_dept = p.add_run("PENTECOST UNIVERSITY\nFACULTY OF COMPUTING & INFORMATION TECHNOLOGY\nDEPARTMENT OF INFORMATION TECHNOLOGY\n")
    run_dept.font.name = "Arial"
    run_dept.font.size = Pt(11)
    run_dept.font.bold = True
    run_dept.font.color.rgb = RGBColor(26, 54, 93)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(14)
    run_title = p_title.add_run("ACADEMIC ASSIGNMENT 2: HOSPITAL MANAGEMENT SYSTEM (PU-HMS)\nSYSTEM ARCHITECTURE & TECHNICAL IMPLEMENTATION REPORT")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(15)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(16, 42, 77)

    # Metadata Table
    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    data = [
        ("Student Name:", "Emmanuel Siaw Asante"),
        ("Student ID / Index Number:", "PYT230047"),
        ("Course Lecturer:", "Mr. Harry Attieku-Boateng"),
        ("GitHub Repository Link:", "https://github.com/wisabuilds/PUIT-Assignment2-Hospital-Management"),
        ("Deployed Web Application:", "https://puit-assignment2-hospital-management.streamlit.app/"),
        ("Submission Date / Deadline:", "November 2026 | Deadline: November 30th")
    ]

    for idx, (label, val) in enumerate(data):
        row = table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.3)
        cell_val.width = Inches(4.2)
        
        set_cell_margins(cell_lbl, 80, 80, 100, 100)
        set_cell_margins(cell_val, 80, 80, 100, 100)
        set_cell_background(cell_lbl, "F0F4F8")
        set_cell_background(cell_val, "FAFAFA")
        
        p1 = cell_lbl.paragraphs[0]
        r1 = p1.add_run(label)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(26, 54, 93)

        p2 = cell_val.paragraphs[0]
        r2 = p2.add_run(val)
        r2.font.size = Pt(9.5)
        if "http" in val:
            r2.font.color.rgb = RGBColor(11, 84, 164)
            r2.font.underline = True
        else:
            r2.font.color.rgb = RGBColor(45, 55, 72)

    doc.add_paragraph().paragraph_format.space_after = Pt(18)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(26, 54, 93)
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(43, 108, 176)
    return p

def add_body_p(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(45, 55, 72)
    return p

def add_bullet_p(bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_bold = p.add_run(bold_prefix + " ")
    r_bold.font.name = "Calibri"
    r_bold.font.size = Pt(10.5)
    r_bold.font.bold = True
    r_bold.font.color.rgb = RGBColor(26, 54, 93)
    
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = RGBColor(45, 55, 72)
    return p

def add_figure_with_caption(fig_name, caption_text, width=Inches(5.8)):
    fig_path = os.path.join(FIGS_DIR, fig_name)
    if os.path.exists(fig_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(fig_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(74, 85, 104)

print("Synthesizing Assignment 2 Document...")
add_header_block()

# -----------------------------------------------------------------------------
# TABLE OF CONTENTS & TABLE OF FIGURES
# -----------------------------------------------------------------------------
add_heading_1("Table of Contents")
toc_items = [
    ("1. Executive Summary & Project Scope", "Page 2"),
    ("2. Problem Analysis & Ghanaian Healthcare Context", "Page 2"),
    ("3. Multi-Tier System Architecture Design", "Page 2"),
    ("4. Relational Database Design & Data Modeling", "Page 3"),
    ("5. Core Functional Modules & Clinical Workflows", "Page 4"),
    ("    5.1 Patient Registration & National Health Insurance (NHIS) Ingestion", "Page 4"),
    ("    5.2 Automated Clinical Triage & Physiological Alert Engine", "Page 4"),
    ("    5.3 Physician Consultation Encounter & Electronic Health Records (EHR)", "Page 5"),
    ("    5.4 Outpatient Clinic Scheduling & Departmental Coordination", "Page 5"),
    ("    5.5 Revenue, Pharmacy & NHIS Claims Settlement Engine", "Page 6"),
    ("6. Operational Intelligence & Patient Cohort Analytics", "Page 6"),
    ("7. System Verification, Testing & Error Handling", "Page 7"),
    ("8. Source Version Control & GitHub Repository Compliance", "Page 7"),
    ("9. Conclusion & Recommendations", "Page 8"),
    ("10. Formal Academic References", "Page 8")
]
for item, pg in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    r1 = p.add_run(item)
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.5)
    r2 = p.add_run(f"  {pg}")
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(113, 128, 150)

add_heading_1("Table of Figures")
tof_items = [
    ("Figure 1.1: Multi-Tier Architectural Blueprint of Pentecost University Hospital Management System", "Section 3"),
    ("Figure 2.1: Hospital Operational Intelligence & Patient Cohort Analytics", "Section 6"),
    ("Figure 2.2: Algorithmic Clinical Triage Decision Logic Flowchart", "Section 5.2")
]
for fig, sec in tof_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    r1 = p.add_run(fig)
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.5)
    r2 = p.add_run(f"  ({sec})")
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(113, 128, 150)

doc.add_page_break()

# -----------------------------------------------------------------------------
# 1. EXECUTIVE SUMMARY
# -----------------------------------------------------------------------------
add_heading_1("1. Executive Summary & Project Scope")
add_body_p(
    "This technical report articulates the end-to-end design, software engineering implementation, and clinical evaluation of the "
    "Pentecost University Hospital Management System (PU-HMS). Developed as a primary deliverable for Assignment 2 under the instruction "
    "of Mr. Harry Attieku-Boateng, the platform establishes a comprehensive, automated clinical operations environment that streamlines "
    "inpatient and outpatient workflows, clinical vitals triage, medical consultations, specialist scheduling, and insurance claim settlements."
)
add_body_p(
    "In accordance with modern healthcare information system standards, PU-HMS addresses critical inefficiencies in paper-based hospital "
    "environments. The platform incorporates a 3-tier software architecture comprising a responsive Streamlit presentation layer, a robust Python "
    "business and triage logic engine, and a normalized SQLite relational persistence store. The system is fully deployed for public evaluation and "
    "all code is managed under Git source control on GitHub, adhering strictly to course submission standards."
)

# -----------------------------------------------------------------------------
# 2. PROBLEM ANALYSIS & GHANAIAN HEALTHCARE CONTEXT
# -----------------------------------------------------------------------------
add_heading_1("2. Problem Analysis & Ghanaian Healthcare Context")
add_body_p(
    "In developing healthcare environments such as Ghana, primary and secondary healthcare delivery continues to struggle with fragmented medical records, "
    "protracted outpatient waiting times, manual calculation of physiological indices, and cumbersome National Health Insurance Scheme (NHIS) claims reconciliation. "
    "Paper folders frequently suffer physical degradation, loss, or misplacement, obstructing continuity of clinical care across physician shifts."
)
add_body_p(
    "PU-HMS was purposefully engineered to reflect authentic Ghanaian clinical realities. It captures vital demographic nuances including Ghanaian ethnic cohorts "
    "(Akan, Ga-Dangme, Ewe, Mole-Dagbon, Guan, Grusi), localized hemoglobin genotypes (AA, AS, SS, AC, SC), and universal NHIS membership identities. "
    "Furthermore, the financial engine automates the 70% state medical subsidy formula, generating clear, itemized patient copayment bills and eliminating billing discrepancies."
)

# -----------------------------------------------------------------------------
# 3. MULTI-TIER SYSTEM ARCHITECTURE
# -----------------------------------------------------------------------------
add_heading_1("3. Multi-Tier System Architecture Design")
add_body_p(
    "The software architecture of PU-HMS is structured around a decoupled, three-tier modular paradigm that guarantees separation of concerns, "
    "operational scalability, and ease of maintainability (Figure 1.1):"
)
add_bullet_p("Tier 1: Presentation & User Experience Layer:", "Constructed utilizing Streamlit's reactive web framework, delivering a unified, mobile-responsive portal partitioned into intuitive operational roles (Records Clerks, Triage Nurses, Attending Physicians, and Billing Officers).")
add_bullet_p("Tier 2: Application & Clinical Logic Layer:", "Implements the core business rules: automated Body Mass Index (BMI) computations, physiological threshold evaluations for triage alert routing, e-prescription generation, and NHIS reimbursement subsidy calculations.")
add_bullet_p("Tier 3: Relational Persistence Layer:", "Engineered on SQLite with enforced primary-foreign key relationships, foreign-key cascade rules, and indexed query optimizations to support high-concurrency read-write transactions.")

add_figure_with_caption("system_architecture.png", "Figure 1.1: Multi-Tier Architectural Blueprint of Pentecost University Hospital Management System.")

# -----------------------------------------------------------------------------
# 4. RELATIONAL DATABASE DESIGN & DATA MODELING
# -----------------------------------------------------------------------------
add_heading_1("4. Relational Database Design & Data Modeling")
add_body_p(
    "The data layer is modeled in Third Normal Form (3NF) across five interconnected relational entities, ensuring zero data redundancy "
    "and strict referential integrity across the clinical continuum:"
)

# Schema Table
schema_table = doc.add_table(rows=6, cols=3)
schema_table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_db = ["Entity / Table Name", "Primary & Foreign Key Schema", "Clinical Operational Purpose"]
for i, h in enumerate(headers_db):
    cell = schema_table.rows[0].cells[i]
    set_cell_background(cell, "1A365D")
    set_cell_margins(cell, 100, 100, 120, 120)
    p = cell.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

db_specs = [
    ("patients", "patient_id (PK, Auto), patient_code (Unique)", "Stores permanent legal biodata, ethnicity, emergency contact, blood group, genotype, and NHIS ID."),
    ("vitals", "vital_id (PK), patient_id (FK -> patients)", "Records longitudinal vital signs (BP, pulse, temp, weight, height), computed BMI, and triage category."),
    ("appointments", "appointment_id (PK), patient_id (FK -> patients)", "Coordinates scheduled outpatient clinical encounters, consultant assignments, and clinic statuses."),
    ("consultations", "consultation_id (PK), patient_id (FK -> patients)", "Contains formal physician progress encounters, chief symptoms, diagnosis, prescriptions, and lab orders."),
    ("billing", "bill_id (PK), patient_id (FK -> patients)", "Maintains financial ledgers, gross charges, 70% NHIS coverage deductions, patient copay, and receipt status.")
]

for row_idx, row_data in enumerate(db_specs, 1):
    row = schema_table.rows[row_idx]
    for col_idx, text in enumerate(row_data):
        cell = row.cells[col_idx]
        set_cell_background(cell, "F7FAFC" if row_idx % 2 == 1 else "FFFFFF")
        set_cell_margins(cell, 80, 80, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.size = Pt(9.0)
        if col_idx == 0:
            r.font.bold = True
            r.font.color.rgb = RGBColor(26, 54, 93)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# -----------------------------------------------------------------------------
# 5. CORE FUNCTIONAL MODULES
# -----------------------------------------------------------------------------
add_heading_1("5. Core Functional Modules & Clinical Workflows")
add_heading_2("5.1 Patient Registration & National Health Insurance (NHIS) Ingestion")
add_body_p(
    "The Patient Registration module establishes a permanent medical record identifier for incoming clients. Upon enrollment, "
    "the system automatically provisions a standardized alphanumeric Medical Record Code (e.g. PU-HOSP-0021). The intake form captures "
    "vital clinical metadata, including the patient's biological sex, ethnicity, blood group (A, B, AB, O), and hemoglobin genotype "
    "(AA, AS, SS, AC, SC), alongside verified NHIS card numbers to facilitate downstream claims verification."
)

add_heading_2("5.2 Automated Clinical Triage & Physiological Alert Engine")
add_body_p(
    "To eliminate subjective delays at the nursing triage station, PU-HMS incorporates an algorithmic decision engine that parses resting "
    "vital measurements immediately upon entry (Figure 2.2). The algorithm calculates Body Mass Index (BMI) using the WHO standard formula: "
    "BMI = Weight (kg) / [Height (m)]^2. Simultaneously, it cross-references systolic and diastolic arterial pressures and body temperature "
    "against emergency medical guidelines, automatically routing the patient into one of three distinct clinical tiers:"
)
add_bullet_p("Emergency (Red):", "Triggered when Systolic BP >= 160 mmHg, Diastolic BP >= 100 mmHg, or Core Temperature >= 38.5°C. Patient is marked for immediate physician alert and emergency resuscitation.")
add_bullet_p("Priority (Yellow):", "Triggered by Stage 1/2 Hypertension (Systolic BP >= 140 mmHg), moderate pyrexia (>= 37.8°C), or clinical obesity (BMI >= 32.0 kg/m²). Patient is placed at the head of the OPD queue.")
add_bullet_p("Routine (Green):", "Assigned when physiological parameters remain within normal baseline limits, queuing the patient for standard outpatient consultation.")

add_figure_with_caption("triage_algorithm_flowchart.png", "Figure 2.2: Algorithmic Clinical Triage Decision Logic Flowchart.")

add_heading_2("5.3 Physician Consultation Encounter & Electronic Health Records (EHR)")
add_body_p(
    "During clinical consultation, the attending physician selects the patient from the active OPD queue. The interface immediately renders "
    "the patient's complete demographic profile, baseline vitals, and computed triage category. The physician completes a standardized electronic encounter form "
    "capturing Chief Complaints, Working Clinical Diagnosis (e.g., Essential Hypertension, Uncomplicated Malaria, Type 2 Diabetes Mellitus), "
    "Itemized Pharmacological Prescriptions with dosage and duration, Diagnostic Laboratory Investigations (e.g., FBC, mRDT, Lipid Profile), "
    "and Clinical Progress Notes. Committing the encounter automatically synchronizes with the pharmacy and billing ledgers."
)

add_heading_2("5.4 Outpatient Clinic Scheduling & Departmental Coordination")
add_body_p(
    "The appointment scheduling module coordinates multi-specialty clinical sessions across five core departments: Internal Medicine, "
    "Cardiology & Clinical AI, General OPD, Pediatrics, and Obstetrics/Gynecology. The module prevents double-booking, maintains real-time "
    "clinic rosters, and supports scheduling modifications (Scheduled, Completed, Cancelled)."
)

add_heading_2("5.5 Revenue, Pharmacy & NHIS Claims Settlement Engine")
add_body_p(
    "The financial administration module automates patient invoicing and insurance claim preparation. For every billed clinical encounter, "
    "the engine calculates the statutory 70% NHIS reimbursement portion and deducts it from the gross bill, establishing the exact 30% "
    "patient copay requirement. The module tracks claim settlements in real time, preventing hospital revenue leakage."
)

# -----------------------------------------------------------------------------
# 6. OPERATIONAL ANALYTICS & PATIENT COHORT INTELLIGENCE
# -----------------------------------------------------------------------------
add_heading_1("6. Operational Intelligence & Patient Cohort Analytics")
add_body_p(
    "The Executive Dashboard aggregates longitudinal clinical metrics to empower hospital administrators with real-time operational insights. "
    "As visualized in Figure 2.1, the platform automatically parses the patient database to render demographic distributions across Ghanaian ethnic cohorts, "
    "triage urgency ratios, hemoglobin genotype prevalence (vital for sickle cell screening and prophylactic folic acid programs), and total revenue streams "
    "stratified by NHIS reimbursements versus direct patient copayments."
)

add_figure_with_caption("operational_analytics.png", "Figure 2.1: Hospital Operational Intelligence & Patient Cohort Analytics.")

# -----------------------------------------------------------------------------
# 7. SYSTEM VERIFICATION & TESTING
# -----------------------------------------------------------------------------
add_heading_1("7. System Verification, Testing & Error Handling")
add_body_p(
    "PU-HMS was subjected to rigorous unit, integration, and UI verification tests prior to final deployment. Key testing milestones include:"
)
add_bullet_p("Database Integrity Verification:", "Validated SQLite primary-foreign key cascade rules to ensure orphaned records cannot exist across vitals, appointments, and billing tables.")
add_bullet_p("Algorithmic Triage Boundary Testing:", "Tested edge-case boundary values (e.g. BP 159/99 vs 160/100, Temp 38.4°C vs 38.5°C) to confirm exact, deterministic triage categorization.")
add_bullet_p("Mathematical Financial Invariant:", "Verified that for every generated bill, Gross Amount == NHIS Covered (70%) + Patient Copay (30%), with zero penny-rounding leakage.")
add_bullet_p("Data Sanitization & Injection Prevention:", "All SQL commands leverage parameterized queries (? substitution), totally eliminating SQL injection vulnerabilities.")

# -----------------------------------------------------------------------------
# 8. SOURCE VERSION CONTROL & GITHUB REPOSITORY COMPLIANCE
# -----------------------------------------------------------------------------
add_heading_1("8. Source Version Control & GitHub Repository Compliance")
add_body_p(
    "In strict conformance with Mr. Harry Attieku-Boateng's grading criterion ('Every work must be committed and pushed to your GitHub; if I don't "
    "see your GitHub repo, the work is zero'), the complete PU-HMS project has been published as a public repository on GitHub. "
    "The repository includes comprehensive setup documentation (README.md), explicit Python dependency requirements (requirements.txt), "
    "database initialization routines (init_db.py), and the full application codebase."
)

# -----------------------------------------------------------------------------
# 9. CONCLUSION & RECOMMENDATIONS
# -----------------------------------------------------------------------------
add_heading_1("9. Conclusion & Practical Recommendations")
add_body_p(
    "The Pentecost University Hospital Management System (PU-HMS) successfully demonstrates the practical application of software engineering "
    "principles and clinical data modeling to solve real-world healthcare administration problems. By integrating automated triage, electronic medical "
    "records, and seamless NHIS financial processing into a modern web framework, the system drastically reduces outpatient bottlenecks and "
    "ensures high-fidelity patient record keeping."
)
add_body_p(
    "Future expansions can incorporate biometric fingerprint authentication for patient identification and machine learning diagnostic risk "
    "models (such as the cardiovascular screening pipeline developed in Assignment 1) directly into the doctor's consultation view."
)

# -----------------------------------------------------------------------------
# 10. REFERENCES
# -----------------------------------------------------------------------------
add_heading_1("10. Formal Academic References")
refs = [
    "[1] World Health Organization. (2020). Global strategy on digital health 2020-2025. World Health Organization.",
    "[2] Ministry of Health Ghana. (2018). National e-Health Strategy for Ghana. Ministry of Health, Republic of Ghana.",
    "[3] Shortliffe, E. H., & Cimino, J. J. (Eds.). (2014). Biomedical informatics: computer applications in health care and biomedicine. Springer.",
    "[4] Atinga, R. A., Abekah-Nkrumah, G., & Domfeh, K. A. (2011). Managing healthcare quality in Ghana: a necessity of patient satisfaction. International Journal of Health Care Quality Assurance, 24(7), 548-563.",
    "[5] National Health Insurance Authority (NHIA). (2022). National Health Insurance Scheme Operational Guidelines and Tariffs. Accra, Ghana.",
    "[6] Date, C. J. (2004). An introduction to database systems (8th ed.). Pearson Education."
]
for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(ref)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(74, 85, 104)

doc.save(OUTPUT_DOCX)
print(f"✓ Technical Report successfully generated at:\n  {OUTPUT_DOCX}")
