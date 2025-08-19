"""
Pydantic models for API request/response schemas.
"""

from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field, validator

class UserInfo(BaseModel):
    """User information schema."""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    id_number: str = Field(..., min_length=9, max_length=9)
    gender: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=120)
    hmo_name: str = Field(..., regex="^(מכבי|מאוחדת|כללית)$")
    hmo_card_number: str = Field(..., min_length=9, max_length=9)
    membership_tier: str = Field(..., regex="^(זהב|כסף|ארד)$")
    
    @validator('id_number', 'hmo_card_number')
    def validate_numeric_string(cls, v):
        """Validate that string contains only digits."""
        if not v.isdigit():
            raise ValueError('Must contain only digits')
        return v

class ChatMessage(BaseModel):
    """Individual chat message schema."""
    role: str = Field(..., regex="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)
    timestamp: Optional[str] = None

class UserInfoCollectionRequest(BaseModel):
    """Request schema for user information collection phase."""
    message: str = Field(..., min_length=1)
    conversation_history: List[ChatMessage] = Field(default_factory=list)
    collected_info: Optional[Dict[str, Any]] = Field(default_factory=dict)

class UserInfoCollectionResponse(BaseModel):
    """Response schema for user information collection phase."""
    status: str = Field(..., regex="^(collecting|completed|error)$")
    response: str
    collected_fields: Optional[List[str]] = None
    missing_fields: Optional[List[str]] = None
    user_info: Optional[UserInfo] = None
    conversation_history: List[ChatMessage]

class MedicalQARequest(BaseModel):
    """Request schema for medical Q&A phase."""
    message: str = Field(..., min_length=1)
    user_info: UserInfo
    conversation_history: List[ChatMessage] = Field(default_factory=list)

class MedicalQAResponse(BaseModel):
    """Response schema for medical Q&A phase."""
    status: str = Field(..., regex="^(success|error)$")
    response: str
    conversation_history: List[ChatMessage]

class HealthCheckResponse(BaseModel):
    """Health check response schema."""
    status: str = "healthy"
    timestamp: str
    azure_openai_configured: bool
    available_contexts: List[str]