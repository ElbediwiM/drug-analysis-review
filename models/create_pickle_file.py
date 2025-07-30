import pickle
from models.dummy_model import DummyMedicineModel

model = DummyMedicineModel()
with open("models/pickled_dummy_model.pkl", "wb") as f:
    pickle.dump(model, f)
