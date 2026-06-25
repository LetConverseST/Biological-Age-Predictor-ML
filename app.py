import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from predict import predict_age

app = FastAPI(title="Biological Age Predictor API")

# Ensure static folder exists
os.makedirs("static", exist_ok=True)

def generate_health_tips(data, predicted_age):
    tips = []
    
    # 1. Stress
    stress = float(data.get("Stress Levels", 0))
    if stress >= 7:
        tips.append({
            "category": "Stress Management",
            "icon": "🧠",
            "text": f"Your stress level is high ({stress:.1f}/10). Elevated cortisol accelerates cellular aging. Practice mindfulness, deep breathing, or yoga to lower stress.",
            "impact": "High"
        })
    elif stress >= 4:
        tips.append({
            "category": "Stress Management",
            "icon": "🧠",
            "text": "Moderate stress levels detected. Prioritize work-life balance and schedule daily relaxation breaks to maintain cognitive health.",
            "impact": "Medium"
        })
        
    # 2. Smoking
    smoking = data.get("Smoking Status", "")
    if smoking == "Current":
        tips.append({
            "category": "Cardiovascular Health",
            "icon": "🚬",
            "text": "Current smoking accelerates arterial stiffness and DNA damage. Quitting smoking is the single most effective way to lower your biological age.",
            "impact": "High"
        })
    elif smoking == "Former":
        tips.append({
            "category": "Cardiovascular Health",
            "icon": "🫁",
            "text": "Great job on quitting smoking! Your cardiovascular system is recovering. Keep maintaining a clean environment.",
            "impact": "Positive"
        })

    # 3. Blood Glucose
    glucose = float(data.get("Blood Glucose Level (mg/dL)", 0))
    if glucose > 140:
        tips.append({
            "category": "Metabolic Health",
            "icon": "🩸",
            "text": f"Blood glucose is elevated ({glucose:.1f} mg/dL). High blood sugar causes glycation, damaging collagen and blood vessels. Limit simple carbs.",
            "impact": "High"
        })
    elif glucose < 80:
        tips.append({
            "category": "Metabolic Health",
            "icon": "🩸",
            "text": f"Blood glucose is slightly low ({glucose:.1f} mg/dL). Ensure you have balanced meals with complex carbohydrates and proteins.",
            "impact": "Medium"
        })

    # 4. Cholesterol
    cholesterol = float(data.get("Cholesterol Level (mg/dL)", 0))
    if cholesterol > 240:
        tips.append({
            "category": "Cardiovascular Health",
            "icon": "❤️",
            "text": f"High cholesterol level ({cholesterol:.1f} mg/dL). Incorporate soluble fiber (oats, beans), healthy fats (olive oil, avocados), and regular exercise.",
            "impact": "High"
        })

    # 5. Physical Activity
    activity = data.get("Physical Activity Level", "")
    if activity == "Low":
        tips.append({
            "category": "Physical Fitness",
            "icon": "🏃",
            "text": "Sedentary lifestyle speeds up muscular and joint aging. Aim for at least 150 minutes of moderate aerobic exercise (e.g. brisk walking) weekly.",
            "impact": "High"
        })
    elif activity == "High":
        tips.append({
            "category": "Physical Fitness",
            "icon": "⚡",
            "text": "Excellent physical activity level! This maintains mitochondrial health, keeps muscles strong, and preserves biological youth.",
            "impact": "Positive"
        })

    # 6. Sleep
    sleep = data.get("Sleep Patterns", "")
    if sleep == "Insomnia":
        tips.append({
            "category": "Rest & Recovery",
            "icon": "😴",
            "text": "Chronic insomnia disrupts cellular repair and cognitive cleanup. Establish a soothing pre-bed routine: avoid screens and stimulants.",
            "impact": "High"
        })
    elif sleep == "Excessive":
        tips.append({
            "category": "Rest & Recovery",
            "icon": "🛌",
            "text": "Excessive sleep can be a marker of fatigue or low energy levels. Focus on improving sleep quality and consistency.",
            "impact": "Medium"
        })

    # 7. Bone Density
    bone = float(data.get("Bone Density (g/cm²)", 0))
    if bone < 0.5:
        tips.append({
            "category": "Bone & Joint",
            "icon": "🦴",
            "text": f"Low bone density ({bone:.2f} g/cm²). Perform resistance training to stimulate bone growth and check Calcium & Vitamin D intake.",
            "impact": "High"
        })

    # 8. BMI
    bmi = float(data.get("BMI", 0))
    if bmi > 28:
        tips.append({
            "category": "Weight Management",
            "icon": "⚖️",
            "text": f"Your BMI is elevated ({bmi:.1f}). Focus on body composition improvements rather than just weight loss. Consult a dietitian.",
            "impact": "Medium"
        })
    elif bmi < 18.5:
        tips.append({
            "category": "Weight Management",
            "icon": "⚖️",
            "text": f"Your BMI is on the lower side ({bmi:.1f}). Ensure you are consuming adequate calories and protein for your height.",
            "impact": "Medium"
        })

    # 9. Sun Exposure
    sun = float(data.get("Sun Exposure", 0))
    if sun >= 8:
        tips.append({
            "category": "Skin Health",
            "icon": "☀️",
            "text": f"High sun exposure ({sun:.1f}/10) speeds up skin photoaging and wrinkling. Always apply broad-spectrum SPF 30+ sunscreen.",
            "impact": "Medium"
        })

    # 10. Alcohol
    alcohol = data.get("Alcohol Consumption", "")
    if alcohol == "Frequent":
        tips.append({
            "category": "Liver & Brain Health",
            "icon": "🍷",
            "text": "Frequent alcohol consumption dehydrates body cells and stresses the liver. Limit your intake to improve skin elasticity and liver health.",
            "impact": "High"
        })

    # Default tip if list is short
    if len(tips) < 3:
        tips.append({
            "category": "General Wellness",
            "icon": "🌱",
            "text": "Keep staying hydrated, eating whole foods, and keeping regular annual checkups to monitor your bio-markers.",
            "impact": "Positive"
        })
        
    return tips

@app.post("/api/predict")
async def predict(request: Request):
    try:
        input_data = await request.json()
        
        # Map user-friendly "None" to "nan" as expected by the LabelEncoder
        cols_to_map = ["Alcohol Consumption", "Chronic Diseases", "Medication Use", "Family History", "Education Level"]
        for col in cols_to_map:
            if col in input_data and (input_data[col] == "None" or input_data[col] is None or input_data[col] == ""):
                input_data[col] = "nan"
                
        # Handle formatting for blood pressure
        # Ensure it has the correct form
        bp = input_data.get("Blood Pressure (s/d)", "120/80")
        if "/" not in bp:
            bp = "120/80"
        input_data["Blood Pressure (s/d)"] = bp
        
        # Make prediction
        predicted_age = float(predict_age(input_data))
        
        # Risk logic
        if predicted_age < 30:
            color = "#22c55e"
            status = "Optimal"
        elif predicted_age < 50:
            color = "#eab308"
            status = "Moderate"
        else:
            color = "#ef4444"
            status = "High Risk"
            
        tips = generate_health_tips(input_data, predicted_age)
        
        return {
            "success": True,
            "predicted_age": predicted_age,
            "status": status,
            "color": color,
            "tips": tips
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Serve Static files
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    # Read port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on http://localhost:{port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)