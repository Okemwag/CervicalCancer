from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database.connection import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    phone = Column(String)
    pregnancies = Column(Integer)
    smoking = Column(Boolean)
    contraceptive_use = Column(Boolean)
    sexual_partners = Column(Integer)
    std_history = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)