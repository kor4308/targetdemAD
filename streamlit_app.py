import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ---------- Demographic Gap Analyzer ----------
st.title("Alzheimer's Disease Persona & Recruitment Analyzer")

# ---------- Trial Characteristics ----------

st.markdown("## 📋 Trial Overview")
total_enrollment = st.number_input("Total Enrollment Target", min_value=0, value=1000)

st.markdown("### Target Demographics")

# --- Gender Input ---
col1, col2 = st.columns(2)
with col1:
    target_female = st.number_input("Target Female %", 0, 100, 50)
with col2:
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

st.markdown("## 🧪 Trial Characteristics")

trial_col1, trial_col2, trial_col3 = st.columns(3)
with trial_col1:
    lp_required = st.selectbox("Lumbar Punctures Required?", ["Yes", "No"])
with trial_col2:
    pet_required = st.selectbox("PET Scans Required?", ["Yes", "No"])
with trial_col3:
    study_partner_required = st.selectbox("Study Partner Required?", ["Yes", "No"])

st.markdown("## 🔄 Current Enrollment")
current_enrollment = st.number_input("Current Total Enrollment", min_value=0, value=800)

# --- Current Gender Input ---
col3, col4 = st.columns(2)
with col3:
    current_female = st.number_input("Currently Enrolled Female %", 0, 100, 40)
with col4:
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

# ---------- Gap Calculation ----------
st.header("📊 Enrollment Gaps")

gender_gap = {
    "Female": target_female - current_female,
    "Male": target_male - current_male
}
race_gap = {race: target_race[race] - current_race[race] for race in races}

st.subheader("Gender Gaps")
for gender, gap in gender_gap.items():
    note = f"(You need to increase {gender.lower()} enrollment by {abs(gap):.1f}% to reach target)" if gap > 0 else ""
    st.write(f"**{gender}:** {gap:+.1f}% {note}")

st.subheader("Race Gaps")
for race, gap in race_gap.items():
    note = f"(You need to increase {race} enrollment by {abs(gap):.1f}% to reach target)" if gap > 0 else ""
    st.write(f"**{race}:** {gap:+.1f}% {note}")

# ---------- Stacked Bar Visualization ----------
st.subheader("📈 Stacked Enrollment Comparison")

# Bar graph with target (gray) and current (blue)
stacked_fig = go.Figure()

# Gender Stacked Bar
stacked_fig.add_trace(go.Bar(
    x=["Female", "Male"] + races,
    y=[target_female, target_male] + [target_race[r] for r in races],
    name='Target Enrollment %',
    marker_color='lightgray'
))

stacked_fig.add_trace(go.Bar(
    x=["Female", "Male"] + races,
    y=[current_female, current_male] + [current_race[r] for r in races],
    name='Current Enrollment %',
    marker_color='steelblue'
))

stacked_fig.update_layout(
    barmode='overlay',
    title="Target vs. Current Enrollment %",
    yaxis=dict(title="Percentage"),
    height=500
)

st.plotly_chart(stacked_fig)

# (rest of the existing code continues unchanged)
