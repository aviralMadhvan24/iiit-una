from app.ml.model_loader import ModelLoader

class InferenceService:
    def __init__(self):
        loader = ModelLoader()
        self.model = loader.model
        self.scaler = loader.scaler

    def predict(self, features: list[float]) -> float:
        X_scaled = self.scaler.transform([features])
        return float(-self.model.score_samples(X_scaled)[0])
