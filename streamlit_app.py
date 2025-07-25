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

therapeutic_area = st.selectbox("Select Therapeutic Area", ["(Select)", "Neuro", "Oncology", "Cardiometabolic"], index=0)
disease = st.selectbox("Select Disease", ["(Select)", "Alzheimer's", "Bipolar Disorder", "Schizophrenia", "Other"], index=0)
if disease == "Alzheimer's":
    trial = st.selectbox("Select Trial", ["(Select)", "Reveli", "South Commons", "Custom"], index=0, key="trial_selection")

    # Add time period dropdown if Reveli is selected
    if trial == "Reveli":
        time_period = st.selectbox("Select Time Period", ["August 2025", "October 2025", "January 2026"], index=0, key="reveli_time")

col2, col3 = st.columns([1, 1])

# (continued...)
# Code after this block continues unchanged
