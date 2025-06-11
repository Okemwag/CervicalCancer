import joblib
import pandas as pd
from pathlib import Path

class CervicalCancerPredictor:
    def __init__(self):
        model_path = Path("data/models/risk_model.pkl")
        self.model = joblib.load(model_path)
    
    def predict(self, patient_data: dict) -> dict:
        # Convert to DataFrame
        df = pd.DataFrame([patient_data])
        
        # Get prediction
        risk_score = self.model.predict_proba(df)[0][1]
        
        # Determine risk level
        if risk_score < 0.3:
            risk_level = "Low"
        elif risk_score < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
            
        return {
            "risk_score": float(risk_score),
            "risk_level": risk_level
        }