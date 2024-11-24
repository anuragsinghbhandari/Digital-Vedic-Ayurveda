from dotenv import load_dotenv
import os
from pathlib import Path

# Get the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env file
load_dotenv(ROOT_DIR / ".env")

# Get Groq API key with error handling
def get_groq_api_key():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    return api_key 