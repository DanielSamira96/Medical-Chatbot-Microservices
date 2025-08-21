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
    
    # Azure OpenAI Configuration - GPT-4o (for Medical Q&A)
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    
    # Azure OpenAI Configuration - GPT-4o-mini (for User Info Collection)
    AZURE_OPENAI_MINI_ENDPOINT: str = os.getenv("AZURE_OPENAI_MINI_ENDPOINT")
    AZURE_OPENAI_MINI_API_KEY: str = os.getenv("AZURE_OPENAI_MINI_API_KEY")
    AZURE_OPENAI_MINI_API_VERSION: str = os.getenv("AZURE_OPENAI_MINI_API_VERSION", "2024-02-01")
    
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
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "8501"))
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
    
    # Data Configuration
    DATA_FOLDER: str = os.getenv("DATA_FOLDER", "user_specific_data")
    
    # Language Configuration
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "he")
    SUPPORTED_LANGUAGES: list = os.getenv("SUPPORTED_LANGUAGES", "he,en").split(",")
    
    # Logging Configuration
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/chatbot.log")
    LOG_MAX_SIZE_MB: int = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
    # Derived Configuration Properties
    @property
    def BACKEND_URL(self) -> str:
        """Backend API base URL."""
        return f"http://{self.APP_HOST}:{self.APP_PORT}"
    
    @property 
    def ENDPOINTS(self) -> dict:
        """API endpoint paths."""
        return {
            "health": f"/api/{self.API_VERSION}/health",
            "user_info": f"/api/{self.API_VERSION}/user-info-collection", 
            "medical_qa": f"/api/{self.API_VERSION}/medical-qa"
        }
    
    def validate_azure_config(self) -> dict:
        """Validate that required Azure OpenAI configuration is properly set."""
        required_fields = {
            'AZURE_OPENAI_ENDPOINT': self.AZURE_OPENAI_ENDPOINT,
            'AZURE_OPENAI_API_KEY': self.AZURE_OPENAI_API_KEY,
            'AZURE_OPENAI_MINI_ENDPOINT': self.AZURE_OPENAI_MINI_ENDPOINT,
            'AZURE_OPENAI_MINI_API_KEY': self.AZURE_OPENAI_MINI_API_KEY,
            'GPT_4O_DEPLOYMENT_NAME': self.GPT_4O_DEPLOYMENT_NAME,
            'GPT_4O_MINI_DEPLOYMENT_NAME': self.GPT_4O_MINI_DEPLOYMENT_NAME
        }
        
        invalid_fields = []
        
        for name, value in required_fields.items():
            if value is None or not value.strip():
                invalid_fields.append(name)
        
        # Check for placeholder values
        if self.AZURE_OPENAI_ENDPOINT == 'https://your-gpt4o-resource-name.openai.azure.com/':
            invalid_fields.append('AZURE_OPENAI_ENDPOINT')
        if self.AZURE_OPENAI_API_KEY == 'your-gpt4o-api-key-here':
            invalid_fields.append('AZURE_OPENAI_API_KEY')
        if self.AZURE_OPENAI_MINI_ENDPOINT == 'https://your-gpt4o-mini-resource-name.openai.azure.com/':
            invalid_fields.append('AZURE_OPENAI_MINI_ENDPOINT')
        if self.AZURE_OPENAI_MINI_API_KEY == 'your-gpt4o-mini-api-key-here':
            invalid_fields.append('AZURE_OPENAI_MINI_API_KEY')
        
        if invalid_fields:
            return {
                'valid': False,
                'invalid_fields': invalid_fields,
                'message': f"Azure OpenAI configuration incomplete: {', '.join(invalid_fields)}"
            }
        
        return {
            'valid': True,
            'invalid_fields': [],
            'message': "Azure OpenAI dual-endpoint configuration ready"
        }

# Create global settings instance
settings = Settings()