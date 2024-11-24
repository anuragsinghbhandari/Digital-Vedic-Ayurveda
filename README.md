# Ayurvedic Consultation Platform 🕉️

A modern digital platform that combines traditional Ayurvedic wisdom with modern technology to provide personalized health consultations and recommendations.

## Features

### 1. Dosha Analysis
- Interactive questionnaire to determine your unique constitution (Dosha)
- Analysis of Vata, Pitta, and Kapha percentages
- Detailed explanation of your primary and secondary doshas
- Visual representation of your dosha profile

### 2. Personal Consultation
- Comprehensive health assessment
- Integration of dosha profile with current health conditions
- Collection of:
  - Personal information
  - Medical history
  - Lifestyle factors
  - Current health concerns
  - Previous treatments

### 3. Personalized Recommendations
- Dosha-specific guidance
- Dietary recommendations
- Lifestyle modifications
- Exercise suggestions
- Herbal remedies
- Therapeutic treatments
- Important health considerations

## Technology Stack

### Backend
- FastAPI: Modern, fast web framework for building APIs
- Pydantic: Data validation using Python type annotations
- Groq API: LLM integration for personalized recommendations

### Frontend
- Streamlit: Interactive web interface
- Python: Core programming language
- Requests: HTTP library for API communication

## Setup Instructions

1. Clone the repository:
   git clone https://github.com/anuragsinghbhandari/Digital-Vedic-Ayurveda.git
   cd Digital-Vedic-Ayurveda

2. Create and activate virtual environment:
   For Windows:
   - python -m venv venv
   - venv\Scripts\activate

   For Linux/Mac:
   - python -m venv venv
   - source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set up Groq API:
   - Sign up at https://console.groq.com
   - Get your API key
   - Create .env file in project root
   - Add your API key: GROQ_API_KEY=your_groq_api_key_here

5. Verify API setup (optional):
   python scripts/verify_api_key.py

6. Start the backend server:
   cd backend
   uvicorn app:app --reload --host 0.0.0.0 --port 8000

7. Start the frontend (in a new terminal):
   cd frontend
   streamlit run app.py

8. Access the application:
   - Frontend: http://localhost:8501
   - API Documentation: http://localhost:8000/docs

## System Requirements

- Python 3.10 or higher
- pip (Python package installer)
- Git
- Internet connection for API access

## Dependencies

Main Python packages:
- fastapi==0.68.1
- uvicorn==0.15.0
- pydantic==2.5.3
- streamlit==1.22.0
- langchain-groq==0.0.3
- python-dotenv==0.19.0
- requests==2.26.0

## Troubleshooting

1. Module Import Errors:
   - Ensure virtual environment is activated
   - Verify all requirements are installed
   - Check you're in the correct directory

2. API Connection Issues:
   - Verify Groq API key in .env file
   - Check internet connection
   - Ensure backend server is running

3. Frontend-Backend Connection:
   - Verify backend is running on port 8000
   - Check for any firewall restrictions
   - Ensure correct URL configuration