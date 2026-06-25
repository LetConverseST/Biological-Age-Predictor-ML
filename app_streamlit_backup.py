import streamlit as st
from predict import predict_age

st.set_page_config(
    page_title="Biological Age Predictor",
    page_icon="🧬",
    layout="wide"
)

# Custom styling
st.markdown("""
    <style>
        .main {
            background-color: #0f172a;
        }
        .stApp {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
        }
        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #38bdf8;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #cbd5e1;
            margin-bottom: 30px;
        }
        .result-box {
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">🧬 Biological Age Prediction Model</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Predict your biological age using health, lifestyle, and physiological factors.</div>',
    unsafe_allow_html=True
)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Personal Details")
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 100.0, 250.0)
    weight = st.number_input("Weight (kg)", 20.0, 300.0)
    bp = st.text_input("Blood Pressure (e.g. 120/80)")
    bmi = st.number_input("BMI")

    st.subheader("🩺 Medical Details")
    cholesterol = st.number_input("Cholesterol Level (mg/dL)")
    glucose = st.number_input("Blood Glucose Level (mg/dL)")
    bone_density = st.number_input("Bone Density (g/cm²)")
    vision = st.number_input("Vision Sharpness")
    hearing = st.number_input("Hearing Ability (dB)")

with col2:
    st.subheader("🏃 Lifestyle")
    physical = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
    smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
    alcohol = st.selectbox("Alcohol Consumption", ["Occasional", "Frequent"])
    diet = st.selectbox("Diet", ["Low-carb", "Balanced", "Vegetarian", "High-fat"])
    sleep = st.selectbox("Sleep Patterns", ["Insomnia", "Normal", "Excessive"])
    stress = st.slider("Stress Levels", 0, 10)

    st.subheader("🧠 Additional Factors")
    chronic = st.selectbox("Chronic Diseases", ["Hypertension", "Diabetes", "Heart Disease"])
    medication = st.selectbox("Medication Use", ["Regular", "Occasional"])
    family = st.selectbox("Family History", ["Heart Disease", "Hypertension", "Diabetes"])
    cognitive = st.slider("Cognitive Function", 0, 100)
    mental = st.selectbox("Mental Health Status", ["Poor", "Fair", "Good", "Excellent"])
    pollution = st.slider("Pollution Exposure", 0, 10)
    sun = st.slider("Sun Exposure", 0, 10)
    education = st.selectbox("Education Level", ["High School", "Undergraduate", "Postgraduate"])
    income = st.selectbox("Income Level", ["Low", "Medium", "High"])

# Predict button
st.markdown("---")

if st.button("🔍 Predict Biological Age", use_container_width=True):
    input_data = {
        "Gender": gender,
        "Height (cm)": height,
        "Weight (kg)": weight,
        "Blood Pressure (s/d)": bp,
        "Cholesterol Level (mg/dL)": cholesterol,
        "BMI": bmi,
        "Blood Glucose Level (mg/dL)": glucose,
        "Bone Density (g/cm²)": bone_density,
        "Vision Sharpness": vision,
        "Hearing Ability (dB)": hearing,
        "Physical Activity Level": physical,
        "Smoking Status": smoking,
        "Alcohol Consumption": alcohol,
        "Diet": diet,
        "Chronic Diseases": chronic,
        "Medication Use": medication,
        "Family History": family,
        "Cognitive Function": cognitive,
        "Mental Health Status": mental,
        "Sleep Patterns": sleep,
        "Stress Levels": stress,
        "Pollution Exposure": pollution,
        "Sun Exposure": sun,
        "Education Level": education,
        "Income Level": income
    }

    result = predict_age(input_data)

    # Risk logic
    if result < 30:
        color = "#22c55e"
        status = "Healthy"
    elif result < 50:
        color = "#eab308"
        status = "Moderate"
    else:
        color = "#ef4444"
        status = "High Risk"

    st.markdown(
        f"""
        <div class="result-box" style="background-color:{color};">
            Predicted Biological Age: {result:.2f} Years <br>
            Status: {status}
        </div>
        """,
        unsafe_allow_html=True
    )