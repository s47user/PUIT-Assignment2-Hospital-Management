import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIGS_DIR = os.path.join(BASE_DIR, "figures")
DB_PATH = os.path.join(BASE_DIR, "database", "hospital.db")
os.makedirs(FIGS_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({"font.size": 10, "figure.autolayout": True})

print("Generating Academic Diagrams for Assignment 2...")

# -----------------------------------------------------------------------------
# 1. SYSTEM ARCHITECTURE DIAGRAM
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# Layer 1: Client / Presentation
rect1 = patches.FancyBboxPatch((0.5, 7.2), 9.0, 2.2, boxstyle="round,pad=0.2", facecolor="#EBF8FF", edgecolor="#3182CE", linewidth=2)
ax.add_patch(rect1)
ax.text(5.0, 9.0, "PRESENTATION LAYER (STREAMLIT WEB & MOBILE-RESPONSIVE UI)", ha="center", va="center", fontsize=11, fontweight="bold", color="#2B6CB0")
ax.text(1.8, 7.8, "• Executive Operations\n  Dashboard & KPIs", ha="center", va="center", fontsize=9, color="#2D3748")
ax.text(4.0, 7.8, "• Patient Registration &\n  Demographics Intake", ha="center", va="center", fontsize=9, color="#2D3748")
ax.text(6.2, 7.8, "• Triage & Clinical\n  Vitals Station", ha="center", va="center", fontsize=9, color="#2D3748")
ax.text(8.3, 7.8, "• Billing & NHIS\n  Claims Module", ha="center", va="center", fontsize=9, color="#2D3748")

# Arrow 1
ax.annotate("", xy=(5.0, 6.8), xytext=(5.0, 7.2), arrowprops=dict(arrowstyle="<->", color="#4A5568", lw=2))

# Layer 2: Application Logic / Services
rect2 = patches.FancyBboxPatch((0.5, 3.8), 9.0, 2.8, boxstyle="round,pad=0.2", facecolor="#F0FFF4", edgecolor="#38A169", linewidth=2)
ax.add_patch(rect2)
ax.text(5.0, 6.2, "APPLICATION & CLINICAL LOGIC LAYER (PYTHON 3.14 SERVICES)", ha="center", va="center", fontsize=11, fontweight="bold", color="#276749")
ax.text(2.2, 4.8, "Automated Triage Engine\n(WHO BMI & Vital Signs\nHypertension / Fever Thresholds)", ha="center", va="center", fontsize=9, color="#2D3748", bbox=dict(boxstyle="square", facecolor="white", edgecolor="#CBD5E0"))
ax.text(5.0, 4.8, "EMR & Consultation Service\n(Physician Progress Notes,\ne-Prescription, Lab Routing)", ha="center", va="center", fontsize=9, color="#2D3748", bbox=dict(boxstyle="square", facecolor="white", edgecolor="#CBD5E0"))
ax.text(7.8, 4.8, "NHIS Financial Engine\n(National Health Insurance\n70% Subsidy & Copay Invoicing)", ha="center", va="center", fontsize=9, color="#2D3748", bbox=dict(boxstyle="square", facecolor="white", edgecolor="#CBD5E0"))

# Arrow 2
ax.annotate("", xy=(5.0, 3.4), xytext=(5.0, 3.8), arrowprops=dict(arrowstyle="<->", color="#4A5568", lw=2))

# Layer 3: Persistence / Database
rect3 = patches.FancyBboxPatch((0.5, 0.5), 9.0, 2.7, boxstyle="round,pad=0.2", facecolor="#FAF5FF", edgecolor="#805AD5", linewidth=2)
ax.add_patch(rect3)
ax.text(5.0, 2.8, "DATA PERSISTENCE LAYER (SQLITE RELATIONAL DATABASE)", ha="center", va="center", fontsize=11, fontweight="bold", color="#553C9A")
ax.text(1.5, 1.4, "[Patients Table]\npatient_id (PK)\nfull_name, age, sex\nnhis_number, genotype", ha="center", va="center", fontsize=8.5, color="#2D3748", bbox=dict(boxstyle="round", facecolor="white", edgecolor="#E2E8F0"))
ax.text(3.3, 1.4, "[Vitals Table]\nvital_id (PK)\nsys_bp, dia_bp\nbmi, triage_status", ha="center", va="center", fontsize=8.5, color="#2D3748", bbox=dict(boxstyle="round", facecolor="white", edgecolor="#E2E8F0"))
ax.text(5.1, 1.4, "[Appointments]\nappointment_id (PK)\ndoctor_name\nclinic, status", ha="center", va="center", fontsize=8.5, color="#2D3748", bbox=dict(boxstyle="round", facecolor="white", edgecolor="#E2E8F0"))
ax.text(6.9, 1.4, "[Consultations]\nconsultation_id (PK)\ndiagnosis, symptoms\nprescription, labs", ha="center", va="center", fontsize=8.5, color="#2D3748", bbox=dict(boxstyle="round", facecolor="white", edgecolor="#E2E8F0"))
ax.text(8.6, 1.4, "[Billing Table]\nbill_id (PK)\ngross_ghs, nhis_ghs\nnet_payable_ghs", ha="center", va="center", fontsize=8.5, color="#2D3748", bbox=dict(boxstyle="round", facecolor="white", edgecolor="#E2E8F0"))

plt.title("Figure 1.1: Multi-Tier Architectural Blueprint of Pentecost University Hospital Management System", fontsize=12, pad=15, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(FIGS_DIR, "system_architecture.png"), dpi=300)
plt.close()
print("  ✓ Figure 1.1: System Architecture Diagram created.")

# -----------------------------------------------------------------------------
# 2. OPERATIONAL ANALYTICS DASHBOARD FIGURE
# -----------------------------------------------------------------------------
conn = sqlite3.connect(DB_PATH)
df_p = pd.read_sql_query("SELECT * FROM patients", conn)
df_v = pd.read_sql_query("SELECT * FROM vitals", conn)
df_b = pd.read_sql_query("SELECT * FROM billing", conn)
conn.close()

fig, axes = plt.subplots(2, 2, figsize=(11, 8.5))

# Subplot 1: Ethnicity
eth_counts = df_p["ethnicity"].value_counts()
sns.barplot(x=eth_counts.index, y=eth_counts.values, ax=axes[0, 0], palette="crest")
axes[0, 0].set_title("A: Patient Demographics by Ethnicity", fontsize=11, fontweight="bold")
axes[0, 0].set_xlabel("Ghanaian Demographic Cohort")
axes[0, 0].set_ylabel("Enrolled Count")
axes[0, 0].tick_params(axis='x', rotation=25)

# Subplot 2: Triage Urgency
triage_counts = df_v["triage_category"].value_counts()
colors = ["#2ecc71", "#f39c12", "#e74c3c"]
axes[0, 1].pie(triage_counts.values, labels=triage_counts.index, autopct='%1.1f%%', colors=colors[:len(triage_counts)], startangle=140)
axes[0, 1].set_title("B: Clinical Triage Urgency Distribution", fontsize=11, fontweight="bold")

# Subplot 3: Blood Group vs Genotype Distribution
gen_counts = df_p["genotype"].value_counts()
sns.barplot(x=gen_counts.index, y=gen_counts.values, ax=axes[1, 0], palette="magma")
axes[1, 0].set_title("C: Hemoglobin Genotype Prevalence", fontsize=11, fontweight="bold")
axes[1, 0].set_xlabel("Genotype (AA, AS, SS, AC, SC)")
axes[1, 0].set_ylabel("Patient Count")

# Subplot 4: Revenue & NHIS Breakdown
rev_summary = pd.Series({
    "Gross Total": df_b["gross_amount_ghs"].sum(),
    "NHIS Covered": df_b["nhis_covered_ghs"].sum(),
    "Patient Copay": df_b["net_payable_ghs"].sum()
})
sns.barplot(x=rev_summary.index, y=rev_summary.values, ax=axes[1, 1], palette="viridis")
axes[1, 1].set_title("D: Hospital Revenue & NHIS Subsidies (GHS)", fontsize=11, fontweight="bold")
axes[1, 1].set_ylabel("Amount (GHS)")
for p in axes[1, 1].patches:
    axes[1, 1].annotate(f"GHS {p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                        ha='center', va='center', color='white', fontweight='bold', fontsize=9.5)

plt.suptitle("Figure 2.1: Hospital Operational Intelligence & Patient Cohort Analytics", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(FIGS_DIR, "operational_analytics.png"), dpi=300)
plt.close()
print("  ✓ Figure 2.1: Operational Analytics figure created.")

# -----------------------------------------------------------------------------
# 3. TRIAGE ALGORITHM FLOWCHART
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# Start
box_start = patches.FancyBboxPatch((3.5, 8.8), 3.0, 0.9, boxstyle="round,pad=0.2", facecolor="#3182CE", edgecolor="#2B6CB0")
ax.add_patch(box_start)
ax.text(5.0, 9.25, "PATIENT ARRIVAL AT TRIAGE\n(Measure Systolic, Diastolic, Temp, BMI)", ha="center", va="center", color="white", fontsize=9, fontweight="bold")

# Decision 1
box_d1 = patches.FancyBboxPatch((3.0, 6.6), 4.0, 1.2, boxstyle="square,pad=0.2", facecolor="#FFF5F5", edgecolor="#E53E3E", linewidth=1.5)
ax.add_patch(box_d1)
ax.text(5.0, 7.2, "Systolic BP >= 160 mmHg OR\nDiastolic BP >= 100 mmHg OR\nBody Temp >= 38.5°C?", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#9B2C2C")

# Red branch
box_red = patches.FancyBboxPatch((0.5, 4.6), 2.5, 1.2, boxstyle="round,pad=0.2", facecolor="#E53E3E", edgecolor="#9B2C2C")
ax.add_patch(box_red)
ax.text(1.75, 5.2, "EMERGENCY (RED)\nImmediate Resuscitation\nAcute OPD Physician Alert", ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")

# Decision 2
box_d2 = patches.FancyBboxPatch((3.0, 4.2), 4.0, 1.2, boxstyle="square,pad=0.2", facecolor="#FFFFF0", edgecolor="#D69E2E", linewidth=1.5)
ax.add_patch(box_d2)
ax.text(5.0, 4.8, "Systolic BP >= 140 mmHg OR\nBody Temp >= 37.8°C OR\nBMI >= 32.0 kg/m²?", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#744210")

# Yellow branch
box_yellow = patches.FancyBboxPatch((7.0, 4.2), 2.6, 1.2, boxstyle="round,pad=0.2", facecolor="#D69E2E", edgecolor="#744210")
ax.add_patch(box_yellow)
ax.text(8.3, 4.8, "PRIORITY (YELLOW)\nStage 1/2 Hypertension\nPriority Medical Queue", ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")

# Routine Green
box_green = patches.FancyBboxPatch((3.5, 1.8), 3.0, 1.2, boxstyle="round,pad=0.2", facecolor="#38A169", edgecolor="#22543D")
ax.add_patch(box_green)
ax.text(5.0, 2.4, "ROUTINE (GREEN)\nStable Vital Baselines\nStandard Outpatient Queue", ha="center", va="center", color="white", fontsize=9, fontweight="bold")

# Connecting Arrows
ax.annotate("", xy=(5.0, 7.8), xytext=(5.0, 8.8), arrowprops=dict(arrowstyle="->", color="#4A5568", lw=1.5))
ax.annotate("YES", xy=(3.0, 5.2), xytext=(3.0, 7.2), arrowprops=dict(arrowstyle="->", color="#E53E3E", lw=1.5))
ax.annotate("NO", xy=(5.0, 5.4), xytext=(5.0, 6.6), arrowprops=dict(arrowstyle="->", color="#4A5568", lw=1.5))
ax.annotate("YES", xy=(7.0, 4.8), xytext=(7.0, 4.8), arrowprops=dict(arrowstyle="->", color="#D69E2E", lw=1.5))
ax.annotate("NO", xy=(5.0, 3.0), xytext=(5.0, 4.2), arrowprops=dict(arrowstyle="->", color="#38A169", lw=1.5))

plt.title("Figure 2.2: Algorithmic Clinical Triage Decision Logic Flowchart", fontsize=12, pad=15, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(FIGS_DIR, "triage_algorithm_flowchart.png"), dpi=300)
plt.close()
print("  ✓ Figure 2.2: Triage Flowchart created.")

print("All diagrams generated successfully!")
