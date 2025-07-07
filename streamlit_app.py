import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ---------- Demographic Gap Analyzer ----------
st.title("Alzheimer's Disease Persona & Recruitment Analyzer")

# ---------- Top Section Layout ----------
top_col1, top_col2, top_col3 = st.columns(3)

# Trial Characteristics (Left)
with top_col1:
    st.markdown("## 🧪 Trial Characteristics")
    therapeutic_area = st.selectbox("Therapeutic Area", ["Neurodegenerative", "Oncology", "Cardiometabolic"])

    if therapeutic_area == "Neurodegenerative":
        lp_required = st.selectbox("Lumbar Punctures Required?", ["Yes", "No"])
        pet_required = st.selectbox("PET Scans Required?", ["Yes", "No"])
        study_partner_required = st.selectbox("Study Partner Required?", ["Yes", "No"])

# Target Demographics (Middle)
with top_col2:
    st.markdown("## 🎯 Target Demographics")
    total_enrollment = st.number_input("Total Enrollment Target", min_value=0, value=1000)

    target_female = st.number_input("Target Female %", 0, 100, 55)
    target_male = 100 - target_female
    st.markdown(f"**Target Male %**: {target_male}")

    races = ["White", "African American", "Hispanic", "Asian", "Other"]
    target_race = {}
    default_target_race = {"White": 55, "African American": 25, "Hispanic": 10, "Asian": 5, "Other": 5}
    target_total = 0
    for race in races:
        target_race[race] = st.number_input(f"Target {race}", 0, 100, default_target_race[race], key=f"t_{race}")
        target_total += target_race[race]
    if target_total != 100:
        st.error(f"Target race percentages must total 100%. Current total: {target_total}%")

# Current Enrollment (Right)
with top_col3:
    st.markdown("## 📍 Current Enrollment")
    current_enrollment = st.number_input("Current Total Enrollment", min_value=0, value=800)

    current_female = st.number_input("Currently Enrolled Female %", 0, 100, 40)
    current_male = 100 - current_female
    st.markdown(f"**Currently Enrolled Male %**: {current_male}")

    current_race = {}
    default_current_race = {"White": 55, "African American": 25, "Hispanic": 10, "Asian": 5, "Other": 5}
    current_total = 0
    for race in races:
        current_race[race] = st.number_input(f"Current {race}", 0, 100, default_current_race[race], key=f"c_{race}")
        current_total += current_race[race]
    if current_total != 100:
        st.error(f"Current race percentages must total 100%. Current total: {current_total}%")

st.markdown(f"**🎯 Target Total Enrollment:** {total_enrollment} participants")
st.markdown(f"**📍 Current Total Enrollment:** {current_enrollment} participants")

# The rest of your code remains unchanged...
