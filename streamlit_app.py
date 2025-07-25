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
    target_gender_male = st.number_input("Target Male %", 0, 100, 45, key="target_male")
    target_gender_female = st.number_input("Target Female %", 0, 100 - target_gender_male, 45, key="target_female")
    target_gender_diverse = 100 - target_gender_male - target_gender_female
    st.markdown(f"Target Gender-Diverse %: **{target_gender_diverse}%**")

    st.markdown("<br><br>", unsafe_allow_html=True)  # Adjusted spacing for alignment

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
    st.markdown(f"- Gender-Diverse: {int(target_gender_diverse / 100 * total_enrollment)} participants")
    for race in race_categories:
        st.markdown(f"- {race}: {int(target_race[race] / 100 * total_enrollment)} participants")

# Current Enrollment (Right)
with top_col3:
    st.markdown("<h3 style='font-size:26px;'>📍 Current Enrollment (Count)</h3>", unsafe_allow_html=True)
    current_enrollment = st.number_input("Current Total Enrollment", min_value=0, value=1000, key="current_enrollment")

    st.subheader("Gender Distribution")
    current_gender_male = st.number_input("Current Male Count", 0, value=450, key="current_male")
    current_gender_female = st.number_input("Current Female Count", 0, value=450, key="current_female")
    current_gender_diverse = current_enrollment - current_gender_male - current_gender_female
    st.markdown(f"Current Gender-Diverse Count: **{current_gender_diverse}**")
    st.caption(f"{(current_gender_diverse / current_enrollment) * 100:.1f}%")

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

# Add bar chart visualizing gaps
bar_data = pd.DataFrame({
    "Group": ["Male", "Female", "Gender-Diverse"] + race_categories,
    "Target": [
        int(target_gender_male / 100 * total_enrollment),
        int(target_gender_female / 100 * total_enrollment),
        int(target_gender_diverse / 100 * total_enrollment)
    ] + [int(target_race[r] / 100 * total_enrollment) for r in race_categories],
    "Current": [
        current_gender_male,
        current_gender_female,
        current_gender_diverse
    ] + [current_race[r] for r in race_categories]
})

fig = go.Figure()
fig.add_trace(go.Bar(
    y=bar_data["Group"],
    x=bar_data["Target"],
    orientation='h',
    name='Target',
    marker_color='lightgrey'
))
fig.add_trace(go.Bar(
    y=bar_data["Group"],
    x=bar_data["Current"],
    orientation='h',
    name='Current',
    marker_color='steelblue'
))

fig.update_layout(
    barmode='overlay',
    title="Diversity goals for RevEli",
    xaxis_title="Participant Count",
    height=600
)

st.plotly_chart(fig)

# Strategy Recommendations Header
if disease == "Alzheimer's":
    st.header("🧠 Strategy Recommendations Based on Gaps in Alzheimer's Disease")
else:
    st.header("💡 General Strategy Recommendations Based on Gaps")

underrepresented = bar_data[bar_data['Current'] < bar_data['Target']].copy()
underrepresented['Gap'] = underrepresented['Target'] - underrepresented['Current']
underrepresented = underrepresented.sort_values(by='Gap', ascending=False)

if not underrepresented.empty:
    st.caption("🔻 Ordered by largest to smallest gap")
    st.subheader("Gender-Based Strategies")
    for _, row in underrepresented.iterrows():
        if row['Group'] in ["Male", "Female", "Gender-Diverse"]:
            st.markdown(f"**Strategies to reach {row['Group']}**")
            if row['Group'] == "Female" and disease == "Alzheimer's" and lp_required == "Yes":
                st.markdown("- Educate about the difference between lumbar punctures and epidurals to reduce fear and misconceptions.")
            if row['Group'] == "Male":
                st.markdown("- Advertise at sports games and male-focused community events")
            st.markdown("- Emphasize legacy/future generation impact")
            st.markdown("- Provide culturally-tailored messaging")
            st.markdown("- Ensure diverse trial staff to increase comfort and trust")
            st.markdown("- Partner with trusted community leaders")
            st.markdown("- Leverage research registries")

    st.subheader("Race-Based Strategies")
    for _, row in underrepresented.iterrows():
        if row['Group'] not in ["Male", "Female", "Gender-Diverse"]:
            st.markdown(f"**Strategies to reach {row['Group']}**")
            st.markdown("- Emphasize legacy/future generation impact")
            st.markdown("- Provide culturally-tailored messaging")
            st.markdown("- Ensure diverse trial staff to increase comfort and trust")
            st.markdown("- Partner with trusted community leaders")
            st.markdown("- Leverage research registries")
