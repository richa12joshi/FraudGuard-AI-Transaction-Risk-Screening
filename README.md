# FraudGuard AI

### AI-Powered Transaction Fraud Detection

FraudGuard AI is a **Machine Learning-based fraud detection project** that analyzes financial transaction data and predicts whether a transaction is legitimate or potentially fraudulent.

The project covers the complete Machine Learning workflow — from understanding and cleaning the data to training, comparing, evaluating, and deploying the final model through Flask.

---

## 🔍 What I Did

The project follows a complete end-to-end Machine Learning process:

**1. Data Understanding**  
Understanding the dataset, its features, data types, patterns, and the problem we are trying to solve.

**2. Data Cleaning**  
Checked and handled:
- Missing values
- Duplicate records
- Incorrect or inconsistent data
- Outliers

**3. Exploratory Data Analysis (EDA)**  
Used data visualization to understand relationships and patterns in the data, including:
- Box plots
- Scatter plots
- Distribution analysis
- Correlation analysis
- Heatmaps

**4. Feature & Target Selection**  
Separated the dataset into:
- **X → Input features**
- **Y → Target variable**

**5. Train-Test Split**  
Divided the data into training and testing sets to train the models and evaluate how well they perform on unseen data.

**6. Feature Selection & Preparation**  
Selected the relevant features and prepared the data for Machine Learning.

**7. Model Selection & Training**  
Experimented with multiple Machine Learning algorithms to determine which models are suitable for fraud classification.

### 🤖 Machine Learning Algorithms

The project includes experimentation with **12 Machine Learning algorithms**, including:

- Logistic Regression
- Decision Tree
- Random Forest
- Naive Bayes
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)
- AdaBoost
- Gradient Boosting
- XGBoost
- Extra Trees
- Bagging Classifier
- Stacking Classifier

The models were trained and compared using the same classification problem and evaluation approach.

---

## 📊 Model Evaluation

The trained models were evaluated using multiple classification metrics:

- **Accuracy**
- **Precision**
- **Recall**
- **F1 Score**
- **Confusion Matrix**
- **Classification Report**

Instead of relying on accuracy alone, multiple metrics were considered because fraud detection is an **imbalanced classification problem** where identifying fraudulent transactions correctly is particularly important.

---

## 🧠 Final Model

After experimenting with different Machine Learning approaches, the final trained model was saved and integrated into a Flask application.

The model takes transaction information as input and returns:

**Legitimate Transaction**  
or  
**Potential Fraud**

along with the model's estimated probability.

---

## 🌐 Flask Application

The trained model is connected to a simple Flask web application.

The application allows a user to:

1. Enter transaction details
2. Submit the transaction
3. Send the data to the Flask backend
4. Run the trained ML model
5. Receive the prediction
6. View the estimated fraud probability

The frontend is intentionally kept simple so that the main focus remains on the **Machine Learning workflow and fraud detection model**.

---

## 🛠️ Technologies Used

**Programming**
- Python

**Data Analysis**
- Pandas
- NumPy

**Data Visualization**
- Matplotlib
- Seaborn

**Machine Learning**
- Scikit-learn
- XGBoost

**Deployment**
- Flask
- HTML
- CSS
- JavaScript

---

## 🔄 Complete Workflow

```text
Data Understanding
        ↓
Data Cleaning
        ↓
Missing Values & Duplicates
        ↓
Exploratory Data Analysis
        ↓
Data Visualization
        ↓
Feature Selection
        ↓
X & Y Selection
        ↓
Train-Test Split
        ↓
Model Selection
        ↓
Model Training
        ↓
Prediction
        ↓
Model Evaluation
        ↓
Algorithm Comparison
        ↓
Final Model
        ↓
Flask Deployment
```

---

## 🎯 Goal of the Project

The goal of FraudGuard AI is to demonstrate how Machine Learning can be applied to a real-world financial problem — identifying potentially fraudulent transactions through data analysis, multiple model experiments, evaluation, and deployment.

This project combines **Data Analysis + Machine Learning + Model Evaluation + Flask Deployment** into one complete workflow.
