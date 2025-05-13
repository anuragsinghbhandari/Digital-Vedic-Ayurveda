import streamlit as st
from typing import Dict
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Page config
st.set_page_config(
    page_title="Ayurvedic Consultation Platform",
    page_icon="🕉️",
    layout="wide"
)

def dosha_analysis():
    st.title("Dosha Analysis")
    
    with st.form("dosha_questionnaire"):
        st.subheader("Physical Characteristics")
        
        body_frame = st.select_slider(
            "Body Frame",
            options=["Very Slim", "Medium", "Large"],
            help="Select your natural body frame type"
        )
        
        skin_type = st.select_slider(
            "Skin Type",
            options=["Dry/Rough", "Warm/Sensitive", "Thick/Oily"],
            help="Select your natural skin type"
        )
        
        st.subheader("Behavioral Patterns")
        
        sleep_pattern = st.select_slider(
            "Sleep Pattern",
            options=["Light/Irregular", "Moderate", "Deep/Heavy"],
            help="Select your typical sleep pattern"
        )
        
        digestion = st.select_slider(
            "Digestion",
            options=["Irregular", "Strong/Sharp", "Slow/Steady"],
            help="Select your typical digestion pattern"
        )
        
        stress_response = st.select_slider(
            "Response to Stress",
            options=["Anxiety/Worry", "Irritation/Anger", "Withdrawal/Calm"],
            help="Select how you typically respond to stress"
        )
        
        submitted = st.form_submit_button("Analyze My Dosha")
        
        if submitted:
            with st.spinner("Analyzing your Dosha..."):
                try:
                    # Convert responses to API format
                    user_responses = {
                        "body_frame": {
                            "trait_name": "body_frame",
                            **map_response_to_dosha_scores(body_frame)
                        },
                        "skin_type": {
                            "trait_name": "skin_type",
                            **map_response_to_dosha_scores(skin_type)
                        },
                        "sleep_pattern": {
                            "trait_name": "sleep_pattern",
                            **map_response_to_dosha_scores(sleep_pattern)
                        },
                        "digestion": {
                            "trait_name": "digestion",
                            **map_response_to_dosha_scores(digestion)
                        },
                        "stress_response": {
                            "trait_name": "stress_response",
                            **map_response_to_dosha_scores(stress_response)
                        }
                    }
                    
                    # Call API
                    response = requests.post(
                        "https://dva-x7pg.onrender.com/api/v1/analyze-dosha",
                        json=user_responses,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        results = response.json()
                        st.session_state.dosha_profile = results
                        display_dosha_results(results)
                    else:
                        st.error(f"Error: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to the server: {str(e)}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

def map_response_to_dosha_scores(response: str) -> Dict[str, int]:
    mappings = {
        # Body Frame
        "Very Slim": {"vata_score": 3, "pitta_score": 1, "kapha_score": 0},
        "Medium": {"vata_score": 1, "pitta_score": 3, "kapha_score": 1},
        "Large": {"vata_score": 0, "pitta_score": 1, "kapha_score": 3},
        # Skin Type
        "Dry/Rough": {"vata_score": 3, "pitta_score": 1, "kapha_score": 0},
        "Warm/Sensitive": {"vata_score": 1, "pitta_score": 3, "kapha_score": 0},
        "Thick/Oily": {"vata_score": 0, "pitta_score": 1, "kapha_score": 3},
        # Sleep Pattern
        "Light/Irregular": {"vata_score": 3, "pitta_score": 1, "kapha_score": 0},
        "Moderate": {"vata_score": 1, "pitta_score": 3, "kapha_score": 1},
        "Deep/Heavy": {"vata_score": 0, "pitta_score": 1, "kapha_score": 3},
        # Digestion
        "Irregular": {"vata_score": 3, "pitta_score": 0, "kapha_score": 1},
        "Strong/Sharp": {"vata_score": 1, "pitta_score": 3, "kapha_score": 0},
        "Slow/Steady": {"vata_score": 0, "pitta_score": 1, "kapha_score": 3},
        # Stress Response
        "Anxiety/Worry": {"vata_score": 3, "pitta_score": 1, "kapha_score": 0},
        "Irritation/Anger": {"vata_score": 1, "pitta_score": 3, "kapha_score": 0},
        "Withdrawal/Calm": {"vata_score": 0, "pitta_score": 1, "kapha_score": 3},
    }
    return mappings.get(response, {"vata_score": 1, "pitta_score": 1, "kapha_score": 1})

def display_dosha_results(results):
    st.success("✨ Dosha Analysis Complete!")
    
    # Create three columns for the doshas with percentages
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Vata",
            f"{results.get('vata_percentage', 0):.1f}%",
            help="Vata represents movement, air, and space elements"
        )
    with col2:
        st.metric(
            "Pitta",
            f"{results.get('pitta_percentage', 0):.1f}%",
            help="Pitta represents transformation, fire, and water elements"
        )
    with col3:
        st.metric(
            "Kapha",
            f"{results.get('kapha_percentage', 0):.1f}%",
            help="Kapha represents structure, earth, and water elements"
        )
    
    # Display primary and secondary doshas
    st.markdown("### 🌟 Your Dosha Profile")
    primary_dosha = results.get('primary_dosha', '')
    
    # Display dosha information in a container
    with st.container():
        st.markdown(f"**Primary Dosha:** {primary_dosha.title()}")
        
        secondary_dosha = results.get('secondary_dosha')
        if secondary_dosha:
            st.markdown(f"**Secondary Dosha:** {secondary_dosha.title()}")
    
    # Add brief dosha description
    st.markdown("### 📝 Understanding Your Dosha")
    dosha_descriptions = {
        'vata': """
            Your Vata dominance indicates a creative and energetic nature. 
            Vata types are typically:
            - Quick thinking and adaptable
            - Creative and enthusiastic
            - Light and agile in movement
            """,
        'pitta': """
            Your Pitta dominance indicates a focused and determined nature. 
            Pitta types are typically:
            - Intelligent and sharp-minded
            - Goal-oriented and organized
            - Warm and dynamic in personality
            """,
        'kapha': """
            Your Kapha dominance indicates a stable and nurturing nature. 
            Kapha types are typically:
            - Patient and thoughtful
            - Calm and steady
            - Strong and enduring
            """
    }
    
    st.markdown(dosha_descriptions.get(primary_dosha.lower(), ""))
    
    # Add next steps guidance
    st.markdown("### 👉 Next Steps")
    st.info("""
        To receive personalized health recommendations based on your dosha profile:
        1. Visit the 'Personal Consultation' section
        2. Fill in your health details
        3. Get customized Ayurvedic recommendations
    """)

def personal_consultation():
    st.title("Personalized Ayurvedic Consultation")
    
    # Store form results in session state
    if 'consultation_results' not in st.session_state:
        st.session_state.consultation_results = None
    
    with st.form("consultation_form"):
        # Basic Information
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col2:
            weight = st.number_input("Weight (kg)", min_value=20, max_value=200)
            height = st.number_input("Height (cm)", min_value=100, max_value=250)

        # Medical History
        st.subheader("Medical History")
        current_conditions = st.multiselect(
            "Current Medical Conditions",
            ["Diabetes", "Hypertension", "Arthritis", "Digestive Issues", 
             "Respiratory Problems", "Skin Conditions", "Sleep Disorders", 
             "Stress/Anxiety", "None"]
        )
        
        medications = st.text_area(
            "Current Medications (if any)",
            placeholder="List your current medications..."
        )
        
        # Lifestyle
        st.subheader("Lifestyle Information")
        col3, col4 = st.columns(2)
        with col3:
            diet_type = st.selectbox(
                "Diet Type",
                ["Vegetarian", "Vegan", "Non-Vegetarian", "Other"]
            )
            physical_activity = st.select_slider(
                "Physical Activity Level",
                options=["Sedentary", "Light", "Moderate", "Active", "Very Active"]
            )
        with col4:
            sleep_hours = st.slider("Average Sleep Hours", 4, 12, 7)
            stress_level = st.select_slider(
                "Stress Level",
                options=["Low", "Medium", "High"]
            )

        # Primary Concerns
        st.subheader("Health Concerns")
        primary_concerns = st.text_area(
            "Describe your main health concerns",
            placeholder="What are your primary health concerns or goals?..."
        )
        
        # Previous Treatments
        previous_treatments = st.text_area(
            "Previous Treatments (if any)",
            placeholder="Describe any previous treatments you've tried..."
        )

        submitted = st.form_submit_button("Get Personalized Recommendations")
        
        if submitted:
            if not primary_concerns:
                st.error("Please describe your health concerns to receive personalized recommendations.")
                return
                
            with st.spinner("Analyzing your profile and generating personalized recommendations..."):
                try:
                    # Prepare consultation data
                    consultation_data = {
                        "personal_info": {
                            "age": age,
                            "gender": gender,
                            "weight": weight,
                            "height": height,
                            "bmi": round(weight / ((height/100) ** 2), 2)
                        },
                        "medical_history": {
                            "conditions": current_conditions,
                            "medications": medications
                        },
                        "lifestyle": {
                            "diet_type": diet_type,
                            "physical_activity": physical_activity,
                            "sleep_hours": sleep_hours,
                            "stress_level": stress_level
                        },
                        "concerns": {
                            "primary_concerns": primary_concerns,
                            "previous_treatments": previous_treatments
                        }
                    }
                    
                    # Get dosha profile from session state if available
                    if 'dosha_profile' in st.session_state:
                        consultation_data["dosha_profile"] = st.session_state.dosha_profile
                    
                    # Call API for personalized recommendations
                    response = requests.post(
                        "https://dva-x7pg.onrender.com/api/v1/personal-consultation",
                        json=consultation_data,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        st.session_state.consultation_results = response.json()
                    else:
                        st.error(f"Error: {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to the server: {str(e)}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    # Display results outside the form
    if st.session_state.consultation_results:
        display_consultation_results(st.session_state.consultation_results)

def display_consultation_results(results):
    st.success("✨ Your Personalized Ayurvedic Consultation Analysis")
    
    # Display Condition Overview and Dosha Impact
    if 'overview' in results:
        st.markdown("### 🔍 Health Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Condition Analysis
            if results['overview']['condition_analysis']:
                st.markdown("#### Current Health Status")
                st.markdown("---")
                for analysis in results['overview']['condition_analysis']:
                    st.markdown(f"🔸 {analysis}")
        
        with col2:
            # Dosha Impact
            if results['overview']['dosha_impact']:
                st.markdown("#### Dosha Analysis")
                st.markdown("---")
                for impact in results['overview']['dosha_impact']:
                    st.markdown(f"🔹 {impact}")
    
    # Display all recommendations in organized sections
    if 'recommendations' in results:
        st.markdown("### 📋 Personalized Recommendations")
        
        # Create tabs for different categories of recommendations
        tabs = st.tabs([
            "🍽️ Diet",
            "🌅 Lifestyle",
            "🧘‍♀️ Exercise",
            "🌿 Herbs",
            "💆‍♂️ Therapies"
        ])
        
        # Dietary Recommendations Tab
        with tabs[0]:
            st.markdown("#### Dietary Guidelines")
            if results['recommendations']['dietary']:
                with st.container():
                    st.markdown("---")
                    for rec in results['recommendations']['dietary']:
                        st.markdown(f"• {rec}")
        
        # Lifestyle Recommendations Tab
        with tabs[1]:
            st.markdown("#### Lifestyle Modifications")
            if results['recommendations']['lifestyle']:
                with st.container():
                    st.markdown("---")
                    for rec in results['recommendations']['lifestyle']:
                        st.markdown(f"• {rec}")
        
        # Exercise Recommendations Tab
        with tabs[2]:
            st.markdown("#### Exercise & Movement")
            if results['recommendations']['exercise']:
                with st.container():
                    st.markdown("---")
                    for rec in results['recommendations']['exercise']:
                        st.markdown(f"• {rec}")
        
        # Herbal Recommendations Tab
        with tabs[3]:
            st.markdown("#### Herbal Remedies")
            if results['recommendations']['herbal']:
                with st.container():
                    st.markdown("---")
                    for rec in results['recommendations']['herbal']:
                        st.markdown(f"• {rec}")
        
        # Therapeutic Recommendations Tab
        with tabs[4]:
            st.markdown("#### Therapeutic Treatments")
            if results['recommendations']['therapeutic']:
                with st.container():
                    st.markdown("---")
                    for rec in results['recommendations']['therapeutic']:
                        st.markdown(f"• {rec}")
    
    # Display Warnings and Special Considerations
    if 'warnings' in results and results['warnings']:
        st.markdown("### ⚠️ Important Considerations")
        for warning in results['warnings']:
            st.warning(warning)
    
    # Add summary metrics
    st.markdown("### 📊 Recommendation Summary")
    metric_cols = st.columns(5)
    
    with metric_cols[0]:
        st.metric("Dietary", f"{len(results['recommendations']['dietary'])} tips")
    with metric_cols[1]:
        st.metric("Lifestyle", f"{len(results['recommendations']['lifestyle'])} tips")
    with metric_cols[2]:
        st.metric("Exercise", f"{len(results['recommendations']['exercise'])} tips")
    with metric_cols[3]:
        st.metric("Herbal", f"{len(results['recommendations']['herbal'])} tips")
    with metric_cols[4]:
        st.metric("Therapeutic", f"{len(results['recommendations']['therapeutic'])} tips")
    
    # Add a disclaimer in a highlighted box
    st.markdown("---")
    st.info("""
        ⚕️ **Medical Disclaimer**: These recommendations are based on Ayurvedic principles 
        and your provided information. They are not a substitute for professional medical 
        advice. Always consult with qualified healthcare practitioners before starting any 
        new treatment regimen.
    """)
    
    # Add download section
    st.markdown("### 💾 Save Your Recommendations")
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.markdown("""
            Download your personalized recommendations to:
            - Keep track of your wellness journey
            - Share with your healthcare providers
            - Reference the suggestions offline
        """)
    with col2:
        recommendations_text = _format_recommendations_for_download(results)
        st.download_button(
            label="Download Report",
            data=recommendations_text,
            file_name="ayurvedic_recommendations.txt",
            mime="text/plain",
            help="Download your personalized recommendations as a text file",
            use_container_width=True
        )

def _format_recommendations_for_download(results: Dict) -> str:
    """Format recommendations for text file download"""
    text = "AYURVEDIC CONSULTATION RECOMMENDATIONS\n\n"
    
    # Add Overview
    if 'overview' in results:
        text += "HEALTH ANALYSIS\n"
        text += "================\n\n"
        
        if results['overview']['condition_analysis']:
            text += "Condition Analysis:\n"
            text += "-----------------\n"
            for analysis in results['overview']['condition_analysis']:
                text += f"• {analysis}\n"
            text += "\n"
        
        if results['overview']['dosha_impact']:
            text += "Dosha Impact:\n"
            text += "-------------\n"
            for impact in results['overview']['dosha_impact']:
                text += f"• {impact}\n"
            text += "\n"
    
    # Add Recommendations
    if 'recommendations' in results:
        text += "PERSONALIZED RECOMMENDATIONS\n"
        text += "===========================\n\n"
        
        sections = {
            'dietary': 'Dietary Guidelines',
            'lifestyle': 'Lifestyle Modifications',
            'exercise': 'Exercise & Movement',
            'herbal': 'Herbal Remedies',
            'therapeutic': 'Therapeutic Treatments'
        }
        
        for key, title in sections.items():
            if results['recommendations'][key]:
                text += f"{title}:\n"
                text += "-" * (len(title) + 1) + "\n"
                for rec in results['recommendations'][key]:
                    text += f"• {rec}\n"
                text += "\n"
    
    # Add Warnings
    if 'warnings' in results and results['warnings']:
        text += "IMPORTANT CONSIDERATIONS\n"
        text += "========================\n\n"
        for warning in results['warnings']:
            text += f"! {warning}\n"
        text += "\n"
    
    # Add Disclaimer
    text += "\nDISCLAIMER\n"
    text += "==========\n"
    text += "These recommendations are based on Ayurvedic principles and your provided information. "
    text += "Always consult with qualified healthcare practitioners before starting any new treatment regimen.\n"
    
    return text

def home_page():
    st.title("Welcome to Ayurvedic Consultation Platform")
    
    st.markdown("""
    ### Discover Your Unique Constitution
    
    Ayurveda, the ancient science of life, teaches us that each person has a unique 
    constitution or Dosha. Understanding your Dosha can help you make better choices 
    for your health and well-being.
    
    ### How it works:
    1. Complete the Dosha analysis questionnaire
    2. Receive your personalized Dosha profile
    3. Get tailored recommendations for:
        - Diet
        - Lifestyle
        - Exercise
        - Beneficial herbs
    
    Get started by selecting "Dosha Analysis" from the sidebar!
    """)

def main():
    with st.sidebar:
        st.title("Navigation")
        choice = st.radio("Go to", ["Home", "Dosha Analysis", "Personal Consultation"])
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "This platform provides personalized Ayurvedic "
            "consultation based on your unique constitution (Dosha)."
        )
    
    if choice == "Home":
        home_page()
    elif choice == "Dosha Analysis":
        dosha_analysis()
    else:
        personal_consultation()

if __name__ == "__main__":
    main() 
