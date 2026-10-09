import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from domains import database, risk_engine


def test_suite():
    print("========================================")
    print("RUNNING EXTENDED FRAUDTWIN TEST SUITE")
    print("========================================")

    database.init_db()

    # 1. Registration with Email & Phone Number
    print("\n[1/6] Testing Registration with Email & Phone...")
    user_alice = database.create_user(
        "alice_analyst", "SecurePass123!", "Alice Smith",
        "alice@fraudtwin.local", "Fraud Analyst", "+91 98765 43210"
    )
    assert user_alice is not None
    assert user_alice["username"] == "alice_analyst"
    assert user_alice["phone_number"] == "+91 98765 43210"
    print(f"  [OK] User Alice created with phone {user_alice['phone_number']} (ID: {user_alice['id']})")

    auth_ok = database.authenticate_user("alice_analyst", "SecurePass123!")
    assert auth_ok is not None and auth_ok["id"] == user_alice["id"]
    print("  [OK] Authentication with username succeeded.")

    # 2. Google Multi-Account Selection
    print("\n[2/6] Testing Google Multi-Account Support...")
    user_g1 = database.get_or_create_google_user("alex.rivers@gmail.com", "Alex Rivers (Personal)")
    user_g2 = database.get_or_create_google_user("alex.secops@enterprise.corp", "Alex Rivers (SecOps)")
    assert user_g1["id"] != user_g2["id"]
    assert user_g1["email"] == "alex.rivers@gmail.com"
    assert user_g2["email"] == "alex.secops@enterprise.corp"
    print("  [OK] Google accounts 1 & 2 assigned distinct isolated tenant IDs.")

    # 3. Forgot Password Recovery Flow
    print("\n[3/6] Testing Forgot Password Recovery Flow...")
    ok, msg = database.reset_user_password("alice@fraudtwin.local", "RecoveredPassword789!")
    assert ok is True
    print("  [OK] Password reset executed by email lookup.")

    auth_old = database.authenticate_user("alice_analyst", "SecurePass123!")
    assert auth_old is None
    auth_new = database.authenticate_user("alice_analyst", "RecoveredPassword789!")
    assert auth_new is not None and auth_new["id"] == user_alice["id"]
    print("  [OK] New password authenticates successfully, old password rejected.")

    # 4. Enterprise Settings & Threshold Calibration
    print("\n[4/6] Testing Risk Engine Calibration & Notification Settings...")
    alice_id = user_alice["id"]
    database.update_user_thresholds(alice_id, 75, 35, 80, True)
    database.update_user_notification_settings(alice_id, True, "Hourly Digest", "https://hooks.slack.com/services/test")
    database.update_user_security_options(alice_id, "1 hour", True)

    refreshed_alice = database.get_user_by_id(alice_id)
    assert refreshed_alice["high_risk_threshold"] == 75
    assert refreshed_alice["medium_risk_threshold"] == 35
    assert refreshed_alice["ml_weight_pct"] == 80
    assert refreshed_alice["digest_frequency"] == "Hourly Digest"
    assert refreshed_alice["session_timeout"] == "1 hour"
    assert refreshed_alice["two_factor_enabled"] == 1
    print("  [OK] Enterprise settings and threshold calibrations persisted.")

    # 5. Audit Logging Trail
    print("\n[5/6] Testing Audit Trail Generation...")
    logs = database.get_user_audit_logs(alice_id)
    assert len(logs) >= 3
    print(f"  [OK] {len(logs)} audit trail events verified for user Alice.")

    # 6. Workspace Data Reset
    print("\n[6/6] Testing Safe Workspace Data Reset...")
    txn_dummy = risk_engine.score_transaction(10, 25000.0, "Desktop - Trusted Chrome", "Mumbai, IN", "Online Purchase")
    database.add_user_transaction(alice_id, txn_dummy)
    assert len(database.get_user_transactions(alice_id)) == 1

    database.reset_user_workspace_data(alice_id)
    assert len(database.get_user_transactions(alice_id)) == 0
    assert database.get_user_by_id(alice_id) is not None
    print("  [OK] Workspace data wiped while preserving user credentials.")

    print("\n========================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("========================================")


if __name__ == "__main__":
    test_suite()
