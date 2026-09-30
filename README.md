# FraudGuard — Flask Frontend for the Supplied Fraud Detection Model

## 1. What I found in the supplied model

`Fraud_Detection_Model_Richa.pkl` loads as an **XGBoost `XGBClassifier`**.

The serialized model reports:

- **12 input features**
- **Binary classes:** `0` and `1`
- Objective: `binary:logistic`
- `predict_proba()` is available
- The model's stored feature schema is already one-hot encoded for transaction type.

Exact feature order:

1. `step`
2. `amount`
3. `oldbalanceOrg`
4. `newbalanceOrig`
5. `oldbalanceDest`
6. `newbalanceDest`
7. `isFlaggedFraud`
8. `type_CASH_IN`
9. `type_CASH_OUT`
10. `type_DEBIT`
11. `type_PAYMENT`
12. `type_TRANSFER`

### Important preprocessing finding

No separate scaler, encoder, or preprocessing pipeline was supplied with the `.pkl` file. The model itself expects the 12-column feature matrix above.

Therefore the Flask backend does **not** invent a new ML preprocessing pipeline. It only converts the user's human-friendly transaction type into the exact five one-hot columns expected by the model and preserves the exact feature order.

## 2. UI workflow

The page is intentionally simple:

1. User selects a transaction type.
2. User enters the seven numeric/binary model inputs.
3. JavaScript validates the form.
4. The browser sends JSON to `POST /predict`.
5. Flask validates the request and builds the exact 12-feature DataFrame.
6. The existing XGBoost model runs `predict()` and `predict_proba()`.
7. Flask returns the class, human-readable label, and class-1 probability.
8. JavaScript renders the result card without navigating away.

The probability is explicitly described as a model estimate, not certainty.

## 3. Project structure

```text
fraud_detection_flask/
├── app.py
├── requirements.txt
├── README.md
├── model/
│   └── Fraud_Detection_Model_Richa.pkl
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## 4. Run locally

### Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start Flask

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/health
```

## 5. Why the backend uses pandas

The model has named features. Passing a pandas DataFrame with the exact feature names and order makes the model interface explicit and reduces accidental column-order mistakes.

## 6. Important deployment note

The `.pkl`/joblib file is executable serialized Python data. Only load a model file you trust.

For production deployment, turn off Flask debug mode, run behind a production WSGI server, and add authentication/rate limiting if the endpoint is exposed publicly.
