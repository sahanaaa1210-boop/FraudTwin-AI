import os
import time
import streamlit as st
from google import genai


def get_active_gemini_key():
    """Silently retrieves the active Gemini API key from backend secrets or environment."""
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY")
        if secret_key:
            return secret_key.strip()
    except Exception:
        pass

    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key.strip()

    return None


def generate_local_expert_assessment(
    amount, transaction_hour, device, location, transaction_type,
    ml_probability, context_score, final_risk_score, risk_level,
    decision, contextual_factors, attack_score=None, attack_indicators=0
):
    """
    Built-in decision intelligence expert analysis.
    Produces identical structured expert analysis matching all 6 headings.
    """
    bullets = []
    if amount >= 100000:
        bullets.append(f"High Transaction Volume: Amount of INR {amount:,.2f} represents an acute exposure spike.")
    elif amount >= 50000:
        bullets.append(f"Elevated Transaction Value: Amount of INR {amount:,.2f} exceeds standard consumer transaction medians.")

    if device == "New Device":
        bullets.append("Unrecognized Endpoint: Transaction originated from an unverified or new device signature.")
    if location == "Unusual Location":
        bullets.append(f"Geographic Deviation: Location '{location}' diverges from the cardholder's baseline activity.")
    if transaction_hour <= 5:
        bullets.append(f"Circadian Anomaly: Activity recorded at {transaction_hour:02d}:00 hours (overnight off-peak window).")
    if transaction_type == "Large Transfer":
        bullets.append("High-Velocity Rails: Wire/Large Transfer context presents heightened settlement finality risk.")
    
    if not bullets:
        bullets.append("Nominal Parameters: Standard transaction metadata matches trusted profile expectations.")

    bullets_text = "\n".join(f"- {b}" for b in bullets[:5])

    if final_risk_score >= 70 or (attack_score and attack_score >= 70):
        rec_decision = "BLOCK / INVESTIGATE"
        decision_reason = "Multiple concurrent high-entropy fraud signals and elevated risk intelligence score mandate immediate transaction interdiction."
        priority = "CRITICAL"
        priority_reason = "Imminent exposure requiring urgent containment to prevent potential unauthorized fund drain."
        controls = [
            "- Implement immediate authorization freeze on the transaction rail.",
            "- Require hardware-token or out-of-band biometric authentication from the account holder.",
            "- Verify device IMEI/Browser fingerprint authenticity against known account device history.",
            "- Escalate case file to the Level-2 Fraud Operations Unit for rapid outreach.",
            "- Temporarily flag secondary account privileges pending identity re-verification."
        ]
    elif final_risk_score >= 30 or (attack_score and attack_score >= 50):
        rec_decision = "VERIFY / AUTHENTICATE"
        decision_reason = "Moderate risk signals detected that warrant step-up customer verification before final settlement."
        priority = "HIGH" if final_risk_score >= 50 else "MEDIUM"
        priority_reason = "Elevated indicators present risk; transaction should be held for customer confirmation."
        controls = [
            "- Dispatch high-priority interactive SMS / Push challenge to registered mobile device.",
            "- Validate recent geolocation velocity against previous successful authentication points.",
            "- Confirm beneficiary account authenticity if transaction is a peer transfer.",
            "- Monitor account activity for subsequent rapid-retry attempts over the next 6 hours."
        ]
    else:
        rec_decision = "APPROVE"
        decision_reason = "Transaction parameters and contextual signals fall well within acceptable risk tolerance thresholds."
        priority = "LOW"
        priority_reason = "Risk score is benign; standard operational processing is recommended."
        controls = [
            "- Approve transaction through straight-through-processing (STP).",
            "- Maintain standard passive behavioral and anomaly monitoring.",
            "- Log transaction fingerprint to bolster account profile accuracy."
        ]

    controls_text = "\n".join(controls)
    attack_note = ""
    if attack_score is not None:
        attack_note = f" In addition, the attack simulation layer registered a stress score of {attack_score:.1f}/100 with {attack_indicators} coordinated stress indicators."

    return f"""### AI Risk Assessment
This transaction exhibits a composite Risk Intelligence Score of {final_risk_score:.2f}/100 ({risk_level}) with a deterministic ML fraud probability of {ml_probability * 100:.2f}%. The detected contextual signals reflect {context_score:.0f}/30 risk units, primarily driven by {'amount and endpoint factors' if final_risk_score >= 40 else 'nominal transaction parameters'}.{attack_note}

### Key Risk Factors
{bullets_text}

### AI Recommended Decision
**{rec_decision}**. {decision_reason}

### Recommended Risk Controls
{controls_text}

### Investigation Priority
**{priority}** — {priority_reason}

### AI Reasoning
The final risk intelligence score ({final_risk_score:.2f}/100) mathematically combines the 30-feature XGBoost statistical classifier ({ml_probability*100:.1f}%) with rule-based behavioral heuristics. Because {decision.lower()} was indicated by the risk engine, human oversight should follow the recommended controls to balance fraud prevention with user experience.

---
*⚡ Generated by FraudTwin Decision Intelligence.*"""


def generate_ai_risk_assessment(
    amount,
    transaction_hour,
    device,
    location,
    transaction_type,
    ml_probability,
    context_score,
    final_risk_score,
    risk_level,
    decision,
    contextual_factors,
    attack_score=None,
    attack_indicators=0
):
    """
    Seamless decision support. Silently uses Google Gemini if configured,
    or falls back cleanly to the built-in decision intelligence engine without exposing API keys.
    """
    api_key = get_active_gemini_key()

    if not api_key:
        return generate_local_expert_assessment(
            amount, transaction_hour, device, location, transaction_type,
            ml_probability, context_score, final_risk_score, risk_level,
            decision, contextual_factors, attack_score, attack_indicators
        )

    try:
        client = genai.Client(api_key=api_key)

        factors_text = (
            "\n".join(f"- {factor}" for factor in contextual_factors)
            if contextual_factors
            else "- No contextual risk factors detected"
        )

        attack_text = (
            f"Attack Stress Score: {attack_score:.2f}/100\nAttack indicators: {attack_indicators}"
            if attack_score is not None
            else "No attack simulation has been run."
        )

        prompt = f"""
You are the AI Risk Manager inside FraudTwin, an AI-powered transaction risk intelligence system.

Your job is to interpret the deterministic ML and contextual risk results and provide concise decision support for a human risk manager.
Do NOT change, override, or recalculate the FraudTwin Risk Intelligence Score. Do NOT invent facts that are not provided.
The AI recommendation must be based only on the transaction information and risk signals below.

TRANSACTION
- Amount: INR {amount:,.2f}
- Time: {transaction_hour:02d}:00
- Device: {device}
- Location: {location}
- Transaction Type: {transaction_type}

FRAUDTWIN RISK SIGNALS
- ML Fraud Probability: {ml_probability * 100:.2f}%
- Context Risk: {context_score:.0f}/30
- Risk Intelligence Score: {final_risk_score:.2f}/100
- Risk Level: {risk_level}
- Existing Recommended Decision: {decision}

CONTEXTUAL RISK FACTORS
{factors_text}

ATTACK SIMULATION
{attack_text}

Return the answer using exactly these six headings:

### AI Risk Assessment
Give a 2-3 sentence interpretation of the overall risk.

### Key Risk Factors
Give 3-5 concise bullet points using only the supplied evidence.

### AI Recommended Decision
State one action: APPROVE, VERIFY / AUTHENTICATE, or BLOCK / INVESTIGATE. Briefly explain why.

### Recommended Risk Controls
Give 3-5 practical controls appropriate to the risk.

### Investigation Priority
Choose LOW, MEDIUM, HIGH, or CRITICAL and explain the priority in one sentence.

### AI Reasoning
Give a short explanation connecting the ML score, contextual risk, and attack signals (if present) to the recommendation.

This is decision support, not a replacement for the human risk manager.
"""

        for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
            for attempt in range(2):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    if response and getattr(response, "text", None):
                        return f"🤖 *AI Risk Manager Decision Support*\n\n" + response.text.strip()
                except Exception as err:
                    if "api_key" in str(err).lower() or "unauthenticated" in str(err).lower():
                        raise err
                    time.sleep(1)

        raise RuntimeError("Live Gemini models returned no content.")

    except Exception:
        return generate_local_expert_assessment(
            amount, transaction_hour, device, location, transaction_type,
            ml_probability, context_score, final_risk_score, risk_level,
            decision, contextual_factors, attack_score, attack_indicators
        )
