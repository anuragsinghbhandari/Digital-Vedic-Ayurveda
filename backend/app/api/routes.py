from typing import Dict
from ..models.dosha import DoshaProfile, DoshaCharacteristic
from ..models.consultation import ConsultationRequest
from ..services.dosha_analyzer import DoshaAnalyzer
from ..services.recommendation_engine import RecommendationEngine
from ..services.consultation_service import ConsultationService


dosha_analyzer = DoshaAnalyzer()
recommendation_engine = RecommendationEngine()
consultation_service = ConsultationService()


def analyze_dosha(user_responses: Dict[str, DoshaCharacteristic]):
    try:
        # Get dosha analysis
        dosha_results = dosha_analyzer.analyze_dosha(user_responses)
        
        # Get recommendations using the dosha results
        recommendations = recommendation_engine.get_recommendations(dosha_results)
        
        # Combine results
        response = {
            **dosha_results,
            "recommendations": recommendations
        }
        
        return response
    except Exception as e:
        raise e

def get_recommendations(dosha_type: str):
    try:
        # Create a mock dosha profile for the specific dosha type
        dosha_profile = {
            "primary_dosha": dosha_type,
            "secondary_dosha": None,
            "vata_percentage": 100 if dosha_type == "vata" else 0,
            "pitta_percentage": 100 if dosha_type == "pitta" else 0,
            "kapha_percentage": 100 if dosha_type == "kapha" else 0
        }
        
        recommendations = recommendation_engine.get_recommendations(dosha_profile)
        return recommendations
    except Exception as e:
        raise e


def get_personal_consultation(consultation_data: ConsultationRequest):
    try:
        recommendations = consultation_service.get_personalized_recommendations(
            consultation_data
        )
        return recommendations
    except Exception as e:
        raise e 