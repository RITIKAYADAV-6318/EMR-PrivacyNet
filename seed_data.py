from auth import create_user
from database import get_connection


def seed_users():
    users = [
        ("doctor1", "testpass123", "doctor"),
        ("reception1", "testpass123", "receptionist"),
        ("researcher1", "testpass123", "researcher"),
        ("admin1", "testpass123", "admin"),
    ]
    for username, password, role in users:
        create_user(username, password, role)


def seed_patients():
    patients = [
        ("Aarav Sharma", "1990-04-12", "9876543210", "Delhi", "Hypertension", "Amlodipine",
         "Patient reports occasional headaches and dizziness over the past two weeks. "
         "Blood pressure elevated at last visit. Advised to monitor BP daily and reduce salt intake."),
        ("Priya Nair", "1985-11-03", "9876500001", "Mumbai", "Type 2 Diabetes", "Metformin",
         "Follow-up visit for diabetes management. Blood sugar levels stable. "
         "Patient adhering to diet plan. No new symptoms reported."),
        ("Rohan Mehta", "1978-06-22", "9876500002", "Bangalore", "Asthma", "Salbutamol inhaler",
         "Patient experienced mild wheezing during physical activity. "
         "Inhaler use increased to twice daily. Advised follow-up in 2 weeks if symptoms persist."),
        ("Sneha Iyer", "1995-02-17", "9876500003", "Chennai", "Migraine", "Sumatriptan",
         "Recurring migraine episodes, roughly twice a week, lasting 4-6 hours. "
         "No visual aura reported. Discussed trigger avoidance and hydration."),
        ("Vikram Singh", "1982-09-30", "9876500004", "Delhi", "Coronary Artery Disease", "Atorvastatin",
         "Routine cardiac follow-up. Patient reports mild chest tightness after exertion. "
         "ECG scheduled for next visit. Advised to avoid strenuous activity until reviewed."),
        ("Ananya Reddy", "2000-01-08", "9876500005", "Hyderabad", "Anemia", "Iron supplements",
         "Patient reports fatigue and occasional shortness of breath. "
         "Hemoglobin levels checked, mildly low. Advised dietary iron intake and follow-up bloodwork."),
    ]

    conn = get_connection()
    cursor = conn.cursor()
    for name, dob, contact, address, diagnosis, medications, visit_notes in patients:
        cursor.execute("""
            INSERT INTO patients (name, dob, contact, address, diagnosis, medications, visit_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, dob, contact, address, diagnosis, medications, visit_notes))
    conn.commit()
    conn.close()
    print(f"Seeded {len(patients)} patients.")


if __name__ == "__main__":
    seed_users()
    seed_patients()