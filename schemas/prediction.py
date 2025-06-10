from pydantic import BaseModel
from datetime import datetime

class PredictionRequest(BaseModel):
    patient_id: int
    age: int
    pregnancies: int
    smoking: bool
    contraceptive_use: bool
    sexual_partners: int
    std_history: bool

class PredictionResponse(BaseModel):
    id: int
    patient_id: int
    risk_score: float
    risk_level: str
    created_at: datetime
    recommendations: list[str]