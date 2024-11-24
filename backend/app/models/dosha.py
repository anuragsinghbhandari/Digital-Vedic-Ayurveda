from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class DoshaType(str, Enum):
    VATA = "vata"
    PITTA = "pitta"
    KAPHA = "kapha"

class DoshaProfile(BaseModel):
    primary_dosha: str = Field(..., description="Primary dosha type")
    secondary_dosha: Optional[str] = Field(None, description="Secondary dosha type")
    vata_percentage: float = Field(..., ge=0, le=100)
    pitta_percentage: float = Field(..., ge=0, le=100)
    kapha_percentage: float = Field(..., ge=0, le=100)
    
    class Config:
        schema_extra = {
            "example": {
                "primary_dosha": "vata",
                "secondary_dosha": "pitta",
                "vata_percentage": 60.0,
                "pitta_percentage": 25.0,
                "kapha_percentage": 15.0
            }
        }

class DoshaCharacteristic(BaseModel):
    trait_name: str
    vata_score: int = Field(..., ge=0)
    pitta_score: int = Field(..., ge=0)
    kapha_score: int = Field(..., ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "trait_name": "body_frame",
                "vata_score": 3,
                "pitta_score": 1,
                "kapha_score": 0
            }
        }