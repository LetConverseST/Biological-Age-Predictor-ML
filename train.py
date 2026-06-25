import joblib
from preprocess import preprocess_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor, StackingRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load and preprocess data
X, y, scaler, encoders = preprocess_data("dataset/Train.csv")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Base models
estimators = [
    ("lr", LinearRegression()),
    ("gbr", GradientBoostingRegressor()),
    ("catboost", CatBoostRegressor(verbose=0))
]

# Stacking model
model = StackingRegressor(
    estimators=estimators,
    final_estimator=LinearRegression()
)

# Train
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Model trained successfully")
print(f"MAE: {mae:.2f}")
print(f"R2 Score: {r2:.4f}")

# Save model and scaler
joblib.dump(model, "models/model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(encoders, "models/encoders.pkl")

print("Model saved successfully")