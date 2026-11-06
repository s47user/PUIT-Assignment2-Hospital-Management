import os
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------------------------------
# APPLICATION CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PU-HMS | Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "hospital.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# -----------------------------------------------------------------------------
# CUSTOM STYLING (MODERN HEALTHCARE THEME)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1A365D;
        margin-bottom: 0px;
    }
    .metric-card {
        background-color: #F7FAFC;
        border-left: 5px solid #2B6CB0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .triage-red {
        background-color: #FED7D7;
        color: #9B2C2C;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .triage-yellow {
        background-color: #FEFCBF;
        color: #975A16;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .triage-green {
        background-color: #C6F6D5;
        color: #22543D;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/hospital-3.png", width=80)
    st.title("PU-HMS Portal")
    st.markdown("**Pentecost University Hospital**  \n*Integrated Clinical & EMR Suite*")
    st.caption("**Assignment 2: Hospital Management System**")
    st.divider()

    menu = st.radio(
        "Hospital Departments",
        [
            "📊 Executive Dashboard",
            "🏥 Patient Registration & EMR",
            "🩺 Triage & Clinical Vitals",
            "👨‍⚕️ Doctor Consultation & Diagnosis",
            "📅 Outpatient Appointments",
            "💳 Billing & NHIS Claims",
            "📑 System Architecture & Docs"
        ],
        index=0
    )

    st.divider()
    st.markdown("""
    **Developer Metadata:**
    * **Student:** Emmanuel Siaw Asante
    * **Student ID:** `PYT230047`
    * **Lecturer:** Mr. Harry Attieku-Boateng
    * **Deadline:** November 30th
    """)

# -----------------------------------------------------------------------------
# 1. EXECUTIVE DASHBOARD
# -----------------------------------------------------------------------------
if menu == "📊 Executive Dashboard":
    st.markdown("<h1 class='main-header'>🏥 Executive Hospital Operations Dashboard</h1>", unsafe_allow_html=True)
    st.caption("Real-time clinical throughput, patient demographics, and NHIS reimbursement analytics.")
    
    conn = get_connection()
    df_patients = pd.read_sql_query("SELECT * FROM patients", conn)
    df_vitals = pd.read_sql_query("SELECT * FROM vitals", conn)
    df_appointments = pd.read_sql_query("SELECT * FROM appointments", conn)
    df_billing = pd.read_sql_query("SELECT * FROM billing", conn)
    conn.close()

    # KPI Top Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Registered Patients", len(df_patients), "+3 this week")
    with col2:
        emergency_count = len(df_vitals[df_vitals["triage_category"].str.contains("Emergency|Red")])
        st.metric("Emergency Triage Cases", emergency_count, "Requires immediate attention")
    with col3:
        active_appts = len(df_appointments[df_appointments["status"] == "Scheduled"])
        st.metric("Scheduled Appointments", active_appts, "Active OPD Queue")
    with col4:
        total_rev = df_billing["gross_amount_ghs"].sum()
        nhis_share = df_billing["nhis_covered_ghs"].sum()
        st.metric("Gross Hospital Revenue", f"GHS {total_rev:,.2f}", f"NHIS: GHS {nhis_share:,.2f}")

    st.divider()

    # Visual Analytics Row
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Patient Demographic Distribution by Ethnicity")
        if not df_patients.empty:
            eth_counts = df_patients["ethnicity"].value_counts()
            fig, ax = plt.subplots(figsize=(7, 4.2))
            sns.barplot(x=eth_counts.index, y=eth_counts.values, palette="Blues_r", ax=ax)
            ax.set_ylabel("Patient Count", fontsize=10)
            ax.set_xlabel("Ghanaian Demographic Cohort", fontsize=10)
            plt.xticks(rotation=25)
            plt.tight_layout()
            st.pyplot(fig)

    with chart_col2:
        st.subheader("Triage Urgency Category Breakdown")
        if not df_vitals.empty:
            triage_counts = df_vitals["triage_category"].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6, 4.2))
            colors = ["#2ecc71", "#f39c12", "#e74c3c"]
            ax2.pie(triage_counts.values, labels=triage_counts.index, autopct='%1.1f%%', startangle=140, colors=colors[:len(triage_counts)])
            ax2.axis('equal')
            plt.tight_layout()
            st.pyplot(fig2)

    st.subheader("Recent Patient Clinical Intake Activity")
    merged_recent = df_patients.merge(df_vitals, on="patient_id", how="inner").tail(8)
    display_cols = ["patient_code", "full_name", "age", "gender", "blood_pressure_sys", "blood_pressure_dia", "bmi", "triage_category", "recorded_at"]
    st.dataframe(merged_recent[display_cols].rename(columns={
        "patient_code": "Patient Code",
        "full_name": "Full Name",
        "age": "Age",
        "gender": "Gender",
        "blood_pressure_sys": "Systolic BP",
        "blood_pressure_dia": "Diastolic BP",
        "bmi": "BMI",
        "triage_category": "Triage Status",
        "recorded_at": "Recorded Timestamp"
    }), use_container_width=True)

# -----------------------------------------------------------------------------
# 2. PATIENT REGISTRATION & DIRECTORY
# -----------------------------------------------------------------------------
elif menu == "🏥 Patient Registration & EMR":
    st.markdown("<h1 class='main-header'>🏥 Patient Registration & Electronic Medical Records</h1>", unsafe_allow_html=True)
    st.caption("Enroll new patients, maintain national insurance identities, and review demographic profiles.")

    tab_register, tab_directory = st.tabs(["📝 New Patient Registration", "🗂️ Patient Directory & EMR Search"])

    with tab_register:
        with st.form("new_patient_form"):
            st.subheader("Patient Biodata & Demographics")
            r1_c1, r1_c2, r1_c3 = st.columns(3)
            with r1_c1:
                name = st.text_input("Full Legal Name", placeholder="e.g. Kwabena Mensah")
            with r1_c2:
                age = st.number_input("Age (Years)", min_value=0, max_value=120, value=32)
            with r1_c3:
                gender = st.selectbox("Biological Sex", ["Male", "Female"])

            r2_c1, r2_c2, r2_c3 = st.columns(3)
            with r2_c1:
                ethnicity = st.selectbox("Ethnicity / Region", ["Akan", "Ga-Dangme", "Ewe", "Mole-Dagbon", "Guan", "Grusi", "Gurma", "Other"])
            with r2_c2:
                contact = st.text_input("Primary Contact (Phone)", placeholder="024XXXXXXX")
            with r2_c3:
                emergency = st.text_input("Emergency Contact", placeholder="020XXXXXXX")

            r3_c1, r3_c2, r3_c3 = st.columns(3)
            with r3_c1:
                blood_group = st.selectbox("Blood Group", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
            with r3_c2:
                genotype = st.selectbox("Hemoglobin Genotype", ["AA", "AS", "SS", "AC", "SC", "CC"])
            with r3_c3:
                nhis = st.text_input("NHIS Membership Number", placeholder="NHIS-GH-XXXXXX")

            submitted = st.form_submit_button("Register Patient in PU-HMS", type="primary", use_container_width=True)

        if submitted:
            if not name.strip() or not contact.strip():
                st.error("Please provide at least the Patient Full Name and Contact Number.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM patients")
                next_id = cur.fetchone()[0] + 1
                p_code = f"PU-HOSP-{next_id:04d}"
                reg_time = datetime.now().strftime("%Y-%m-%d %H:%M")

                cur.execute("""
                INSERT INTO patients (patient_code, full_name, age, gender, ethnicity, contact_number, emergency_contact, blood_group, genotype, nhis_number, registration_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (p_code, name, age, gender, ethnicity, contact, emergency, blood_group, genotype, nhis, reg_time))
                conn.commit()
                conn.close()
                st.success(f"Patient **{name}** successfully enrolled with Medical Record Code: **{p_code}**")

    with tab_directory:
        conn = get_connection()
        df_patients = pd.read_sql_query("SELECT * FROM patients ORDER BY patient_id DESC", conn)
        conn.close()

        search_query = st.text_input("🔍 Search Patient by Name, Code, or Phone Number", "")
        if search_query:
            df_filtered = df_patients[
                df_patients["full_name"].str.contains(search_query, case=False, na=False) |
                df_patients["patient_code"].str.contains(search_query, case=False, na=False) |
                df_patients["contact_number"].str.contains(search_query, case=False, na=False)
            ]
        else:
            df_filtered = df_patients

        st.dataframe(df_filtered[[
            "patient_code", "full_name", "age", "gender", "ethnicity", "blood_group", "genotype", "nhis_number", "contact_number", "registration_date"
        ]].rename(columns={
            "patient_code": "Code", "full_name": "Name", "age": "Age", "gender": "Sex",
            "ethnicity": "Ethnicity", "blood_group": "Blood", "genotype": "Genotype",
            "nhis_number": "NHIS ID", "contact_number": "Phone", "registration_date": "Enrolled"
        }), use_container_width=True)

# -----------------------------------------------------------------------------
# 3. TRIAGE & CLINICAL VITALS
# -----------------------------------------------------------------------------
elif menu == "🩺 Triage & Clinical Vitals":
    st.markdown("<h1 class='main-header'>🩺 Clinical Vitals & Automated Triage Station</h1>", unsafe_allow_html=True)
    st.caption("Measure vital signs, calculate BMI automatically, and triage patients by clinical urgency.")

    conn = get_connection()
    df_pts = pd.read_sql_query("SELECT patient_id, patient_code, full_name FROM patients", conn)
    conn.close()

    patient_options = {f"{row['patient_code']} - {row['full_name']}": row['patient_id'] for _, row in df_pts.iterrows()}
    
    col_input, col_status = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("Record Patient Vitals")
        selected_patient_label = st.selectbox("Select Patient", list(patient_options.keys()))
        selected_patient_id = patient_options[selected_patient_label]

        v1_c1, v1_c2 = st.columns(2)
        with v1_c1:
            sys_bp = st.number_input("Systolic BP (mmHg)", min_value=70, max_value=240, value=128)
        with v1_c2:
            dia_bp = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=140, value=82)

        v2_c1, v2_c2 = st.columns(2)
        with v2_c1:
            pulse = st.number_input("Pulse Rate (BPM)", min_value=40, max_value=180, value=74)
        with v2_c2:
            temp = st.number_input("Body Temp (°C)", min_value=34.0, max_value=42.0, value=36.8, step=0.1)

        v3_c1, v3_c2 = st.columns(2)
        with v3_c1:
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, value=72.5, step=0.5)
        with v3_c2:
            height = st.number_input("Height (cm)", min_value=100.0, max_value=220.0, value=172.0, step=0.5)

        # Automated BMI
        bmi = round(weight / ((height / 100.0) ** 2), 1)

        # Automated Triage
        if sys_bp >= 160 or dia_bp >= 100 or temp >= 38.5:
            triage = "Emergency (Red)"
        elif sys_bp >= 140 or dia_bp >= 90 or temp >= 37.8 or bmi >= 32.0:
            triage = "Priority (Yellow)"
        else:
            triage = "Routine (Green)"

        save_vitals = st.button("Commit Vitals & Triage Status", type="primary", use_container_width=True)

    with col_status:
        st.subheader("Automated Clinical Assessment")
        
        # Display BMI Card
        st.markdown(f"**Computed Body Mass Index (BMI):** `{bmi} kg/m²`")
        if bmi < 18.5:
            st.info("BMI Category: Underweight")
        elif 18.5 <= bmi < 25.0:
            st.success("BMI Category: Normal / Healthy Weight")
        elif 25.0 <= bmi < 30.0:
            st.warning("BMI Category: Overweight")
        else:
            st.error("BMI Category: Class I / II Obesity")

        st.divider()

        # Display Triage Badge
        st.markdown(f"**Automated Triage Category:**")
        if triage == "Emergency (Red)":
            st.markdown("<div class='triage-red'>🚨 EMERGENCY (RED): Severe Hypertension or Pyrexia detected. Direct immediately to Resuscitation/Acute OPD.</div>", unsafe_allow_html=True)
        elif triage == "Priority (Yellow)":
            st.markdown("<div class='triage-yellow'>⚠️ PRIORITY (YELLOW): Stage 1/2 Hypertension or Mild Fever. Route to Doctor Priority Queue.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='triage-green'>✅ ROUTINE (GREEN): Stable physiological baseline. Normal outpatient consultation queue.</div>", unsafe_allow_html=True)

        if save_vitals:
            conn = get_connection()
            cur = conn.cursor()
            recorded_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            cur.execute("""
            INSERT INTO vitals (patient_id, blood_pressure_sys, blood_pressure_dia, pulse_rate, temperature_c, weight_kg, height_cm, bmi, triage_category, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (selected_patient_id, sys_bp, dia_bp, pulse, temp, weight, height, bmi, triage, recorded_time))
            conn.commit()
            conn.close()
            st.success(f"Vitals successfully saved for patient ID {selected_patient_id}!")

# -----------------------------------------------------------------------------
# 4. DOCTOR CONSULTATION & DIAGNOSIS
# -----------------------------------------------------------------------------
elif menu == "👨‍⚕️ Doctor Consultation & Diagnosis":
    st.markdown("<h1 class='main-header'>👨‍⚕️ Clinical Consultation & Physician Encounter</h1>", unsafe_allow_html=True)
    st.caption("Electronic Health Record (EHR) review, clinical diagnosis entry, and e-prescription issuance.")

    conn = get_connection()
    df_pts = pd.read_sql_query("SELECT patient_id, patient_code, full_name, age, gender, blood_group, genotype FROM patients", conn)
    conn.close()

    patient_options = {f"{row['patient_code']} - {row['full_name']}": row for _, row in df_pts.iterrows()}
    selected_label = st.selectbox("Select Patient for Clinical Encounter", list(patient_options.keys()))
    patient_info = patient_options[selected_label]

    # Show patient banner
    st.info(f"**Patient Code:** {patient_info['patient_code']} | **Name:** {patient_info['full_name']} | **Age:** {patient_info['age']} yrs | **Sex:** {patient_info['gender']} | **Blood:** {patient_info['blood_group']} | **Genotype:** {patient_info['genotype']}")

    with st.form("consultation_form"):
        doctor_name = st.selectbox("Attending Physician", [
            "Dr. Harry Attieku-Boateng (Internal Medicine)",
            "Dr. Emmanuel Asante (Cardiology & Clinical AI)",
            "Dr. Beatrice Nkrumah (General OPD)",
            "Dr. Joseph Danquah (Pediatrics)",
            "Dr. Cynthia Opoku (Obstetrics/Gynecology)"
        ])

        symptoms = st.text_area("Chief Complaints & Presenting Symptoms", placeholder="e.g. Throbbing frontal headache, blurred vision, palpitations for 3 days...")
        diagnosis = st.text_input("Definitive / Working Clinical Diagnosis", placeholder="e.g. Stage 2 Essential Hypertension with Cardiovascular Risk")
        prescription = st.text_area("Pharmacological Prescription (Rx)", placeholder="e.g. 1. Amlodipine 10mg PO OD x 30 days\n2. Losartan 50mg PO OD x 30 days")
        labs = st.text_input("Diagnostic Investigations / Lab Orders", placeholder="e.g. Lipid Profile, Fasting Blood Sugar, 12-lead ECG")
        clinical_notes = st.text_area("Physician Clinical Notes & Review Timeline", placeholder="e.g. Patient advised on low-sodium dietary regimen. Review BP in 14 days.")

        finish_consultation = st.form_submit_button("Sign & Complete Encounter", type="primary", use_container_width=True)

    if finish_consultation:
        if not diagnosis.strip():
            st.error("Please enter a working clinical diagnosis before signing.")
        else:
            conn = get_connection()
            cur = conn.cursor()
            c_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            cur.execute("""
            INSERT INTO consultations (patient_id, doctor_name, symptoms, diagnosis, prescription, lab_requests, clinical_notes, consultation_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (int(patient_info['patient_id']), doctor_name, symptoms, diagnosis, prescription, labs, clinical_notes, c_time))
            
            # Automatically generate consultation bill
            cur.execute("""
            INSERT INTO billing (patient_id, service_description, gross_amount_ghs, nhis_covered_ghs, net_payable_ghs, payment_status, billing_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (int(patient_info['patient_id']), f"Specialist Consultation - {doctor_name.split('(')[0].strip()}", 200.0, 140.0, 60.0, "Pending", c_time))

            conn.commit()
            conn.close()
            st.success(f"Encounter successfully logged for **{patient_info['full_name']}**. Bill forwarded to Accounts/Billing.")

# -----------------------------------------------------------------------------
# 5. OUTPATIENT APPOINTMENTS
# -----------------------------------------------------------------------------
elif menu == "📅 Outpatient Appointments":
    st.markdown("<h1 class='main-header'>📅 Outpatient Appointment Management</h1>", unsafe_allow_html=True)
    st.caption("Coordinate specialist clinics, outpatient queues, and follow-up schedules.")

    conn = get_connection()
    df_pts = pd.read_sql_query("SELECT patient_id, patient_code, full_name FROM patients", conn)
    df_appts = pd.read_sql_query("""
    SELECT a.appointment_id, p.patient_code, p.full_name, a.doctor_name, a.department, a.appointment_date, a.appointment_time, a.status, a.reason
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    ORDER BY a.appointment_date DESC
    """, conn)
    conn.close()

    tab_book, tab_roster = st.tabs(["📝 Book Appointment", "📋 Master Clinic Roster"])

    with tab_book:
        patient_options = {f"{row['patient_code']} - {row['full_name']}": row['patient_id'] for _, row in df_pts.iterrows()}
        with st.form("book_appt_form"):
            pt_choice = st.selectbox("Patient", list(patient_options.keys()))
            pt_id = patient_options[pt_choice]

            col_doc, col_dept = st.columns(2)
            with col_doc:
                doc = st.selectbox("Consultant", ["Dr. Harry Attieku-Boateng", "Dr. Emmanuel Asante", "Dr. Beatrice Nkrumah", "Dr. Joseph Danquah", "Dr. Cynthia Opoku"])
            with col_dept:
                dept = st.selectbox("Department", ["Internal Medicine", "Cardiology Clinic", "General OPD", "Pediatrics Unit", "Obstetrics & Gynecology"])

            col_dt, col_tm = st.columns(2)
            with col_dt:
                appt_d = st.date_input("Scheduled Date")
            with col_tm:
                appt_t = st.time_input("Scheduled Time")

            reason = st.text_input("Visit Purpose / Clinical Indication", "Specialist Follow-up & Review")
            submit_appt = st.form_submit_button("Confirm Booking", type="primary", use_container_width=True)

        if submit_appt:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO appointments (patient_id, doctor_name, department, appointment_date, appointment_time, status, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (pt_id, doc, dept, str(appt_d), str(appt_t)[:5], "Scheduled", reason))
            conn.commit()
            conn.close()
            st.success(f"Appointment confirmed with **{doc}** for **{appt_d}** at **{str(appt_t)[:5]}**.")

    with tab_roster:
        st.subheader("Upcoming Outpatient Clinics")
        st.dataframe(df_appts.rename(columns={
            "patient_code": "Code", "full_name": "Patient Name", "doctor_name": "Consultant",
            "department": "Department", "appointment_date": "Date", "appointment_time": "Time",
            "status": "Status", "reason": "Reason"
        }), use_container_width=True)

# -----------------------------------------------------------------------------
# 6. BILLING & NHIS CLAIMS
# -----------------------------------------------------------------------------
elif menu == "💳 Billing & NHIS Claims":
    st.markdown("<h1 class='main-header'>💳 Revenue, Billing & NHIS Claims Management</h1>", unsafe_allow_html=True)
    st.caption("Manage patient medical invoices, National Health Insurance Scheme (NHIS) claims, and payments.")

    conn = get_connection()
    df_billing = pd.read_sql_query("""
    SELECT b.bill_id, p.patient_code, p.full_name, p.nhis_number, b.service_description, b.gross_amount_ghs, b.nhis_covered_ghs, b.net_payable_ghs, b.payment_status, b.billing_date
    FROM billing b
    JOIN patients p ON b.patient_id = p.patient_id
    ORDER BY b.bill_id DESC
    """, conn)
    conn.close()

    # Metric summaries
    gross_total = df_billing["gross_amount_ghs"].sum()
    nhis_total = df_billing["nhis_covered_ghs"].sum()
    copay_total = df_billing["net_payable_ghs"].sum()
    paid_count = len(df_billing[df_billing["payment_status"] == "Paid"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Gross Billings", f"GHS {gross_total:,.2f}")
    m2.metric("NHIS Subsidies Claimed", f"GHS {nhis_total:,.2f}", "70% Coverage")
    m3.metric("Patient Out-of-Pocket", f"GHS {copay_total:,.2f}", "Copay Total")
    m4.metric("Settled Bills", f"{paid_count} of {len(df_billing)}", "Completed Claims")

    st.divider()
    st.subheader("Billing Ledger & Claims Audit")
    st.dataframe(df_billing.rename(columns={
        "bill_id": "Bill #", "patient_code": "Code", "full_name": "Patient Name",
        "nhis_number": "NHIS Card #", "service_description": "Care Bundle",
        "gross_amount_ghs": "Gross (GHS)", "nhis_covered_ghs": "NHIS (GHS)",
        "net_payable_ghs": "Patient Copay (GHS)", "payment_status": "Status",
        "billing_date": "Invoice Date"
    }), use_container_width=True)

# -----------------------------------------------------------------------------
# 7. SYSTEM ARCHITECTURE & DOCS
# -----------------------------------------------------------------------------
elif menu == "📑 System Architecture & Docs":
    st.markdown("<h1 class='main-header'>📑 System Architecture & Academic Specification</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    ### Course Information & Academic Credits
    * **Student Name:** Emmanuel Siaw Asante
    * **Student ID / Index:** `PYT230047`
    * **Course Instructor:** Mr. Harry Attieku-Boateng
    * **Institution:** Pentecost University (Faculty of Computing & Information Technology)
    * **Course Assessment:** Assignment 2 (Hospital Management System)
    
    ### Architectural Highlights
    1. **Integrated 3-Tier Web Architecture:** Built using Streamlit for dynamic frontend rendering, Python for business and triage rules, and a relational SQLite database with foreign-key referential integrity.
    2. **Ghana NHIS Integration Engine:** Implements the National Health Insurance Scheme copay formula, calculating 70% state medical subsidy coverage and generating patient copay invoices.
    3. **Automated Clinical Triage:** Dynamically calculates WHO-standard Body Mass Index (BMI) and assigns color-coded triage urgency (Emergency/Red, Priority/Yellow, Routine/Green) based on blood pressure thresholds and thermal readings.
    4. **Source Control Compliance:** Full source tracked under Git and pushed to GitHub with clean modular separation (`database/`, `app.py`, `init_db.py`, `requirements.txt`).
    """)
