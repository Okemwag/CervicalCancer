# FastAPI + ML Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # App configuration
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py        # API endpoints
│   │   └── dependencies.py  # Route dependencies
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py    # Database connection
│   │   └── session.py       # Database sessions
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── patient.py       # Patient database model
│   │   ├── appointment.py   # Appointment model
│   │   ├── clinic.py        # Clinic model
│   │   └── prediction.py    # Prediction history model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── patient.py       # Patient request/response schemas
│   │   ├── appointment.py   # Appointment schemas
│   │   ├── prediction.py    # Prediction schemas
│   │   └── clinic.py        # Clinic schemas
│   │
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── patient.py       # Patient CRUD operations
│   │   ├── appointment.py   # Appointment CRUD
│   │   └── prediction.py    # Prediction CRUD
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── model.py         # ML model class
│   │   ├── predictor.py     # Prediction service
│   │   └── training.py      # Model training functions
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── prediction_service.py  # Prediction business logic
│   │   ├── appointment_service.py # Appointment scheduling
│   │   └── notification_service.py # SMS/Email notifications
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py        # Logging setup
│       ├── validators.py    # Data validation
│       └── helpers.py       # Helper functions
│
├── data/
│   ├── raw/
│   │   └── cervical_data.csv
│   ├── processed/
│   │   └── clean_data.csv
│   └── models/
│       ├── risk_model.pkl
│       └── preprocessor.pkl
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_model_evaluation.ipynb
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_ml.py
│   └── test_services.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Key Files Overview:

### `app/main.py`
```python
from fastapi import FastAPI
from app.api.routes import router
from app.database.connection import create_tables
from app.config import settings

app = FastAPI(title="Cervical Cancer Risk Predictor")
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    create_tables()
```

### `app/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./cervical_cancer.db"
    secret_key: str = "your-secret-key"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### `app/database/connection.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
```

### `app/models/patient.py`
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.database.connection import Base
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
    created_at = Column(DateTime, default=datetime.utcnow)
```

### `app/schemas/patient.py`
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PatientBase(BaseModel):
    name: str
    age: int
    phone: str
    pregnancies: int
    smoking: bool
    contraceptive_use: bool

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### `app/schemas/prediction.py`
```python
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    age: int
    pregnancies: int
    smoking: bool
    contraceptive_use: bool
    sexual_partners: int
    std_history: bool

class PredictionResponse(BaseModel):
    risk_score: float
    risk_level: str  # "Low", "Medium", "High"
    recommendations: list[str]
```

### `app/ml/predictor.py`
```python
import joblib
import pandas as pd
from pathlib import Path

class CervicalCancerPredictor:
    def __init__(self):
        model_path = Path("data/models/risk_model.pkl")
        self.model = joblib.load(model_path)
    
    def predict(self, patient_data: dict) -> dict:
        df = pd.DataFrame([patient_data])
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
```

### `app/api/routes.py`
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_cancer_risk(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    service = PredictionService(db)
    return service.predict_risk(request)

@router.get("/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    # Get patient logic
    pass
```

### `app/services/prediction_service.py`
```python
from app.ml.predictor import CervicalCancerPredictor
from app.schemas.prediction import PredictionRequest, PredictionResponse

class PredictionService:
    def __init__(self, db):
        self.db = db
        self.predictor = CervicalCancerPredictor()
    
    def predict_risk(self, request: PredictionRequest) -> PredictionResponse:
        # Convert request to dict
        patient_data = request.dict()
        
        # Get prediction
        prediction = self.predictor.predict(patient_data)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(prediction["risk_level"])
        
        return PredictionResponse(
            risk_score=prediction["risk_score"],
            risk_level=prediction["risk_level"],
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, risk_level: str) -> list[str]:
        if risk_level == "High":
            return ["Schedule immediate screening", "Consult gynecologist"]
        elif risk_level == "Medium":
            return ["Schedule screening within 6 months", "Regular check-ups"]
        else:
            return ["Continue regular screening", "Maintain healthy lifestyle"]
```

### `requirements.txt`
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
pandas==2.1.4
scikit-learn==1.3.2
joblib==1.3.2
python-multipart==0.0.6
```

## This structure gives you:
- **Clean separation** of concerns
- **Easy testing** with dedicated test files
- **ML pipeline** for training and prediction
- **Database management** with SQLAlchemy
- **API validation** with Pydantic
- **Business logic** in services layer
- **Utilities** for common functions