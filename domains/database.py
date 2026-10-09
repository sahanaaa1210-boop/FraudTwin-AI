import sqlite3
import hashlib
import os
import json
from datetime import datetime
from contextlib import contextmanager
from .config import DB_PATH, DATA_DIR


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def db_session():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return pwd_hash.hex(), salt.hex()


def verify_password(password: str, stored_hash_hex: str, salt_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return pwd_hash.hex() == stored_hash_hex


def init_db():
    with db_session() as conn:
        cursor = conn.cursor()
        
        # 1. Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            phone_number TEXT,
            role TEXT DEFAULT 'Fraud Analyst',
            appearance TEXT DEFAULT 'Dark',
            notifications INTEGER DEFAULT 1,
            risk_view TEXT DEFAULT 'Risk Score',
            gemini_api_key TEXT,
            high_risk_threshold INTEGER DEFAULT 70,
            medium_risk_threshold INTEGER DEFAULT 30,
            ml_weight_pct INTEGER DEFAULT 70,
            auto_escalate INTEGER DEFAULT 1,
            alert_chime INTEGER DEFAULT 1,
            digest_frequency TEXT DEFAULT 'Instant',
            webhook_url TEXT,
            session_timeout TEXT DEFAULT '4 hours',
            two_factor_enabled INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Migration columns for older user tables
        columns_to_add = [
            ("phone_number", "TEXT"),
            ("gemini_api_key", "TEXT"),
            ("high_risk_threshold", "INTEGER DEFAULT 70"),
            ("medium_risk_threshold", "INTEGER DEFAULT 30"),
            ("ml_weight_pct", "INTEGER DEFAULT 70"),
            ("auto_escalate", "INTEGER DEFAULT 1"),
            ("alert_chime", "INTEGER DEFAULT 1"),
            ("digest_frequency", "TEXT DEFAULT 'Instant'"),
            ("webhook_url", "TEXT"),
            ("session_timeout", "TEXT DEFAULT '4 hours'"),
            ("two_factor_enabled", "INTEGER DEFAULT 0"),
        ]
        for col_name, col_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};")
            except sqlite3.OperationalError:
                pass

        # 2. Transactions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            time_recorded TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_time TEXT NOT NULL,
            hour INTEGER NOT NULL,
            device TEXT NOT NULL,
            location TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            ml_probability REAL NOT NULL,
            context_score REAL NOT NULL,
            risk_score REAL NOT NULL,
            risk_level TEXT NOT NULL,
            decision TEXT NOT NULL,
            factors_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 3. Investigations table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created TEXT NOT NULL,
            amount REAL NOT NULL,
            risk_score REAL NOT NULL,
            alert_priority TEXT NOT NULL,
            status TEXT NOT NULL,
            decision TEXT NOT NULL,
            notes TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 4. Audit logs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            action TEXT NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_txn_user ON transactions(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inv_user ON investigations(user_id);")


# ============================================================
# USER AUTHENTICATION & PROFILE METHODS
# ============================================================

def create_user(username, password, full_name="", email="", role="Fraud Analyst", phone_number=""):
    username = username.strip()
    if not username or not password:
        raise ValueError("Username and password cannot be empty.")

    pwd_hash, salt = hash_password(password)
    with db_session() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, salt, full_name, email, phone_number, role)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (username, pwd_hash, salt, full_name or username, email, phone_number, role),
            )
            user_id = cursor.lastrowid
            
            cursor.execute(
                "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
                (user_id, "USER_REGISTERED", f"Account created for {username} ({email or 'No email'}, {phone_number or 'No phone'})")
            )
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.IntegrityError:
            raise ValueError(f"Username '{username}' already exists. Please choose another.")


def authenticate_user(username, password):
    username = username.strip()
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username, username)
        )
        row = cursor.fetchone()
        if not row:
            return None

        if verify_password(password, row["password_hash"], row["salt"]):
            user_dict = dict(row)
            cursor.execute(
                "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
                (user_dict["id"], "LOGIN_SUCCESS", f"User {row['username']} authenticated successfully.")
            )
            return user_dict
        else:
            return None


def get_user_by_id(user_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_or_create_google_user(email="alex.rivers@gmail.com", display_name="Alex Rivers"):
    """Creates or logs in a specific Google account with tenant isolation."""
    email = email.strip().lower()
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? OR username = ?", (email, email))
        row = cursor.fetchone()
        if row:
            user_dict = dict(row)
            cursor.execute(
                "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
                (user_dict["id"], "GOOGLE_LOGIN", f"Signed in via Google account ({email})")
            )
            return user_dict

        # Create new Google user
        random_pwd = os.urandom(16).hex()
        pwd_hash, salt = hash_password(random_pwd)
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, salt, full_name, email, role)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (email, pwd_hash, salt, display_name, email, "Risk Analyst")
        )
        user_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "GOOGLE_REGISTERED", f"Created workspace via Google account ({email})")
        )
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return dict(cursor.fetchone())


def reset_user_password(username_or_email, new_password):
    username_or_email = username_or_email.strip()
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username_or_email, username_or_email)
        )
        row = cursor.fetchone()
        if not row:
            return False, "No account was found matching that username or email."

        user_id = row["id"]
        pwd_hash, salt = hash_password(new_password)
        cursor.execute(
            "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?",
            (pwd_hash, salt, user_id)
        )
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "PASSWORD_RESET", "Password was reset via recovery verification.")
        )
        return True, "Your password has been successfully reset! You can now sign in."


def update_user_profile(user_id, full_name, email, role, phone_number=None):
    with db_session() as conn:
        cursor = conn.cursor()
        if phone_number is not None:
            cursor.execute(
                """
                UPDATE users
                SET full_name = ?, email = ?, role = ?, phone_number = ?
                WHERE id = ?
                """,
                (full_name, email, role, phone_number, user_id)
            )
        else:
            cursor.execute(
                """
                UPDATE users
                SET full_name = ?, email = ?, role = ?
                WHERE id = ?
                """,
                (full_name, email, role, user_id)
            )
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "PROFILE_UPDATED", f"Updated profile: {full_name}, {role}")
        )


def update_user_preferences(user_id, appearance, notifications, risk_view):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET appearance = ?, notifications = ?, risk_view = ?
            WHERE id = ?
            """,
            (appearance, 1 if notifications else 0, risk_view, user_id)
        )


def update_user_thresholds(user_id, high_threshold, med_threshold, ml_weight, auto_escalate):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET high_risk_threshold = ?, medium_risk_threshold = ?,
                ml_weight_pct = ?, auto_escalate = ?
            WHERE id = ?
            """,
            (high_threshold, med_threshold, ml_weight, 1 if auto_escalate else 0, user_id)
        )
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "THRESHOLDS_UPDATED", f"Updated thresholds: High={high_threshold}, Med={med_threshold}, ML={ml_weight}%")
        )


def update_user_notification_settings(user_id, alert_chime, digest_freq, webhook_url):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET alert_chime = ?, digest_frequency = ?, webhook_url = ?
            WHERE id = ?
            """,
            (1 if alert_chime else 0, digest_freq, webhook_url.strip() if webhook_url else None, user_id)
        )
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "NOTIFICATIONS_CONFIGURED", f"Digest: {digest_freq}, Webhook configured: {bool(webhook_url)}")
        )


def update_user_security_options(user_id, session_timeout, two_factor_enabled):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET session_timeout = ?, two_factor_enabled = ?
            WHERE id = ?
            """,
            (session_timeout, 1 if two_factor_enabled else 0, user_id)
        )
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "SECURITY_OPTIONS_UPDATED", f"Timeout={session_timeout}, 2FA={bool(two_factor_enabled)}")
        )


def change_user_password(user_id, current_password, new_password):
    user = get_user_by_id(user_id)
    if not user:
        return False, "User not found."

    if not verify_password(current_password, user["password_hash"], user["salt"]):
        return False, "Current password is incorrect."

    pwd_hash, salt = hash_password(new_password)
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?",
            (pwd_hash, salt, user_id)
        )
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "PASSWORD_CHANGED", "Password updated successfully.")
        )
    return True, "Password updated successfully."


def get_user_audit_logs(user_id, limit=25):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT action, details, created_at
            FROM audit_logs
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit)
        )
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def reset_user_workspace_data(user_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM investigations WHERE user_id = ?", (user_id,))
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "WORKSPACE_RESET", "User wiped all transaction and case history.")
        )


# ============================================================
# USER-SPECIFIC TRANSACTION METHODS
# ============================================================

def add_user_transaction(user_id, result):
    factors_json = json.dumps(result.get("factors", []))
    time_recorded = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions (
                user_id, time_recorded, amount, transaction_time, hour,
                device, location, transaction_type, ml_probability,
                context_score, risk_score, risk_level, decision, factors_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                time_recorded,
                float(result["amount"]),
                f"{int(result['hour']):02d}:00",
                int(result["hour"]),
                str(result["device"]),
                str(result["location"]),
                str(result["type"]),
                float(result["probability"]) * 100,
                float(result["context_score"]),
                float(result["final_score"]),
                str(result["level"]),
                str(result["decision"]),
                factors_json,
            ),
        )
        return cursor.lastrowid


def get_user_transactions(user_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT time_recorded, amount, transaction_time, device,
                   location, transaction_type, ml_probability,
                   context_score, risk_score, risk_level, decision, factors_json
            FROM transactions
            WHERE user_id = ?
            ORDER BY id ASC
            """,
            (user_id,)
        )
        rows = cursor.fetchall()
        result = []
        for r in rows:
            result.append({
                "Time Recorded": r["time_recorded"],
                "Amount": r["amount"],
                "Transaction Time": r["transaction_time"],
                "Device": r["device"],
                "Location": r["location"],
                "Transaction Type": r["transaction_type"],
                "ML Probability": r["ml_probability"],
                "Context Risk": r["context_score"],
                "Risk Score": r["risk_score"],
                "Risk Level": r["risk_level"],
                "Decision": r["decision"],
                "Factors": json.loads(r["factors_json"]) if r["factors_json"] else [],
            })
        return result


def clear_user_transactions(user_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "CLEAR_TRANSACTIONS", "Cleared all transaction history.")
        )


# ============================================================
# USER-SPECIFIC INVESTIGATION METHODS
# ============================================================

def save_user_investigation_case(user_id, case):
    case_id = case.get("Case ID")
    created = case.get("Created", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    amount = float(case.get("Amount", 0.0))
    risk_score = float(case.get("Risk Score", 0.0))
    alert_priority = case.get("Alert Priority", "LOW")
    status = case.get("Status", "Open")
    decision = case.get("Decision", "APPROVE")
    notes = case.get("Notes", "")

    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO investigations (
                case_id, user_id, created, amount, risk_score,
                alert_priority, status, decision, notes, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(case_id) DO UPDATE SET
                status = excluded.status,
                notes = excluded.notes,
                updated_at = CURRENT_TIMESTAMP
            """,
            (case_id, user_id, created, amount, risk_score, alert_priority, status, decision, notes)
        )


def get_user_investigations(user_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT case_id, created, amount, risk_score, alert_priority, status, decision, notes
            FROM investigations
            WHERE user_id = ?
            ORDER BY id ASC
            """,
            (user_id,)
        )
        rows = cursor.fetchall()
        result = []
        for r in rows:
            result.append({
                "Case ID": r["case_id"],
                "Created": r["created"],
                "Amount": r["amount"],
                "Risk Score": r["risk_score"],
                "Alert Priority": r["alert_priority"],
                "Status": r["status"],
                "Decision": r["decision"],
                "Notes": r["notes"] or "",
            })
        return result


def clear_user_investigations(user_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM investigations WHERE user_id = ?", (user_id,))
        cursor.execute(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, "CLEAR_INVESTIGATIONS", "Cleared all investigation cases.")
        )


init_db()
