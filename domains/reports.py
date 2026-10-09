import pandas as pd
import streamlit as st

from .storage import save_risk_history, save_investigation_history
from .ui import (
    ft_bar_chart,
    ft_line_chart,
    section_title,
    stat_card,
)


def page_reports():
    section_title(
        "Reports & Audit Center",
        "Your dedicated risk dashboard, transaction history, trends, and investigation cases"
    )

    history = st.session_state.get("risk_history", [])

    if history:
        df = pd.DataFrame(history)

        total = len(df)
        high = int((df["Risk Level"] == "HIGH RISK").sum())
        medium = int((df["Risk Level"] == "MEDIUM RISK").sum())
        low = int((df["Risk Level"] == "LOW RISK").sum())
        avg_score = df["Risk Score"].astype(float).mean()

        c1, c2, c3, c4 = st.columns(4)
        with c1: stat_card(total, "Transactions Analyzed")
        with c2: stat_card(f"{avg_score:.0f}/100", "Average Risk Score")
        with c3: stat_card(high, "High Risk")
        with c4: stat_card(medium + low, "Medium / Low")

        st.markdown("<div class='ft-divider'></div>", unsafe_allow_html=True)

        left, right = st.columns([1.3, 1])

        with left:
            section_title("Risk score over time")
            chart_df = df.copy()
            chart_df.index = [f"Txn {i + 1}" for i in range(len(chart_df))]
            ft_line_chart(chart_df["Risk Score"], "Risk Intelligence Score")

        with right:
            section_title("Risk distribution")
            dist_df = pd.DataFrame({
                "Level": ["High", "Medium", "Low"],
                "Count": [high, medium, low]
            }).set_index("Level")
            ft_bar_chart(dist_df, "Count", "Count")

        st.markdown("<div class='ft-divider'></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Transaction History", "Investigation Cases"])

    # ----------------------------------------------------
    # TAB 1: TRANSACTION HISTORY
    # ----------------------------------------------------
    with tab1:
        if not history:
            st.info("No transaction history in your workspace yet. Analyze a transaction to create your first record.")
        else:
            df = pd.DataFrame(history)
            c1, c2, c3 = st.columns(3)
            with c1: stat_card(len(df), "Transactions Analyzed")
            with c2: stat_card(int((df["Risk Level"] == "HIGH RISK").sum()), "High Risk")
            with c3: stat_card(int((df["Risk Level"] == "MEDIUM RISK").sum()), "Medium Risk")

            display_history = df.copy()
            if "Factors" in display_history.columns:
                display_history = display_history.drop(columns=["Factors"])

            display_history["Amount"] = display_history["Amount"].apply(lambda x: f"₹{float(x):,.2f}")
            display_history["ML Probability"] = display_history["ML Probability"].apply(lambda x: f"{float(x):.2f}%")
            display_history["Context Risk"] = display_history["Context Risk"].apply(lambda x: f"{float(x):.0f}/30")
            display_history["Risk Score"] = display_history["Risk Score"].apply(lambda x: f"{float(x):.2f}/100")

            st.dataframe(display_history, use_container_width=True, hide_index=True)

            highest_risk = max(history, key=lambda x: float(x["Risk Score"]))
            section_title("Highest Risk Transaction")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Highest Risk Score", f"{float(highest_risk['Risk Score']):.2f}/100")
                st.write(f"**Amount:** ₹{float(highest_risk['Amount']):,.2f}")
                st.write(f"**Time:** {highest_risk['Transaction Time']}")
            with c2:
                st.write(f"**Device:** {highest_risk['Device']}")
                st.write(f"**Location:** {highest_risk['Location']}")
                st.write(f"**Decision:** {highest_risk['Decision']}")

            export_df = pd.DataFrame(history)
            if "Factors" in export_df.columns:
                export_df = export_df.drop(columns=["Factors"])
            export_csv = export_df.to_csv(index=False).encode("utf-8")

            e1, e2 = st.columns(2)
            with e1:
                st.download_button(
                    "Export Transaction History (CSV)",
                    data=export_csv,
                    file_name="fraudtwin_transaction_history.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="export_transaction_history"
                )
            with e2:
                if st.button("Clear Transaction History", use_container_width=True, key="clear_transaction_history"):
                    st.session_state.risk_history = []
                    save_risk_history()
                    st.rerun()

    # ----------------------------------------------------
    # TAB 2: INVESTIGATION CASES
    # ----------------------------------------------------
    with tab2:
        investigation_history = st.session_state.get("investigation_history", [])

        if not investigation_history:
            st.info("No investigation cases have been saved in your workspace yet.")
        else:
            inv_df = pd.DataFrame(investigation_history).iloc[::-1].reset_index(drop=True)
            cols = ["Case ID", "Created", "Amount", "Risk Score", "Alert Priority", "Status", "Decision", "Notes"]
            available = [c for c in cols if c in inv_df.columns]

            display_inv = inv_df[available].copy()
            if "Amount" in display_inv.columns:
                display_inv["Amount"] = display_inv["Amount"].apply(lambda v: f"₹{float(v):,.2f}")
            if "Risk Score" in display_inv.columns:
                display_inv["Risk Score"] = display_inv["Risk Score"].apply(lambda v: f"{float(v):.2f}/100")

            st.dataframe(display_inv, use_container_width=True, hide_index=True)
            st.caption(f"📁 {len(investigation_history)} investigation case(s) saved in your workspace.")

            investigation_export_csv = pd.DataFrame(investigation_history).to_csv(index=False).encode("utf-8")

            e1, e2 = st.columns(2)
            with e1:
                st.download_button(
                    "Export Investigation Cases (CSV)",
                    data=investigation_export_csv,
                    file_name="fraudtwin_investigation_cases.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="export_investigation_cases"
                )
            with e2:
                if st.button(
                    "Clear Investigation Cases",
                    use_container_width=True,
                    key="clear_investigation_cases_reports",
                    help="Delete all saved investigation cases in your workspace."
                ):
                    st.session_state["confirm_clear_investigation_cases"] = True
                    st.rerun()

            if st.session_state.get("confirm_clear_investigation_cases", False):
                st.warning("⚠️ This will permanently remove all saved investigation cases from your workspace.")
                c_clear, c_cancel = st.columns(2)
                with c_clear:
                    if st.button("Yes, Clear All Investigation Cases", use_container_width=True, key="confirm_clear_all_investigation_cases"):
                        st.session_state.investigation_history = []
                        st.session_state.investigation_case = None
                        st.session_state.investigation_status = "Open"
                        st.session_state.investigation_notes = ""
                        st.session_state["investigation_status_selector"] = "Open"
                        st.session_state["investigation_notes_input"] = ""
                        save_investigation_history()
                        st.session_state["confirm_clear_investigation_cases"] = False
                        st.success("All saved investigation cases have been cleared.")
                        st.rerun()
                with c_cancel:
                    if st.button("Cancel", use_container_width=True, key="cancel_clear_investigation_cases"):
                        st.session_state["confirm_clear_investigation_cases"] = False
                        st.rerun()
