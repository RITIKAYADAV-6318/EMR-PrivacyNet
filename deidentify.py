import re


def deidentify_patient(patient_row: dict) -> dict:
    """
    Takes a raw patient record (as a dict) and returns a de-identified version
    safe for the researcher role. Drops direct identifiers and generalizes
    quasi-identifiers.
    """
    dob = patient_row["dob"]
    birth_year = dob.split("-")[0] if dob else "Unknown"

    address = patient_row["address"] or ""
    city = address.split(",")[0].strip() if address else "Unknown"

    return {
        "patient_ref": f"PT-{patient_row['id']:04d}",
        "birth_year": birth_year,
        "region": city,
        "diagnosis_category": _generalize_diagnosis(patient_row["diagnosis"]),
    }


def _generalize_diagnosis(diagnosis: str) -> str:
    """
    Maps a specific diagnosis to a broader category, so researchers see
    a clinical category rather than a highly specific (and more identifying)
    diagnosis string.
    """
    if not diagnosis:
        return "Unknown"

    diagnosis_lower = diagnosis.lower()
    categories = {
        "cardiovascular": ["hypertension", "coronary artery disease", "heart"],
        "metabolic": ["diabetes", "thyroid"],
        "respiratory": ["asthma", "copd", "bronchitis"],
        "neurological": ["migraine", "epilepsy", "seizure"],
        "hematological": ["anemia"],
    }

    for category, keywords in categories.items():
        if any(keyword in diagnosis_lower for keyword in keywords):
            return category

    return "Other"