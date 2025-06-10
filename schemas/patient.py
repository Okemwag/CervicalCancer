from pydantic import BaseModel
from datetime import datetime

class PatientBase(BaseModel):
    name: str
    age: int
    phone: str
    pregnancies: int
    smoking: bool
    contraceptive_use: bool
    sexual_partners: int
    std_history: bool

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True