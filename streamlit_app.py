import streamlit as st
import plotly.graph_objects as go

# ---------- Demographic Gap Analyzer ----------
st.title("Alzheimer's Disease Persona & Recruitment Analyzer")

# ---------- Trial Characteristics ----------
st.markdown("## 🧪 Trial Characteristics")

trial_col1, trial_col2, trial_col3 = st.columns(3)
with trial_col1:
    lp_required = st.selectbox("Lumbar Punctures Required?", ["Yes", "No"])
with trial_col2:
    pet_required = st.selectbox("PET Scans Required?", ["Yes", "No"])
with trial_col3:
    study_partner_required = st.selectbox("Study Partner Required?", ["Yes", "No"])

st.markdown("## 🌟 Target vs. Current Enrollment")

# --- Gender Input ---
st.subheader("Gender Distribution")
col1, col2 = st.columns(2)
with col1:
    target_female = st.number_input("Target Female %", 0, 100, 50)
with col2:
    target_male = 100 - target_female
    st.markdown(f"**Target Male %**: {target_male}")

col3, col4 = st.columns(2)
with col3:
    current_female = st.number_input("Currently Enrolled Female %", 0, 100, 40)
with col4:
    current_male = 100 - current_female
    st.markdown(f"**Currently Enrolled Male %**: {current_male}")

# --- Race Input ---
races = ["White", "African American", "Hispanic", "Asian", "Other"]
st.subheader("Race Distribution")
target_race = {}
current_race = {}

st.markdown("### Target Race %")
target_total = 0
for race in races:
    target_race[race] = st.number_input(f"Target {race}", 0, 100, 20, key=f"t_{race}")
    target_total += target_race[race]

if target_total != 100:
    st.error(f"Target race percentages must total 100%. Current total: {target_total}%")

st.markdown("### Current Race %")
current_total = 0
for race in races:
    current_race[race] = st.number_input(f"Current {race}", 0, 100, 15, key=f"c_{race}")
    current_total += current_race[race]

if current_total != 100:
    st.error(f"Current race percentages must total 100%. Current total: {current_total}%")

# ---------- Gap Calculation ----------
st.markdown("---")
st.header("📊 Enrollment Gaps")

gender_gap = {
    "Female": target_female - current_female,
    "Male": target_male - current_male
}
race_gap = {race: target_race[race] - current_race[race] for race in races}

st.subheader("Gender Gaps")
for gender, gap in gender_gap.items():
    st.write(f"**{gender}:** {gap:+.1f}%")

st.subheader("Race Gaps")
for race, gap in race_gap.items():
    st.write(f"**{race}:** {gap:+.1f}%")

# ---------- Strategy Recommendations ----------
st.markdown("---")
st.header("📌 Strategy Recommendations Based on Gaps")

if gender_gap["Female"] > 5:
    st.markdown("### 👩 Female Underrepresentation Strategies")
    st.write("- Connect with Alzheimer's research registries")
    st.write("- Collaborate with women-led organizations")
    st.write("- Emphasize legacy/future generation impact")
    st.write("- Offer flexible scheduling and childcare")
    if lp_required == "Yes":
        st.warning("Female underrepresentation combined with lumbar puncture requirement may cause fear or confusion. Provide educational materials explaining the difference between lumbar punctures and epidurals to reduce anxiety and improve trust.")

for race, gap in race_gap.items():
    if gap > 5:
        st.markdown(f"### 🧑🏽 {race} Underrepresentation Strategies")
        st.write("- Partner with trusted community leaders")
        st.write("- Leverage cultural practices in recruitment")
        st.write("- Return personal results as incentive")
        st.write("- Address medical mistrust transparently")

# ---------- Optional Radar Chart Demo (for a single persona) ----------
st.markdown("---")
st.header("🧠 Individual Persona Radar Chart")

left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("Persona Characteristics")
    race = st.selectbox("Race", races)
    gender = st.selectbox("Gender", ["Male", "Female"])
    family_history = st.selectbox("Family History of Alzheimer's", ["Yes", "No"])
    study_partner = st.selectbox("Type of Study Partner", ["Spousal", "Son/Daughter", "Non-Family"])

with right_col:
    st.subheader("Recruitment Strategies")
    recruitment_strategy = st.selectbox("Return Personal Results?", ["Do not return personal results", "Return personal results"])
    childcare_services = st.selectbox("Provide Childcare Services?", ["No", "Yes"])
    cultural_practices = st.selectbox("Recruitment Leverages Cultural Practices?", ["No", "Yes"])
    emphasize_generations = st.selectbox("Emphasize Impact on Future Generations?", ["No", "Yes"])
    st.subheader("Recruitment Strategy Effects")

    base_scores = {
        "Race": {"White": 80, "African American": 40, "Hispanic": 50, "Asian": 50, "Other": 50}[race],
        "Gender": 65 if gender == "Male" else 45,
        "Family History": 80 if family_history == "Yes" else 20,
        "Study Partner": {"Spousal": 85, "Son/Daughter": 60, "Non-Family": 40}[study_partner]
    }

    # Apply bonuses
    race_score = base_scores["Race"]
    gender_score = base_scores["Gender"]
    family_score = base_scores["Family History"]
    partner_score = base_scores["Study Partner"]

    score_explanations = []

    if recruitment_strategy == "Return personal results" and family_history == "Yes":
        family_score += 20
        score_explanations.append("✅ Returning personal results increased family history score by 20.")

    if childcare_services == "Yes":
        bonus = {"Spousal": 2, "Son/Daughter": 15, "Non-Family": 8}[study_partner]
        partner_score += bonus
        score_explanations.append(f"✅ Childcare services increased study partner score by {bonus}.")

    if cultural_practices == "Yes":
        bonus = 2 if race == "White" else 8
        race_score += bonus
        score_explanations.append(f"✅ Cultural practice alignment increased race score by {bonus}.")

    if emphasize_generations == "Yes":
        bonus = 6 if family_history == "Yes" or race == "African American" else 3
        race_score += bonus
        score_explanations.append(f"✅ Emphasis on future generations increased race score by {bonus}.")

    

# Persona scoring
scores = [min(100, race_score), min(100, gender_score), min(100, family_score), min(100, partner_score)]
total_score = sum(scores) / 4

# Radar chart

# Add base (pre-strategy) scores to compare
base_score_values = [
    base_scores["Race"],
    base_scores["Gender"],
    base_scores["Family History"],
    base_scores["Study Partner"]
]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=base_score_values,
    theta=["Race", "Gender", "Family History", "Study Partner"],
    fill="toself",
    name="Baseline Persona",
    line=dict(color="lightblue"),
    fillcolor="rgba(173, 216, 230, 0.3)"
))

fig.add_trace(go.Scatterpolar(
    r=scores,
    theta=["Race", "Gender", "Family History", "Study Partner"],
    fill="toself",
    name="With Recruitment Strategies",
    line=dict(color="blue"),
    fillcolor="rgba(0, 100, 255, 0.3)"
))
fig.add_trace(go.Scatterpolar(
    r=scores,
    theta=["Race", "Gender", "Family History", "Study Partner"],
    fill="toself",
    name="Risk Factors",
    line=dict(color="blue"),
    fillcolor="rgba(0, 100, 255, 0.3)"
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    title="Alzheimer's Risk Factors",
    height=500,
    width=600
)

st.plotly_chart(fig)
st.subheader(f"Total Score: {total_score:.1f}")

st.markdown("---")
st.subheader("📈 Recruitment Strategy Score Impact")
for explanation in score_explanations:
    st.success(explanation)
