from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from tensorflow.keras.models import model_from_json
import numpy as np

app = FastAPI()

# Load the logistic regression model
with open("models/logisitc_model.pkl2", "rb") as f:
    medicine_model = joblib.load(f)

# Load LSTM model architecture and weights
with open("models/carmen_lstm_model_architecture.json", "r") as json_file:
    json_config = json_file.read()

lstm_model = model_from_json(json_config)
lstm_model.load_weights("models/carmen_lstm_model.weights.h5")

# --- SCHEMAS ---

class PatientData(BaseModel):
    age: int
    gender: str
    condition: str
    ease_of_use: int
    effectiveness: int
    satisfaction: int

class DoctorInput(BaseModel):
    drug: float
    condition: float

# --- ROUTES ---

@app.get("/")
def root():
    return {"greeting": "hello"}

@app.post("/predict")
def predict_medicine(patient: PatientData):
    input_df = pd.DataFrame([{
        "Age": patient.age,
        "EaseofUse": patient.ease_of_use,
        "Sex": patient.gender,
        "Effectiveness": patient.effectiveness,
        "Satisfaction": patient.satisfaction,
        "Condition": patient.condition
    }])
    prediction = medicine_model.predict(input_df)
    return {"medicine": prediction[0]}

@app.post("/satisfaction")
def predict_satisfaction(data: DoctorInput):
    # Model expects a 2D numpy array input
    input_array = np.array([[data.drug, data.condition]])
    prediction = lstm_model.predict(input_array)
    score = float(prediction[0][0])  # assuming output shape (1,1)
    return {"satisfaction_score": score}
