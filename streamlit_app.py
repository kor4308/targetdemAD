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
    st.markdown("<h3 style='font-size:22px;'>🧪 Trial Characteristics</h3>", unsafe_allow_html=True)
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

    target_groups = ["Male White", "Female White", "Male African American", "Female African American",
                     "Male Hispanic", "Female Hispanic", "Male Asian", "Female Asian", "Male Other", "Female Other"]

    target_counts = {}
    target_total = 0
    for group in target_groups:
        target_counts[group] = st.number_input(f"Target {group} %", 0, 100, 5, key=f"t_{group}")
        target_total += target_counts[group]

    if target_total != 100:
        st.error(f"Target group percentages must total 100%. Current total: {target_total}%")

# Current Enrollment (Right)
with top_col3:
    st.markdown("## 📍 Current Enrollment")
    current_enrollment = st.number_input("Current Total Enrollment", min_value=0, value=800)

    current_counts = {}
    current_total = 0
    for group in target_groups:
        current_counts[group] = st.number_input(f"Current {group} %", 0, 100, 5, key=f"c_{group}")
        current_total += current_counts[group]

    if current_total != 100:
        st.error(f"Current group percentages must total 100%. Current total: {current_total}%")

st.markdown(f"**🎯 Target Total Enrollment:** {total_enrollment} participants")
st.markdown(f"**📍 Current Total Enrollment:** {current_enrollment} participants")

# ---------- Enrollment Visualization & Strategies ----------

group_gap = {}
target_vals = []
current_vals = []
diffs = []

for group in target_groups:
    t_count = target_counts[group] / 100 * total_enrollment
    c_count = current_counts[group] / 100 * current_enrollment
    target_vals.append(t_count)
    current_vals.append(c_count)
    diff = t_count - c_count
    diffs.append(diff)
    group_gap[group] = diff

# Visualization
graph_col, table_col = st.columns([2, 1])
with graph_col:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=target_groups,
        y=target_vals,
        name='Target',
        marker_color='lightgrey'
    ))
    fig.add_trace(go.Bar(
        x=target_groups,
        y=current_vals,
        name='Current',
        marker_color='steelblue'
    ))
    fig.update_layout(barmode='overlay', title='Enrollment by Group', height=400)
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
    st.dataframe(pd.DataFrame(table_data))

# Strategies Section
st.markdown("---")
st.header("📌 Strategy Recommendations Based on Gaps")

for group in target_groups:
    if group_gap[group] > 0:
        st.subheader(f"🧑🏽 {group} Underrepresentation Strategies")
        st.write("- Emphasize impact on future generations")
        st.write("- Culturally-tailored messaging")
        st.write("- Ensure diverse study team to build trust")
        if "Male" in group:
            st.write("- Advertise at sports games and male-dominated venues")
            st.write("- Frame participation as contributing to science and legacy")
            st.write("- Reduce perceived stigma around cognitive testing")
        if "Female" in group:
            st.write("- Connect with Alzheimer's research registries")
            st.write("- Collaborate with women-led organizations")
            st.write("- Offer flexible scheduling and childcare")
