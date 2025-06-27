import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ---------- Demographic Gap Analyzer ----------
st.title("Alzheimer's Disease Persona & Recruitment Analyzer")

# ---------- Trial Characteristics ----------

st.markdown("## 📋 Trial Overview")
total_enrollment = st.number_input("Total Enrollment Target", min_value=0, value=1000)

st.markdown("### Target Demographics")

# --- Gender Input ---
col1, col2 = st.columns(2)
with col1:
    target_female = st.number_input("Target Female %", 0, 100, 55)
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

groups = ["Female", "Male"] + races
current_counts = [
    int(current_enrollment * current_female / 100),
    int(current_enrollment * current_male / 100),
] + [int(current_enrollment * current_race[r] / 100) for r in races]

target_counts = [
    int(total_enrollment * target_female / 100),
    int(total_enrollment * target_male / 100),
] + [int(total_enrollment * target_race[r] / 100) for r in races]

# ---------- Strategy Recommendations ----------
st.markdown("---")
st.header("📌 Strategy Recommendations Based on Gaps")

if (target_counts[0] - current_counts[0]) > total_enrollment * 0.05:
    st.markdown("### 👩 Female Underrepresentation Strategies")
    if lp_required == "Yes":
        st.write("- Educate about lumbar punctures vs. epidurals to reduce fear")
    st.write("- Connect with Alzheimer's research registries")
    st.write("- Collaborate with women-led organizations")
    st.write("- Emphasize legacy/future generation impact")
    st.write("- Offer flexible scheduling and childcare")

for i, race in enumerate(races):
    if (target_counts[i + 2] - current_counts[i + 2]) > total_enrollment * 0.05:
        st.markdown(f"### 🧑🏽 {race} Underrepresentation Strategies")
        st.write("- Tailor messaging around leaving a legacy for future generations")
        st.write("- Use culturally-tailored outreach")
        st.write("- Ensure diverse trial teams to increase comfort")

# ---------- Stacked Bar Visualization and Table ----------
st.subheader("📈 Enrollment Comparison")

chart_col, table_col = st.columns([2, 1])

with chart_col:
    stacked_fig = go.Figure()
    stacked_fig.add_trace(go.Bar(
        x=groups,
        y=target_counts,
        name='Target Enrollment',
        marker_color='lightgray',
        textposition='none'
    ))
    stacked_fig.add_trace(go.Bar(
        x=groups,
        y=current_counts,
        name='Current Enrollment',
        marker_color='steelblue',
        textposition='none'
    ))
    stacked_fig.update_layout(
        barmode='overlay',
        title="Target vs. Current Enrollment (Counts)",
        yaxis=dict(title="Participant Count"),
        height=550
    )
    st.plotly_chart(stacked_fig)

with table_col:
    st.markdown("#### 📋 Enrollment Table")
    df = pd.DataFrame({
        "Group": groups,
        "Target Count": target_counts,
        "Current Count": current_counts,
        "Change Needed": [t - c for t, c in zip(target_counts, current_counts)],
        "Target %": [f"{(t/total_enrollment)*100:.1f}%" for t in target_counts],
        "Current %": [f"{(c/current_enrollment)*100:.1f}%" for c in current_counts],
    })
    st.dataframe(df)

# ---------- Optional Radar Chart Demo (for a single persona) ----------

st.header("🧠 Individual Persona Radar Chart")

persona_col1, persona_col2 = st.columns(2)

with persona_col1:
    st.subheader("Persona Characteristics")
    race = st.selectbox("Race", races)
    gender = st.selectbox("Gender", ["Male", "Female"])
    family_history = st.selectbox("Family History of Alzheimer's", ["Yes", "No"])
    study_partner = st.selectbox("Type of Study Partner", ["Spousal", "Son/Daughter", "Non-Family"])

with persona_col2:
    st.subheader("Recruitment Strategies")
    return_results = st.selectbox("Return Personal Results?", ["Do not return personal results", "Return personal results"])
    childcare = st.selectbox("Provide Childcare Services?", ["No", "Yes"])
    cultural_practices = st.selectbox("Leverage Cultural Practices?", ["No", "Yes"])
    emphasize_generations = st.selectbox("Emphasize Impact on Future Generations?", ["No", "Yes"])

# Baseline scores
race_score = {"White": 80, "African American": 40, "Hispanic": 50, "Asian": 50, "Other": 50}[race]
gender_score = 65 if gender == "Male" else 45
family_score = 80 if family_history == "Yes" else 20
partner_score = {"Spousal": 85, "Son/Daughter": 60, "Non-Family": 40}[study_partner]

baseline_scores = [min(100, race_score), min(100, gender_score), min(100, family_score), min(100, partner_score)]

bonus_labels = []

# Recruitment strategy adjustments
if return_results == "Return personal results" and family_history == "Yes":
    family_score += 20
    bonus_labels.append("✅ Bonus Applied: Returning personal results boosted family history score.")
if childcare == "Yes":
    inc = {"Spousal": 2, "Son/Daughter": 15, "Non-Family": 8}[study_partner]
    partner_score += inc
    bonus_labels.append(f"✅ Bonus Applied: Childcare support increased partner score by {inc}.")
if cultural_practices == "Yes":
    inc = 2 if race == "White" else 8
    race_score += inc
    bonus_labels.append(f"✅ Bonus Applied: Cultural practice emphasis increased race score by {inc}.")
if emphasize_generations == "Yes":
    inc = 6 if family_history == "Yes" or race == "African American" else 3
    race_score += inc
    bonus_labels.append(f"✅ Bonus Applied: Legacy messaging increased race score by {inc}.")

adjusted_scores = [min(100, race_score), min(100, gender_score), min(100, family_score), min(100, partner_score)]
total_score = sum(adjusted_scores) / 4

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=baseline_scores,
    theta=["Race", "Gender", "Family History", "Study Partner"],
    fill='toself',
    name='Baseline',
    line=dict(color='lightblue')
))
fig.add_trace(go.Scatterpolar(
    r=adjusted_scores,
    theta=["Race", "Gender", "Family History", "Study Partner"],
    fill='toself',
    name='With Recruitment Strategies',
    line=dict(color='darkblue')
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    title="Alzheimer's Risk Persona Chart",
    height=500,
    width=600
)

st.plotly_chart(fig)
st.subheader(f"Total Adjusted Score: {total_score:.1f}")

for label in bonus_labels:
    st.success(label)
