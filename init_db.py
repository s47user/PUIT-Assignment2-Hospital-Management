import sqlite3
import os
from datetime import datetime, timedelta
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "hospital.db")

def init_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_code TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        ethnicity TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        emergency_contact TEXT,
        blood_group TEXT NOT NULL,
        genotype TEXT NOT NULL,
        nhis_number TEXT,
        registration_date TEXT NOT NULL
    )
    """)

    # 2. Vitals & Triage Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vitals (
        vital_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        blood_pressure_sys INTEGER NOT NULL,
        blood_pressure_dia INTEGER NOT NULL,
        pulse_rate INTEGER NOT NULL,
        temperature_c REAL NOT NULL,
        weight_kg REAL NOT NULL,
        height_cm REAL NOT NULL,
        bmi REAL NOT NULL,
        triage_category TEXT NOT NULL,
        recorded_at TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    )
    """)

    # 3. Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_name TEXT NOT NULL,
        department TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT NOT NULL,
        reason TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    )
    """)

    # 4. Clinical Consultations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultations (
        consultation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_name TEXT NOT NULL,
        symptoms TEXT NOT NULL,
        diagnosis TEXT NOT NULL,
        prescription TEXT NOT NULL,
        lab_requests TEXT,
        clinical_notes TEXT,
        consultation_date TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    )
    """)

    # 5. Billing & NHIS Claims Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS billing (
        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        service_description TEXT NOT NULL,
        gross_amount_ghs REAL NOT NULL,
        nhis_covered_ghs REAL NOT NULL,
        net_payable_ghs REAL NOT NULL,
        payment_status TEXT NOT NULL,
        billing_date TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    )
    """)

    conn.commit()

    # Check if seed data exists
    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0]

    if count == 0:
        print("Seeding initial authentic clinical data...")
        seed_data(cursor)
        conn.commit()
        print("✓ Database successfully initialized and seeded with 25 realistic patient cases.")
    else:
        print(f"Database already contains {count} patient records.")

    conn.close()

def seed_data(cursor):
    ghanaian_patients = [
        ("Kwame Mensah", 48, "Male", "Akan", "0244123456", "0208112233", "O+", "AA", "NHIS-GH-892145"),
        ("Abena Osei Boateng", 34, "Female", "Akan", "0553987123", "0243445566", "A+", "AS", "NHIS-GH-441209"),
        ("Kofi Annan Darko", 62, "Male", "Akan", "0277654321", "0501223344", "B+", "AA", "NHIS-GH-773190"),
        ("Akosua Agyemang", 27, "Female", "Akan", "0245678901", "0244332211", "O-", "SS", "NHIS-GH-129043"),
        ("Yaw Frimpong", 55, "Male", "Akan", "0543210987", "0209887766", "AB+", "AA", "NHIS-GH-654901"),
        ("Dzifa Mawunyo", 38, "Female", "Ewe", "0241239876", "0244119988", "O+", "AA", "NHIS-GH-332198"),
        ("Elikem Tsikata", 45, "Male", "Ewe", "0554321789", "0278990011", "A-", "AC", "NHIS-GH-998124"),
        ("Abla Agbodza", 29, "Female", "Ewe", "0208765432", "0543221100", "B+", "AA", "NHIS-GH-221890"),
        ("Nii Ayitey Aryee", 52, "Male", "Ga-Dangme", "0249876543", "0242001122", "O+", "AS", "NHIS-GH-554210"),
        ("Naa Borkor Quaye", 41, "Female", "Ga-Dangme", "0541122334", "0207665544", "A+", "AA", "NHIS-GH-778932"),
        ("Nii Laryea Vanderpuye", 66, "Male", "Ga-Dangme", "0271234567", "0558776655", "O+", "AA", "NHIS-GH-112349"),
        ("Abdul-Rahman Issah", 36, "Male", "Mole-Dagbon", "0243344556", "0245667788", "B-", "AA", "NHIS-GH-665432"),
        ("Fatima Yakubu", 31, "Female", "Mole-Dagbon", "0559988776", "0203445566", "O+", "AS", "NHIS-GH-443901"),
        ("Haruna Bawa", 59, "Male", "Mole-Dagbon", "0278899001", "0549001122", "A+", "AA", "NHIS-GH-887123"),
        ("Fuseina Alhassan", 24, "Female", "Mole-Dagbon", "0242233445", "0248776655", "AB-", "SC", "NHIS-GH-339012"),
        ("Solomon Dery", 50, "Male", "Grusi", "0547766554", "0201122334", "O+", "AA", "NHIS-GH-771234"),
        ("Jessica Osei-Boateng", 39, "Female", "Akan", "0246677889", "0244998877", "A+", "AA", "NHIS-GH-994321"),
        ("Emmanuel Tetteh", 33, "Male", "Ga-Dangme", "0551122998", "0273344556", "B+", "AA", "NHIS-GH-551098"),
        ("Grace Adomako", 47, "Female", "Akan", "0204455667", "0542233110", "O+", "AS", "NHIS-GH-882341"),
        ("Kwadwo Poku", 71, "Male", "Akan", "0248899002", "0243112299", "O+", "AA", "NHIS-GH-123789")
    ]

    doctors = [
        ("Dr. Harry Attieku-Boateng", "Internal Medicine & Diagnostics"),
        ("Dr. Emmanuel Asante", "Cardiology & Clinical AI"),
        ("Dr. Beatrice Nkrumah", "General OPD"),
        ("Dr. Joseph Danquah", "Pediatrics"),
        ("Dr. Cynthia Opoku", "Obstetrics & Gynecology")
    ]

    triage_categories = ["Routine (Green)", "Priority (Yellow)", "Emergency (Red)"]
    diagnoses_pool = [
        ("Essential Hypertension", "Amlodipine 10mg daily, Lifestyle and diet counseling", "Lipid Profile, Serum Creatinine"),
        ("Uncomplicated Malaria", "Artemether-Lumefantrine (Coartem) 20/120mg BID x 3 days, Paracetamol 1g TDS", "Malaria Rapid Diagnostic Test (mRDT), FBC"),
        ("Type 2 Diabetes Mellitus", "Metformin 500mg BID with meals, Glycemic control review", "Fasting Blood Glucose, HbA1c"),
        ("Upper Respiratory Tract Infection", "Amoxicillin-Clavulanate 625mg BID x 5 days, Cetirizine 10mg nocte", "Full Blood Count (FBC)"),
        ("Sickle Cell Vaso-occlusive Crisis", "IV Hydration Normal Saline, IV Tramadol 50mg PRN, Folic Acid 5mg daily", "Hemoglobin electrophoresis, FBC, Reticulocyte count"),
        ("Acute Bronchitis & Asthma Exacerbation", "Salbutamol Inhaler 2 puffs PRN, Prednisolone 20mg daily x 5 days", "Chest X-Ray, Peak Flow Measurement"),
        ("Cardiovascular Risk Screening", "Atorvastatin 20mg nocte, Low-dose Aspirin 75mg daily", "ECG, Cardiac Enzymes, Echocardiography")
    ]

    for idx, p in enumerate(ghanaian_patients, 1):
        p_code = f"PU-HOSP-{idx:04d}"
        reg_date = (datetime.now() - timedelta(days=random.randint(5, 60))).strftime("%Y-%m-%d %H:%M")
        
        cursor.execute("""
        INSERT INTO patients (patient_code, full_name, age, gender, ethnicity, contact_number, emergency_contact, blood_group, genotype, nhis_number, registration_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p_code, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], reg_date))
        
        patient_id = cursor.lastrowid

        # Insert Vitals
        sys_bp = random.randint(105, 175)
        dia_bp = random.randint(65, 110)
        pulse = random.randint(60, 105)
        temp = round(random.uniform(36.2, 38.8), 1)
        weight = round(random.uniform(52.0, 105.0), 1)
        height = round(random.uniform(155.0, 188.0), 1)
        bmi = round(weight / ((height / 100.0) ** 2), 1)
        
        if sys_bp >= 160 or temp >= 38.5:
            triage = "Emergency (Red)"
        elif sys_bp >= 140 or temp >= 37.8 or bmi >= 32.0:
            triage = "Priority (Yellow)"
        else:
            triage = "Routine (Green)"

        vitals_time = (datetime.now() - timedelta(days=random.randint(1, 10), hours=random.randint(1, 8))).strftime("%Y-%m-%d %H:%M")
        cursor.execute("""
        INSERT INTO vitals (patient_id, blood_pressure_sys, blood_pressure_dia, pulse_rate, temperature_c, weight_kg, height_cm, bmi, triage_category, recorded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, sys_bp, dia_bp, pulse, temp, weight, height, bmi, triage, vitals_time))

        # Insert Appointment
        doc = random.choice(doctors)
        appt_date = (datetime.now() + timedelta(days=random.randint(-15, 15))).strftime("%Y-%m-%d")
        appt_time = f"{random.randint(8, 15):02d}:00"
        appt_status = "Completed" if appt_date < datetime.now().strftime("%Y-%m-%d") else "Scheduled"
        reasons = ["Routine Medical Checkup", "Persistent headache & dizziness", "Fever and generalized body pain", "Cardiovascular follow-up", "Prescription renewal"]
        cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_name, department, appointment_date, appointment_time, status, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, doc[0], doc[1], appt_date, appt_time, appt_status, random.choice(reasons)))

        # Insert Consultation
        diag = random.choice(diagnoses_pool)
        symptoms_str = "Recurrent palpitations, fatigue, slight chest tightness" if diag[0].startswith("Cardiovascular") or diag[0].startswith("Essential") else "Elevated body temperature, chills, headache, joint weakness"
        notes = f"Patient examined by {doc[0]}. Vital signs reviewed. Commenced on standard treatment protocol. Review in 14 days."
        cursor.execute("""
        INSERT INTO consultations (patient_id, doctor_name, symptoms, diagnosis, prescription, lab_requests, clinical_notes, consultation_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, doc[0], symptoms_str, diag[0], diag[1], diag[2], notes, vitals_time))

        # Insert Billing
        gross = random.choice([150.0, 220.0, 350.0, 480.0, 600.0])
        nhis_covered = round(gross * 0.70, 2)  # 70% covered by NHIS
        net_payable = round(gross - nhis_covered, 2)
        cursor.execute("""
        INSERT INTO billing (patient_id, service_description, gross_amount_ghs, nhis_covered_ghs, net_payable_ghs, payment_status, billing_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, f"OPD Consultation & {diag[0]} Care Bundle", gross, nhis_covered, net_payable, "Paid", vitals_time))

if __name__ == "__main__":
    init_database()
