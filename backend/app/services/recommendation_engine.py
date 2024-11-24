from typing import Dict, List
import requests
import json
import logging
from ..config import get_groq_api_key

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        try:
            # Get API key from config
            self.groq_api_key = get_groq_api_key()
            self.api_url = "https://api.groq.com/openai/v1/chat/completions"
            logger.info("Successfully loaded GROQ API key")
            
        except Exception as e:
            logger.error(f"Failed to initialize RecommendationEngine: {str(e)}")
            raise

    def get_recommendations(self, consultation_data: Dict) -> Dict:
        try:
            # Create detailed prompt based on consultation data
            prompt = self._create_consultation_prompt(consultation_data)
            
            # Get recommendations from LLM
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            # Updated model name and message format
            data = {
                "model": "llama-3.1-70b-versatile",  # Corrected model name
                "messages": [
                    {
                        "role": "user",
                        "content": prompt if prompt else "Provide general Ayurvedic recommendations"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 2048
            }
            
            logger.info(f"Sending request to Groq API with prompt length: {len(prompt)}")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"API call failed: {response.text}")
                return self._get_default_recommendations()
            
            # Parse and structure the response
            content = response.json()['choices'][0]['message']['content']
            return self._parse_consultation_response(content, consultation_data)
            
        except Exception as e:
            logger.error(f"Error in consultation service: {str(e)}")
            return self._get_default_recommendations()

    def _create_health_status_analysis(self, data: Dict) -> List[str]:
        """Create detailed health status analysis based on conditions and dosha"""
        try:
            conditions = data.get('medical_history', {}).get('conditions', [])
            dosha_profile = data.get('dosha_profile', {})
            analysis = []
            
            # Add dosha-based health analysis
            if dosha_profile:
                primary_dosha = dosha_profile.get('primary_dosha', '').lower()
                if primary_dosha:
                    analysis.append(f"Your {primary_dosha.title()} dominance influences your health patterns and tendencies.")
            
            # Add condition-specific analysis
            if not conditions or "None" in conditions:
                analysis.append("No current medical conditions reported. Focus will be on preventive care and maintaining dosha balance.")
            else:
                analysis.append("Current Health Conditions Analysis:")
                for condition in conditions:
                    if condition in self.condition_info:
                        analysis.append(f"• {condition}: {self.condition_info[condition]}")
            
            # Add lifestyle impact analysis
            lifestyle = data.get('lifestyle', {})
            if lifestyle:
                stress_level = lifestyle.get('stress_level', '').lower()
                sleep_hours = lifestyle.get('sleep_hours')
                physical_activity = lifestyle.get('physical_activity', '').lower()
                
                if stress_level in ['high', 'medium']:
                    analysis.append("• Current stress levels may be impacting your dosha balance and overall health.")
                if sleep_hours and (sleep_hours < 6 or sleep_hours > 9):
                    analysis.append("• Your sleep patterns may need attention for optimal health.")
                if physical_activity in ['sedentary', 'light']:
                    analysis.append("• Current activity levels suggest a need for increased movement and exercise.")
            
            return analysis if analysis else ["Please consult an Ayurvedic practitioner for a detailed health analysis."]
            
        except Exception as e:
            logger.error(f"Error creating health status analysis: {str(e)}")
            return ["Unable to generate health status analysis. Please consult a practitioner."]

    def _parse_consultation_response(self, response: str, consultation_data: Dict) -> Dict:
        sections = {
            "overview": {
                "condition_analysis": self._create_health_status_analysis(consultation_data),
                "dosha_impact": []
            },
            "recommendations": {
                "dietary": [],
                "lifestyle": [],
                "herbal": [],
                "therapeutic": [],
                "exercise": []
            },
            "warnings": []
        }
        
        current_section = None
        current_subsection = None
        
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            lower_line = line.lower()
            
            # Identify sections
            if 'dosha impact' in lower_line:
                current_section = 'overview'
                current_subsection = 'dosha_impact'
            elif 'dietary' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'dietary'
            elif 'lifestyle' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'lifestyle'
            elif 'exercise' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'exercise'
            elif 'herbal' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'herbal'
            elif 'therapeutic' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'therapeutic'
            elif any(word in lower_line for word in ['warning', 'caution', 'consideration']):
                current_section = 'warnings'
                current_subsection = None
            
            # Add content to appropriate section
            if current_section and (line.startswith(('•', '-', '*')) or line[0].isdigit()):
                cleaned_line = line.lstrip('•-*123456789. ')
                if cleaned_line and len(cleaned_line) > 10:  # Minimum length for meaningful content
                    if current_section == 'recommendations':
                        sections[current_section][current_subsection].append(cleaned_line)
                    elif current_section == 'overview':
                        sections[current_section][current_subsection].append(cleaned_line)
                    else:
                        sections[current_section].append(cleaned_line)
        
        return sections

    def _get_default_recommendations(self) -> Dict:
        """Provide default recommendations with health status analysis"""
        return {
            "overview": {
                "condition_analysis": ["Please consult an Ayurvedic practitioner for a detailed health analysis."],
                "dosha_impact": ["Please consult an Ayurvedic practitioner for detailed dosha analysis"]
            },
            "recommendations": {
                "dietary": ["Please consult an Ayurvedic practitioner for personalized dietary recommendations"],
                "lifestyle": ["Please consult an Ayurvedic practitioner for lifestyle recommendations"],
                "herbal": ["Please consult an Ayurvedic practitioner for herbal recommendations"],
                "therapeutic": ["Please consult an Ayurvedic practitioner for therapeutic recommendations"],
                "exercise": ["Please consult an Ayurvedic practitioner for exercise recommendations"]
            },
            "warnings": ["Please consult a healthcare provider before starting any new treatment regimen"]
        }
    
    # Ayurvedic condition descriptions
    condition_info = {
        "Diabetes": "In Ayurveda, diabetes (Prameha) is primarily seen as a Kapha disorder with possible Pitta involvement, characterized by impaired metabolism and tissue nutrition.",
        "Hypertension": "Hypertension in Ayurveda (Rakta Gata Vata) is often related to Vata and Pitta imbalances, affecting blood circulation and heart function.",
        "Arthritis": "Arthritis (Sandhivata) is typically viewed as a Vata disorder affecting the joints, with potential Ama (toxin) accumulation.",
        "Digestive Issues": "Digestive problems can involve all three doshas, with specific symptoms indicating the primary dosha imbalance. Often relates to Agni (digestive fire).",
        "Respiratory Problems": "Respiratory issues often involve Kapha dosha, with possible Vata and Pitta complications, affecting the Pranavaha Srotas (respiratory channels).",
        "Skin Conditions": "Skin disorders (Kushtha) can involve all three doshas, but often have a strong Pitta component, affecting the skin's health and appearance.",
        "Sleep Disorders": "Sleep issues are often related to Vata imbalance, though other doshas may be involved, affecting the natural sleep-wake cycle.",
        "Stress/Anxiety": "Anxiety and stress primarily affect Vata dosha, leading to mental and physical imbalances in the body-mind complex."
    }
    
    def _create_consultation_prompt(self, data: Dict) -> str:
        try:
            # Safely get all required data with defaults
            personal = data.get('personal_info', {})
            medical = data.get('medical_history', {})
            lifestyle = data.get('lifestyle', {})
            concerns = data.get('concerns', {})

            # Get dosha and condition information
            dosha_info = self._get_dosha_context(data.get('dosha_profile'))
            conditions_info = self._get_conditions_context(medical.get('conditions', []))
            
            # Ensure prompt is not empty
            prompt = f"""
            As an experienced Ayurvedic practitioner, provide comprehensive personalized recommendations for a patient with the following profile:

            {dosha_info}
            
            Personal Information:
            - Age: {personal.get('age', 'Not provided')}
            - Gender: {personal.get('gender', 'Not provided')}
            - BMI: {personal.get('bmi', 'Not provided')} (Weight: {personal.get('weight', 'Not provided')}kg, Height: {personal.get('height', 'Not provided')}cm)
            
            Medical Conditions and Ayurvedic Context:
            {conditions_info}
            
            Current Medications:
            {medical.get('medications', 'None reported')}
            
            Lifestyle Factors:
            - Diet: {lifestyle.get('diet_type', 'Not provided')}
            - Physical Activity: {lifestyle.get('physical_activity', 'Not provided')}
            - Sleep: {lifestyle.get('sleep_hours', 'Not provided')} hours
            - Stress Level: {lifestyle.get('stress_level', 'Not provided')}
            
            Primary Health Concerns:
            {concerns.get('primary_concerns', 'Not provided')}
            
            Previous Treatments:
            {concerns.get('previous_treatments', 'None reported')}

            Please provide specific, actionable recommendations in the following format:

            DOSHA IMPACT:
            - Explain how their current dosha state affects their health
            - Describe specific dosha-related symptoms to watch for
            - Suggest dosha-balancing priorities

            DIETARY RECOMMENDATIONS:
            - Specific foods to include or avoid
            - Best times and ways to consume
            - Quantity guidelines when applicable
            - Special preparations or combinations

            LIFESTYLE MODIFICATIONS:
            - Specific daily routine adjustments
            - Best times for activities
            - Duration and frequency
            - Practical implementation tips

            EXERCISE RECOMMENDATIONS:
            - Specific types of exercise
            - Intensity levels
            - Duration and frequency
            - Best times to practice
            - Precautions or modifications

            HERBAL REMEDIES:
            - Specific herb or formulation
            - Dosage and timing
            - Method of preparation
            - Duration of use
            - Specific benefits

            THERAPEUTIC TREATMENTS:
            - Specific therapy name
            - Frequency and duration
            - Expected benefits
            - Any preparations needed
            - Precautions

            WARNINGS AND PRECAUTIONS:
            - List specific contraindications
            - Interactions with medications
            - Signs to watch for
            - When to seek additional help

            Please ensure each recommendation is detailed and actionable.
            """
            
            return prompt.strip()
            
        except Exception as e:
            logger.error(f"Error creating consultation prompt: {str(e)}")
            return "Provide general Ayurvedic recommendations"
    
    def _parse_recommendations(self, response: str) -> Dict[str, List[str]]:
        """Parse the LLM response into structured recommendations"""
        sections = {
            "diet": [],
            "lifestyle": [],
            "exercises": [],
            "herbs": []
        }
        
        if not response:
            return self._get_default_recommendations()
        
        current_section = None
        lines = response.split('\n')
        
        for line in lines:
            if not line:
                continue
                
            line = line.strip()
            lower_line = line.lower()
            
            # Identify sections
            if 'diet' in lower_line:
                current_section = 'diet'
                continue
            elif 'lifestyle' in lower_line:
                current_section = 'lifestyle'
                continue
            elif 'exercise' in lower_line:
                current_section = 'exercises'
                continue
            elif 'herb' in lower_line:
                current_section = 'herbs'
                continue
            
            # Add recommendation if we're in a section and line starts with a bullet or number
            if current_section:
                if any(line.startswith(prefix) for prefix in ['•', '-', '*', '1.', '2.', '3.', '4.', '5.']):
                    cleaned_line = line.lstrip('•-*123456789. ')
                    if cleaned_line:
                        sections[current_section].append(cleaned_line)
        
        # Ensure each section has content
        for section in sections:
            if not sections[section]:
                sections[section] = [f"Please consult an Ayurvedic practitioner for {section} recommendations."]
        
        return sections
    
    def _get_default_recommendations(self) -> Dict[str, List[str]]:
        """Fallback recommendations if LLM fails"""
        return {
            "diet": ["Please consult an Ayurvedic practitioner for dietary recommendations"],
            "lifestyle": ["Please consult an Ayurvedic practitioner for lifestyle recommendations"],
            "exercises": ["Please consult an Ayurvedic practitioner for exercise recommendations"],
            "herbs": ["Please consult an Ayurvedic practitioner for herbal recommendations"]
        } 

    def _get_dosha_context(self, dosha_profile: Dict) -> str:
        """Safely get dosha context even if dosha profile is missing"""
        if not dosha_profile:
            return """
            Dosha Profile: Not Available
            Note: Recommendations will be based on current symptoms and conditions.
            Please complete a dosha analysis for more personalized recommendations.
            """
            
        try:
            primary_dosha = str(dosha_profile.get('primary_dosha', '')).lower() if dosha_profile.get('primary_dosha') else 'unknown'
            secondary_dosha = str(dosha_profile.get('secondary_dosha', '')).lower() if dosha_profile.get('secondary_dosha') else 'none'
            
            dosha_percentages = f"""
            Dosha Distribution:
            - Vata: {dosha_profile.get('vata_percentage', 0):.1f}%
            - Pitta: {dosha_profile.get('pitta_percentage', 0):.1f}%
            - Kapha: {dosha_profile.get('kapha_percentage', 0):.1f}%
            """
            
            return f"""
            Dosha Profile:
            Primary Dosha: {primary_dosha.title()}
            Secondary Dosha: {secondary_dosha.title() if secondary_dosha != 'none' else 'None'}
            {dosha_percentages}
            """
        except Exception as e:
            logger.error(f"Error processing dosha profile: {str(e)}")
            return "Dosha Profile: Error processing dosha information"

    def _get_conditions_context(self, conditions: List[str]) -> str:
        """Safely get conditions context"""
        if not conditions:
            return "No current medical conditions reported."
            
        try:
            if "None" in conditions:
                return "No current medical conditions reported."
                
            context = "Current Medical Conditions and Their Ayurvedic Context:\n"
            for condition in conditions:
                if condition in self.condition_info:
                    context += f"- {condition}: {self.condition_info[condition]}\n"
                else:
                    context += f"- {condition}\n"
            return context
        except Exception as e:
            logger.error(f"Error processing conditions: {str(e)}")
            return "Error processing medical conditions"
    