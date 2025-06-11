from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.patient import PatientCreate, PatientResponse
from schemas.prediction import PredictionRequest, PredictionResponse
from crud.patient import create_patient, get_patient, get_patients
from services.prediction_service import PredictionService

router = APIRouter()

# Patient endpoints
@router.post("/patients", response_model=PatientResponse)
def create_new_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db=db, patient=patient)

@router.get("/patients/{patient_id}", response_model=PatientResponse)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient(db, patient_id=patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/patients", response_model=list[PatientResponse])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_patients(db, skip=skip, limit=limit)

# Prediction endpoints
@router.post("/predict", response_model=PredictionResponse)
def predict_cancer_risk(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    service = PredictionService(db)
    return service.predict_risk(request)