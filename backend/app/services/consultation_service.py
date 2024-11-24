from typing import Dict, List
import logging
from ..config import get_groq_api_key
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsultationService:
    def __init__(self):
        self.groq_api_key = get_groq_api_key()
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Ayurvedic condition descriptions
        self.condition_info = {
            "Diabetes": "In Ayurveda, diabetes (Prameha) is primarily seen as a Kapha disorder with possible Pitta involvement.",
            "Hypertension": "Hypertension in Ayurveda (Rakta Gata Vata) is often related to Vata and Pitta imbalances.",
            "Arthritis": "Arthritis (Sandhivata) is typically viewed as a Vata disorder affecting the joints.",
            "Digestive Issues": "Digestive problems can involve all three doshas, with specific symptoms indicating the primary dosha imbalance.",
            "Respiratory Problems": "Respiratory issues often involve Kapha dosha, with possible Vata and Pitta complications.",
            "Skin Conditions": "Skin disorders (Kushtha) can involve all three doshas, but often have a strong Pitta component.",
            "Sleep Disorders": "Sleep issues are often related to Vata imbalance, though other doshas may be involved.",
            "Stress/Anxiety": "Anxiety and stress primarily affect Vata dosha, leading to mental and physical imbalances."
        }
        
    def get_personalized_recommendations(self, consultation_data: Dict) -> Dict:
        try:
            # Ensure consultation_data is not None
            if not consultation_data:
                raise ValueError("Consultation data is missing")

            # Safely get medical history
            medical_history = consultation_data.get('medical_history', {})
            if not isinstance(medical_history, dict):
                medical_history = {}

            # Create prompt with safe data access
            prompt = self._create_consultation_prompt(consultation_data)
            
            # Get recommendations from LLM
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "llama-3.1-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"API call failed: {response.text}")
                return self._get_default_recommendations(consultation_data)
            
            # Parse and structure the response
            content = response.json()['choices'][0]['message']['content']
            return self._parse_consultation_response(content, consultation_data)
            
        except Exception as e:
            logger.error(f"Error in consultation service: {str(e)}")
            return self._get_default_recommendations(consultation_data)
    
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
            
            return f"""
            As an experienced Ayurvedic practitioner, provide detailed and practical recommendations for a patient with the following profile:

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

            CONDITION OVERVIEW:
            - Explain how their current conditions relate to their dosha type
            - Describe specific imbalances that need addressing
            - Identify key areas for improvement

            DOSHA IMPACT:
            - Explain how their current dosha state affects their health
            - Describe specific dosha-related symptoms to watch for
            - Suggest dosha-balancing priorities

            DIETARY RECOMMENDATIONS:
            For each recommendation, provide:
            - Specific foods to include or avoid
            - Best times and ways to consume
            - Quantity guidelines when applicable
            - Special preparations or combinations

            LIFESTYLE MODIFICATIONS:
            For each recommendation, provide:
            - Specific daily routine adjustments
            - Best times for activities
            - Duration and frequency
            - Practical implementation tips

            EXERCISE RECOMMENDATIONS:
            For each recommendation, provide:
            - Specific types of exercise
            - Intensity levels
            - Duration and frequency
            - Best times to practice
            - Precautions or modifications

            HERBAL REMEDIES:
            For each recommendation, provide:
            - Specific herb or formulation
            - Dosage and timing
            - Method of preparation
            - Duration of use
            - Specific benefits

            THERAPEUTIC TREATMENTS:
            For each recommendation, provide:
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

            Please ensure each recommendation is:
            1. Practical and actionable
            2. Specific with quantities and timings
            3. Clear about duration and frequency
            4. Includes implementation guidance
            5. Mentions expected benefits
            6. Notes any precautions

            Format each recommendation as a complete, detailed statement rather than just a heading or brief phrase.
            """
            
        except Exception as e:
            logger.error(f"Error creating consultation prompt: {str(e)}")
            return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """Provide a default prompt if there's an error"""
        return """
        Please provide general Ayurvedic health recommendations covering:
        1. Basic dietary guidelines
        2. General lifestyle recommendations
        3. Common herbal supplements
        4. Basic exercise suggestions
        5. General health precautions
        """
    
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
    
    def _parse_consultation_response(self, response: str, consultation_data: Dict) -> Dict:
        """Parse the LLM response into structured recommendations"""
        sections = {
            "overview": {
                "condition_analysis": [],
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
        buffer = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            lower_line = line.lower()
            
            # Check for section headers
            if 'condition overview' in lower_line:
                current_section = 'overview'
                current_subsection = 'condition_analysis'
                continue
            elif 'dosha impact' in lower_line:
                current_section = 'overview'
                current_subsection = 'dosha_impact'
                continue
            elif 'dietary' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'dietary'
                continue
            elif 'lifestyle' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'lifestyle'
                continue
            elif 'exercise' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'exercise'
                continue
            elif 'herbal' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'herbal'
                continue
            elif 'therapeutic' in lower_line:
                current_section = 'recommendations'
                current_subsection = 'therapeutic'
                continue
            elif any(word in lower_line for word in ['warning', 'precaution', 'caution']):
                current_section = 'warnings'
                current_subsection = None
                continue
            
            # Process content
            if current_section and line.startswith(('-', '•', '*')) or line[0].isdigit():
                cleaned_line = line.lstrip('•-*123456789. ')
                if cleaned_line:
                    # Ensure the line is a complete recommendation
                    if len(cleaned_line) > 10:  # Arbitrary minimum length for a complete recommendation
                        if current_section == 'recommendations':
                            sections[current_section][current_subsection].append(cleaned_line)
                        elif current_section == 'overview':
                            sections[current_section][current_subsection].append(cleaned_line)
                        else:
                            sections[current_section].append(cleaned_line)
        
        # Filter out any section headers that got captured as recommendations
        for section in sections['recommendations']:
            sections['recommendations'][section] = [
                rec for rec in sections['recommendations'][section]
                if len(rec.split()) > 3  # Filter out very short lines
                and not any(header in rec.lower() for header in ['recommendation', 'guidelines', 'suggested'])
            ]
        
        return sections
    
    def _get_default_recommendations(self, consultation_data: Dict) -> Dict:
        conditions = consultation_data.get('medical_history', {}).get('conditions', [])
        conditions_info = self._get_conditions_context(conditions)
        
        return {
            "overview": {
                "condition_analysis": [conditions_info],
                "dosha_impact": ["Please consult an Ayurvedic practitioner for detailed dosha analysis"]
            },
            "recommendations": {
                "dietary": ["Please consult an Ayurvedic practitioner for personalized dietary recommendations"],
                "lifestyle": ["Please consult an Ayurvedic practitioner for lifestyle recommendations"],
                "herbal": ["Please consult an Ayurvedic practitioner for herbal recommendations"],
                "therapeutic": ["Please consult an Ayurvedic practitioner for therapeutic recommendations"],
                "exercise": ["Please consult an Ayurvedic practitioner for exercise recommendations"]
            },
            "warnings": ["Please consult a healthcare provider before starting any new treatment regimen"],
            "lifestyle_modifications": [],
            "recommended_therapies": []
        } 