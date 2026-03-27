import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Settings:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = "voting_system"
    
    TWILIO_SID = os.getenv("TWILIO_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE = os.getenv("TWILIO_PHONE", "+1234567890")
    
    VOTING_DEADLINE = datetime.fromisoformat(
        os.getenv("VOTING_DEADLINE", "2024-12-31T23:59:59").replace('Z', '+00:00')
    )
    
    PROOF_IMAGES_DIR = "proof_images"
    RESULTS_DIR = "results"
    
    @classmethod
    def is_voting_open(cls):
        return datetime.now() < cls.VOTING_DEADLINE