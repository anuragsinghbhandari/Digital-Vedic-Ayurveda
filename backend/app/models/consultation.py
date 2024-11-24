from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class PersonalInfo(BaseModel):
    age: int = Field(..., ge=1, le=120)
    gender: str
    weight: float = Field(..., ge=20, le=200)
    height: float = Field(..., ge=100, le=250)
    bmi: float

class MedicalHistory(BaseModel):
    conditions: List[str]
    medications: Optional[str]

class Lifestyle(BaseModel):
    diet_type: str
    physical_activity: str
    sleep_hours: int = Field(..., ge=4, le=12)
    stress_level: str

class HealthConcerns(BaseModel):
    primary_concerns: str
    previous_treatments: Optional[str]

class ConsultationRequest(BaseModel):
    personal_info: PersonalInfo
    medical_history: MedicalHistory
    lifestyle: Lifestyle
    concerns: HealthConcerns
    dosha_profile: Optional[Dict] = None 