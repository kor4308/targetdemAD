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

    target_groups = ["Male White", "Female White", "Male African American", "Female African American",
                     "Male Hispanic", "Female Hispanic", "Male Asian", "Female Asian", "Male Other", "Female Other"]

    target_counts = {}
    target_total = 0
    for group in target_groups:
        target_counts[group] = st.number_input(f"Target {group} %", 0, 100, 10, key=f"t_{group}")
        count_val = int(target_counts[group] / 100 * total_enrollment)
        st.caption(f"{count_val} participants")
        target_total += target_counts[group]

    if target_total != 100:
        st.error(f"Target group percentages must total 100%. Current total: {target_total}%")

    gender_rollup = {"Male": 0, "Female": 0}
    race_rollup = {"White": 0, "African American": 0, "Hispanic": 0, "Asian": 0, "Other": 0}

    for group in target_groups:
        gender = group.split()[0]
        race = group[len(gender)+1:]
        count_val = target_counts[group] / 100 * total_enrollment
        gender_rollup[gender] += count_val
        race_rollup[race] += count_val

    st.markdown("### Overall Totals (Target Enrollment)")
    for gender, val in gender_rollup.items():
        st.markdown(f"- {gender}: {int(val)} participants")
    for race, val in race_rollup.items():
        st.markdown(f"- {race}: {int(val)} participants")

# Current Enrollment (Right)
with top_col3:
    st.markdown("<h3 style='font-size:26px;'>📍 Current Enrollment (Count)</h3>", unsafe_allow_html=True)
    current_enrollment = st.number_input("Current Total Enrollment", min_value=0, value=1000, key="current_enrollment")

    current_counts = {}
    current_total = 0
    for group in target_groups:
        current_counts[group] = st.number_input(f"Current {group} Count", 0, value=80, key=f"c_{group}")
        current_total += current_counts[group]
        percent_val = (current_counts[group] / current_enrollment) * 100 if current_enrollment > 0 else 0
        st.caption(f"{percent_val:.1f}%")

st.markdown(f"**🎯 Target Total Enrollment:** {total_enrollment} participants")
st.markdown(f"**📍 Current Total Enrollment:** {current_enrollment} participants")

# ---------- Enrollment Visualization & Strategies ----------

group_gap = {}
target_vals = []
current_vals = []
diffs = []

for group in target_groups:
    t_count = target_counts[group] / 100 * total_enrollment
    c_count = current_counts[group]
    target_vals.append(t_count)
    current_vals.append(c_count)
    diff = t_count - c_count
    diffs.append(diff)
    group_gap[group] = diff

# Roll-up totals for gender and race
gender_totals = {"Male": 0, "Female": 0}
current_gender_totals = {"Male": 0, "Female": 0}
race_totals = {"White": 0, "African American": 0, "Hispanic": 0, "Asian": 0, "Other": 0}
current_race_totals = {"White": 0, "African American": 0, "Hispanic": 0, "Asian": 0, "Other": 0}

for group in target_groups:
    gender = group.split()[0]
    race = group[len(gender)+1:]
    race_totals[race] += target_counts[group] / 100 * total_enrollment
    current_race_totals[race] += current_counts[group]
    gender_totals[gender] += target_counts[group] / 100 * total_enrollment
    current_gender_totals[gender] += current_counts[group]

# Combine data for visualization
bar_data = []
for race in race_totals:
    bar_data.append({"Group": race, "Type": "Target", "Count": race_totals[race]})
    bar_data.append({"Group": race, "Type": "Current", "Count": current_race_totals[race]})

for gender in gender_totals:
    bar_data.append({"Group": gender, "Type": "Target", "Count": gender_totals[gender]})
    bar_data.append({"Group": gender, "Type": "Current", "Count": current_gender_totals[gender]})

bar_df = pd.DataFrame(bar_data)

# Visualization
graph_col, table_col = st.columns([2, 1])
with graph_col:
    fig = px.bar(bar_df, x="Group", y="Count", color="Type", barmode="overlay",
                 color_discrete_map={"Target": "lightgrey", "Current": "steelblue"}, height=400, opacity=0.7)
    fig.update_layout(title="Enrollment by Race and Gender")
    st.plotly_chart(fig)

with table_col:
    st.markdown("#### 📋 Enrollment Table")
    table_data = []
    for i, group in enumerate(target_groups):
        abs_change = diffs[i]
        pct_change = (abs_change / target_vals[i]) * 100 if target_vals[i] != 0 else 0
        table_data.append({
            "Group": group,
            "Target Count": int(target_vals[i]),
            "Current Count": int(current_vals[i]),
            "Change Needed (n)": int(abs_change),
            "Change Needed (%)": f"{pct_change:+.1f}%"
        })
    table_df = pd.DataFrame(table_data)
    table_df = table_df.sort_values(by="Change Needed (n)", ascending=False)
    st.dataframe(table_df)

# Strategies Section
st.markdown("---")
display_disease = disease if disease else "this condition"
st.header(f"📌 Strategy Recommendations Based on Gaps in {display_disease}")

emoji_map = {
    "White": "🧑🏻",
    "African American": "🧑🏿",
    "Hispanic": "🧑🏽",
    "Asian": "🧑🏻\u200d🦱",
    "Other": "🧑🏻",
    "Male": "👨",
    "Female": "👩"
}

def print_female_strategies():
    st.write("- Connect with research registries")
    st.write("- Collaborate with women-led organizations")
    st.write("- Offer flexible scheduling and childcare")
    if disease == "Alzheimer's" and lp_required == "Yes":
        st.write("- Educate on difference between lumbar punctures and epidurals to reduce fear")

def print_male_strategies():
    st.write("- Advertise at sports games and male-dominated venues")
    st.write("- Frame participation as contributing to science and legacy")
    st.write("- Reduce perceived stigma around cognitive testing")

def print_race_strategies(race):
    st.subheader(f"{emoji_map[race]} {race} Participants - Underrepresentation Strategies")
    st.write("- Emphasize impact on future generations")
    st.write("- Culturally-tailored messaging")
    st.write("- Ensure diverse study team to build trust")

gender_flags = {"Male": False, "Female": False}
race_flags = {"White": False, "African American": False, "Hispanic": False, "Asian": False, "Other": False}

sorted_gaps = sorted(group_gap.items(), key=lambda x: x[1], reverse=True)
for group, gap in sorted_gaps:
    if gap > 0:
        gender = group.split()[0]
        race = group[len(gender)+1:]
        if not race_flags[race]:
            print_race_strategies(race)
            race_flags[race] = True
        if not gender_flags[gender]:
            st.subheader(f"{emoji_map[gender]} {gender} Participants - Underrepresentation Strategies")
            if gender == "Male":
                print_male_strategies()
            else:
                print_female_strategies()
            gender_flags[gender] = True
