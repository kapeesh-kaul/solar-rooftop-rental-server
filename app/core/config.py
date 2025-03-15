import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

class Settings:
    MONGO_URI: str = os.getenv("MONGODB_URI")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL")

    def __init__(self):
        if not self.MONGO_URI:
            raise ValueError("MONGODB_URI is not set in the environment variables.")
        if not self.OLLAMA_MODEL:
            raise ValueError("OLLAMA_MODEL is not set in the environment variables.")
    
settings = Settings()
