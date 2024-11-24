import os
from dotenv import load_dotenv
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_groq_api_key():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        logger.error("GROQ_API_KEY not found in environment variables")
        return False
        
    if not api_key.startswith("gsk_"):
        logger.error("Invalid API key format. GROQ API keys should start with 'gsk_'")
        return False
    
    # Test API key with a simple request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={
                "model": "llama-3.1-70b-versatile",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 1
            }
        )
        
        if response.status_code == 200:
            logger.info("API key is valid!")
            return True
        else:
            logger.error(f"API key validation failed: {response.json()}")
            return False
            
    except Exception as e:
        logger.error(f"Error verifying API key: {str(e)}")
        return False

if __name__ == "__main__":
    verify_groq_api_key() 