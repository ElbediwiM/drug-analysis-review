
class DummyMedicineModel:
    def __init__(self):
        self.medicine_map = {
            "headache": "Paracetamol",
            "fever": "Ibuprofen",
            "nausea": "Ondansetron",
            "cough": "Dextromethorphan",
            "cold": "Cetirizine",
        }

    def predict(self, input_data):
        # input_data is a dict
        condition = input_data.get("condition", "").strip().lower()
        return [self.medicine_map.get(condition, "No recommendation found.")]
