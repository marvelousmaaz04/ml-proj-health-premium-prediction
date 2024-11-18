from joblib import load
import pandas as pd

model_young = load('artifacts/model_young.joblib')
model_rest = load('artifacts/model_rest.joblib')

scaler_young = load('artifacts/scaler_young.joblib')
scaler_rest = load('artifacts/scaler_rest.joblib')

def calc_normalized_risk_score(medical_history):
    # Define risk scores
    risk_scores = {
        'diabetes': 6,
        'heart disease': 8,
        'high blood pressure': 6,
        'thyroid': 4,
        'no disease': 0,
        'none': 0,
    }



    # Split medical history into individual diseases
    diseases = medical_history.lower().split(' & ')

    # Calculate total risk score
    total_risk_score = sum(risk_scores.get(disease.strip(), 0) for disease in diseases)
    # Min and Max possible risk scores
    min_risk = 0
    max_risk = 14
    # Apply Min-Max scaling
    normalized_risk_score = (total_risk_score - min_risk) / (max_risk - min_risk)

    return normalized_risk_score


def preprocess_input(input_dict):
    # Define the expected columns in the model
    expected_columns = [
        'age', 'number_of_dependants',
        'income_lakhs', 'insurance_plan', 'genetical_risk',
        'normalized_risk_score', 'gender_Male', 'region_Northwest',
        'region_Southeast', 'region_Southwest', 'marital_status_Unmarried',
        'bmi_category_Obesity', 'bmi_category_Overweight', 'bmi_category_Underweight',
        'smoking_status_Occasional', 'smoking_status_Regular', 'employment_status_Salaried',
        'employment_status_Self-Employed'
    ]

    # Encoding mappings
    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}


    # Initialize a DataFrame with all zeros
    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    # Fill in numeric features directly
    df['age'] = input_dict['Age']
    df['number_of_dependants'] = input_dict['Dependants']
    df['income_lakhs'] = input_dict['Income in Lakhs']
    df['genetical_risk'] = input_dict['Genetical Risk']

    # Map and fill encoded categorical fields
    df['insurance_plan'] = insurance_plan_encoding[input_dict['Insurance Plan']]

    # One-hot encode categorical features
    if input_dict['Gender'] == 'Male':
        df['gender_Male'] = 1
    if input_dict['Region'] == 'Northwest':
        df['region_Northwest'] = 1
    elif input_dict['Region'] == 'Southeast':
        df['region_Southeast'] = 1
    elif input_dict['Region'] == 'Southwest':
        df['region_Southwest'] = 1

    if input_dict['Marital Status'] == 'Unmarried':
        df['marital_status_Unmarried'] = 1

    if input_dict['BMI Category'] == 'Obesity':
        df['bmi_category_Obesity'] = 1
    elif input_dict['BMI Category'] == 'Overweight':
        df['bmi_category_Overweight'] = 1
    elif input_dict['BMI Category'] == 'Underweight':
        df['bmi_category_Underweight'] = 1

    if input_dict['Smoking Status'] == 'Occasional':
        df['smoking_status_Occasional'] = 1
    elif input_dict['Smoking Status'] == 'Regular':
        df['smoking_status_Regular'] = 1

    if input_dict['Employment Status'] == 'Salaried':
        df['employment_status_Salaried'] = 1
    elif input_dict['Employment Status'] == 'Self-Employed':
        df['employment_status_Self-Employed'] = 1

    # Normalize or scale numeric fields if needed (e.g., normalized_risk_score)
    # Example: Add normalized risk score
    df['normalized_risk_score'] = calc_normalized_risk_score(input_dict['Medical History'])
    df = handle_scaling(input_dict['Age'], df)
    return df

def handle_scaling(age, df):
    if age <= 25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    scaler = scaler_object['scaler']
    cols_to_scale = scaler_object['cols_to_scale']
    print(cols_to_scale)
    # Be careful, don't use fit_transform, use transform only since we want the exact same scaling to be replicated
    df['income_level'] = None # creating dummy columns
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df.drop('income_level', axis=1, inplace=True)
    return df

def predict(input_dict):
    input_df = preprocess_input(input_dict)

    if input_dict['Age'] <= 25:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)


    print(input_dict)
    return int(prediction)