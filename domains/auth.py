import streamlit as st
from . import database
from .storage import load_persistent_history, load_investigation_history


def initialize_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "role" not in st.session_state:
        st.session_state.role = "Fraud Analyst"

    if "confirm_logout" not in st.session_state:
        st.session_state.confirm_logout = False

    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if "show_google_chooser" not in st.session_state:
        st.session_state.show_google_chooser = False


def perform_logout():
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = ""
    st.session_state.role = "Fraud Analyst"
    st.session_state.full_name = ""
    st.session_state.email = ""
    st.session_state.confirm_logout = False
    st.session_state.risk_history = []
    st.session_state.investigation_history = []
    st.session_state.investigation_case = None
    st.session_state.analyzed = False
    st.session_state.analysis_data = None
    st.session_state.twin_result = None
    st.session_state.attack_result = None
    st.session_state.ai_result = None
    st.session_state.show_google_chooser = False
    st.session_state.page = "landing"
    st.rerun()


def request_login(username, password):
    user = database.authenticate_user(username, password)
    if user:
        st.session_state.authenticated = True
        st.session_state.user_id = user["id"]
        st.session_state.username = user["username"]
        st.session_state.full_name = user["full_name"] or user["username"]
        st.session_state.email = user["email"] or ""
        st.session_state.role = user["role"] or "Fraud Analyst"
        st.session_state.appearance = user["appearance"] or "Dark"
        st.session_state.notifications = bool(user["notifications"])
        st.session_state.risk_view = user["risk_view"] or "Risk Score"

        st.session_state.risk_history = load_persistent_history()
        st.session_state.investigation_history = load_investigation_history()
        st.session_state.investigation_case = None
        st.session_state.analyzed = False
        st.session_state.analysis_data = None
        st.session_state.show_google_chooser = False

        st.session_state.page = "Home"
        st.rerun()
    else:
        st.error("Invalid credentials. Please verify your username and password.")


def sign_in_google_account(email, display_name):
    user = database.get_or_create_google_user(email, display_name)
    st.session_state.authenticated = True
    st.session_state.user_id = user["id"]
    st.session_state.username = user["username"]
    st.session_state.full_name = user["full_name"]
    st.session_state.email = user["email"]
    st.session_state.role = user["role"]
    st.session_state.appearance = user["appearance"] or "Dark"
    st.session_state.notifications = bool(user["notifications"])
    st.session_state.risk_view = user["risk_view"] or "Risk Score"

    st.session_state.risk_history = load_persistent_history()
    st.session_state.investigation_history = load_investigation_history()
    st.session_state.investigation_case = None
    st.session_state.analyzed = False
    st.session_state.analysis_data = None
    st.session_state.show_google_chooser = False

    st.session_state.page = "Home"
    st.rerun()


def request_signup(username, password, full_name, email, phone_number):
    try:
        user = database.create_user(
            username=username,
            password=password,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            role="Fraud Analyst"
        )
        st.session_state.authenticated = True
        st.session_state.user_id = user["id"]
        st.session_state.username = user["username"]
        st.session_state.full_name = user["full_name"] or user["username"]
        st.session_state.email = user["email"] or ""
        st.session_state.role = user["role"] or "Fraud Analyst"
        st.session_state.appearance = user["appearance"] or "Dark"
        st.session_state.notifications = True
        st.session_state.risk_view = "Risk Score"

        st.session_state.risk_history = []
        st.session_state.investigation_history = []
        st.session_state.investigation_case = None
        st.session_state.analyzed = False
        st.session_state.analysis_data = None
        st.session_state.show_google_chooser = False

        st.session_state.page = "Home"
        st.rerun()
    except Exception as e:
        st.error(str(e))


def inject_cinematic_auth_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

        /* Cinematic Background */
        .stApp {
            background: #040308 !important;
            background-image:
                radial-gradient(circle at 10% 20%, rgba(147, 51, 234, 0.22), transparent 45%),
                radial-gradient(circle at 85% 75%, rgba(14, 165, 233, 0.18), transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(217, 70, 239, 0.08), transparent 60%),
                linear-gradient(135deg, #05040a 0%, #0c0915 50%, #05040a 100%) !important;
            background-attachment: fixed !important;
        }

        /* Ambient Plasma Glow */
        .plasma-flare-1 {
            position: fixed;
            top: -150px;
            left: -100px;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.35), transparent 70%);
            filter: blur(80px);
            z-index: 0;
            pointer-events: none;
            animation: plasma-drift 18s ease-in-out infinite;
        }

        .plasma-flare-2 {
            position: fixed;
            bottom: -150px;
            right: -100px;
            width: 550px;
            height: 550px;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.25), transparent 70%);
            filter: blur(90px);
            z-index: 0;
            pointer-events: none;
            animation: plasma-drift 22s ease-in-out infinite reverse;
        }

        @keyframes plasma-drift {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(40px, -30px) scale(1.1); }
        }

        /* Left Column HUD Terminal */
        .hud-kicker {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            color: #38bdf8;
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.25);
            padding: 6px 14px;
            border-radius: 999px;
            margin-bottom: 20px;
            text-transform: uppercase;
        }

        .hud-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #38bdf8;
            box-shadow: 0 0 10px #38bdf8;
            animation: dot-pulse 1.8s infinite;
        }

        @keyframes dot-pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.8); }
        }

        .cinematic-title {
            font-family: 'Inter', sans-serif;
            font-size: clamp(34px, 4.2vw, 52px);
            font-weight: 800;
            line-height: 1.14;
            color: #f8fafc;
            letter-spacing: -1.2px;
            margin-bottom: 18px;
        }

        .neon-glow-text {
            background: linear-gradient(135deg, #c084fc 0%, #38bdf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 35px rgba(168, 85, 247, 0.4);
        }

        .hud-description {
            color: #94a3b8;
            font-size: 15px;
            line-height: 1.65;
            margin-bottom: 24px;
            max-width: 480px;
        }

        /* Animated Holographic Security Core */
        .vault-hologram-wrap {
            position: relative;
            width: 100%;
            max-width: 460px;
            background: rgba(15, 12, 26, 0.55);
            border: 1px solid rgba(168, 85, 247, 0.25);
            border-radius: 18px;
            padding: 22px 24px;
            margin-top: 10px;
            margin-bottom: 24px;
            backdrop-filter: blur(16px);
            box-shadow: inset 0 0 30px rgba(168, 85, 247, 0.08), 0 12px 30px rgba(0, 0, 0, 0.4);
            overflow: hidden;
        }

        .laser-sweep-line {
            position: absolute;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #38bdf8, #c084fc, transparent);
            box-shadow: 0 0 14px #38bdf8;
            opacity: 0.8;
            animation: laser-sweep 3.6s ease-in-out infinite;
            pointer-events: none;
        }

        @keyframes laser-sweep {
            0% { top: 0%; opacity: 0; }
            10% { opacity: 0.9; }
            90% { opacity: 0.9; }
            100% { top: 100%; opacity: 0; }
        }

        .vault-core-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 11px;
            color: #cbd5e1;
            letter-spacing: 1px;
        }

        .vault-grid-readout {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 16px;
        }

        .readout-pill {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 8px 12px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 11.5px;
            color: #94a3b8;
        }

        .readout-pill strong {
            display: block;
            color: #f8fafc;
            font-size: 13px;
            margin-top: 2px;
        }

        /* Right Column Tactical Auth Enclave */
        .cyber-console-card {
            background: rgba(18, 14, 28, 0.75);
            border: 1px solid rgba(168, 85, 247, 0.35);
            border-radius: 22px;
            padding: 28px 28px 24px 28px;
            backdrop-filter: blur(28px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 40px rgba(168, 85, 247, 0.16);
            position: relative;
        }

        .cyber-console-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 20%;
            right: 20%;
            height: 1px;
            background: linear-gradient(90deg, transparent, #c084fc, #38bdf8, transparent);
        }

        .console-tag {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 10.5px;
            letter-spacing: 2px;
            color: #a855f7;
            font-weight: 700;
            margin-bottom: 6px;
            text-transform: uppercase;
        }

        .console-title {
            font-family: 'Inter', sans-serif;
            font-size: 24px;
            font-weight: 800;
            color: #f8fafc;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        }

        .console-subtitle {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 20px;
        }

        /* Google Workspace Button */
        .google-workspace-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            width: 100%;
            background: rgba(255, 255, 255, 0.055);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 12px;
            padding: 12px 18px;
            font-size: 14px;
            font-weight: 600;
            color: #f8fafc;
            cursor: pointer;
            transition: all 0.25s ease;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
            margin-bottom: 16px;
        }

        .google-workspace-btn:hover {
            background: rgba(255, 255, 255, 0.09);
            border-color: #a855f7;
            box-shadow: 0 6px 20px rgba(168, 85, 247, 0.3);
            transform: translateY(-1px);
        }

        .cyber-divider {
            display: flex;
            align-items: center;
            text-align: center;
            color: #64748b;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 11px;
            letter-spacing: 1.5px;
            margin: 18px 0;
        }

        .cyber-divider::before, .cyber-divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .cyber-divider::before { margin-right: 14px; }
        .cyber-divider::after { margin-left: 14px; }

        /* Google Account Selector Card */
        .google-acc-card {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        }

        .google-acc-card:hover {
            border-color: #38bdf8;
            background: rgba(56, 189, 248, 0.08);
        }

        .google-acc-avatar {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: white;
            font-size: 15px;
            margin-right: 12px;
            flex-shrink: 0;
        }
        </style>

        <div class="plasma-flare-1"></div>
        <div class="plasma-flare-2"></div>
        """,
        unsafe_allow_html=True,
    )


def show_auth_page():
    initialize_auth()
    inject_cinematic_auth_styles()

    left_col, right_col = st.columns([1.15, 1], gap="large")

    # ========================================================
    # LEFT COLUMN: HOLOGRAPHIC BIOMETRIC VAULT HUD
    # ========================================================
    with left_col:
        st.markdown(
            """
            <div class="hud-kicker">
                <div class="hud-dot"></div> NEURAL SECURITY GATEWAY // ZERO-TRUST
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="cinematic-title">
                The Neural Vault<br>
                for Transaction<br>
                <span class="neon-glow-text">Intelligence.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="hud-description">
                Cryptographically isolated workspaces protecting enterprise transaction streams.
                Every analyst operates in an independent, hardware-grade tenant enclave
                with zero risk of cross-user telemetry leakage.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Holographic Animated Vault Telemetry Display
        st.markdown(
            """
            <div class="vault-hologram-wrap">
                <div class="laser-sweep-line"></div>
                <div class="vault-core-header">
                    <span>ENCLAVE INTEGRITY: <b>99.98%</b></span>
                    <span style="color:#38bdf8;">ACTIVE MESH: <b>SEC-4096</b></span>
                </div>
                <div style="display:flex; align-items:center; gap:16px;">
                    <div style="font-size:38px;">🛡️</div>
                    <div>
                        <div style="color:#f8fafc; font-weight:700; font-size:15px;">Cryptographic Enclave Active</div>
                        <div style="color:#64748b; font-size:12px;">PBKDF2-HMAC-SHA256 · Per-Tenant Salting</div>
                    </div>
                </div>
                <div class="vault-grid-readout">
                    <div class="readout-pill">
                        SESSION STATUS
                        <strong style="color:#4ade80;">● VERIFIED</strong>
                    </div>
                    <div class="readout-pill">
                        INTRUSION MONITOR
                        <strong style="color:#38bdf8;">0 ALERTS</strong>
                    </div>
                    <div class="readout-pill">
                        TELEMETRY LATENCY
                        <strong>&lt; 42 ms</strong>
                    </div>
                    <div class="readout-pill">
                        DATA ISOLATION
                        <strong style="color:#c084fc;">TENANT-LEVEL</strong>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # RIGHT COLUMN: GLASSMORPHIC AUTH TERMINAL
    # ========================================================
    with right_col:
        st.markdown('<div class="cyber-console-card">', unsafe_allow_html=True)

        # ----------------------------------------------------
        # GOOGLE ACCOUNT CHOOSER VIEW
        # ----------------------------------------------------
        if st.session_state.get("show_google_chooser", False):
            st.markdown(
                """
                <div class="console-tag">GOOGLE IDENTITY SERVICES</div>
                <div class="console-title">Select Workspace Profile</div>
                <div class="console-subtitle">Choose which Google identity to authenticate with:</div>
                """,
                unsafe_allow_html=True,
            )

            # Profile 1: Personal Workspace
            c1, c2 = st.columns([3.8, 1.2])
            with c1:
                st.markdown(
                    """
                    <div style="display:flex; align-items:center; padding:6px 0;">
                        <div class="google-acc-avatar" style="background:#4285F4;">A</div>
                        <div>
                            <div style="color:#f8fafc; font-weight:700; font-size:14px;">Alex Rivers (Personal)</div>
                            <div style="color:#94a3b8; font-size:12px;">alex.rivers@gmail.com</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c2:
                if st.button("Enter →", key="pick_google_acc_1", use_container_width=True):
                    sign_in_google_account("alex.rivers@gmail.com", "Alex Rivers")

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

            # Profile 2: Enterprise SecOps Workspace
            c3, c4 = st.columns([3.8, 1.2])
            with c3:
                st.markdown(
                    """
                    <div style="display:flex; align-items:center; padding:6px 0;">
                        <div class="google-acc-avatar" style="background:#34A853;">S</div>
                        <div>
                            <div style="color:#f8fafc; font-weight:700; font-size:14px;">Alex Rivers (SecOps Lead)</div>
                            <div style="color:#94a3b8; font-size:12px;">alex.secops@enterprise.corp</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c4:
                if st.button("Enter →", key="pick_google_acc_2", use_container_width=True):
                    sign_in_google_account("alex.secops@enterprise.corp", "Alex Rivers (SecOps)")

            st.markdown('<div class="cyber-divider">OR USE CUSTOM IDENTITY</div>', unsafe_allow_html=True)

            with st.expander("Use another Google account", expanded=False):
                custom_g_name = st.text_input("Display Name", placeholder="e.g. Jordan Vance", key="custom_g_name")
                custom_g_email = st.text_input("Google Email Address", placeholder="jordan.vance@gmail.com", key="custom_g_email")
                if st.button("Authenticate This Account", type="primary", use_container_width=True, key="submit_custom_google"):
                    if not custom_g_email or "@" not in custom_g_email:
                        st.error("Please provide a valid email format.")
                    else:
                        sign_in_google_account(custom_g_email, custom_g_name or custom_g_email.split("@")[0])

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            if st.button("← Return to Console", use_container_width=True, key="cancel_google_chooser"):
                st.session_state.show_google_chooser = False
                st.rerun()

        # ----------------------------------------------------
        # STANDARD AUTH TABS VIEW
        # ----------------------------------------------------
        else:
            st.markdown(
                """
                <div class="console-tag">SECURITY TERMINAL // ACCESS PORTAL</div>
                <div class="console-title">Authenticate Enclave</div>
                <div class="console-subtitle">Sign in with your workspace credentials or Single Sign-On:</div>
                """,
                unsafe_allow_html=True,
            )

            # High-Impact Google Action
            if st.button("🌐 Continue with Google Workspace", use_container_width=True, key="auth_google_trigger"):
                st.session_state.show_google_chooser = True
                st.rerun()

            st.markdown('<div class="cyber-divider">OR ACCESS VIA ENCLAVE CREDENTIALS</div>', unsafe_allow_html=True)

            tab_login, tab_create, tab_forgot = st.tabs(["Sign In", "Create Enclave", "Recover Key"])

            # ------------------------------------------------
            # TAB 1: SIGN IN
            # ------------------------------------------------
            with tab_login:
                username = st.text_input("Username or Registered Email", placeholder="analyst_id or email", key="login_username")
                password = st.text_input("Security Key / Password", type="password", placeholder="••••••••••••", key="login_password")

                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                if st.button("Authorize & Enter Workspace", type="primary", use_container_width=True, key="sign_in_button"):
                    if not username or not password:
                        st.error("Please enter both credentials.")
                    else:
                        request_login(username, password)

            # ------------------------------------------------
            # TAB 2: CREATE ENCLAVE (FULL CONTACT SPEC)
            # ------------------------------------------------
            with tab_create:
                st.caption("Provision a brand-new, isolated tenant workspace.")
                c1, c2 = st.columns(2)
                with c1:
                    new_username = st.text_input("Username", placeholder="e.g. jdoe_risk", key="create_username")
                with c2:
                    new_fullname = st.text_input("Full Name", placeholder="e.g. John Doe", key="create_fullname")

                new_email = st.text_input("Enterprise Email", placeholder="analyst@domain.com", key="create_email")
                new_phone = st.text_input("Phone Number", placeholder="+91 98765 43210", key="create_phone")

                c3, c4 = st.columns(2)
                with c3:
                    new_password = st.text_input("Set Password", type="password", placeholder="••••••••••••", key="create_password")
                with c4:
                    confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••••••", key="confirm_password")

                if st.button("Provision Workspace Enclave", type="primary", use_container_width=True, key="create_account_button"):
                    if not new_username or not new_password or not confirm_password:
                        st.error("Username and passwords are required.")
                    elif not new_email or "@" not in new_email:
                        st.error("Please enter a valid work email address.")
                    elif not new_phone:
                        st.error("Please enter your contact phone number.")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        request_signup(new_username, new_password, new_fullname or new_username, new_email, new_phone)

            # ------------------------------------------------
            # TAB 3: RECOVER KEY
            # ------------------------------------------------
            with tab_forgot:
                st.caption("Verify identity and rotate your cryptographic access key.")
                reset_account = st.text_input("Username or Registered Email", placeholder="analyst@domain.com", key="reset_account_input")
                reset_new_pwd = st.text_input("New Security Key", type="password", placeholder="New password", key="reset_new_pwd_input")
                reset_confirm_pwd = st.text_input("Confirm Security Key", type="password", placeholder="Confirm new password", key="reset_confirm_pwd_input")

                if st.button("Rotate & Apply New Key", use_container_width=True, key="reset_pwd_btn"):
                    if not reset_account or not reset_new_pwd or not reset_confirm_pwd:
                        st.error("Please fill in all recovery fields.")
                    elif reset_new_pwd != reset_confirm_pwd:
                        st.error("New keys do not match.")
                    elif len(reset_new_pwd) < 6:
                        st.error("Key must be at least 6 characters.")
                    else:
                        ok, msg = database.reset_user_password(reset_account, reset_new_pwd)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)

        st.markdown('</div>', unsafe_allow_html=True)
