import streamlit as st
from prediction_helper import predict

st.title("Health Insurance Premium Prediction App")

st.header("Input Details")

# First Row: Gender, Region, Marital Status
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
with col2:
    dependants = st.number_input("Dependants", min_value=0, max_value=10, step=1)
with col3:
    income_lakhs = st.number_input("Income (Lakhs)", min_value=1, max_value=100)

col1, col2, col3 = st.columns(3)
with col1:
    gender = st.selectbox("Gender", ['Male', 'Female'])
with col2:
    region = st.selectbox("Region", ['Northeast', 'Northwest', 'Southeast', 'Southwest'])
with col3:
    marital_status = st.selectbox("Marital Status", ['Unmarried', 'Married'])

# Second Row: BMI Category, Smoking Status, Employment Status
col4, col5, col6 = st.columns(3)
with col4:
    bmi_category = st.selectbox("BMI Category", ['Overweight', 'Underweight', 'Normal', 'Obesity'])
with col5:
    smoking_status = st.selectbox(
        "Smoking Status",
        ['No Smoking', 'Occasional', 'Regular',]
    )
with col6:
    employment_status = st.selectbox(
        "Employment Status",
        ['Self-Employed', 'Freelancer', 'Salaried']
    )

# Third Row: Income Level, Medical History, Insurance Plan
col7, col8, col9 = st.columns(3)
with col7:
    genetical_risk = st.number_input(
        "Genetical Risk",
        min_value=0, max_value=5, step=1
    )
with col8:
    medical_history = st.selectbox(
        "Medical History",
        [
            'High blood pressure',
            'No Disease',
            'Diabetes & High blood pressure',
            'Diabetes & Heart disease',
            'Diabetes',
            'Diabetes & Thyroid',
            'Heart disease',
            'Thyroid',
            'High blood pressure & Heart disease'
        ]
    )
with col9:
    insurance_plan = st.selectbox(
        "Insurance Plan",
        ['Silver', 'Bronze', 'Gold']
    )


input_dict = {
    "Age": age,
    "Dependants": dependants,
    "Income in Lakhs": income_lakhs,
    "Genetical Risk": genetical_risk,
    "Insurance Plan": insurance_plan,
"Employment Status": employment_status,
    "Gender": gender,
"Marital Status": marital_status,
"BMI Category": bmi_category,
"Smoking Status": smoking_status,
    "Region": region,



    "Medical History": medical_history,



}


if st.button("Predict"):
    print('Predict Clicked!')
    prediction = predict(input_dict)
    st.success(f'Predicted Premium: {prediction}')
