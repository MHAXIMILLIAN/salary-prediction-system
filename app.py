# app.py - Salary Prediction System Streamlit App

import streamlit as st
import pandas as pd
import joblib

# Load trained model
MODEL_PATH = r"C:\Users\valen\PycharmProjects\Salary_Prediction_System\best_salary_model.pkl"
model = joblib.load(MODEL_PATH)

st.set_page_config(page_title="Salary Prediction System", layout="wide")
st.title("💼 Salary Prediction System")

st.markdown("""
Predict an employee's salary based on their features using the trained machine learning model.
""")

# Input fields
with st.form("salary_form"):
    st.subheader("Employee Details")
    age = st.number_input("Age", min_value=18, max_value=70, value=30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    education = st.selectbox("Education Level", ["HighSchool", "Bachelor's", "Masters", "PhD"])
    job_title = st.text_input("Job Title", "Software Engineer")
    experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=5)

    submitted = st.form_submit_button("Predict Salary")

if submitted:
    # Create dataframe for model
    input_df = pd.DataFrame({
        "Age": [age],
        "Gender": [gender],
        "Education Level": [education],
        "Job Title": [job_title],
        "Years of Experience": [experience]
    })

    # Predict salary
    predicted_salary = model.predict(input_df)[0]

    st.success(f"💰 Predicted Salary: ${predicted_salary:,.0f}")
