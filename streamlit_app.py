import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math

st.set_page_config(layout="wide")

# --- Constants ---
SCHIZOPHRENIA_TARGET = {
    "Gender": {"Female": 40.0, "Male": 60.0},
    "Race": {
        "Hispanic": 15.0,
        "White, NH": 30.0,
        "African American": 25.0,
        "Asian, NH": 10.0,
        "AIAN, NH": 10.0,
        "NHPI, NH": 5.0,
        "Other": 5.0
    }
}

US_CENSUS = {
    "Gender": {"Female": 50.5, "Male": 49.5},
    "Race": {
        "Hispanic": 17.6,
        "White, NH": 61.1,
        "African American": 12.3,
        "Asian, NH": 6.3,
        "AIAN, NH": 0.7,
        "NHPI, NH": 0.2,
        "Other": 1.8
    }
}

US_65PLUS = {
    "Gender": {"Female": 50.9, "Male": 49.1},
    "Race": {
        "Hispanic": 8.8,
        "White, NH": 76.6,
        "African American": 9.2,
        "Asian, NH": 4.5,
        "AIAN, NH": 0.7,
        "NHPI, NH": 0.1,
        "Other": 3.4
    }
}

ALZHEIMERS_TARGET = {
    "Gender": {"Female": 64.0, "Male": 36.0},
    "Race": {
        "Hispanic": 21.2,
        "White, NH": 51.7,
        "African American": 19.2,
        "Asian, NH": 5.9,
        "AIAN, NH": 0.8,
        "NHPI, NH": 0.3,
        "Other": 0.9
    }
}

BIPOLAR_TARGET = {
    "Gender": {"Female": 51.0, "Male": 49.0},
    "Race": {
        "Hispanic": 18.5,
        "White, NH": 53.0,
        "African American": 16.0,
        "Asian, NH": 7.0,
        "AIAN, NH": 1.0,
        "NHPI, NH": 0.5,
        "Other": 4.0
    }
}

DISEASE_TOTALS = {
    "Alzheimer's_18+": 7100000,
    "Alzheimer's_65+": 6900000,
    "Schizophrenia": 3200000,
    "Bipolar Disorder": 3100000
}

DISEASE_PREVALENCE = {
    "Alzheimer's": {
        "screen_success": {
            "Female": 0.3,
            "Male": 0.7,
            "White, NH": 0.75,
            "African American": 0.35,
            "Hispanic": 0.28,
            "Asian, NH": 0.50,
            "AIAN, NH": 0.50,
            "NHPI, NH": 0.50,
            "Other": 0.50
        },
        "screen_fail": {}
    },
    "Schizophrenia": {
        "screen_fail": {k: 0.5 for k in ["Female", "Male", "White, NH", "African American", "Hispanic", "Asian, NH", "AIAN, NH", "NHPI, NH", "Other"]}
    },
    "Bipolar Disorder": {
        "screen_fail": {k: 0.5 for k in ["Female", "Male", "White, NH", "African American", "Hispanic", "Asian, NH", "AIAN, NH", "NHPI, NH", "Other"]}
    }
}

st.title("US vs Target Demographic Comparator")

time_period = None  # Ensure time_period is always defined
trial = None  # Ensure trial is always defined

therapeutic_area = st.selectbox("Select Therapeutic Area", ["(Select)", "Neuro", "Oncology", "Cardiometabolic"], index=0)
disease = st.selectbox("Select Disease", ["(Select)", "Alzheimer's", "Bipolar Disorder", "Schizophrenia", "Other"], index=0)
if disease == "Alzheimer's":
    trial = st.selectbox("Select Trial", ["(Select)", "Reveli", "South Commons", "Custom"], index=0, key="trial_selection")

    # Add time period dropdown if Reveli is selected
    if trial == "Reveli":
        time_period = st.selectbox("Select Time Period", ["August 2025", "October 2025", "January 2026"], index=0, key="reveli_time")

col2, col3 = st.columns([1, 1])

# Determine U.S. total population and disease population
if disease in ["Alzheimer's", "Alzheimer's disease"]:
    US_TOTAL_POP = 55792501
    current_us = US_65PLUS
else:
    US_TOTAL_POP = 342_000_000
    current_us = US_CENSUS

pop_key = f"{disease}_65+" if disease == "Alzheimer's" else disease

target = ALZHEIMERS_TARGET if disease == "Alzheimer's" else BIPOLAR_TARGET if disease == "Bipolar Disorder" else SCHIZOPHRENIA_TARGET

race_categories = list(target["Race"].keys())

total_disease_pop = DISEASE_TOTALS.get(pop_key, US_TOTAL_POP)

with col2:
    with st.expander("Target Enrollment Inputs"):
        total_enroll = st.number_input("Total Enrollment Target", min_value=100, max_value=1000000, value=1000, step=100, key="total_enroll")

        gender_total = 0
        st.markdown("**Gender Target % and Screen Success**")
        st.caption("Target % comes from disease population and screen success information, doi: 10.1001/jamanetworkopen.2021.14364, although does not include all races (such as missing NHPI and AIAN)")
        for key, value in target["Gender"].items():
            cols = st.columns([2, 2])
            with cols[0]:
                st.number_input(f"{key} (%)", min_value=0.0, max_value=100.0, value=value, step=0.1, key=f"gender_{key}")
                updated_val = st.session_state.get(f"gender_{key}", value)
                gender_total += updated_val
                st.caption(f"Targeting {int(total_enroll * (updated_val / 100)):,} {key} participants")
            with cols[1]:
                default_success = DISEASE_PREVALENCE["Alzheimer's"].get("screen_success", {}).get(key, 0.5) * 100
                st.number_input("Screen Success %", min_value=0.0, max_value=100.0, value=default_success, step=1.0, key=f"sf_gender_{key}")

        if abs(gender_total - 100.0) > 0.01:
            st.markdown(f":red[Total Gender %: {gender_total:.1f}%]")
        else:
            st.markdown(f":green[Total Gender %: {gender_total:.1f}%]")

        st.markdown("**Race Target % and Screen Success**")
        race_total = 0
        for key, value in target["Race"].items():
            cols = st.columns([2, 2])
            with cols[0]:
                st.number_input(f"{key} (%)", min_value=0.0, max_value=100.0, value=value, step=0.1, key=f"race_{key}")
                updated_val = st.session_state.get(f"race_{key}", value)
                race_total += updated_val
                if key == "Other":
                    st.caption(f"Targeting {int(total_enroll * (updated_val / 100)):,} participants from other or multiple races")
                else:
                    st.caption(f"Targeting {int(total_enroll * (updated_val / 100)):,} {key} participants")
            with cols[1]:
                default_success = DISEASE_PREVALENCE["Alzheimer's"].get("screen_success", {}).get(key, 0.5) * 100
                st.number_input("Screen Success %", min_value=0.0, max_value=100.0, value=default_success, step=1.0, key=f"sf_race_{key}")

        if abs(race_total - 100.0) > 0.01:
            st.markdown(f":red[Total Race %: {race_total:.1f}%]")
        else:
            st.markdown(f":green[Total Race %: {race_total:.1f}%]")

with col3:
    with st.expander("📍 Current Enrollment (Count)"):
        current_enrollment = 1000
        if trial == "Reveli" and time_period == "August 2025":
            current_gender_male = 400
            current_gender_female = 100
            current_gender_diverse = 1000 - current_gender_male - current_gender_female
            current_race = {
                "Hispanic": 199,
                "White, NH": 500,
                "African American": 180,
                "Asian, NH": 5,
                "AIAN, NH": 7,
                "NHPI, NH": 2,
                "Other": 8
            }
        elif trial == "Reveli" and time_period == "January 2026":
            current_gender_male = 360
            current_gender_female = 640
            current_gender_diverse = 1000 - current_gender_male - current_gender_female
            current_race = {
                "Hispanic": 212,
                "White, NH": 517,
                "African American": 192,
                "Asian, NH": 59,
                "AIAN, NH": 8,
                "NHPI, NH": 3,
                "Other": 9
            }
        else:
            current_gender_male = st.number_input("Current Male Count", 0, value=450, key="current_male")
            current_gender_female = st.number_input("Current Female Count", 0, value=450, key="current_female")
            current_gender_diverse = 1000 - current_gender_male - current_gender_female
            st.markdown(f"Current Gender-Diverse Count: **{current_gender_diverse}**")
            st.caption(f"{(current_gender_diverse / 1000) * 100:.1f}%")
            st.subheader("Race Distribution")
            current_race = {}
            for race in race_categories:
                current_race[race] = st.number_input(f"Current {race} Count", 0, value=80, key=f"c_{race}")
                percent_val = (current_race[race] / 1000) * 100
                st.caption(f"{percent_val:.1f}%")

# --- Horizontal Bar Chart ---
target_gender_male = st.session_state.get("gender_Male", target["Gender"].get("Male", 0))
target_gender_female = st.session_state.get("gender_Female", target["Gender"].get("Female", 0))
target_gender_diverse = 100 - target_gender_male - target_gender_female

bar_data = pd.DataFrame({
    "Group": ["Male", "Female", "Gender-Diverse"] + race_categories,
    "Target": [
        int(target_gender_male / 100 * total_enroll),
        int(target_gender_female / 100 * total_enroll),
        int(target_gender_diverse / 100 * total_enroll)
    ] + [int(st.session_state.get(f"race_{r}", target["Race"].get(r, 0)) / 100 * total_enroll) for r in race_categories],
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
    title="Target vs Current Enrollment by Group",
    xaxis_title="Participant Count",
    height=600
)

st.plotly_chart(fig)

# --- Recruitment Strategies ---
st.markdown("---")
st.subheader("General Motivators and Barriers for (Select)")
st.markdown("### Asian Recruitment Strategies")
st.markdown("- Leverage trusted community centers and Asian language media")
st.markdown("- Emphasize confidentiality, physician trust, and family involvement")

st.markdown("### Other Recruitment Strategies")
st.markdown("- Culturally tailored materials")
st.markdown("- Address transportation and time barriers")
st.markdown("- Engage community leaders and local organizations")        current_enrollment = 1000
        if trial == "Reveli" and time_period == "August 2025":
            current_gender_male = 400
            current_gender_female = 100
            current_gender_diverse = 1000 - current_gender_male - current_gender_female
            current_race = {
                "Hispanic": 199,
                "White, NH": 500,
                "African American": 180,
                "Asian, NH": 5,
                "AIAN, NH": 7,
                "NHPI, NH": 2,
                "Other": 8
            }
        elif trial == "Reveli" and time_period == "January 2026":
            current_gender_male = 360
            current_gender_female = 640
            current_gender_diverse = 1000 - current_gender_male - current_gender_female
            current_race = {
                "Hispanic": 212,
                "White, NH": 517,
                "African American": 192,
                "Asian, NH": 59,
                "AIAN, NH": 8,
                "NHPI, NH": 3,
                "Other": 9
            }
        else:
            current_gender_male = st.number_input("Current Male Count", 0, value=450, key="current_male")
            current_gender_female = st.number_input("Current Female Count", 0, value=450, key="current_female")
            current_gender_diverse = 1000 - current_gender_male - current_gender_female
            st.markdown(f"Current Gender-Diverse Count: **{current_gender_diverse}**")
            st.caption(f"{(current_gender_diverse / 1000) * 100:.1f}%")
            st.subheader("Race Distribution")
            current_race = {}
            for race in race_categories:
                current_race[race] = st.number_input(f"Current {race} Count", 0, value=80, key=f"c_{race}")
                percent_val = (current_race[race] / 1000) * 100
                st.caption(f"{percent_val:.1f}%")
