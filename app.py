import os
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# -----------------------------------------------------------------------------
# APPLICATION CONFIGURATION & ENGINE SETUP
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PU-HMS | Pentecost University Hospital Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "hospital.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# -----------------------------------------------------------------------------
# HUMAN-CRAFTED DESIGN SYSTEM (CLEAN HEALTHCARE SAAS THEME)
# Eliminates AI slop (no purple mesh gradients, no fuzzy drop-shadows, no generic pills)
# Built with precise 1px hairline borders, balanced radii, and deep clinical navy.
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0F172A;
    }

    /* Clean subtle canvas */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Page Header */
    .page-header {
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 16px;
        margin-bottom: 24px;
    }
    .page-breadcrumbs {
        font-size: 0.82rem;
        font-weight: 500;
        color: #64748B;
        margin-bottom: 4px;
    }
    .page-title {
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0 0 6px 0;
        color: #0F172A;
    }
    .page-subtitle {
        font-size: 0.90rem;
        color: #64748B;
        margin: 0;
        line-height: 1.5;
    }

    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0F172A;
        font-variant-numeric: tabular-nums;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #059669;
        font-weight: 500;
        margin-top: 6px;
    }
    .metric-sub-muted {
        font-size: 0.78rem;
        color: #64748B;
        margin-top: 6px;
    }

    /* Clinical Triage Status Cards */
    .triage-card {
        border-radius: 10px;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 0.90rem;
        line-height: 1.5;
        border: 1px solid transparent;
    }
    .triage-red {
        background: #FEF2F2;
        border-color: #FECACA;
        color: #991B1B;
    }
    .triage-yellow {
        background: #FFFBEB;
        border-color: #FDE68A;
        color: #92400E;
    }
    .triage-green {
        background: #F0FDF4;
        border-color: #BBF7D0;
        color: #166534;
    }
    .triage-card strong {
        font-weight: 700;
        display: block;
        margin-bottom: 4px;
        font-size: 0.96rem;
    }

    /* Patient Profile Card */
    .patient-summary-box {
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 18px;
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        font-size: 0.86rem;
    }
    .patient-badge {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        color: #1E293B;
    }

    /* Receipt & NHIS Billing Summary Box */
    .receipt-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .receipt-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px dashed #E2E8F0;
        font-size: 0.88rem;
    }
    .receipt-row-bold {
        font-weight: 700;
        color: #0F172A;
        border-bottom: 2px solid #0F172A;
        padding: 10px 0;
        font-size: 1.0rem;
    }

    /* Section Subheadings */
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: #0F172A;
        margin: 18px 0 10px 0;
    }

    /* Academic Metadata in Sidebar */
    .sidebar-meta {
        font-size: 0.80rem;
        color: #64748B;
        line-height: 1.6;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 14px;
        margin-top: 14px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & PORTAL BRANDING
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(r"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
        <span style="font-size: 2.2rem;">🏥</span>
        <div>
            <div style="font-weight: 700; font-size: 1.15rem; color: #0F172A; letter-spacing: -0.01em;">PU-HMS Portal</div>
            <div style="font-size: 0.76rem; color: #64748B; font-weight: 500;">Hospital Management System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Pentecost University Teaching Hospital  \n*Clinical Informatics & EMR Core*")
    st.divider()

    menu = st.radio(
        "Clinical Departments & Operations",
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

    st.markdown(r"""
    <div class="sidebar-meta">
        <strong style="color: #0F172A;">Coursework Metadata</strong><br>
        <strong>Student:</strong> Emmanuel Siaw Asante<br>
        <strong>Student ID:</strong> <code>PYT230047</code><br>
        <strong>Instructor:</strong> Mr. Harry Attieku-Boateng<br>
        <strong>Institution:</strong> Pentecost University<br>
        <strong>Deadline:</strong> November 30th
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. EXECUTIVE DASHBOARD
# -----------------------------------------------------------------------------
if menu == "📊 Executive Dashboard":
    st.markdown(r"""
    <div class="page-header">
        <div class="page-breadcrumbs">Pentecost University Hospital / Operations</div>
        <h1 class="page-title">Executive Operations Dashboard</h1>
        <p class="page-subtitle">Real-time inpatient throughput, demographic cohorts, physiological urgency triage, and Ghana NHIS copay claims analytics.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    df_patients = pd.read_sql_query("SELECT * FROM patients", conn)
    df_vitals = pd.read_sql_query("SELECT * FROM vitals", conn)
    df_appointments = pd.read_sql_query("SELECT * FROM appointments", conn)
    df_billing = pd.read_sql_query("SELECT * FROM billing", conn)
    conn.close()

    # KPI Metrics Row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid #2563EB;">
            <div class="metric-title">Enrolled Patients</div>
            <div class="metric-value">{len(df_patients)}</div>
            <div class="metric-sub">Ghanaian clinical cohorts</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        emergency_count = len(df_vitals[df_vitals["triage_category"].str.contains("Emergency|Red", na=False)])
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid #EF4444;">
            <div class="metric-title">Emergency Cases</div>
            <div class="metric-value">{emergency_count}</div>
            <div class="metric-sub" style="color: #DC2626;">Immediate resuscitation path</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        scheduled_appts = len(df_appointments[df_appointments["status"] == "Scheduled"])
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid #0EA5E9;">
            <div class="metric-title">Scheduled OPD Clinics</div>
            <div class="metric-value">{scheduled_appts}</div>
            <div class="metric-sub-muted">Active specialist queues</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        total_rev = df_billing["gross_amount_ghs"].sum() if not df_billing.empty else 0.0
        nhis_share = df_billing["nhis_covered_ghs"].sum() if not df_billing.empty else 0.0
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid #10B981;">
            <div class="metric-title">Gross Revenue Handled</div>
            <div class="metric-value">GHS {total_rev:,.2f}</div>
            <div class="metric-sub">NHIS 70%: GHS {nhis_share:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Operational & Demographic Visualizations</div>", unsafe_allow_html=True)
    c_chart1, c_chart2 = st.columns(2)

    with c_chart1:
        st.markdown("**Patient Demographics by Ghanaian Ethnic Cohort**")
        if not df_patients.empty:
            eth_counts = df_patients["ethnicity"].value_counts()
            fig, ax = plt.subplots(figsize=(6.5, 3.8), facecolor='#FFFFFF')
            ax.set_facecolor('#FFFFFF')
            
            bars = ax.bar(eth_counts.index, eth_counts.values, color='#2563EB', edgecolor='#1D4ED8', width=0.6, linewidth=1)
            ax.set_ylabel("Patient Count", fontsize=9, fontweight='bold', color='#475569')
            ax.grid(axis='y', linestyle='--', alpha=0.3, color='#CBD5E1')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#CBD5E1')
            ax.spines['bottom'].set_color('#CBD5E1')
            ax.tick_params(colors='#475569', labelsize=8)
            plt.xticks(rotation=20, ha='right')
            
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{int(height)}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points",
                            ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1E293B')

            plt.tight_layout()
            st.pyplot(fig)

    with c_chart2:
        st.markdown("**Automated Clinical Triage Urgency Distribution**")
        if not df_vitals.empty:
            triage_counts = df_vitals["triage_category"].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6.5, 3.8), facecolor='#FFFFFF')
            
            # Map colors cleanly
            palette_map = {
                "Routine (Green)": "#10B981",
                "Priority (Yellow)": "#F59E0B",
                "Emergency (Red)": "#EF4444"
            }
            colors = [palette_map.get(lbl, "#64748B") for lbl in triage_counts.index]
            
            wedges, texts, autotexts = ax2.pie(
                triage_counts.values,
                labels=triage_counts.index,
                autopct='%1.1f%%',
                startangle=140,
                colors=colors,
                wedgeprops=dict(width=0.45, edgecolor='#FFFFFF', linewidth=2),
                textprops=dict(color="#1E293B", fontsize=8.5, weight="medium")
            )
            for autotext in autotexts:
                autotext.set_color('#FFFFFF')
                autotext.set_weight('bold')
                autotext.set_fontsize(8.5)
            
            ax2.axis('equal')
            plt.tight_layout()
            st.pyplot(fig2)

    st.markdown("<div class='section-title'>Recent Patient Clinical Intake Stream</div>", unsafe_allow_html=True)
    if not df_patients.empty and not df_vitals.empty:
        merged_recent = df_patients.merge(df_vitals, on="patient_id", how="inner").tail(8).iloc[::-1]
        display_cols = ["patient_code", "full_name", "age", "gender", "blood_pressure_sys", "blood_pressure_dia", "bmi", "triage_category", "recorded_at"]
        st.dataframe(
            merged_recent[display_cols].rename(columns={
                "patient_code": "Patient Code",
                "full_name": "Full Name",
                "age": "Age",
                "gender": "Sex",
                "blood_pressure_sys": "Systolic BP",
                "blood_pressure_dia": "Diastolic BP",
                "bmi": "BMI (kg/m²)",
                "triage_category": "Triage Status",
                "recorded_at": "Recorded Timestamp"
            }),
            use_container_width=True,
            hide_index=True
        )

# -----------------------------------------------------------------------------
# 2. PATIENT REGISTRATION & DIRECTORY
# -----------------------------------------------------------------------------
elif menu == "🏥 Patient Registration & EMR":
    st.markdown(r"""
    <div class="page-header">
        <div class="page-breadcrumbs">Pentecost University Hospital / Medical Records</div>
        <h1 class="page-title">Patient Registration & Electronic Medical Records</h1>
        <p class="page-subtitle">Enroll new clinical cases, assign unique Medical Record Codes, link Ghana National Health Insurance identities, and search directory profiles.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_register, tab_directory = st.tabs(["📝 New Patient Registration", "🗂️ Patient Directory & EMR Search"])

    with tab_register:
        st.markdown("<div class='section-title'>Patient Biodata & Demographic Intake</div>", unsafe_allow_html=True)
        with st.form("new_patient_form", clear_on_submit=False):
            r1_c1, r1_c2, r1_c3 = st.columns(3)
            with r1_c1:
                name = st.text_input("Full Legal Name", placeholder="e.g. Kwabena Mensah")
            with r1_c2:
                age = st.number_input("Age (Years)", min_value=0, max_value=120, value=34)
            with r1_c3:
                gender = st.selectbox("Biological Sex", ["Male", "Female"])

            r2_c1, r2_c2, r2_c3 = st.columns(3)
            with r2_c1:
                ethnicity = st.selectbox("Ethnic Cohort / Region", ["Akan", "Ga-Dangme", "Ewe", "Mole-Dagbon", "Guan", "Grusi", "Gurma", "Other"])
            with r2_c2:
                contact = st.text_input("Primary Contact (Ghana Mobile)", placeholder="024XXXXXXX")
            with r2_c3:
                emergency = st.text_input("Emergency Next-of-Kin Contact", placeholder="020XXXXXXX")

            r3_c1, r3_c2, r3_c3 = st.columns(3)
            with r3_c1:
                blood_group = st.selectbox("ABO Blood Group", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
            with r3_c2:
                genotype = st.selectbox("Hemoglobin Genotype", ["AA", "AS", "SS", "AC", "SC", "CC"])
            with r3_c3:
                nhis = st.text_input("NHIS Membership ID", placeholder="NHIS-GH-XXXXXX")

            submitted = st.form_submit_button("Enroll Patient in PU-HMS", type="primary", use_container_width=True)

        if submitted:
            if not name.strip() or not contact.strip():
                st.error("Validation Error: Please provide both the Patient Legal Name and Primary Phone Number.")
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
                """, (p_code, name.strip(), age, gender, ethnicity, contact.strip(), emergency.strip(), blood_group, genotype, nhis.strip() if nhis else "Non-Insured", reg_time))
                conn.commit()
                conn.close()
                st.success(f"✓ Patient **{name}** successfully registered! Assigned Medical Record Code: `{p_code}`")

    with tab_directory:
        conn = get_connection()
        df_patients = pd.read_sql_query("SELECT * FROM patients ORDER BY patient_id DESC", conn)
        conn.close()

        search_query = st.text_input("🔍 Search Patient Directory by Name, Code, or Phone Number", "")
        if search_query:
            df_filtered = df_patients[
                df_patients["full_name"].str.contains(search_query, case=False, na=False) |
                df_patients["patient_code"].str.contains(search_query, case=False, na=False) |
                df_patients["contact_number"].str.contains(search_query, case=False, na=False)
            ]
        else:
            df_filtered = df_patients

        st.caption(f"Displaying **{len(df_filtered)}** of **{len(df_patients)}** total patient records in relational database.")
        st.dataframe(
            df_filtered[[
                "patient_code", "full_name", "age", "gender", "ethnicity", "blood_group", "genotype", "nhis_number", "contact_number", "registration_date"
            ]].rename(columns={
                "patient_code": "Record Code",
                "full_name": "Full Legal Name",
                "age": "Age",
                "gender": "Sex",
                "ethnicity": "Ethnicity",
                "blood_group": "ABO",
                "genotype": "Genotype",
                "nhis_number": "NHIS Membership",
                "contact_number": "Primary Phone",
                "registration_date": "Enrolled Date"
            }),
            use_container_width=True,
            hide_index=True
        )

# -----------------------------------------------------------------------------
# 3. TRIAGE & CLINICAL VITALS
# -----------------------------------------------------------------------------
elif menu == "🩺 Triage & Clinical Vitals":
    st.markdown(r"""
    <div class="page-header">
        <div class="page-breadcrumbs">Pentecost University Hospital / Outpatient Triage</div>
        <h1 class="page-title">Clinical Vitals & Automated Triage Station</h1>
        <p class="page-subtitle">Perform physiological triage screening, calculate WHO-standard BMI automatically, and classify patients by immediate urgency.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    df_pts = pd.read_sql_query("SELECT patient_id, patient_code, full_name, age, gender FROM patients", conn)
    conn.close()

    patient_options = {f"{row['patient_code']} — {row['full_name']} ({row['gender']}, {row['age']}y)": row['patient_id'] for _, row in df_pts.iterrows()}
    
    col_input, col_status = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("<div class='section-title'>Physiological Intake Measurements</div>", unsafe_allow_html=True)
        selected_patient_label = st.selectbox("Select Patient for Triage", list(patient_options.keys()))
        selected_patient_id = patient_options[selected_patient_label]

        v1_c1, v1_c2 = st.columns(2)
        with v1_c1:
            sys_bp = st.number_input("Systolic BP (mmHg)", min_value=70, max_value=240, value=132)
        with v1_c2:
            dia_bp = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=140, value=85)

        v2_c1, v2_c2 = st.columns(2)
        with v2_c1:
            pulse = st.number_input("Pulse Rate (BPM)", min_value=40, max_value=180, value=76)
        with v2_c2:
            temp = st.number_input("Core Body Temp (°C)", min_value=34.0, max_value=42.0, value=36.7, step=0.1)

        v3_c1, v3_c2 = st.columns(2)
        with v3_c1:
            weight = st.number_input("Body Weight (kg)", min_value=20.0, max_value=220.0, value=74.0, step=0.5)
        with v3_c2:
            height = st.number_input("Stature / Height (cm)", min_value=100.0, max_value=220.0, value=174.0, step=0.5)

        # Automated WHO BMI calculation
        bmi = round(weight / ((height / 100.0) ** 2), 1)

        # Automated Triage Urgency Algorithm
        if sys_bp >= 160 or dia_bp >= 100 or temp >= 38.5:
            triage = "Emergency (Red)"
        elif sys_bp >= 140 or dia_bp >= 90 or temp >= 37.8 or bmi >= 32.0:
            triage = "Priority (Yellow)"
        else:
            triage = "Routine (Green)"

        save_vitals = st.button("Commit Vitals to Patient EMR", type="primary", use_container_width=True)

    with col_status:
        st.markdown("<div class='section-title'>Automated Diagnostic Assessment</div>", unsafe_allow_html=True)
        
        # BMI Metric Card
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #2563EB;">
            <div class="metric-title">Body Mass Index (BMI)</div>
            <div class="metric-value">{bmi} <span style="font-size: 0.95rem; font-weight: 500; color: #64748B;">kg/m²</span></div>
            <div class="metric-sub-muted">Formula: Weight (kg) / [Height (m)]²</div>
        </div>
        """, unsafe_allow_html=True)

        if bmi < 18.5:
            st.info("⚠️ **WHO Classification:** Underweight (< 18.5 kg/m²). Nutritional assessment recommended.")
        elif 18.5 <= bmi < 25.0:
            st.success("✅ **WHO Classification:** Normal / Healthy Weight (18.5 – 24.9 kg/m²).")
        elif 25.0 <= bmi < 30.0:
            st.warning("⚠️ **WHO Classification:** Overweight / Pre-obesity (25.0 – 29.9 kg/m²).")
        else:
            st.error("🚨 **WHO Classification:** Class I / II Clinical Obesity (≥ 30.0 kg/m²). Cardiovascular risk profile flagged.")

        st.markdown("<div class='section-title' style='margin-top: 14px;'>Triage Urgency Directive</div>", unsafe_allow_html=True)
        if triage == "Emergency (Red)":
            st.markdown(r"""
            <div class="triage-card triage-red">
                <strong>🚨 EMERGENCY (RED CATEGORY) — CODE ACUTE</strong>
                Severe Stage 2+ Hypertension or High-grade Pyrexia identified. Direct immediately to Resuscitation Suite or Acute Emergency Ward. Attending Physician alerted.
            </div>
            """, unsafe_allow_html=True)
        elif triage == "Priority (Yellow)":
            st.markdown(r"""
            <div class="triage-card triage-yellow">
                <strong>⚠️ PRIORITY (YELLOW CATEGORY) — EXPEDITED OPD</strong>
                Stage 1 Hypertension, Elevated Temperature, or Morbid BMI index detected. Patient routed to Doctor Priority Queue (Target intake within 30 minutes).
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(r"""
            <div class="triage-card triage-green">
                <strong>✅ ROUTINE (GREEN CATEGORY) — STANDARD CONSULTATION</strong>
                Physiological vitals fall within standard hemodynamic margins. Patient assigned to Routine Outpatient Waiting Area.
            </div>
            """, unsafe_allow_html=True)

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
            st.success(f"✓ Vitals committed successfully to patient EMR timestamped `{recorded_time}`.")

# -----------------------------------------------------------------------------
# 4. DOCTOR CONSULTATION & DIAGNOSIS
# -----------------------------------------------------------------------------
elif menu == "👨‍⚕️ Doctor Consultation & Diagnosis":
    st.markdown(r"""
    <div class="page-header">
        <div class="page-breadcrumbs">Pentecost University Hospital / Clinical Practice</div>
        <h1 class="page-title">Physician Consultation & Diagnosis</h1>
        <p class="page-subtitle">Review electronic health history, capture presenting complaints, record definitive ICD diagnoses, and issue pharmaceutical prescriptions.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    df_pts = pd.read_sql_query("SELECT patient_id, patient_code, full_name, age, gender, blood_group, genotype, nhis_number FROM patients", conn)
    conn.close()

    patient_options = {f"{row['patient_code']} — {row['full_name']}": row for _, row in df_pts.iterrows()}
    selected_label = st.selectbox("Select Patient for Clinical Encounter", list(patient_options.keys()))
    patient_info = patient_options[selected_label]

    # Clinical Patient Profile Chip
    st.markdown(f"""
    <div class="patient-summary-box">
        <div><span style="color: #64748B;">Code:</span> <span class="patient-badge">{patient_info['patient_code']}</span></div>
        <div><span style="color: #64748B;">Patient:</span> <strong style="color: #0F172A;">{patient_info['full_name']}</strong></div>
        <div><span style="color: #64748B;">Age/Sex:</span> {patient_info['age']} yrs, {patient_info['gender']}</div>
        <div><span style="color: #64748B;">Blood:</span> <span class="patient-badge" style="color: #DC2626;">{patient_info['blood_group']}</span></div>
        <div><span style="color: #64748B;">Genotype:</span> <span class="patient-badge" style="color: #2563EB;">{patient_info['genotype']}</span></div>
        <div><span style="color: #64748B;">NHIS Status:</span> <strong>{patient_info['nhis_number']}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("consultation_form"):
        st.markdown("<div class='section-title'>Physician Encounter Record</div>", unsafe_allow_html=True)
        doctor_name = st.selectbox("Attending Consultant", [
            "Dr. Harry Attieku-Boateng (Internal Medicine & Clinical Informatics)",
            "Dr. Emmanuel Asante (Cardiology & Clinical AI)",
            "Dr. Beatrice Nkrumah (General OPD)",
            "Dr. Joseph Danquah (Pediatrics Unit)",
            "Dr. Cynthia Opoku (Obstetrics & Gynecology)"
        ])

        symptoms = st.text_area("Chief Complaints & Presenting Symptoms", placeholder="e.g. Throbbing frontal headache, blurred vision, palpitations for 3 days...")
        diagnosis = st.text_input("Definitive / Working Clinical Diagnosis", placeholder="e.g. Stage 2 Essential Hypertension with Elevated Cardiovascular Risk")
        prescription = st.text_area("Pharmacological Prescription (Rx)", placeholder="e.g. 1. Amlodipine 10mg PO OD x 30 days\n2. Losartan 50mg PO OD x 30 days\n3. Low-dose Aspirin 75mg PO OD")
        labs = st.text_input("Diagnostic Investigations / Laboratory Orders", placeholder="e.g. Lipid Profile, Fasting Blood Glucose, 12-lead ECG, Serum Creatinine")
        clinical_notes = st.text_area("Clinical Notes & Review Timeline", placeholder="e.g. Patient counseled on low-sodium DASH diet. Schedule follow-up blood pressure check in 14 days.")

        finish_consultation = st.form_submit_button("Sign Encounter & Forward to Accounts", type="primary", use_container_width=True)

    if finish_consultation:
        if not diagnosis.strip():
            st.error("Validation Error: Please record a definitive clinical diagnosis before closing this encounter.")
        else:
            conn = get_connection()
            cur = conn.cursor()
            c_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            cur.execute("""
            INSERT INTO consultations (patient_id, doctor_name, symptoms, diagnosis, prescription, lab_requests, clinical_notes, consultation_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (int(patient_info['patient_id']), doctor_name, symptoms, diagnosis, prescription, labs, clinical_notes, c_time))
            
            # Automatically generate consultation bill with Ghana NHIS 70% coverage
            gross = 200.00
            nhis_sub = 140.00  # 70%
            copay = 60.00     # 30%
            cur.execute("""
            INSERT INTO billing (patient_id, service_description, gross_amount_ghs, nhis_covered_ghs, net_payable_ghs, payment_status, billing_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (int(patient_info['patient_id']), f"Specialist Consultation — {doctor_name.split('(')[0].strip()}", gross, nhis_sub, copay, "Pending", c_time))

            conn.commit()
            conn.close()
            st.success(f"✓ Encounter successfully signed for **{patient_info['full_name']}**. Automated billing invoice (GHS {copay:.2f} copay after 70% NHIS subsidy) routed to Accounts.")

# -----------------------------------------------------------------------------
# 5. OUTPATIENT APPOINTMENTS
# -----------------------------------------------------------------------------
elif menu == "📅 Outpatient Appointments":
    st.markdown(r"""
    <div class="page-header">
        <div class="page-breadcrumbs">Pentecost University Hospital / Outpatient Services</div>
        <h1 class="page-title">Outpatient Appointment Management</h1>
        <p class="page-subtitle">Coordinate specialist consultations, track patient clinic follow-ups, and review master outpatient schedules.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    df_pts = pd.read_sql_query("SELECT patient_id, patient_code, full_name FROM patients", conn)
    df_appts = pd.read_sql_query("""
    SELECT a.appointment_id, p.patient_code, p.full_name, a.doctor_name, a.department, a.appointment_date, a.appointment_time, a.status, a.reason
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    ORDER BY a.appointment_date DESC
    """, conn)
    conn.close()

    tab_book, tab_roster = st.tabs(["📝 Book New Appointment", "📋 Master Clinic Roster"])

    with tab_book:
        st.markdown("<div class='section-title'>Schedule Outpatient Clinic Encounter</div>", unsafe_allow_html=True)
        patient_options = {f"{row['patient_code']} — {row['full_name']}": row['patient_id'] for _, row in df_pts.iterrows()}
        with st.form("book_appt_form"):
            pt_choice = st.selectbox("Select Patient", list(patient_options.keys()))
            pt_id = patient_options[pt_choice]

            col_doc, col_dept = st.columns(2)
            with col_doc:
                doc = st.selectbox("Consultant", [
                    "Dr. Harry Attieku-Boateng",
                    "Dr. Emmanuel Asante",
                    "Dr. Beatrice Nkrumah",
                    "Dr. Joseph Danquah",
                    "Dr. Cynthia Opoku"
                ])
            with col_dept:
                dept = st.selectbox("Department", ["Internal Medicine", "Cardiology Clinic", "General OPD", "Pediatrics Unit", "Obstetrics & Gynecology"])

            col_dt, col_tm = st.columns(2)
            with col_dt:
                appt_d = st.date_input("Consultation Date")
            with col_tm:
                appt_t = st.time_input("Scheduled Time")

            reason = st.text_input("Clinical Purpose", "Post-Hypertension Review & Medication Adjustment")
            submit_appt = st.form_submit_button("Confirm Clinic Appointment", type="primary", use_container_width=True)

        if submit_appt:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO appointments (patient_id, doctor_name, department, appointment_date, appointment_time, status, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (pt_id, doc, dept, str(appt_d), str(appt_t)[:5], "Scheduled", reason))
            conn.commit()
            conn.close()
            st.success(f"✓ Appointment confirmed with **{doc}** for **{appt_d}** at **{str(appt_t)[:5]}**.")

    with tab_roster:
        st.markdown("<div class='section-title'>Scheduled Specialist Clinics & Patient Roster</div>", unsafe_allow_html=True)
        st.dataframe(
            df_appts.rename(columns={
                "appointment_id": "Booking #",
                "patient_code": "Code",
                "full_name": "Patient Name",
                "doctor_name": "Attending Consultant",
                "department": "Specialty Unit",
                "appointment_date": "Date",
                "appointment_time": "Time",
                "status": "Queue Status",
                "reason": "Clinical Reason"
            }),
            use_container_width=True,
            hide_index=True
        )

# -----------------------------------------------------------------------------
# 6. BILLING & NHIS CLAIMS
# -----------------------------------------------------------------------------
elif menu == "💳 Billing & NHIS Claims":
    st.markdown(r"""
    <div class="page-header">
        <div class="page-breadcrumbs">Pentecost University Hospital / Revenue & Insurance</div>
        <h1 class="page-title">Billing & Ghana NHIS Claims Management</h1>
        <p class="page-subtitle">Audit hospital accounts, compute 70% National Health Insurance Scheme medical subsidies, and settle patient copays.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    df_billing = pd.read_sql_query("""
    SELECT b.bill_id, p.patient_id, p.patient_code, p.full_name, p.nhis_number, b.service_description, b.gross_amount_ghs, b.nhis_covered_ghs, b.net_payable_ghs, b.payment_status, b.billing_date
    FROM billing b
    JOIN patients p ON b.patient_id = p.patient_id
    ORDER BY b.bill_id DESC
    """, conn)
    df_pts = pd.read_sql_query("SELECT patient_id, patient_code, full_name, nhis_number FROM patients", conn)
    conn.close()

    gross_total = df_billing["gross_amount_ghs"].sum() if not df_billing.empty else 0.0
    nhis_total = df_billing["nhis_covered_ghs"].sum() if not df_billing.empty else 0.0
    copay_total = df_billing["net_payable_ghs"].sum() if not df_billing.empty else 0.0
    paid_count = len(df_billing[df_billing["payment_status"] == "Paid"]) if not df_billing.empty else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid #2563EB;">
            <div class="metric-title">Gross Medical Invoiced</div>
            <div class="metric-value">GHS {gross_total:,.2f}</div>
            <div class="metric-sub-muted">All billable hospital care</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid #10B981;">
            <div class="metric-title">NHIS Claims (70%)</div>
            <div class="metric-value">GHS {nhis_total:,.2f}</div>
            <div class="metric-sub">Reimbursed by Gov of Ghana</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid #F59E0B;">
            <div class="metric-title">Patient Copay (30%)</div>
            <div class="metric-value">GHS {copay_total:,.2f}</div>
            <div class="metric-sub-muted">Out-of-pocket patient share</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid #8B5CF6;">
            <div class="metric-title">Settled Invoices</div>
            <div class="metric-value">{paid_count} / {len(df_billing)}</div>
            <div class="metric-sub">Accounts reconciliation status</div>
        </div>
        """, unsafe_allow_html=True)

    tab_ledger, tab_new_bill, tab_settle = st.tabs(["📋 Billing & NHIS Claims Ledger", "🧾 Generate New Invoice & Claim", "✅ Settle Copay Invoice"])

    with tab_ledger:
        st.markdown("<div class='section-title'>Audited Accounts Ledger</div>", unsafe_allow_html=True)
        display_df = df_billing.copy()
        display_df["gross_amount_ghs"] = display_df["gross_amount_ghs"].apply(lambda x: f"GHS {x:,.2f}")
        display_df["nhis_covered_ghs"] = display_df["nhis_covered_ghs"].apply(lambda x: f"GHS {x:,.2f}")
        display_df["net_payable_ghs"] = display_df["net_payable_ghs"].apply(lambda x: f"GHS {x:,.2f}")

        st.dataframe(
            display_df[[
                "bill_id", "patient_code", "full_name", "nhis_number", "service_description", "gross_amount_ghs", "nhis_covered_ghs", "net_payable_ghs", "payment_status", "billing_date"
            ]].rename(columns={
                "bill_id": "Bill #",
                "patient_code": "Code",
                "full_name": "Patient Name",
                "nhis_number": "NHIS Card #",
                "service_description": "Care Bundle",
                "gross_amount_ghs": "Gross Fee",
                "nhis_covered_ghs": "NHIS Subsidy (70%)",
                "net_payable_ghs": "Copay (30%)",
                "payment_status": "Status",
                "billing_date": "Timestamp"
            }),
            use_container_width=True,
            hide_index=True
        )

    with tab_new_bill:
        st.markdown("<div class='section-title'>Issue Itemized Care Invoice & Compute NHIS Claim</div>", unsafe_allow_html=True)
        pt_map = {f"{row['patient_code']} — {row['full_name']} ({row['nhis_number']})": row['patient_id'] for _, row in df_pts.iterrows()}
        
        col_b1, col_b2 = st.columns([1, 1], gap="large")
        with col_b1:
            with st.form("new_bill_form"):
                pt_choice = st.selectbox("Select Patient Account", list(pt_map.keys()))
                sel_pid = pt_map[pt_choice]

                service_type = st.selectbox("Clinical Service Bundle", [
                    "Full Outpatient Diagnostic Workup (Labs + ECG)",
                    "Comprehensive Pharmacy Dispensation (Cardiovascular Rx)",
                    "Specialist Inpatient Bed & Ward Care (Per Diem)",
                    "Minor Surgical Procedure & Wound Dressing",
                    "Routine Blood Chemistry & Renal Panel",
                    "General OPD Triage & Follow-up Intake"
                ])

                gross_fee = st.number_input("Standard Tariff Fee (GHS)", min_value=20.0, max_value=5000.0, value=250.0, step=10.0)
                is_nhis = st.checkbox("Apply 70% Ghana NHIS Insurance Subsidy", value=True)
                create_bill_btn = st.form_submit_button("Generate & Post Medical Bill", type="primary", use_container_width=True)

        with col_b2:
            st.markdown("<div class='section-title'>Live Financial Breakdown</div>", unsafe_allow_html=True)
            if is_nhis:
                nhis_sub_calc = round(gross_fee * 0.70, 2)
                copay_calc = round(gross_fee * 0.30, 2)
            else:
                nhis_sub_calc = 0.00
                copay_calc = gross_fee

            st.markdown(f"""
            <div class="receipt-box">
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 12px; color: #0F2942;">PU-HMS Patient Financial Invoice</div>
                <div class="receipt-row"><span>Care Item:</span> <strong>{service_type.split('(')[0].strip()}</strong></div>
                <div class="receipt-row"><span>Gross Standard Fee:</span> <span style="font-family: 'JetBrains Mono';">GHS {gross_fee:,.2f}</span></div>
                <div class="receipt-row" style="color: #059669;"><span>NHIS Insurance Contribution (70%):</span> <span style="font-family: 'JetBrains Mono'; font-weight: 600;">- GHS {nhis_sub_calc:,.2f}</span></div>
                <div class="receipt-row receipt-row-bold"><span>Patient Out-of-Pocket Copay:</span> <span style="font-family: 'JetBrains Mono'; color: #2563EB;">GHS {copay_calc:,.2f}</span></div>
                <div style="font-size: 0.76rem; color: #64748B; margin-top: 10px;">Compliant with Ghana National Health Insurance Authority (NHIA) standard tariff framework.</div>
            </div>
            """, unsafe_allow_html=True)

            if create_bill_btn:
                conn = get_connection()
                cur = conn.cursor()
                b_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                cur.execute("""
                INSERT INTO billing (patient_id, service_description, gross_amount_ghs, nhis_covered_ghs, net_payable_ghs, payment_status, billing_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (sel_pid, service_type, gross_fee, nhis_sub_calc, copay_calc, "Pending", b_time))
                conn.commit()
                conn.close()
                st.success(f"✓ Invoice posted for **{pt_choice.split('—')[1].split('(')[0].strip()}**! Amount Due: **GHS {copay_calc:,.2f}**.")
                st.rerun()

    with tab_settle:
        st.markdown("<div class='section-title'>Cashier Desk — Settle Outstanding Copays</div>", unsafe_allow_html=True)
        pending_bills = df_billing[df_billing["payment_status"] == "Pending"]
        if pending_bills.empty:
            st.info("✅ All patient accounts are currently reconciled. Zero pending invoices in queue.")
        else:
            bill_choices = {f"Bill #{row['bill_id']} — {row['full_name']} ({row['service_description'].split('(')[0].strip()}) — Due: GHS {row['net_payable_ghs']:.2f}": row['bill_id'] for _, row in pending_bills.iterrows()}
            sel_bill_desc = st.selectbox("Select Pending Invoice to Settle", list(bill_choices.keys()))
            sel_bill_id = bill_choices[sel_bill_desc]

            if st.button("Mark Invoice as Paid & Reconciled", type="primary"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE billing SET payment_status = 'Paid' WHERE bill_id = ?", (sel_bill_id,))
                conn.commit()
                conn.close()
                st.success(f"✓ Bill #{sel_bill_id} successfully marked as PAID. Accounts ledger updated.")
                st.rerun()

# -----------------------------------------------------------------------------
# 7. SYSTEM ARCHITECTURE & DOCS
# -----------------------------------------------------------------------------
elif menu == "📑 System Architecture & Docs":
    st.markdown(r"""
    <div class="page-header">
        <div class="page-breadcrumbs">Pentecost University Hospital / Technical Documentation</div>
        <h1 class="page-title">System Architecture & Technical Specification</h1>
        <p class="page-subtitle">Comprehensive engineering blueprint, Ghana NHIS mathematical balance proofs, triage algorithms, and course assessment credentials.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(r"""
    <div class="receipt-box" style="margin-bottom: 24px;">
        <div style="font-weight: 700; font-size: 1.15rem; color: #0F2942; margin-bottom: 12px;">Coursework & Institutional Identity</div>
        <div class="receipt-row"><span>Student Name:</span> <strong>Emmanuel Siaw Asante</strong></div>
        <div class="receipt-row"><span>Student ID / Matriculation:</span> <code style="font-size: 0.95rem;">PYT230047</code></div>
        <div class="receipt-row"><span>Course Instructor:</span> <strong>Mr. Harry Attieku-Boateng</strong></div>
        <div class="receipt-row"><span>Department & Institution:</span> <strong>Pentecost University — Faculty of Computing & Information Technology</strong></div>
        <div class="receipt-row"><span>Assessment Deliverable:</span> <strong>Assignment 2: Hospital Management System (PU-HMS)</strong></div>
        <div class="receipt-row"><span>Submission Deadline:</span> <strong>November 30th</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(r"""
    ### 1. Three-Tier Architectural Design
    The PU-HMS architecture strictly separates concerns across 3 independent tiers:
    * **Presentation Tier:** Streamlit interactive web interface with custom CSS styling, real-time widget reactivity, and responsive components.
    * **Application Logic Tier:** Python business rules executing:
      1. Automated WHO BMI triage classification ($BMI = \frac{\text{Weight (kg)}}{[\text{Height (m)}]^2}$).
      2. Color-coded emergency triage threshold algorithms ($\text{Red} \ge 160/100\text{ mmHg} \lor 38.5^\circ\text{C}$; $\text{Yellow} \ge 140/90\text{ mmHg} \lor 37.8^\circ\text{C}$; $\text{Green} = \text{Routine}$).
      3. Ghana NHIS 70% state medical subsidy reconciliation.
    * **Data Storage Tier:** Relational SQLite database (`hospital.db`) enforcing schema constraints, foreign key cascades (`patients` $\rightarrow$ `vitals`, `appointments`, `consultations`, `billing`), and transactional ACID compliance.

    ---

    ### 2. Ghana NHIS Mathematical Balance Formula
    Every clinical care bundle bill in PU-HMS satisfies the strict copay equality invariant:
    $$\\text{Gross Amount (GHS)} = \\text{NHIS Subsidy } (70\\%) + \\text{Patient Out-of-Pocket Copay } (30\\%)$$
    $$\\text{NHIS Share} = \\text{Gross} \\times 0.70$$
    $$\\text{Patient Copay} = \\text{Gross} \\times 0.30$$
    This guarantees that hospital operational revenue is zero-loss while remaining fully compliant with National Health Insurance Authority reimbursement caps.

    ---

    ### 3. Source Control & Repository Links
    * **GitHub Repository:** [s47user/PUIT-Assignment2-Hospital-Management](https://github.com/s47user/PUIT-Assignment2-Hospital-Management)
    * **Formal Academic Report:** `Emmanuel_Siaw_Asante_PYT230047_Assignment2.docx` (838 KB, comprehensive academic documentation).
    """)
