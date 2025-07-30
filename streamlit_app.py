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

with col3.expander("Estimated Quantity Needed to Screen"):
    st.markdown("**Estimated Quantity Needed to Screen - Gender**")
    st.caption("⬇️ List is in order from greatest % population needed to screen")
    total_enroll = st.session_state.get("total_enroll", 1000)

    gender_data = []
    for key in target["Gender"]:
        pct = st.session_state.get(f"gender_{key}", target["Gender"][key])
        target_n = total_enroll * (pct / 100)
        screen_success_rate = st.session_state.get(f"sf_gender_{key}", 100) / 100
        screened_needed = math.ceil(target_n / screen_success_rate) if screen_success_rate > 0 else 0
        eligible_pop = int((target["Gender"].get(key, 100) / 100) * total_disease_pop)
        screen_percent = (screened_needed / eligible_pop) * 100 if eligible_pop > 0 else 0
        gender_data.append((key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop))

    gender_data.sort(key=lambda x: -x[2])
    for key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop in gender_data:
        st.markdown(f"{key}: {screened_needed:,} ({screen_percent:.3f}%)")
        st.caption(f"Approximately {screen_percent:.3f}% of {key} {disease} population must be screened to enroll target")

    st.markdown("**Estimated Quantity Needed to Screen - Race**")
    st.caption("⬇️ List is in order from greatest % population needed to screen")
    race_data = []
    for key in target["Race"]:
        pct = st.session_state.get(f"race_{key}", target["Race"][key])
        target_n = total_enroll * (pct / 100)
        screen_success_rate = st.session_state.get(f"sf_race_{key}", 100) / 100
        screened_needed = math.ceil(target_n / screen_success_rate) if screen_success_rate > 0 else 0
        eligible_pop = int((target["Race"].get(key, 0) / 100) * total_disease_pop)
        screen_percent = (screened_needed / eligible_pop) * 100 if eligible_pop > 0 else 0
        race_data.append((key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop))

    race_data.sort(key=lambda x: -x[2])
    for key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop in race_data:
        st.markdown(f"{key}: {screened_needed:,} ({screen_percent:.3f}%)")
        st.caption(f"Approximately {screen_percent:.3f}% of {key} {disease} population must be screened to enroll target")

    if st.toggle("Show Calculation Steps"):
        st.markdown("### Calculation Breakdown")
        for category, data in [("Gender", gender_data), ("Race", race_data)]:
            st.markdown(f"**{category} Calculations**")
            for key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop in data:
                st.text(f"{key}: Target = {target_n:.1f}, Screen Success Rate = {screen_success_rate:.2f}, Eligible Pop = {eligible_pop}, Screened Needed = {screened_needed}, Percent = {screen_percent:.3f}%")

# --- General Recruitment Strategies Section ---
st.markdown("---")
st.header(f"General Motivators and Barriers for {disease}")
st.caption("These motivators and barriers can be explored through Patient dossiers.")
if disease != "Alzheimer's":
    st.caption("Each group below includes an estimate of the % of the {disease} population that must be screened to meet enrollment targets.")

if disease == "Alzheimer's":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Motivators")
        st.markdown("- Trusted Voices")
        st.markdown("- Altruism")
        st.markdown("- Education & Disease Awareness")
        st.markdown("- Personal Benefit")
        st.markdown("- Emphasize that memory loss is not just a part of the aging process")
        st.markdown("""
<details>
<summary><strong>Sources</strong></summary>
<a href='https://www.alz.org/help-support/resources/asian-americans-and-alzheimers' target='_blank'>Alzheimer's Association Resource</a>
</details>

<details>
<summary><strong>Solutions</strong></summary>
<a href='https://www.canva.com/design/DAGuITbntEI/jfZ6fArnWEWgH-KC9V2BNA/view?utm_content=DAGuITbntEI&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hf3030029bc' target='_blank'>Canva Educational Graphic</a>
</details>
""", unsafe_allow_html=True)

    with col2:
        st.subheader("⛔ Barriers")
        st.markdown("- Study Partner Requirement")
        st.markdown("- Procedure/Investigational Burden")
        st.markdown("- Disease Stigma")
        st.markdown("- Specific Population Injustices")

# --- Recruitment Strategies for Subgroups ---
st.markdown("---")
st.subheader(f"📣 Recruitment Strategies for Focus Populations with {disease}")

if disease == "Alzheimer's":
    st.caption("⬇️ List is in order from greatest % population needed to screen; thus greatest need to focus")

    recruitment_strategies = {
        "Female": [
            "Connect with women's health networks and caregiving support groups",
            "Partner with research registries",
            "Provide flexible study visit schedules or caregiver support"
        ],
        "Male": [
            "Target outreach through male-dominated environments such as sporting events",
            "Promote messaging around benefitting future generations",
            "Address stigma around mental health and participation"
        ],
        "African American": [
            "Engage trusted faith-based and civic leaders",
            "Highlight historical medical distrust and steps taken to ensure ethical practices",
            "Avoid or reassess the need for MMSE and logical memory scoring inclusion criteria as these can be inequitable barriers."
        ],
        "Hispanic": [
            "Use Spanish-language materials and bilingual coordinators",
            "Partner with local Hispanic/Latino organizations and clinics",
            "Avoid or reassess the need for MMSE and logical memory scoring as these can be barriers."
        ]
    }

    mmse_keywords = [
        "MMSE and logical memory scoring inclusion criteria",
        "MMSE and logical memory scoring"
    ]

    combined_data = gender_data + race_data
    seen = set()
    sorted_groups = []
    for group, _, screen_percent, *_ in sorted(combined_data, key=lambda x: -x[2]):
        if group not in seen:
            seen.add(group)
            sorted_groups.append(group)

    for group in sorted_groups:
        if group in recruitment_strategies:
            match = next((x for x in (gender_data + race_data) if x[0] == group), None)
            if match:
                _, _, screen_percent, *_ = match
                st.markdown(f"### {group}")
                st.caption(f"Approximately {screen_percent:.3f}% of {group} {disease} population must be screened to enroll target")
                for strategy in recruitment_strategies[group]:
                    st.markdown(f"- {strategy}", unsafe_allow_html=True)
                    if any(keyword in strategy for keyword in mmse_keywords):
                        st.markdown("""
<details>
<summary><strong>Sources</strong></summary>
<ul>
<li><a href='https://pubmed.ncbi.nlm.nih.gov/34228129/' target='_blank'>PubMed Article</a></li>
<li><a href='https://pmc.ncbi.nlm.nih.gov/articles/PMC10171211/' target='_blank'>PMC Article</a></li>
</ul>
</details>

<details>
<summary><strong>Solutions</strong></summary>
Consider a switch of inclusion/exclusion to Montreal Cognitive Assessment (MoCA).<br>
<strong>Sources:</strong> <a href='https://pmc.ncbi.nlm.nih.gov/articles/PMC4562190/' target='_blank'>PMC Article</a>
</details>
""", unsafe_allow_html=True)
            st.markdown("---")
else:
    st.caption(f"Recruitment strategies for {disease} are currently being further explored.")
