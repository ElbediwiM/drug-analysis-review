from fastapi import FastAPI
from pydantic import BaseModel
import pickle

from models.dummy_model import DummyMedicineModel

# Load the dummy model
with open("models/pickled_dummy_model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

# Define input schema
class PatientData(BaseModel):
    age: int
    gender: str
    condition: str
    ease_of_use: int
    effectiveness: int

# Root endpoint
@app.get("/")
def root():
    return {"greeting": "hello"}

# Prediction endpoint
@app.post("/predict")
def predict_medicine(patient: PatientData):
    input_data = patient.model_dump()  # single dict, not a list
    prediction = model.predict(input_data)
    return {"medicine": prediction[0]}
