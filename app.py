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

    for p in patients:
        with st.expander(p["name"]):
            st.write(f"**Contact:** {p['contact']}")
            st.write("*(Appointment info will be shown here once appointments are seeded.)*")


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
    else:
        st.info(f"'{role}' view not yet built — coming in later days.")


if __name__ == "__main__":
    main()