import streamlit as st


def inject_landing_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        #MainMenu, header, footer {visibility: hidden;}

        .stApp {
            background: #08070d;
            background-image:
                radial-gradient(ellipse 600px 350px at 15% 20%, rgba(168, 85, 247, 0.16), transparent 70%),
                radial-gradient(ellipse 500px 300px at 85% 65%, rgba(59, 130, 246, 0.12), transparent 70%),
                linear-gradient(135deg, #07060a 0%, #0d0b14 100%);
            background-attachment: fixed;
            overflow-x: hidden;
        }

        /* Top Navbar */
        .top-navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 28px;
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            backdrop-filter: blur(16px);
            margin-bottom: 32px;
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .nav-logo-badge {
            width: 34px;
            height: 34px;
            border-radius: 10px;
            background: linear-gradient(135deg, #a855f7, #6d28d9);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 14px;
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(168, 85, 247, 0.4);
        }

        .nav-title {
            font-size: 19px;
            font-weight: 800;
            color: #f5f3ff;
            letter-spacing: -0.4px;
        }

        .nav-status {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(74, 222, 128, 0.10);
            border: 1px solid rgba(74, 222, 128, 0.28);
            border-radius: 999px;
            padding: 4px 12px;
            font-size: 11px;
            font-weight: 700;
            color: #86efac;
        }

        .nav-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #4ade80;
            box-shadow: 0 0 8px rgba(74, 222, 128, 0.8);
        }

        /* Hero Typography */
        .hero-kicker {
            display: inline-block;
            color: #c084fc;
            font-size: 11.5px;
            letter-spacing: 2.5px;
            font-weight: 700;
            margin-bottom: 16px;
            padding: 5px 14px;
            border: 1px solid rgba(168, 85, 247, 0.30);
            border-radius: 999px;
            background: rgba(168, 85, 247, 0.08);
            text-transform: uppercase;
        }

        .hero-heading {
            font-size: clamp(34px, 4.4vw, 54px);
            font-weight: 800;
            line-height: 1.14;
            color: #f6f4fb;
            letter-spacing: -1.2px;
            margin-bottom: 18px;
        }

        .gradient-text {
            background: linear-gradient(135deg, #c084fc 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .hero-description {
            color: #a49bb8;
            font-size: 15.5px;
            line-height: 1.65;
            margin-bottom: 26px;
            max-width: 520px;
        }

        .trust-row {
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 22px;
            color: #7a7288;
            font-size: 12px;
            font-weight: 600;
        }

        .trust-item {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: #948da3;
        }

        /* Right Column Radar Telemetry Card */
        .radar-telemetry-card {
            background: linear-gradient(160deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.015) 100%);
            border: 1px solid rgba(168, 85, 247, 0.25);
            border-radius: 20px;
            padding: 24px 26px;
            backdrop-filter: blur(20px);
            box-shadow: 0 24px 48px rgba(0, 0, 0, 0.45), 0 0 40px rgba(168, 85, 247, 0.12);
            position: relative;
            overflow: hidden;
        }

        .radar-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
        }

        .radar-card-label {
            color: #cabdea;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.2px;
        }

        .radar-score-num {
            font-size: 38px;
            font-weight: 800;
            color: #f5f3ff;
            letter-spacing: -0.6px;
        }

        .radar-score-sub {
            font-size: 13px;
            font-weight: 700;
            margin-top: 2px;
        }

        .radar-bars-container {
            display: flex;
            align-items: flex-end;
            gap: 7px;
            height: 68px;
            margin: 18px 0;
            padding: 4px 0;
        }

        .radar-bar {
            flex: 1;
            border-radius: 5px 5px 2px 2px;
            background: linear-gradient(180deg, #c084fc, #7c3aed);
            opacity: 0.85;
            transition: height 0.3s ease;
        }

        .radar-card-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            padding-top: 14px;
            color: #8a8298;
            font-size: 11.5px;
        }

        .radar-card-footer b {
            color: #d9d3e8;
        }

        /* Metric Ticker Strip */
        .ticker-strip {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-top: 48px;
            margin-bottom: 32px;
            padding: 22px 26px;
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 16px;
        }

        .ticker-stat {
            font-size: 26px;
            font-weight: 800;
            color: #f5f3ff;
            letter-spacing: -0.5px;
        }

        .ticker-desc {
            font-size: 12px;
            color: #948da3;
            font-weight: 500;
            margin-top: 4px;
        }

        /* Feature Pillars */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            margin-bottom: 40px;
        }

        .feat-card {
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
            padding: 22px;
            transition: all 0.2s ease;
        }

        .feat-card:hover {
            border-color: rgba(168, 85, 247, 0.35);
            transform: translateY(-2px);
        }

        .feat-num {
            font-size: 11px;
            font-weight: 800;
            color: #a855f7;
            background: rgba(168, 85, 247, 0.14);
            padding: 3px 8px;
            border-radius: 6px;
            display: inline-block;
            margin-bottom: 12px;
        }

        .feat-title {
            color: #f5f3ff;
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .feat-text {
            color: #948da3;
            font-size: 13px;
            line-height: 1.55;
        }

        @media (max-width: 900px) {
            .ticker-strip { grid-template-columns: repeat(2, 1fr); }
            .feature-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_landing_page():
    inject_landing_styles()

    # 1. Sleek Top Navbar
    st.markdown(
        """
        <div class="top-navbar">
            <div class="nav-brand">
                <div class="nav-logo-badge">FT</div>
                <div>
                    <span class="nav-title">FraudTwin</span>
                    <span style="color:#7a7288; font-size:12px; margin-left:8px;">· Risk Intelligence Platform</span>
                </div>
            </div>
            <div class="nav-status">
                <div class="nav-dot"></div> Live Detection Engine
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Main 2-Column Responsive Hero
    left_col, right_col = st.columns([1.15, 1], gap="large")

    with left_col:
        st.markdown('<div class="hero-kicker">🛡️ AI TRANSACTION RISK INTELLIGENCE</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="hero-heading">
                Understand risk<br>
                before it becomes<br>
                <span class="gradient-text">fraud.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="hero-description">
                FraudTwin unifies machine learning fraud scoring, contextual heuristics,
                explainable AI drivers, counterfactual what-if simulation, and isolated
                case management into one seamless, user-specific workspace.
            </div>
            """,
            unsafe_allow_html=True,
        )

        b1, b2 = st.columns([1.1, 1.2])
        with b1:
            if st.button("Launch Workspace →", type="primary", use_container_width=True, key="landing_launch_btn"):
                st.session_state.page = "auth"
                st.session_state.show_google_chooser = False
                st.rerun()

        with b2:
            if st.button("🌐 Sign In with Google", use_container_width=True, key="landing_google_btn"):
                st.session_state.page = "auth"
                st.session_state.show_google_chooser = True
                st.rerun()

        st.markdown(
            """
            <div class="trust-row">
                <span class="trust-item">⚡ &lt; 42ms Latency</span>
                <span class="trust-item">🔒 Strict Tenant Isolation</span>
                <span class="trust-item">🛡️ SOC-2 Ready</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        # Dynamic interactive preview
        sim_amt = st.session_state.get("landing_sim_amount", 50000.0)

        if sim_amt >= 90000:
            p_score = 88.5
            p_label = "HIGH EXPOSURE"
            p_color = "#f87171"
            bars = [60, 85, 92, 78, 95, 88, 70]
        elif sim_amt >= 40000:
            p_score = 64.2
            p_label = "MODERATE FLAGGED"
            p_color = "#fbbf24"
            bars = [42, 60, 72, 55, 68, 50, 45]
        else:
            p_score = 21.4
            p_label = "NOMINAL TRUSTED"
            p_color = "#4ade80"
            bars = [22, 30, 26, 32, 28, 20, 24]

        bars_html = "".join(f'<div class="radar-bar" style="height:{h}%;"></div>' for h in bars)

        st.markdown(
            f"""
            <div class="radar-telemetry-card">
                <div class="radar-card-header">
                    <span class="radar-card-label">SIMULATED STREAM · MERCHANT #4471</span>
                    <span style="font-size:11px; font-weight:700; color:{p_color};">● {p_label}</span>
                </div>
                <div>
                    <span class="radar-score-num">{p_score:.1f}</span>
                    <span style="font-size:18px; color:#948da3;">/100</span>
                    <div class="radar-score-sub" style="color:{p_color};">
                        Risk Intelligence Delta · ₹{sim_amt:,.0f}
                    </div>
                </div>
                <div class="radar-bars-container">{bars_html}</div>
                <div class="radar-card-footer">
                    <span>Latency: <b>38 ms</b></span>
                    <span>ML Engine: <b>XGBoost + SHAP</b></span>
                    <span>Decision: <b>{p_label.split()[0]}</b></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        new_val = st.slider(
            "Interactive Simulation Slider (₹):",
            min_value=5000.0,
            max_value=150000.0,
            value=sim_amt,
            step=5000.0,
            key="landing_slider_widget",
        )
        if new_val != sim_amt:
            st.session_state.landing_sim_amount = new_val
            st.rerun()

    # 3. High-Impact Metrics Strip
    st.markdown(
        """
        <div class="ticker-strip">
            <div>
                <div class="ticker-stat">₹140M+</div>
                <div class="ticker-desc">Transactions Scored</div>
            </div>
            <div>
                <div class="ticker-stat">99.6%</div>
                <div class="ticker-desc">Decision Precision</div>
            </div>
            <div>
                <div class="ticker-stat">&lt; 42 ms</div>
                <div class="ticker-desc">Inference Latency</div>
            </div>
            <div>
                <div class="ticker-stat">100%</div>
                <div class="ticker-desc">Tenant Data Isolation</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4. Feature Architecture Grid
    st.markdown(
        """
        <div class="feature-grid">
            <div class="feat-card">
                <span class="feat-num">01</span>
                <div class="feat-title">Calibrated ML Scoring</div>
                <div class="feat-text">30-feature statistical classifier combining transaction amount, timing, and anonymized PCA telemetry.</div>
            </div>
            <div class="feat-card">
                <span class="feat-num">02</span>
                <div class="feat-title">Explainable SHAP Signals</div>
                <div class="feat-text">Mathematical feature decomposition displaying exact indicators that pushed risk scores up or down.</div>
            </div>
            <div class="feat-card">
                <span class="feat-num">03</span>
                <div class="feat-title">What-If Digital Twin</div>
                <div class="feat-text">Test counterfactual hypotheses and coordinate attack stress testing before live fraud strikes.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
