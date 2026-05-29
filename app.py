import streamlit as st
import pandas as pd
import pyodbc
import joblib
import re
from datetime import date, datetime
st.set_page_config(
    page_title="AI Health Prediction",
    page_icon="🩺",
    layout="wide"
)

model = joblib.load("model.pkl")
le = joblib.load("label_encoder.pkl")

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Your_Server_Name;"
    "Database=HealthDB;"
    "UID=Your_User_name;"
    "PWD=Your_password;"
)

cursor = conn.cursor()

def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def predict_health(glucose, haemoglobin, cholesterol):
    data = pd.DataFrame(
        [[glucose, haemoglobin, cholesterol]],
        columns=["Glucose", "Haemoglobin", "Cholesterol"]
    )
    pred = model.predict(data)
    result = le.inverse_transform(pred)
    return result[0]

def convert_to_date(value):
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value), "%Y-%m-%d").date()


st.set_page_config(page_title="AI Health Prediction", page_icon="🩺", layout="wide")

st.markdown("""
<style>
.main {
    background-color: #f4f8fb;
}
.stApp {
    background: linear-gradient(to right, #e3f2fd, #ffffff);
}
.title-box {
    background-color: #0d47a1;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}
.stButton>button {
    background-color: #0d47a1;
    color: white;
    border-radius: 8px;
    height: 45px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #1565c0;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-box">
    <h1>🩺 AI Health Prediction Application</h1>
    <p>Patient Health Risk Prediction using Machine Learning</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.title("📋 Navigation")
menu = st.sidebar.selectbox(
    "Menu",
    ["Add Patient", "View Patients", "Update Patient", "Delete Patient"]
)

if menu == "Add Patient":
    st.subheader("Add Patient")

    name = st.text_input("Full Name")

    dob = st.date_input(
        "Date of Birth",
        value=date(2002, 12, 16),
        min_value=date(1950, 1, 1),
        max_value=date.today()
    )

    email = st.text_input("Email Address")

    glucose = st.number_input("Glucose", min_value=0.0)
    haemoglobin = st.number_input("Haemoglobin", min_value=0.0)
    cholesterol = st.number_input("Cholesterol", min_value=0.0)

    if st.button("Save Patient"):
        if name == "":
            st.error("Full Name is required")
        elif not valid_email(email):
            st.error("Invalid email address")
        else:
            remarks = predict_health(glucose, haemoglobin, cholesterol)

            cursor.execute("""
            INSERT INTO patients
            (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                name, dob, email, glucose,
                haemoglobin, cholesterol, remarks
            ))

            conn.commit()
            st.success("Patient saved successfully!")
            st.info(f"AI Generated Remarks: {remarks}")

elif menu == "View Patients":
    st.subheader("View Patients")

    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()

    if len(rows) == 0:
        st.warning("No patient records found")
    else:
        data = [list(row) for row in rows]

        df = pd.DataFrame(
            data,
            columns=[
                "ID", "Full Name", "DOB", "Email",
                "Glucose", "Haemoglobin", "Cholesterol", "Remarks"
            ]
        )

        st.dataframe(df)

elif menu == "Update Patient":
    st.subheader("Update Patient")

    patient_id = st.number_input("Enter Patient ID", min_value=1, step=1)

    if st.button("Load Patient"):
        cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
        row = cursor.fetchone()

        if row:
            st.session_state["patient_data"] = list(row)
        else:
            st.error("Patient not found")

    if "patient_data" in st.session_state:
        row = st.session_state["patient_data"]

        name = st.text_input("Full Name", value=row[1])

        dob = st.date_input(
            "Date of Birth",
            value=convert_to_date(row[2]),
            min_value=date(1950, 1, 1),
            max_value=date.today()
        )

        email = st.text_input("Email Address", value=row[3])

        glucose = st.number_input("Glucose", value=float(row[4]), min_value=0.0)
        haemoglobin = st.number_input("Haemoglobin", value=float(row[5]), min_value=0.0)
        cholesterol = st.number_input("Cholesterol", value=float(row[6]), min_value=0.0)

        if st.button("Update Patient"):
            if name == "":
                st.error("Full Name is required")
            elif not valid_email(email):
                st.error("Invalid email address")
            else:
                remarks = predict_health(glucose, haemoglobin, cholesterol)

                cursor.execute("""
                UPDATE patients
                SET full_name=?,
                    dob=?,
                    email=?,
                    glucose=?,
                    haemoglobin=?,
                    cholesterol=?,
                    remarks=?
                WHERE id=?
                """, (
                    name, dob, email, glucose,
                    haemoglobin, cholesterol, remarks,
                    patient_id
                ))

                conn.commit()
                st.success("Patient updated successfully!")
                st.info(f"Updated AI Remarks: {remarks}")

elif menu == "Delete Patient":
    st.subheader("Delete Patient")

    patient_id = st.number_input("Enter Patient ID", min_value=1, step=1)

    if st.button("Delete Patient"):
        cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
        row = cursor.fetchone()

        if row:
            cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
            conn.commit()
            st.success("Patient deleted successfully!")
        else:
            st.error("Patient not found")