import os
from datetime import timedelta
from dotenv import load_dotenv

# to load variables from .env
load_dotenv()

LINKEDIN_CONFIG = {
    "email": os.getenv("LINKEDIN_EMAIL"),
    "password": os.getenv("LINKEDIN_PASSWORD"),
    "max_requests_per_day": 50,
    "delay_between_requests": (3, 7)
}

TARGET_CRITERIA = {
    "companies": ["Wipro", "Infosys", "TCS", "Cognizant", "HCL"],
    "experience_range": (0, 3),
    "activity_timeframe": timedelta(days=180) #kept a 6 month timeframe
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
