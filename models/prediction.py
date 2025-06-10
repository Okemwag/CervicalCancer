from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base
from datetime import datetime

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    risk_score = Column(Float)
    risk_level = Column(String)  # "Low", "Medium", "High"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient")