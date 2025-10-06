import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for GhostLink."""
    
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ghostlink.db")
    
    # External API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Security settings
    API_KEY_EXPIRATION_DAYS: int = int(os.getenv("API_KEY_EXPIRATION_DAYS", "365"))
    
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    @classmethod
    def get_openai_api_key(cls) -> str:
        """Get OpenAI API key with validation."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI integration")
        return cls.OPENAI_API_KEY
    
    @classmethod
    def validate_required_config(cls) -> None:
        """Validate that all required configuration is present."""
        # Add validation logic here if needed
        pass

# Global config instance
config = Config()
