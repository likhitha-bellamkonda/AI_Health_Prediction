# 🩺 AI Health Prediction Application

## Project Overview

The AI Health Prediction Application is a machine learning-powered healthcare system developed using Python, Streamlit, SQL Server, and Scikit-learn.

The application allows users to manage patient records through CRUD operations (Create, Read, Update, Delete) and automatically predicts health risk categories based on patient health parameters such as Glucose, Haemoglobin, and Cholesterol levels.

The system stores patient information in SQL Server and generates AI-based health remarks using a trained Random Forest Machine Learning model.

---

## Features

### Patient Management

* Add Patient Records
* View Patient Records
* Update Patient Records
* Delete Patient Records

### AI Health Prediction

Predicts patient health status based on medical parameters.

Prediction Categories:

* Healthy
* Diabetes Risk
* Heart Disease Risk
* Diabetes & Heart Disease Risk

### Input Validation

* Full Name validation
* Email validation
* Future Date of Birth restriction

### Database Integration

* SQL Server Database
* Persistent Data Storage
* CRUD Operations

---

## Technologies Used

### Programming Language

* Python

### Machine Learning

* Scikit-learn
* Random Forest Classifier
* Label Encoder

### Database

* Microsoft SQL Server
* PyODBC

### Frontend

* Streamlit

### Data Processing

* Pandas
* Joblib

---

## Project Structure

Health_Prediction_App

├── app.py

├── train_model.py

├── health_data.csv

├── model.pkl

├── label_encoder.pkl

├── requirements.txt

├── README.md

└── .gitignore

---

## Dataset Features

Input Features:

* Glucose
* Haemoglobin
* Cholesterol

Target Variable:

* Condition

Classes:

* Healthy
* Diabetes Risk
* Heart Disease Risk
* Diabetes & Heart Disease Risk

---

## Machine Learning Workflow

1. Load Dataset
2. Data Preprocessing
3. Label Encoding
4. Train-Test Split
5. Random Forest Training
6. Model Evaluation
7. Save Model
8. Streamlit Integration

---

## Model Performance

Model Used:

* Random Forest Classifier

Performance Metrics:

* Accuracy: 99%
* Precision: 99%
* Recall: 99%
* F1-Score: 99%

---

## Database Design

Table Name:
patients

Columns:

* id
* full_name
* dob
* email
* glucose
* haemoglobin
* cholesterol
* remarks

---

## Installation

### Clone Repository

git clone <repository-url>

### Install Dependencies

pip install -r requirements.txt

### Configure SQL Server

Update the SQL Server connection details in app.py:

* Server Name
* Database Name
* Username
* Password

### Run Application

streamlit run app.py

---

## Future Enhancements

* Cloud Deployment
* User Authentication
* Dashboard Analytics
* Advanced Disease Prediction Models
* Email Notifications

---

## Author

Likhitha Bellamkonda

Data Science Graduate

Skills:

* Python
* Machine Learning
* SQL Server
* Streamlit
* Power BI
* Data Analytics
