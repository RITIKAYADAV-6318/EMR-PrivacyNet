import pandas as pd
import numpy as np
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

DATA_PATH = os.path.join("data", "risk_training_data.csv")
MODEL_PATH = os.path.join("data", "risk_model.pkl")

FEATURES = ["age", "systolic_bp", "diastolic_bp", "bmi", "smoking_binary", "family_history_binary", "prior_conditions_count"]


def generate_synthetic_dataset(n_rows: int = 1500, seed: int = 42) -> pd.DataFrame:
    """
    Generates a synthetic dataset with deliberately correlated features,
    so the model has a real (if simplified) pattern to learn.
    NOT based on real clinical data or formulas — illustrative only.
    """
    rng = np.random.default_rng(seed)

    age = rng.integers(20, 80, n_rows)
    smoking_binary = rng.binomial(1, 0.25, n_rows)  # ~25% smokers
    family_history_binary = rng.binomial(1, 0.35, n_rows)
    prior_conditions_count = rng.poisson(1.2, n_rows)

    # BP and BMI trend upward with age, with some noise
    systolic_bp = 100 + (age * 0.6) + (smoking_binary * 10) + rng.normal(0, 8, n_rows)
    diastolic_bp = 65 + (age * 0.25) + (smoking_binary * 5) + rng.normal(0, 5, n_rows)
    bmi = 21 + (age * 0.05) + rng.normal(0, 3, n_rows)

    systolic_bp = np.clip(systolic_bp, 90, 200).round(0)
    diastolic_bp = np.clip(diastolic_bp, 60, 130).round(0)
    bmi = np.clip(bmi, 16, 45).round(1)

    # Risk score is a weighted combination — deliberately correlated, not random
    risk_score = (
        (age > 50).astype(int) * 1.5 +
        (systolic_bp > 140).astype(int) * 2 +
        (diastolic_bp > 90).astype(int) * 1.5 +
        (bmi > 28).astype(int) * 1 +
        smoking_binary * 2 +
        family_history_binary * 1.5 +
        (prior_conditions_count >= 2).astype(int) * 2 +
        rng.normal(0, 1.2, n_rows)  # noise so it's not perfectly separable
    )

    # Threshold the score into a binary label
    high_risk = (risk_score > np.percentile(risk_score, 70)).astype(int)  # top 30% flagged high risk

    df = pd.DataFrame({
        "age": age,
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
        "bmi": bmi,
        "smoking_binary": smoking_binary,
        "family_history_binary": family_history_binary,
        "prior_conditions_count": prior_conditions_count,
        "high_risk": high_risk
    })
    return df


def train_model():
    """Generates the dataset, trains a logistic regression model, evaluates it, and saves both."""
    df = generate_synthetic_dataset(n_rows=1500)
    df.to_csv(DATA_PATH, index=False)

    X = df[FEATURES]
    y = df["high_risk"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    # Scale features so they contribute proportionally, not by raw magnitude
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_train_scaled, y_train)

    # Cross-validation for a more stable performance estimate
    cv_scores = cross_val_score(model, scaler.transform(X), y, cv=5, scoring="recall")
    print(f"5-fold CV recall scores: {cv_scores.round(3)}")
    print(f"Mean CV recall: {cv_scores.mean():.3f}")

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("Model trained.")
    print(f"Accuracy:  {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print("Confusion Matrix:")
    print(cm)

    # Save both model and scaler — predict_risk needs the scaler too
    with open(MODEL_PATH, "wb") as f:
        pickle.dump({"model": model, "scaler": scaler}, f)
    print(f"Model saved to {MODEL_PATH}")

    return model, {"accuracy": accuracy, "precision": precision, "recall": recall, "confusion_matrix": cm.tolist()}


def load_model():
    """Loads the trained model + scaler from disk, training new ones if they don't exist yet."""
    if not os.path.exists(MODEL_PATH):
        train_model()
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def predict_risk(patient_features: dict):
    """
    Takes a dict of a single patient's features and returns (label, probability).
    Expects keys matching FEATURES.
    """
    saved = load_model()
    model = saved["model"]
    scaler = saved["scaler"]

    X = pd.DataFrame([patient_features])[FEATURES]
    X_scaled = scaler.transform(X)
    probability = model.predict_proba(X_scaled)[0][1]
    label = "High Risk" if probability >= 0.5 else "Low Risk"
    return label, round(probability, 3)


def explain_risk(patient_features: dict, top_n: int = 3):
    """
    Returns the top N features contributing most to this patient's risk score,
    based on the logistic regression coefficients (scaled contribution = coefficient * scaled feature value).
    """
    saved = load_model()
    model = saved["model"]
    scaler = saved["scaler"]

    X = pd.DataFrame([patient_features])[FEATURES]
    X_scaled = scaler.transform(X)[0]
    coefficients = model.coef_[0]

    contributions = X_scaled * coefficients
    feature_contributions = list(zip(FEATURES, contributions))
    feature_contributions.sort(key=lambda x: abs(x[1]), reverse=True)

    return feature_contributions[:top_n]

if __name__ == "__main__":
    train_model()