import json
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Speech & LLM Quality Lab",
    layout="wide"
)

st.title("Speech & LLM Quality Lab")

STATE_CONFIG = {
    "pending": "Pending",
    "failed": "Failed",
    "incomplete": "Incomplete",
    "unavailable": "Unavailable",
}


def state_badge(state: str):
    return STATE_CONFIG.get(state, "Unavailable")

def load_llm_cases():
    cases = []

    cases_dir = Path("data/llm_cases")

    if not cases_dir.exists():
        return cases

    for file in sorted(cases_dir.glob("*.json")):
        with open(file, "r", encoding="utf-8") as f:
            cases.append(json.load(f))

    return cases


tabs = st.tabs([
    "Overview",
    "Data Quality",
    "ASR Analysis",
    "LLM Review",
    "End-to-End",
    "Regression",
    "Reports",
    "Configuration",
])

# ------------------------------------------------------------------
# Overview
# ------------------------------------------------------------------

with tabs[0]:
    st.subheader("Welcome to Speech & LLM Quality Lab")

    st.write("Evaluate and understand the quality of your speech and language pipeline, from audio to transcripts to LLM outputs.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### Approved Audio")
        st.write("Not available")
        st.caption("No approved recordings")

    with col2:
        st.markdown("### Processed")
        st.write("Not available")
        st.caption("No processed cases")

    with col3:
        st.markdown("### WER")
        st.write("Not available")
        st.caption("No evaluated references")

    with col4:
        st.markdown("### LLM Reviews")
        st.write("Not available")
        st.caption("No completed reviews")

    st.divider()

    st.info("No project data available yet.")

# Another line

    left, right = st.columns([2,1])

    with left:
        st.markdown("### Getting started")
        st.markdown("""
            1. Perpare approved speech samples  
            
            2. Validate references  

            3. Run asr analysis  

            4. Review illustrative LLM cases

            5. Generate reports
                    """)
        st.button("#### Import audio\nAdd your own audio files",
                  use_container_width=True)
        st.button("#### Open sample cases\nTry examples data(French)" ,
                  use_container_width=True)

    with right:
        st.markdown("### Recent Activity")
        st.info("No recent activity available")


# ------------------------------------------------------------------
# Data Quality
# ------------------------------------------------------------------

with tabs[1]:
    st.subheader("Data Quality")

    st.write(f"Status: {state_badge('unavailable')}")

    st.info("No recordings or references available.")

# ------------------------------------------------------------------
# ASR Analysis
# ------------------------------------------------------------------

with tabs[2]:
    st.subheader("ASR Analysis")

    st.write(f"Status: {state_badge('unavailable')}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Reference")
        st.info("Not available")

    with col2:
        st.markdown("### Prediction")
        st.info("Not available")

    st.markdown("### Metrics")

    col3, col4 = st.columns(2)

    with col3:
        st.metric("WER", "Not available")

    with col4:
        st.metric("CER", "Not available")

# ------------------------------------------------------------------
# LLM Review
# ------------------------------------------------------------------

with tabs[3]:
    st.subheader("LLM Review")

    st.write(f"Status: {state_badge('unavailable')}")

    st.warning(
        "Illustrative review cases are separate from real model performance."
    )

    cases = load_llm_cases()

    st.write("Number of cases loaded:", len(cases))

    for case in cases:

        with st.expander(case["title"]):

            st.write(f"Case ID: {case['id']}")
            st.write(f"Source: {case['source']}")
            st.write(f"Type: {case['type']}")

            st.markdown("### Review Rubric")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Correctness: Not rated")
                st.write("Grounding: Not rated")

            with col2:
                st.write("Completeness: Not rated")
                st.write("Revision: Not available")

# ------------------------------------------------------------------
# End-to-End
# ------------------------------------------------------------------

with tabs[4]:
    st.subheader("End-to-End")

    st.write(f"Status: {state_badge('unavailable')}")

    st.info(
        "End-to-end workflow results are not available."
    )

# ------------------------------------------------------------------
# Regression
# ------------------------------------------------------------------

with tabs[5]:
    st.subheader("Regression")

    st.write(f"Status: {state_badge('unavailable')}")

    st.info(
        "Regression comparisons are not available."
    )

# ------------------------------------------------------------------
# Reports
# ------------------------------------------------------------------

with tabs[6]:
    st.subheader("Reports")

    st.write(f"Status: {state_badge('unavailable')}")

    st.info(
        "Export and reporting functionality is not available."
    )

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

with tabs[7]:
    st.subheader("Configuration")

    st.write(f"Status: {state_badge('unavailable')}")

    st.info(
        "Configuration management is not available."
    )
