import joblib
import pandas as pd

model = joblib.load("models/model.pkl")
scaler = joblib.load("models/scaler.pkl")
encoders = joblib.load("models/encoders.pkl")


def predict_age(input_data):
    systolic, diastolic = map(float, input_data["Blood Pressure (s/d)"].split('/'))

    # Make a copy to avoid modifying the input dictionary in-place
    data = input_data.copy()
    data["Systolic"] = systolic
    data["Diastolic"] = diastolic
    if "Blood Pressure (s/d)" in data:
        del data["Blood Pressure (s/d)"]

    df = pd.DataFrame([data])
    
    # Explicitly reorder columns to match the features used to fit the scaler
    df = df[list(scaler.feature_names_in_)]

    for col in df.columns:
        if col in encoders:
            df[col] = encoders[col].transform(df[col].astype(str))

    df_scaled = scaler.transform(df)

    prediction = model.predict(df_scaled)

    return prediction[0]