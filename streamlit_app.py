import streamlit as st
import plotly.graph_objects as go

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
import plotly.express as px

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
    if gap > 5:
        st.markdown("### 🧑🏽 Minority Underrepresentation Strategies")
        st.write("- Partner with trusted community leaders")
        st.write("- Leverage cultural practices in recruitment")
        st.write("- Return personal results as incentive")
        st.write("- Address medical mistrust transparently")
        st.write("- Increase awareness campaigns tailored to underrepresented populations")

gap_data = {
    "Demographic": [],
    "Gap Count": [],
    "Gap Label": []
}

# Compute absolute count gaps
female_count_gap = int((target_female / 100 * total_enrollment) - (current_female / 100 * current_enrollment))
gap_data["Demographic"].append("Female")
gap_data["Gap Count"].append(female_count_gap)
gap_data["Gap Label"].append(f"{female_count_gap:+} ({gender_gap['Female']:+.1f}%)")

for race in races:
    target_count = target_race[race] / 100 * total_enrollment
    current_count = current_race[race] / 100 * current_enrollment
    gap_count = int(target_count - current_count)
    gap_data["Demographic"].append(race)
    gap_data["Gap Count"].append(gap_count)
    gap_data["Gap Label"].append(f"{gap_count:+} ({race_gap[race]:+.1f}%)")

bar_fig = px.bar(
    gap_data,
    x="Demographic",
    y="Gap Count",
    title="Enrollment Gaps by Count (and Percent)",
    text="Gap Label",
    color="Gap Count",
    color_continuous_scale="RdBu",
    height=400
)
bar_fig.update_traces(texttemplate='%{text}', textposition='outside')
bar_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(bar_fig)

# ---------- Strategy Recommendations ----------

if gender_gap["Female"] > 5:
    st.markdown("### 👩 Female Underrepresentation Strategies")
    st.write("- Connect with Alzheimer's research registries")
    st.write("- Collaborate with women-led organizations")
    st.write("- Emphasize legacy/future generation impact")
    st.write("- Offer flexible scheduling and childcare")
    if lp_required == "Yes":
        st.warning("Female underrepresentation combined with lumbar puncture requirement may cause fear or confusion. Provide educational materials explaining the difference between lumbar punctures and epidurals to reduce anxiety and improve trust.")

if gender_gap["Male"] > 5:
    st.markdown("### 👨 Male Underrepresentation Strategies")
    st.write("- Highlight relevance to brain health and family leadership roles")
    st.write("- Emphasize convenience and low time commitment")
    st.write("- Partner with male-focused community organizations or barbershop networks")
    st.write("- Share testimonials from other male participants to reduce stigma")
    st.write("- Provide transportation or remote visit options")
for race, gap in race_gap.items():
    if gap > 5:
        st.markdown(f"### 🧑🏽 {race} Underrepresentation Strategies")
        if race == "African American":
            st.write("- Partner with barbershops, churches, and historically Black institutions")
            st.write("- Use trusted community figures and storytelling")
        elif race == "Hispanic":
            st.write("- Offer materials and consent forms in Spanish")
            st.write("- Partner with Latino community health workers and cultural centers")
        elif race == "Asian":
            st.write("- Engage multilingual Asian outreach coordinators")
            st.write("- Respect cultural norms around elder care and decision making")
        elif race == "Other":
            st.write("- Tailor messaging to reflect local minority populations")
            st.write("- Collaborate with grassroots or refugee support orgs")
        elif race == "White":
            st.write("- Use broad national outreach campaigns and digital health tools")
        st.write("- Return personal results as incentive")
        st.write("- Address medical mistrust transparently")
        st.write("- Tailor messaging to leaving a legacy for future generations")
        st.write("- Ensure culturally-tailored messaging is used")
        st.write("- Make sure the trial team is diverse to increase comfortability")
        st.write(f"- Increase awareness campaigns tailored to {race} communities")

# ---------- Optional Radar Chart Demo (for a single persona) ----------
# Optional section placeholder. Add your radar chart code below if needed.
