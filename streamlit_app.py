import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ---------- Demographic Gap Analyzer ----------
st.title("Patient Engagement Gap Analyzer and Recruitment Advisor")

# ---------- Top Section Layout ----------
top_col1, top_col2, top_col3 = st.columns(3)

# Trial Characteristics (Left)
with top_col1:
    st.markdown("<h4>🧪 Trial Characteristics</h4>", unsafe_allow_html=True)
    therapeutic_area = st.selectbox("Therapeutic Area", ["Neurodegenerative", "Oncology", "Cardiometabolic"])

    if therapeutic_area == "Neurodegenerative":
        current_trial = st.selectbox("Current Trial", ["Trailblazer-3", "Other"], key="trial_select")
        lp_required = st.selectbox("Lumbar Punctures Required?", ["Yes", "No"], key="lp_req")
        pet_required = st.selectbox("PET Scans Required?", ["Yes", "No"], key="pet_req")
        study_partner_required = st.selectbox("Study Partner Required?", ["Yes", "No"], key="partner_req")

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

# ---------- Enrollment Visualization & Strategies ----------

# Gender gap calculation
gender_gap = {
    "Female": target_female / 100 * total_enrollment - current_female / 100 * current_enrollment,
    "Male": target_male / 100 * total_enrollment - current_male / 100 * current_enrollment
}

# Race gap calculation
race_gap = {}
for race in races:
    target_count = target_race[race] / 100 * total_enrollment
    current_count = current_race[race] / 100 * current_enrollment
    race_gap[race] = target_count - current_count

# Visualization prep
groups = ["Female", "Male"] + races
target_counts = [target_female, target_male] + [target_race[r] for r in races]
target_counts = [v / 100 * total_enrollment for v in target_counts]
current_counts = [current_female, current_male] + [current_race[r] for r in races]
current_counts = [v / 100 * current_enrollment for v in current_counts]
diffs = [target_counts[i] - current_counts[i] for i in range(len(groups))]

# Only show underrepresented gaps
graph_col, table_col = st.columns([2, 1])
with graph_col:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=groups,
        y=target_counts,
        name='Target',
        marker_color='lightgrey'
    ))
    fig.add_trace(go.Bar(
        x=groups,
        y=current_counts,
        name='Current',
        marker_color='steelblue'
    ))
    fig.update_layout(barmode='overlay', title='Enrollment by Group', height=400)
    st.plotly_chart(fig)

with table_col:
    st.markdown("#### 📋 Enrollment Table")
    table_data = []
    for i, label in enumerate(groups):
        abs_change = diffs[i]
        pct_change = (abs_change / target_counts[i]) * 100 if target_counts[i] != 0 else 0
        table_data.append({
            "Group": label,
            "Target Count": int(target_counts[i]),
            "Current Count": int(current_counts[i]),
            "Change Needed (n)": int(abs_change),
            "Change Needed (%)": f"{pct_change:+.1f}%"
        })
    st.dataframe(pd.DataFrame(table_data))

# Strategies Section
st.markdown("---")
st.header("📌 Strategy Recommendations Based on Gaps")

if gender_gap["Female"] > 0:
    st.subheader("👩 Female Underrepresentation Strategies")
    st.write("- Connect with Alzheimer's research registries")
    st.write("- Collaborate with women-led organizations")
    st.write("- Emphasize legacy/future generation impact")
    st.write("- Offer flexible scheduling and childcare")

if gender_gap["Male"] > 0:
    st.subheader("👨 Male Underrepresentation Strategies")
    st.write("- Advertise at sports games and male-dominated venues")
    st.write("- Frame participation as contributing to science and legacy")
    st.write("- Reduce perceived stigma around cognitive testing")

for race in races:
    if race_gap[race] > 0:
        st.subheader(f"🧑🏽 {race} Underrepresentation Strategies")
        st.write("- Emphasize impact on future generations")
        st.write("- Culturally-tailored messaging")
        st.write("- Ensure diverse study team to build trust")
