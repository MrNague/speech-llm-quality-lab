import json
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Speech & LLM Quality Lab",
    layout="wide"
)

st.title("Speech & LLM Quality Lab")
st.caption("M5 UI scaffold - no backend wiring")

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

    for fil in sorted(cases_dir.glob("*.json")):
        with open(file, "r", encoding="utf-8") as f:
            cases.append(json.load(f))

    return cases


tabs = st.tabs([
    "Import / Record",
    "Validation",
    "Inference",
    "Reference Review",
    "Metrics",
    "Critical Annotations"
])

with tabs[0]:
    st.subheader("Import / Record")
    st.write(f"Status: {state_badge('unavailable')}")
    st.info("Not available.")

with tabs[1]:
    st.subheader("Validation")
    st.write(f"Status: {state_badge('unavailable')}")
    st.info("Not available.")

with tabs[2]:
    st.subheader("Inference")
    st.write(f"Status: {state_badge('unavailable')}")
    st.info("Not available.")

with tabs[3]:
    st.subheader("Reference Review")

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

with tabs[2]:
    st.subheader("Reference Review")
    st.write(f"Status: {state_badge('unavailable')}")
    st.warning(
        "Illustrative review cases are separate from real model performance."
    )

with tabs[4]:
    st.subheader("Metrics")
    st.write(f"Status: {state_badge('unavailable')}")
    st.info("Not available.")

with tabs[5]:
    st.subheader("Critical Annotations")
    st.write(f"Status: {state_badge('unavailable')}")
    st.info("Not available.")
