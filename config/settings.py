"""
Application Settings

Configuration management using environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    
    # Model Configuration
    GPT_4O_DEPLOYMENT_NAME: str = os.getenv("GPT_4O_DEPLOYMENT_NAME", "gpt-4o")
    GPT_4O_MINI_DEPLOYMENT_NAME: str = os.getenv("GPT_4O_MINI_DEPLOYMENT_NAME", "gpt-4o-mini")
    
    # Azure OpenAI Parameters
    USER_INFO_MAX_TOKENS: int = int(os.getenv("USER_INFO_MAX_TOKENS", "1500"))
    USER_INFO_TEMPERATURE: float = float(os.getenv("USER_INFO_TEMPERATURE", "0.3"))
    MEDICAL_QA_MAX_TOKENS: int = int(os.getenv("MEDICAL_QA_MAX_TOKENS", "8000"))
    MEDICAL_QA_TEMPERATURE: float = float(os.getenv("MEDICAL_QA_TEMPERATURE", "0.1"))
    
    # Application Configuration
    APP_HOST: str = os.getenv("APP_HOST", "localhost")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Data Configuration
    DATA_FOLDER: str = os.getenv("DATA_FOLDER", "user_specific_data")
    
    # Language Configuration
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "hebrew")
    SUPPORTED_LANGUAGES: list = os.getenv("SUPPORTED_LANGUAGES", "hebrew,english").split(",")
    
    # Logging Configuration
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/chatbot.log")
    LOG_MAX_SIZE_MB: int = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
    def validate_azure_config(self) -> bool:
        """Validate that required Azure OpenAI configuration is present."""
        required_fields = [
            self.AZURE_OPENAI_ENDPOINT,
            self.AZURE_OPENAI_API_KEY,
            self.GPT_4O_DEPLOYMENT_NAME,
            self.GPT_4O_MINI_DEPLOYMENT_NAME
        ]
        return all(field.strip() for field in required_fields)

# Create global settings instance
settings = Settings()