from typing import Dict
import numpy as np
from ..models.dosha import DoshaProfile, DoshaType, DoshaCharacteristic

class DoshaAnalyzer:
    def __init__(self):
        self.characteristic_weights = {
            "body_frame": 2.0,
            "skin_type": 1.5,
            "digestion": 2.0,
            "sleep_pattern": 1.5,
            "stress_response": 1.8,
        }
    
    def analyze_dosha(self, user_responses: Dict[str, DoshaCharacteristic]) -> Dict:
        scores = {
            "vata": 0.0,
            "pitta": 0.0,
            "kapha": 0.0
        }
        
        total_weight = sum(self.characteristic_weights.values())
        
        for trait, response in user_responses.items():
            weight = self.characteristic_weights.get(trait, 1.0)
            scores["vata"] += response['vata_score'] * weight
            scores["pitta"] += response['pitta_score'] * weight
            scores["kapha"] += response['kapha_score'] * weight
        
        # Normalize scores to percentages
        total_score = sum(scores.values())
        percentages = {
            dosha: (score / total_score) * 100 
            for dosha, score in scores.items()
        }
        
        # Determine primary and secondary doshas
        sorted_doshas = sorted(
            percentages.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Create response dictionary
        response = {
            "primary_dosha": sorted_doshas[0][0],
            "secondary_dosha": sorted_doshas[1][0] if sorted_doshas[1][1] > 25 else None,
            "vata_percentage": percentages["vata"],
            "pitta_percentage": percentages["pitta"],
            "kapha_percentage": percentages["kapha"]
        }
        
        return response 