from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "Fraud_Detection_Model_Richa.pkl"

# This is the exact feature schema found inside the supplied XGBoost model.
FEATURES = [
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "isFlaggedFraud",
    "type_CASH_IN",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]

TRANSACTION_TYPES = (
    "CASH_IN",
    "CASH_OUT",
    "DEBIT",
    "PAYMENT",
    "TRANSFER",
)

app = Flask(__name__)

model = None
model_load_error = None

try:
    # Only load model files you trust: pickle/joblib can execute code during loading.
    model = joblib.load(MODEL_PATH)
except Exception as exc:
    model_load_error = str(exc)


def parse_number(payload, key, *, integer=False, minimum=0.0):
    """Parse and validate a numeric request field."""
    raw = payload.get(key)
    if raw is None or str(raw).strip() == "":
        raise ValueError(f"{key} is required.")

    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{key} must be a valid number.")

    if not np.isfinite(value):
        raise ValueError(f"{key} must be finite.")

    if value < minimum:
        raise ValueError(f"{key} must be at least {minimum:g}.")

    if integer and not value.is_integer():
        raise ValueError(f"{key} must be a whole number.")

    return int(value) if integer else value


def build_model_input(payload):
    transaction_type = str(payload.get("transaction_type", "")).strip().upper()
    if transaction_type not in TRANSACTION_TYPES:
        raise ValueError("Please select a valid transaction type.")

    # The supplied model already contains the one-hot encoded transaction-type
    # feature schema. We reproduce that schema here; no new encoder/scaler is used.
    row = {
        "step": parse_number(payload, "step", integer=True, minimum=1),
        "amount": parse_number(payload, "amount"),
        "oldbalanceOrg": parse_number(payload, "oldbalanceOrg"),
        "newbalanceOrig": parse_number(payload, "newbalanceOrig"),
        "oldbalanceDest": parse_number(payload, "oldbalanceDest"),
        "newbalanceDest": parse_number(payload, "newbalanceDest"),
        "isFlaggedFraud": parse_number(
            payload, "isFlaggedFraud", integer=True, minimum=0
        ),
    }

    if row["isFlaggedFraud"] not in (0, 1):
        raise ValueError("isFlaggedFraud must be either 0 or 1.")

    for kind in TRANSACTION_TYPES:
        row[f"type_{kind}"] = int(transaction_type == kind)

    # Explicitly enforce the exact feature order expected by the model.
    return pd.DataFrame([[row[name] for name in FEATURES]], columns=FEATURES)


@app.get("/")
def index():
    return render_template("index.html", model_loaded=model is not None)


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok" if model is not None else "error",
            "model_loaded": model is not None,
            "error": model_load_error,
        }
    ), (200 if model is not None else 503)


@app.post("/predict")
def predict():
    if model is None:
        return jsonify(
            {
                "ok": False,
                "error": "The ML model could not be loaded. Check the model file and installed package versions.",
            }
        ), 503

    try:
        payload = request.get_json(silent=True) or request.form
        features = build_model_input(payload)

        prediction = int(np.asarray(model.predict(features)).reshape(-1)[0])
        probability = None

        if hasattr(model, "predict_proba"):
            probabilities = np.asarray(model.predict_proba(features))
            if probabilities.ndim == 2 and probabilities.shape[1] >= 2:
                probability = float(probabilities[0, 1])

        is_fraud = prediction == 1

        response = {
            "ok": True,
            "prediction": prediction,
            "label": "Potential Fraud" if is_fraud else "Likely Legitimate",
            "is_fraud": is_fraud,
            "probability": probability,
            "note": (
                "This probability is the model's estimated probability for class 1; "
                "it is not a guarantee that the transaction is fraudulent."
            ),
        }
        return jsonify(response)

    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception:
        # Do not expose Python stack traces to the browser.
        app.logger.exception("Prediction failed")
        return jsonify(
            {
                "ok": False,
                "error": "Prediction could not be generated. Please check the inputs and try again.",
            }
        ), 500


if __name__ == "__main__":
    app.run(debug=True)
