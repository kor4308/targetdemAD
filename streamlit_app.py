import streamlit as st
import plotly.graph_objects as go

# ---------- Demographic Gap Analyzer ----------
st.title("Alzheimer's Disease Persona & Recruitment Analyzer")

st.markdown("## 🎯 Target vs. Current Enrollment")

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
for race in races:
    target_race[race] = st.number_input(f"Target {race}", 0, 100, 20, key=f"t_{race}")

st.markdown("### Current Race %")
for race in races:
    current_race[race] = st.number_input(f"Current {race}", 0, 100, 15, key=f"c_{race}")

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

race = st.selectbox("Race", races)
gender = st.selectbox("Gender", ["Male", "Female"])
family_history = st.selectbox("Family History of Alzheimer's", ["Yes", "No"])
study_partner = st.selectbox("Type of Study Partner", ["Spousal", "Son/Daughter", "Non-Family"])
recruitment_strategy = st.selectbox("Return Personal Results?", ["Do not return personal results", "Return personal results"])
childcare_services = st.selectbox("Provide Childcare Services?", ["No", "Yes"])
cultural_practices = st.selectbox("Recruitment Leverages Cultural Practices?", ["No", "Yes"])
emphasize_generations = st.selectbox("Emphasize Impact on Future Generations?", ["No", "Yes"])

# Persona scoring
race_score = {"White": 80, "African American": 40, "Hispanic": 50, "Asian": 50, "Other": 50}[race]
gender_score = 65 if gender == "Male" else 45
family_score = 80 if family_history == "Yes" else 20
partner_score = {"Spousal": 85, "Son/Daughter": 60, "Non-Family": 40}[study_partner]

# Final score (without recruitment bonuses)
scores = [race_score, gender_score, family_score, partner_score]
total_score = sum(scores) / 4

# Radar chart
fig = go.Figure()
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
    showlegend=False,
    title="Alzheimer's Risk Factors",
    height=500,
    width=600
)

st.plotly_chart(fig)
st.subheader(f"Total Score: {total_score:.1f}")

# ---------- Bonus Strategy Bar Chart ----------
st.header("📈 Recruitment Strategy Bonuses")

bonus_labels = []
bonus_values = []

if recruitment_strategy == "Return personal results" and family_history == "Yes":
    bonus_labels.append("Return Results")
    bonus_values.append(20)

if childcare_services == "Yes":
    bonus_labels.append("Childcare")
    bonus_values.append({"Spousal": 2, "Son/Daughter": 15, "Non-Family": 8}[study_partner])

if cultural_practices == "Yes":
    bonus_labels.append("Cultural Practices")
    bonus_values.append(2 if race == "White" else 8)

if emphasize_generations == "Yes":
    bonus_labels.append("Generational Messaging")
    bonus_values.append(6 if family_history == "Yes" or race == "African American" else 3)

if bonus_labels:
    bonus_fig = go.Figure([go.Bar(x=bonus_labels, y=bonus_values)])
    bonus_fig.update_layout(
        yaxis=dict(range=[0, max(bonus_values) + 10]),
        title="Bonus Contribution from Recruitment Strategies",
        height=400
    )
    st.plotly_chart(bonus_fig)
else:
    st.write("No recruitment strategy bonuses selected.")
