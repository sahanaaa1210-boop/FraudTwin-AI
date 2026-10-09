from datetime import datetime
import streamlit as st
from . import database


def get_current_user_id():
    """Returns the authenticated user's ID or None."""
    return st.session_state.get("user_id")


def load_persistent_history():
    """Loads transaction history for the currently logged-in user."""
    user_id = get_current_user_id()
    if user_id:
        return database.get_user_transactions(user_id)
    return []


def load_investigation_history():
    """Loads investigation cases for the currently logged-in user."""
    user_id = get_current_user_id()
    if user_id:
        return database.get_user_investigations(user_id)
    return []


def save_investigation_history():
    """Persists all cases in session state to the database for this user."""
    user_id = get_current_user_id()
    if not user_id:
        return

    cases = st.session_state.get("investigation_history", [])
    if not cases:
        database.clear_user_investigations(user_id)
    else:
        for case in cases:
            database.save_user_investigation_case(user_id, case)


def save_risk_history():
    """Persists risk history changes (including clearing)."""
    user_id = get_current_user_id()
    if not user_id:
        return

    history = st.session_state.get("risk_history", [])
    if not history:
        database.clear_user_transactions(user_id)


def add_to_risk_history(result):
    """
    Records a scored transaction in both session state and the database
    strictly isolated to the authenticated user.
    """
    history_entry = {
        "Time Recorded": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Amount": result["amount"],
        "Transaction Time": f"{int(result['hour']):02d}:00",
        "Device": result["device"],
        "Location": result["location"],
        "Transaction Type": result["type"],
        "ML Probability": result["probability"] * 100,
        "Context Risk": result["context_score"],
        "Risk Score": result["final_score"],
        "Risk Level": result["level"],
        "Decision": result["decision"],
        "Factors": result.get("factors", []),
    }

    if "risk_history" not in st.session_state:
        st.session_state.risk_history = []

    st.session_state.risk_history.append(history_entry)

    user_id = get_current_user_id()
    if user_id:
        database.add_user_transaction(user_id, result)


def persist_active_case():
    """Persists the currently active investigation case in session state."""
    if st.session_state.get("investigation_case") is None:
        return

    case = st.session_state.investigation_case
    case_id = case.get("Case ID")
    user_id = get_current_user_id()

    history = st.session_state.get("investigation_history", [])
    for index, c in enumerate(history):
        if c.get("Case ID") == case_id:
            history[index] = dict(case)
            break
    else:
        history.append(dict(case))

    st.session_state.investigation_history = history

    if user_id:
        database.save_user_investigation_case(user_id, case)
