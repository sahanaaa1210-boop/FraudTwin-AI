import streamlit as st
from .storage import load_persistent_history, load_investigation_history, persist_active_case


def initialize_state():
    """Initializes session state keys if not already present."""
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if "risk_history" not in st.session_state:
        st.session_state.risk_history = load_persistent_history()

    if "investigation_history" not in st.session_state:
        st.session_state.investigation_history = load_investigation_history()

    if "investigation_status" not in st.session_state:
        st.session_state.investigation_status = "Open"

    if "investigation_notes" not in st.session_state:
        st.session_state.investigation_notes = ""

    if "investigation_case" not in st.session_state:
        st.session_state.investigation_case = None

    if "analyzed" not in st.session_state:
        st.session_state.analyzed = False

    if "analysis_data" not in st.session_state:
        st.session_state.analysis_data = None

    if "twin_result" not in st.session_state:
        st.session_state.twin_result = None

    if "attack_result" not in st.session_state:
        st.session_state.attack_result = None

    if "ai_result" not in st.session_state:
        st.session_state.ai_result = None


def go_to(page_name):
    """Navigates to a specific page."""
    st.session_state.page = page_name
    st.session_state.confirm_logout = False


def mark_case_under_review():
    """Marks current investigation case as Under Review and persists."""
    st.session_state.investigation_status = "Under Review"
    st.session_state.investigation_status_selector = "Under Review"
    if st.session_state.investigation_case:
        st.session_state.investigation_case["Status"] = "Under Review"
        persist_active_case()


def resolve_case():
    """Marks current investigation case as Resolved and persists."""
    decision = st.session_state.get("analysis_data", {}).get("decision", "")
    new_status = "Resolved - Fraud" if "BLOCK" in decision.upper() else "Resolved - Legitimate"
    st.session_state.investigation_status = new_status
    st.session_state.investigation_status_selector = new_status
    if st.session_state.investigation_case:
        st.session_state.investigation_case["Status"] = new_status
        persist_active_case()


def sync_investigation_status():
    """Synchronizes dropdown selection with investigation state."""
    new_val = st.session_state.get("investigation_status_selector")
    if new_val:
        st.session_state.investigation_status = new_val
        if st.session_state.investigation_case:
            st.session_state.investigation_case["Status"] = new_val
            persist_active_case()
