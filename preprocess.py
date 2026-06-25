import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


def preprocess_data(path):
    df = pd.read_csv(path)

    # Split blood pressure
    df[['Systolic', 'Diastolic']] = df['Blood Pressure (s/d)'].str.split('/', expand=True).astype(float)
    df.drop(columns=['Blood Pressure (s/d)'], inplace=True)

    categorical_cols = df.select_dtypes(include=['object']).columns
    encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    target_col = "Age (years)"

    X = df.drop(columns=[target_col])
    y = df[target_col]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, encoders