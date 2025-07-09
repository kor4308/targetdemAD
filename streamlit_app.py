import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ---------- Demographic Gap Analyzer ----------
st.title("Patient Engagement Gap Analyzer and Behavioral Sciences Advisor")

# ---------- Top Section Layout ----------
top_col1, top_col2, top_col3 = st.columns(3)

# Trial Characteristics (Left)
with top_col1:
    st.markdown("<h3 style='font-size:26px;'>🧪 Trial Characteristics</h3>", unsafe_allow_html=True)
    therapeutic_area = st.selectbox("Therapeutic Area", ["Neuro", "Oncology", "Cardiometabolic"], key="therapeutic_area")

    disease = None
    current_trial = None
    lp_required = None
    pet_required = None
    study_partner_required = None

    if therapeutic_area == "Neuro":
        disease = st.selectbox("Disease", ["Alzheimer's", "Other"], key="disease")
        if disease == "Alzheimer's":
            current_trial = st.selectbox("Current Trial", ["Trailblazer-3", "Other"], key="trial_select")
            lp_required = st.selectbox("Lumbar Punctures Required?", ["Yes", "No"], key="lp_req")
            pet_required = st.selectbox("PET Scans Required?", ["Yes", "No"], key="pet_req")
            study_partner_required = st.selectbox("Study Partner Required?", ["Yes", "No"], key="partner_req")

# Target Demographics (Middle)
with top_col2:
    st.markdown("<h3 style='font-size:26px;'>🎯 Target Demographics (%)</h3>", unsafe_allow_html=True)
    total_enrollment = st.number_input("Total Enrollment Target", min_value=0, value=1000, key="total_enrollment")

    st.subheader("Gender Distribution")
    target_gender_male = st.number_input("Target Male %", 0, 100, 50, key="target_male")
    target_gender_female = 100 - target_gender_male
    st.markdown(f"Target Female %: **{target_gender_female}%**")

    st.subheader("Race Distribution")
    race_categories = [
        "Hispanic",
        "White (non-Hispanic)",
        "Black (non-Hispanic)",
        "Asian (non-Hispanic)",
        "American Indian and Alaska Native",
        "Native Hawaiian and Pacific Islander",
        "Other"
    ]
    target_race = {}
    race_total = 0
    for race in race_categories:
        target_race[race] = st.number_input(f"Target {race} %", 0, 100, 10, key=f"t_{race}")
        count_val = int(target_race[race] / 100 * total_enrollment)
        st.caption(f"{count_val} participants")
        race_total += target_race[race]

    if race_total != 100:
        st.error(f"Target race percentages must total 100%. Current total: {race_total}%")

    st.markdown("### Overall Totals (Target Enrollment)")
    st.markdown(f"- Male: {int(target_gender_male / 100 * total_enrollment)} participants")
    st.markdown(f"- Female: {int(target_gender_female / 100 * total_enrollment)} participants")
    for race in race_categories:
        st.markdown(f"- {race}: {int(target_race[race] / 100 * total_enrollment)} participants")

# Current Enrollment (Right)
with top_col3:
    st.markdown("<h3 style='font-size:26px;'>📍 Current Enrollment (Count)</h3>", unsafe_allow_html=True)
    current_enrollment = st.number_input("Current Total Enrollment", min_value=0, value=1000, key="current_enrollment")

    st.subheader("Gender Distribution")
    current_gender_male = st.number_input("Current Male Count", 0, value=500, key="current_male")
    current_gender_female = current_enrollment - current_gender_male
    st.markdown(f"Current Female Count: **{current_gender_female}**")
    st.caption(f"{(current_gender_female / current_enrollment) * 100:.1f}%")

    st.subheader("Race Distribution")
    current_race = {}
    race_current_total = 0
    for race in race_categories:
        current_race[race] = st.number_input(f"Current {race} Count", 0, value=80, key=f"c_{race}")
        race_current_total += current_race[race]
        percent_val = (current_race[race] / current_enrollment) * 100 if current_enrollment > 0 else 0
        st.caption(f"{percent_val:.1f}%")

st.markdown(f"**🎯 Target Total Enrollment:** {total_enrollment} participants")
st.markdown(f"**📍 Current Total Enrollment:** {current_enrollment} participants")

# --- Continue with rest of code logic (recalculating gaps, charts, and strategy recommendations) ---
