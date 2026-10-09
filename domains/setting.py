import pandas as pd
import streamlit as st
from . import database
from .auth import perform_logout


def show_settings_page():
    """FraudTwin Enterprise Settings Page (API keys securely hidden on backend)."""

    st.markdown(
        """
        <style>
        .settings-header {
            margin-bottom: 25px;
        }

        .settings-title {
            font-size: 32px;
            font-weight: 700;
            color: var(--ft-text, #F5F3F7);
            margin-bottom: 5px;
        }

        .settings-subtitle {
            color: var(--ft-muted, #AAA3B5);
            font-size: 14px;
        }

        .settings-card {
            background: var(--ft-surface, rgba(20, 17, 30, 0.90));
            border: 1px solid rgba(155, 77, 255, 0.20);
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 20px;
        }

        .settings-card-title {
            color: var(--ft-text, #F5F3F7);
            font-size: 19px;
            font-weight: 650;
            margin-bottom: 5px;
        }

        .settings-card-description {
            color: var(--ft-muted, #AAA3B5);
            font-size: 13px;
            margin-bottom: 20px;
        }

        .profile-avatar {
            width: 75px;
            height: 75px;
            border-radius: 50%;
            background: linear-gradient(135deg, #8B3FF2, #C04CFF);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 15px;
        }

        .profile-name {
            color: var(--ft-text, #F5F3F7);
            font-size: 20px;
            font-weight: 650;
        }

        .profile-role {
            color: var(--ft-muted, #AAA3B5);
            font-size: 13px;
            margin-top: 3px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="settings-header">'
        '<div class="settings-title">Settings &amp; Workspace Controls</div>'
        '<div class="settings-subtitle">Manage profile, algorithmic sensitivity thresholds, webhooks, and audit trails.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    user_id = st.session_state.get("user_id")
    user_record = database.get_user_by_id(user_id) if user_id else {}
    username = st.session_state.get("username", "User")
    current_role = user_record.get("role", st.session_state.get("role", "Fraud Analyst"))

    tab_profile, tab_pref, tab_engine, tab_alerts, tab_audit, tab_sec, tab_about = st.tabs(
        [
            "Profile",
            "Preferences",
            "Risk Engine Tuning",
            "Alerts & Webhooks",
            "Audit & Workspace",
            "Security",
            "About"
        ]
    )

    # =========================================================
    # 1. PROFILE
    # =========================================================
    with tab_profile:
        st.markdown(
            '<div class="settings-card">'
            '<div class="settings-card-title">Profile Information</div>'
            '<div class="settings-card-description">Manage analyst credentials and assigned operational roles.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([1, 2])
        with col1:
            initials = username[:1].upper() if username else "U"
            st.markdown(
                f'<div class="profile-avatar">{initials}</div>'
                f'<div class="profile-name">{username}</div>'
                f'<div class="profile-role">{current_role}</div>',
                unsafe_allow_html=True,
            )

        with col2:
            full_name = st.text_input(
                "Full Name",
                value=user_record.get("full_name", st.session_state.get("full_name", username)),
                key="settings_full_name",
            )
            email = st.text_input(
                "Email Address",
                value=user_record.get("email", st.session_state.get("email", "")),
                placeholder="analyst@domain.com",
                key="settings_email",
            )
            role_options = ["Fraud Analyst", "Risk Analyst", "Senior Investigator", "Security Administrator"]
            role_index = role_options.index(current_role) if current_role in role_options else 0
            role = st.selectbox("Operational Role", role_options, index=role_index, key="settings_role")

            if st.button("Save Profile", type="primary", use_container_width=True):
                st.session_state.full_name = full_name
                st.session_state.email = email
                st.session_state.role = role
                if user_id:
                    database.update_user_profile(user_id, full_name, email, role)
                st.success("Profile updated successfully in your account database.")
                st.rerun()

    # =========================================================
    # 2. PREFERENCES
    # =========================================================
    with tab_pref:
        st.markdown(
            '<div class="settings-card">'
            '<div class="settings-card-title">Workspace Appearance &amp; Layout</div>'
            '<div class="settings-card-description">Customize visual themes, notification states, and telemetry views.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        appearance_options = ["Dark", "Light", "System Default"]
        risk_view_options = ["Risk Score", "Risk Level", "Investigation Priority"]

        saved_appearance = user_record.get("appearance", st.session_state.get("appearance", "Dark"))
        appearance_index = appearance_options.index(saved_appearance) if saved_appearance in appearance_options else 0
        appearance = st.selectbox("Interface Theme", appearance_options, index=appearance_index, key="settings_appearance")

        notifications = st.toggle(
            "Enable Desktop Alert Notifications",
            value=bool(user_record.get("notifications", st.session_state.get("notifications", True))),
            key="settings_notifications",
        )

        saved_risk_view = user_record.get("risk_view", st.session_state.get("risk_view", "Risk Score"))
        risk_view_index = risk_view_options.index(saved_risk_view) if saved_risk_view in risk_view_options else 0
        risk_view = st.selectbox("Default Triage Risk View", risk_view_options, index=risk_view_index, key="settings_risk_view")

        if st.button("Save Preferences", type="primary", use_container_width=True):
            st.session_state.appearance = appearance
            st.session_state.notifications = notifications
            st.session_state.risk_view = risk_view
            if user_id:
                database.update_user_preferences(user_id, appearance, notifications, risk_view)
            st.success("Preferences saved successfully.")
            st.rerun()

    # =========================================================
    # 3. RISK ENGINE TUNING
    # =========================================================
    with tab_engine:
        st.markdown(
            '<div class="settings-card">'
            '<div class="settings-card-title">Algorithmic Risk Engine Calibration</div>'
            '<div class="settings-card-description">Tune decision thresholds, ML weighting, and auto-escalation heuristics.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            high_thresh = st.slider(
                "High Risk Interdiction Threshold (Score >=)",
                min_value=50, max_value=90,
                value=int(user_record.get("high_risk_threshold", 70)),
                help="Transactions scoring above this threshold trigger BLOCK / INVESTIGATE actions."
            )
        with c2:
            med_thresh = st.slider(
                "Medium Risk Authentication Threshold (Score >=)",
                min_value=15, max_value=50,
                value=int(user_record.get("medium_risk_threshold", 30)),
                help="Transactions scoring above this threshold trigger VERIFY / STEP-UP challenges."
            )

        ml_weight = st.slider(
            "ML Statistical Weight vs. Heuristic Context Weight",
            min_value=50, max_value=90,
            value=int(user_record.get("ml_weight_pct", 70)),
            help="Balance between trained XGBoost classification probability and real-time contextual rules."
        )
        st.caption(f"Current weighting ratio: **{ml_weight}% ML Classifier** / **{100 - ml_weight}% Contextual Rules**")

        auto_escalate = st.toggle(
            "Auto-Escalate Severe Attack Simulations",
            value=bool(user_record.get("auto_escalate", 1)),
            help="Automatically open a high-priority investigation case when attack stress scores reach critical levels."
        )

        if st.button("Save Risk Engine Calibration", type="primary", use_container_width=True):
            if user_id:
                database.update_user_thresholds(user_id, high_thresh, med_thresh, ml_weight, auto_escalate)
            st.success("Risk engine sensitivity parameters calibrated successfully.")
            st.rerun()

    # =========================================================
    # 4. ALERTS & WEBHOOKS
    # =========================================================
    with tab_alerts:
        st.markdown(
            '<div class="settings-card">'
            '<div class="settings-card-title">Alert Routing &amp; Webhook Endpoints</div>'
            '<div class="settings-card-description">Configure outbound notification integrations for SIEM, Slack, or PagerDuty.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        alert_chime = st.toggle(
            "Play Audio Chime on Elevated Alerts",
            value=bool(user_record.get("alert_chime", 1)),
        )

        freq_options = ["Instant (Per Transaction)", "Hourly Digest", "Daily Summary", "Off"]
        saved_freq = user_record.get("digest_frequency", "Instant (Per Transaction)")
        freq_idx = freq_options.index(saved_freq) if saved_freq in freq_options else 0
        digest_freq = st.selectbox("Alert Aggregation Frequency", freq_options, index=freq_idx)

        webhook_url = st.text_input(
            "Outbound Webhook URL (Slack, Splunk, PagerDuty)",
            value=user_record.get("webhook_url", "") or "",
            placeholder="https://hooks.slack.com/services/...",
            help="FraudTwin dispatches JSON payloads containing transaction ID, risk scores, and attack vectors."
        )

        if st.button("Save Alert Routing", type="primary", use_container_width=True):
            if user_id:
                database.update_user_notification_settings(user_id, alert_chime, digest_freq, webhook_url)
            st.success("Alert notification and webhook routing saved.")
            st.rerun()

    # =========================================================
    # 5. AUDIT & WORKSPACE DATA
    # =========================================================
    with tab_audit:
        st.markdown(
            '<div class="settings-card">'
            '<div class="settings-card-title">Audit Trail &amp; Workspace Records</div>'
            '<div class="settings-card-description">Review operational activity logs or reset workspace transaction state.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        audit_logs = database.get_user_audit_logs(user_id, limit=15) if user_id else []
        if audit_logs:
            audit_df = pd.DataFrame(audit_logs)
            audit_df.columns = ["Action", "Details", "Timestamp"]
            st.dataframe(audit_df, use_container_width=True, hide_index=True)

            audit_csv = audit_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Export Audit Trail (CSV)",
                data=audit_csv,
                file_name="fraudtwin_audit_trail.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No audit logs recorded for this workspace yet.")

        st.divider()
        st.subheader("Data Lifecycle Management")
        st.caption("Safely wipe all scored transactions and case files while preserving your account credentials.")

        if st.button("Reset Workspace Data", use_container_width=True, key="reset_workspace_btn"):
            st.session_state["confirm_reset_workspace"] = True

        if st.session_state.get("confirm_reset_workspace", False):
            st.warning("Are you sure? This will permanently delete all transaction history and cases in your workspace.")
            c_yes, c_no = st.columns(2)
            with c_yes:
                if st.button("Yes, Clear Workspace Records", use_container_width=True, key="confirm_reset_yes"):
                    if user_id:
                        database.reset_user_workspace_data(user_id)
                    st.session_state.risk_history = []
                    st.session_state.investigation_history = []
                    st.session_state.investigation_case = None
                    st.session_state.analyzed = False
                    st.session_state.analysis_data = None
                    st.session_state["confirm_reset_workspace"] = False
                    st.success("Workspace transaction data reset successfully.")
                    st.rerun()
            with c_no:
                if st.button("Cancel", use_container_width=True, key="confirm_reset_no"):
                    st.session_state["confirm_reset_workspace"] = False
                    st.rerun()

    # =========================================================
    # 6. SECURITY
    # =========================================================
    with tab_sec:
        st.markdown(
            '<div class="settings-card">'
            '<div class="settings-card-title">Security &amp; Session Management</div>'
            '<div class="settings-card-description">Configure authentication policies, password rotation, and active sessions.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.subheader("Session Controls")
        timeout_options = ["15 minutes", "1 hour", "4 hours", "24 hours", "Never"]
        saved_timeout = user_record.get("session_timeout", "4 hours")
        timeout_idx = timeout_options.index(saved_timeout) if saved_timeout in timeout_options else 2
        session_timeout = st.selectbox("Inactivity Session Expiry", timeout_options, index=timeout_idx)

        two_factor = st.toggle(
            "Enforce Multi-Factor Authentication (MFA)",
            value=bool(user_record.get("two_factor_enabled", 0)),
            help="Enforces verification challenges on unrecognized endpoints."
        )

        if st.button("Save Security Options", use_container_width=True):
            if user_id:
                database.update_user_security_options(user_id, session_timeout, two_factor)
            st.success("Security policies updated.")
            st.rerun()

        st.divider()
        st.subheader("Change Password")
        curr_pwd = st.text_input("Current Password", type="password", key="settings_curr_pwd")
        new_pwd = st.text_input("New Password", type="password", key="settings_new_pwd")
        conf_pwd = st.text_input("Confirm New Password", type="password", key="settings_conf_pwd")

        if st.button("Update Account Password", use_container_width=True):
            if not curr_pwd or not new_pwd:
                st.error("Please fill in current and new password fields.")
            elif new_pwd != conf_pwd:
                st.error("New passwords do not match.")
            elif len(new_pwd) < 6:
                st.error("New password must be at least 6 characters.")
            else:
                ok, msg = database.change_user_password(user_id, curr_pwd, new_pwd)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.divider()
        if st.button("Sign Out of Session", use_container_width=True, key="settings_logout_btn"):
            perform_logout()

    # =========================================================
    # 7. ABOUT
    # =========================================================
    with tab_about:
        st.markdown(
            '<div class="settings-card">'
            '<div class="settings-card-title">About FraudTwin Platform</div>'
            '<div class="settings-card-description">Enterprise transaction intelligence and decision support architecture.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Version", "1.2.0")
            st.metric("Architecture", "Multi-Tenant Isolated DB")
        with col2:
            st.metric("ML Engine", "XGBoost + SHAP")
            st.metric("GenAI Engine", "Gemini 2.5 Decision Support")

        st.divider()
        st.write(
            "FraudTwin operates as an integrated intelligence layer across your transaction streams. "
            "It combines real-time statistical modeling with counterfactual what-if analysis and "
            "deep generative AI decision support — ensuring every risk score is defensible, auditable, "
            "and understandable."
        )
        st.caption("FraudTwin — Transaction risk intelligence, defensible and explained.")
