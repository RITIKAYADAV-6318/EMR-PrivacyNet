import streamlit as st
from auth import verify_login
from database import get_connection

st.set_page_config(page_title="EMR-PrivacyNet", layout="wide")


def login_screen():
    st.title("EMR-PrivacyNet — Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        role = verify_login(username, password)
        if role:
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.rerun()
        else:
            st.error("Invalid username or password.")


def doctor_view():
    st.header(f"Doctor Dashboard — Welcome, {st.session_state['username']}")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()

    from audit import log_access
    log_access(st.session_state["username"], "doctor", "Viewed patient list")

    for p in patients:
        with st.expander(f"{p['name']} — {p['diagnosis']}"):
            st.write(f"**DOB:** {p['dob']}")
            st.write(f"**Contact:** {p['contact']}")
            st.write(f"**Address:** {p['address']}")
            st.write(f"**Diagnosis:** {p['diagnosis']}")
            st.write(f"**Medications:** {p['medications']}")
            st.write(f"**Visit Notes:** {p['visit_notes']}")


def receptionist_view():
    st.header(f"Receptionist Dashboard — Welcome, {st.session_state['username']}")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, contact FROM patients")
    patients = cursor.fetchall()
    conn.close()

    from audit import log_access
    log_access(st.session_state["username"], "receptionist", "Viewed patient list")
    
    for p in patients:
        with st.expander(p["name"]):
            st.write(f"**Contact:** {p['contact']}")
            st.write("*(Appointment info will be shown here once appointments are seeded.)*")

def researcher_view():
    st.header("Researcher Dashboard — De-identified Data")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()

    from audit import log_access
    log_access(st.session_state["username"], "researcher", "Viewed de-identified data")
    
    from deidentify import deidentify_patient

    rows = [deidentify_patient(dict(p)) for p in patients]

    import pandas as pd
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    st.caption("All identifying information has been removed or generalized. "
               "This view never accesses patient names, contact details, or exact addresses/dates of birth.")


def admin_view():
    st.header("Admin — Audit Log")
    from audit import get_audit_log
    import pandas as pd
    logs = get_audit_log()
    if logs:
        df = pd.DataFrame([dict(row) for row in logs])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No audit log entries yet.") 

def main():
    if "role" not in st.session_state:
        login_screen()
        return

    st.sidebar.write(f"Logged in as: **{st.session_state['username']}** ({st.session_state['role']})")
    if st.sidebar.button("Log Out"):
        st.session_state.clear()
        st.rerun()

    role = st.session_state["role"]
    if role == "doctor":
        doctor_view()
    elif role == "receptionist":
        receptionist_view()
    elif role == "researcher":
        researcher_view()
    elif role == "admin":
        admin_view()    
    else:
        st.info(f"'{role}' view not yet built — coming in later days.")


if __name__ == "__main__":
    main()