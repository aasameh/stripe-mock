import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BASE_URL = os.getenv("STRIPE_MOCK_URL", "http://localhost:12111")
    API_KEY = os.getenv("STRIPE_API_KEY", "sk_test_123")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    VERIFY_SSL = os.getenv("VERIFY_SSL", "false").lower() == "true"
    
    @classmethod
    def get_base_url(cls) -> str:
        return f"{cls.BASE_URL}"
    
    @classmethod
    def get_auth_header(cls) -> dict:
        return {"Authorization": f"Bearer {cls.API_KEY}"}


settings = Settings()