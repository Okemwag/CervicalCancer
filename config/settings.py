from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./cervical_cancer.db"
    
    # Security
    secret_key: str = "sxdcfgvbhjnmkloiuytrewq1234567890"
    
    # API Settings
    api_title: str = "Cervical Cancer Risk Predictor"
    api_version: str = "1.0.0"
    
    # ML Model Settings
    model_path: str = "data/models/risk_model.pkl"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()

