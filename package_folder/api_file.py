from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Load the trained logistic regression model pipeline with joblib
#Because it is more efficient for more complex and larger models
with open("models/logisitc_model.pkl2", "rb") as f:  # spelling matches saved file
    model = joblib.load(f)

app = FastAPI()

# Define the input schema expected by the API
class PatientData(BaseModel):
    age: int
    gender: str
    condition: str
    ease_of_use: int
    effectiveness: int
    satisfaction: int

# Root endpoint
@app.get("/")
def root():
    return {"greeting": "hello"}

# Prediction endpoint
@app.post("/predict")
def predict_medicine(patient: PatientData):
    # Prepare input data for model
    input_df = pd.DataFrame([{
        "Age": patient.age,
        "EaseofUse": patient.ease_of_use,
        "Sex": patient.gender,
        "Effectiveness": patient.effectiveness,
        "Satisfaction": patient.satisfaction,
        "Condition": patient.condition
    }])

    # Predict drug recommendation
    prediction = model.predict(input_df)

    return {"medicine": prediction[0]}
