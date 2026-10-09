import sys
from pathlib import Path
import streamlit as st

# ============================================================
# PATH SETUP
# ============================================================

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="FraudTwin",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# IMPORTS
# ============================================================

from domains.config import NAV_PAGES
from domains.state import initialize_state
from domains.ui import inject_css, risk_badge_html
from domains.auth import (
    initialize_auth,
    show_auth_page,
    perform_logout,
)
from domains.landing import show_landing_page
from domains.home import page_home
from domains.analysis import page_transaction_analysis
from domains.investigation import page_investigation_center
from domains.reports import page_reports
from domains import setting


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="ft-side-brand">FraudTwin</div>'
            '<div class="ft-side-sub">AI-Powered Transaction Risk Intelligence</div>'
            '<div class="ft-side-label">Navigation</div>',
            unsafe_allow_html=True,
        )

        navigation_pages = list(NAV_PAGES)
        if "Settings" not in navigation_pages:
            navigation_pages.append("Settings")

        current_page = st.session_state.get("page", "Home")

        for index, nav_item in enumerate(navigation_pages):
            is_current = (nav_item == current_page)
            if st.button(
                nav_item,
                key=f"sidebar_nav_{index}",
                type="primary" if is_current else "secondary",
                use_container_width=True,
            ):
                st.session_state.page = nav_item
                st.session_state.confirm_logout = False
                st.rerun()

        st.markdown("<div class='ft-side-divider'></div>", unsafe_allow_html=True)

        if st.session_state.get("analyzed", False) and st.session_state.get("analysis_data"):
            data = st.session_state.analysis_data
            st.markdown('<div class="ft-side-current">', unsafe_allow_html=True)
            st.markdown('<div class="ft-side-current-label">CURRENT TRANSACTION</div>', unsafe_allow_html=True)

            if "level" in data and "icon" in data:
                st.markdown(risk_badge_html(data["level"], data["icon"]), unsafe_allow_html=True)

            if "amount" in data:
                st.markdown(
                    f'<div class="ft-side-current-value">₹{float(data["amount"]):,.2f}</div>',
                    unsafe_allow_html=True,
                )

            if "hour" in data:
                st.markdown(
                    f'<div style="color:#AAA3B5 !important; font-size:11.5px; margin-top:5px;">'
                    f'Transaction time · {int(data["hour"]):02d}:00</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div class='ft-side-divider'></div>", unsafe_allow_html=True)

        username = st.session_state.get("username", "User")
        role = st.session_state.get("role", "Fraud Analyst")
        st.markdown(
            f"""
            <div style="color:#AAA3B5; font-size:11.5px; line-height:1.6; margin-bottom:10px;">
                Workspace user: <strong style="color:#F5F3F7;">{username}</strong><br>
                Role: <span style="color:#C4B5FD;">{role}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Log out", use_container_width=True, key="sidebar_logout"):
            perform_logout()

        st.markdown("<div class='ft-side-divider'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="color:#AAA3B5; font-size:11.5px; line-height:1.6;">
                Analyze transactions · Investigate alerts · Review reports
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# PAGE ROUTER
# ============================================================

def route_page():
    page = st.session_state.get("page", "landing")
    authenticated = st.session_state.get("authenticated", False)

    if page == "landing":
        if authenticated:
            st.session_state.page = "Home"
            st.rerun()
        show_landing_page()
        return

    if page == "auth":
        if authenticated:
            st.session_state.page = "Home"
            st.rerun()

        if st.button("← Back to Landing Page", key="back_to_landing_page"):
            st.session_state.page = "landing"
            st.rerun()

        show_auth_page()
        return

    if not authenticated:
        st.session_state.page = "landing"
        st.rerun()

    appearance = st.session_state.get("appearance", "Dark")
    theme = appearance if appearance in ("Dark", "Light") else "Dark"

    inject_css(theme)
    render_sidebar()

    if page == "Home" or page == "🏠 Home":
        page_home()
    elif page == "Analyze" or page == "🔍 Analyze":
        page_transaction_analysis()
    elif page == "Investigate" or page == "🕵️ Investigate":
        page_investigation_center()
    elif page == "Reports" or page == "📈 Reports":
        page_reports()
    elif page == "Settings":
        setting.show_settings_page()
    else:
        st.session_state.page = "Home"
        st.rerun()


# ============================================================
# MAIN
# ============================================================

def main():
    initialize_auth()
    initialize_state()
    route_page()


if __name__ == "__main__":
    main()
