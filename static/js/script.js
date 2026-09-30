const form = document.getElementById("prediction-form");
const predictBtn = document.getElementById("predict-btn");
const btnLabel = predictBtn.querySelector(".btn-label");
const spinner = predictBtn.querySelector(".spinner");
const formError = document.getElementById("form-error");
const resultEmpty = document.getElementById("result-empty");
const resultContent = document.getElementById("result-content");
const resultError = document.getElementById("result-error");
const resultBanner = document.getElementById("result-banner");
const resultSymbol = document.getElementById("result-symbol");
const resultTitle = document.getElementById("result-title");
const resultSummary = document.getElementById("result-summary");
const probabilityLabel = document.getElementById("probability-label");
const probabilityValue = document.getElementById("probability-value");
const probabilityBar = document.getElementById("probability-bar");
const resultNote = document.getElementById("result-note");
const resetBtn = document.getElementById("reset-btn");

const hiddenStep = document.getElementById("step");
const hiddenFlag = document.getElementById("isFlaggedFraud");

hiddenStep.value = "1";
hiddenFlag.value = "0";

function showError(target, message) {
  target.textContent = message;
  target.classList.remove("hidden");
}

function clearErrors() {
  formError.classList.add("hidden");
  resultError.classList.add("hidden");
}

function validateForm() {
  const required = Array.from(form.querySelectorAll("input[required], select[required]"));

  for (const input of required) {
    if (input.type === "hidden") continue;

    const rawValue = input.value;
    if (!String(rawValue).trim()) {
      input.focus();
      return "Please enter all transaction details.";
    }

    if (input.type === "number") {
      const numberValue = Number(rawValue);
      if (Number.isNaN(numberValue) || numberValue < 0) {
        input.focus();
        return "Please enter valid amounts and balances.";
      }
    }
  }

  return null;
}

function setLoading(isLoading) {
  predictBtn.disabled = isLoading;
  btnLabel.classList.toggle("hidden", isLoading);
  spinner.classList.toggle("hidden", !isLoading);

  if (isLoading) {
    btnLabel.innerHTML = "Analyzing transaction <span aria-hidden=\"true\">…</span>";
  } else {
    btnLabel.innerHTML = "Check transaction <span aria-hidden=\"true\">→</span>";
  }
}

function showResult(data) {
  const isFraud = Boolean(data.is_fraud);

  resultEmpty.classList.add("hidden");
  resultContent.classList.remove("hidden");
  resultError.classList.add("hidden");

  resultBanner.classList.toggle("fraud", isFraud);
  resultSymbol.textContent = isFraud ? "!" : "✓";
  resultTitle.textContent = isFraud ? "Potential fraud detected" : "Looks legitimate";
  resultSummary.textContent = isFraud
    ? "This transaction shows patterns associated with fraudulent activity."
    : "No significant fraud risk was detected for this transaction.";

  probabilityLabel.textContent = isFraud ? "Fraud probability" : "Model confidence";

  if (typeof data.probability === "number" && Number.isFinite(data.probability)) {
    const pct = data.probability * 100;
    probabilityValue.textContent = `${pct.toFixed(1)}%`;
    probabilityBar.style.width = `${Math.max(0, Math.min(100, pct))}%`;
  } else {
    probabilityValue.textContent = "Not available";
    probabilityBar.style.width = "0%";
  }

  resultNote.textContent = "Probability is an estimate, not certainty.";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearErrors();

  const validationError = validateForm();
  if (validationError) {
    showError(formError, validationError);
    return;
  }

  const payload = Object.fromEntries(new FormData(form).entries());
  hiddenStep.value = "1";
  hiddenFlag.value = "0";

  setLoading(true);

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok || !data.ok) {
      throw new Error(data.error || "Something went wrong while analyzing the transaction. Please try again.");
    }

    showResult(data);
    document.getElementById("result-card").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    showError(resultError, error.message || "Something went wrong while analyzing the transaction. Please try again.");
    resultEmpty.classList.add("hidden");
    resultContent.classList.add("hidden");
    resultError.classList.remove("hidden");
  } finally {
    setLoading(false);
  }
});

resetBtn.addEventListener("click", () => {
  resultContent.classList.add("hidden");
  resultEmpty.classList.remove("hidden");
  form.reset();
  hiddenStep.value = "1";
  hiddenFlag.value = "0";
  clearErrors();
  document.getElementById("transaction_type").focus();
});
