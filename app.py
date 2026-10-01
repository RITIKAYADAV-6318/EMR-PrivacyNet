import streamlit as st
import streamlit.components.v1 as components
from auth import verify_login
from database import get_connection

import os
from database import init_db, get_connection as _check_connection

DB_PATH = os.path.join("data", "emr.db")

if not os.path.exists(DB_PATH):
    os.makedirs("data", exist_ok=True)
    init_db()
    from seed_data import seed_users, seed_patients
    seed_users()
    seed_patients()

st.set_page_config(page_title="EMR-PrivacyNet", layout="wide")

from style_block import APP_CSS, LOGIN_BG_HTML, HEADER_HTML, FOOTER_HTML, ABOUT_SECTION_HTML
st.markdown(APP_CSS, unsafe_allow_html=True)
st.markdown(HEADER_HTML, unsafe_allow_html=True)
st.markdown(FOOTER_HTML, unsafe_allow_html=True)


def login_screen():
    st.markdown('<div id="login-section"></div>', unsafe_allow_html=True)
    components.html(LOGIN_BG_HTML, height=320)

    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        st.markdown('<div class="login-card"><h4 style="margin-top:0;margin-bottom:4px;">Sign In</h4>', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(ABOUT_SECTION_HTML, unsafe_allow_html=True)


def show_privacy_notice():
    with st.sidebar.expander("Privacy and Consent Notice"):
        st.write(
            "This is a prototype system built with **synthetic data only**. "
            "No real patient information is used or stored.\n\n"
            "- Access to records is **role-restricted** and every view is **logged**.\n"
            "- Data shown to researchers is **de-identified** before display.\n"
            "- AI-generated summaries and risk flags are **documentation aids**, "
            "not diagnoses, and should always be verified by clinical judgment."
        )


def doctor_view():
    st.header(f"Doctor Dashboard: Welcome, {st.session_state['username']}")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()

    from audit import log_access
    log_access(st.session_state["username"], "doctor", "Viewed patient list")

    from llm_summarizer import summarize_note
    from risk_model import predict_risk, explain_risk

    search_term = st.text_input("Search patients by name", "")
    if search_term:
        patients = [p for p in patients if search_term.lower() in p['name'].lower()]

    for p in patients:
        patient_features = {
            "age": 2026 - int(p['dob'].split('-')[0]),
            "systolic_bp": p['systolic_bp'],
            "diastolic_bp": p['diastolic_bp'],
            "bmi": p['bmi'],
            "smoking_binary": 1 if p['smoking_status'] == "Current smoker" else 0,
            "family_history_binary": 1 if p['family_history'] == "Yes" else 0,
            "prior_conditions_count": p['prior_conditions_count'],
        }
        label, probability = predict_risk(patient_features)
        badge_class = "risk-badge-high" if label == "High Risk" else "risk-badge-low"

        with st.expander(f"{p['name']} : {p['diagnosis']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**DOB:** {p['dob']}")
                st.write(f"**Contact:** {p['contact']}")
                st.write(f"**Address:** {p['address']}")
            with col2:
                st.write(f"**Diagnosis:** {p['diagnosis']}")
                st.write(f"**Medications:** {p['medications']}")
                st.write(f"**Visit Notes:** {p['visit_notes']}")

            st.divider()

            if st.button("Summarize Note (AI)", key=f"summarize_{p['id']}"):
                with st.spinner("Summarizing..."):
                    summary = summarize_note(p['visit_notes'])
                st.markdown("**AI-Generated Summary**")
                st.write(f"**Symptoms:** {', '.join(summary['symptoms'])}")
                st.write(f"**{summary['probable_diagnosis']}**")
                st.write(f"**Follow-up Plan:** {summary['follow_up_plan']}")
                st.write(f"**Flags:** {summary['flags']}")
                st.markdown('<p class="caution-note">This is an AI-generated documentation aid, not a diagnosis. Always verify against clinical judgment.</p>', unsafe_allow_html=True)

                log_access(st.session_state["username"], "doctor", f"AI-summarized note for patient {p['id']}", patient_id=p['id'])

            st.divider()

            st.markdown(
                f'**Risk Flag:** <span class="{badge_class}">{label}</span> &nbsp; ({probability:.1%} probability)',
                unsafe_allow_html=True
            )

            if label == "High Risk":
                top_factors = explain_risk(patient_features)
                factor_names = {
                    "age": "Age", "systolic_bp": "Systolic BP", "diastolic_bp": "Diastolic BP",
                    "bmi": "BMI", "smoking_binary": "Smoking status",
                    "family_history_binary": "Family history", "prior_conditions_count": "Prior conditions"
                }
                factors_str = ", ".join([factor_names[f] for f, _ in top_factors])
                st.markdown(f'<p class="caution-note">Top contributing factors: {factors_str}</p>', unsafe_allow_html=True)


def receptionist_view():
    st.header(f"Receptionist Dashboard: Welcome, {st.session_state['username']}")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, contact FROM patients")
    patients = cursor.fetchall()
    conn.close()

    from audit import log_access
    log_access(st.session_state["username"], "receptionist", "Viewed patient list")

    for p in patients:
        with st.expander(f"{p['name']} (ID: {p['id']})"):
            st.write(f"**Contact:** {p['contact']}")


def researcher_view():
    st.header("Researcher Dashboard: De-identified Data")
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
    st.markdown(
        '<p class="caution-note">All identifying information has been removed or generalized. '
        'This view never accesses patient names, contact details, or exact addresses/dates of birth.</p>',
        unsafe_allow_html=True
    )


def admin_view():
    st.header("Admin: Audit Log")
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

    show_privacy_notice()

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
        st.info(f"'{role}' view not yet built.")


if __name__ == "__main__":
    main()