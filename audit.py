from datetime import datetime
from database import get_connection


def log_access(username: str, role: str, action: str, patient_id: int = None):
    """
    Records an access event in the audit log.
    Called every time a user views or interacts with patient data.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_log (username, role, action, patient_id, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (username, role, action, patient_id, datetime.now().isoformat(timespec="seconds")))
    conn.commit()
    conn.close()


def get_audit_log():
    """Returns all audit log entries, most recent first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_log ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows 