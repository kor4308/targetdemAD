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

# ---------- Strategy Recommendations ----------
st.markdown("---")
st.header("📌 Strategy Recommendations Based on Gaps")

if gender_gap["Female"] > 5:
    st.markdown("### 👩 Female Underrepresentation Strategies")
    if lp_required == "Yes":
        st.write("- Educate about lumbar punctures vs. epidurals to reduce fear")
    st.write("- Connect with Alzheimer's research registries")
    st.write("- Collaborate with women-led organizations")
    st.write("- Emphasize legacy/future generation impact")
    st.write("- Offer flexible scheduling and childcare")

for race, gap in race_gap.items():
    if gap > 5:
        st.markdown(f"### 🧑🏽 {race} Underrepresentation Strategies")
        st.write("- Tailor messaging around leaving a legacy for future generations")
        st.write("- Use culturally-tailored outreach")
        st.write("- Ensure diverse trial teams to increase comfort")

# ---------- Stacked Bar Visualization and Table ----------
st.subheader("📈 Enrollment Comparison")

# Calculate counts
current_female_count = int(current_enrollment * current_female / 100)
current_male_count = current_enrollment - current_female_count
target_female_count = int(total_enrollment * target_female / 100)
target_male_count = total_enrollment - target_female_count

current_race_count = {r: int(current_enrollment * current_race[r] / 100) for r in races}
target_race_count = {r: int(total_enrollment * target_race[r] / 100) for r in races}

# Combine labels and values
labels = ["Female", "Male"] + races
current_counts = [current_female_count, current_male_count] + [current_race_count[r] for r in races]
target_counts = [target_female_count, target_male_count] + [target_race_count[r] for r in races]
current_percent = [current_female, current_male] + [current_race[r] for r in races]
target_percent = [target_female, target_male] + [target_race[r] for r in races]

# Layout: bar chart left, table right
bar_col, table_col = st.columns(2)

with bar_col:
    stacked_fig = go.Figure()
    stacked_fig.add_trace(go.Bar(
        x=labels,
        y=target_counts,
        name='Target Enrollment',
        marker_color='lightgray',
        text=[f"{count} ({pct:.1f}%)" for count, pct in zip(target_counts, target_percent)],
        textposition='auto'
    ))
    stacked_fig.add_trace(go.Bar(
        x=labels,
        y=current_counts,
        name='Current Enrollment',
        marker_color='steelblue',
        text=[f"{count} ({pct:.1f}%)" for count, pct in zip(current_counts, current_percent)],
        textposition='auto'
    ))
    stacked_fig.update_layout(
        barmode='overlay',
        title="Target vs. Current Enrollment (Counts with %)",
        yaxis=dict(title="Participant Count"),
        height=550
    )
    st.plotly_chart(stacked_fig)

with table_col:
    df = pd.DataFrame({
        "Demographic": labels,
        "Target Count": target_counts,
        "Current Count": current_counts,
        "% Change Needed": [f"{target_percent[i] - current_percent[i]:+.1f}%" for i in range(len(labels))]
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

# Recruitment strategy adjustments
if return_results == "Return personal results" and family_history == "Yes":
    family_score += 20
if childcare == "Yes":
    partner_score += {"Spousal": 2, "Son/Daughter": 15, "Non-Family": 8}[study_partner]
if cultural_practices == "Yes":
    race_score += 2 if race == "White" else 8
if emphasize_generations == "Yes":
    race_score += 6 if family_history == "Yes" or race == "African American" else 3

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
