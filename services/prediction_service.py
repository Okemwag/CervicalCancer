from sqlalchemy.orm import Session
from ml.predictor import CervicalCancerPredictor
from models.prediction import Prediction
from schemas.prediction import PredictionRequest, PredictionResponse

class PredictionService:
    def __init__(self, db: Session):
        self.db = db
        self.predictor = CervicalCancerPredictor()
    
    def predict_risk(self, request: PredictionRequest) -> PredictionResponse:
        # Prepare data for ML model
        patient_data = {
            "age": request.age,
            "pregnancies": request.pregnancies,
            "smoking": request.smoking,
            "contraceptive_use": request.contraceptive_use,
            "sexual_partners": request.sexual_partners,
            "std_history": request.std_history
        }
        
        # Get prediction
        prediction = self.predictor.predict(patient_data)
        
        # Save to database
        db_prediction = Prediction(
            patient_id=request.patient_id,
            risk_score=prediction["risk_score"],
            risk_level=prediction["risk_level"]
        )
        self.db.add(db_prediction)
        self.db.commit()
        self.db.refresh(db_prediction)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(prediction["risk_level"])
        
        return PredictionResponse(
            id=db_prediction.id,
            patient_id=db_prediction.patient_id,
            risk_score=db_prediction.risk_score,
            risk_level=db_prediction.risk_level,
            created_at=db_prediction.created_at,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, risk_level: str) -> list[str]:
        if risk_level == "High":
            return [
                "Schedule immediate screening",
                "Consult gynecologist within 2 weeks",
                "Consider HPV testing"
            ]
        elif risk_level == "Medium":
            return [
                "Schedule screening within 6 months",
                "Regular check-ups",
                "Discuss risk factors with doctor"
            ]
        else:
            return [
                "Continue regular screening",
                "Maintain healthy lifestyle",
                "Annual check-up recommended"
            ]