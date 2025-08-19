"""
User Information Collection API endpoints.
"""

from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    UserInfoCollectionRequest, 
    UserInfoCollectionResponse, 
    ChatMessage,
    UserInfo
)
from backend.services import azure_openai_service
from config.prompts.user_info_collection import USER_INFO_COLLECTION_PROMPT
from utils.helpers import detect_language_from_text, error_messages
from config.settings import settings

router = APIRouter()

@router.post("/user-info-collection", response_model=UserInfoCollectionResponse)
async def collect_user_info(request: UserInfoCollectionRequest):
    """
    Handle user information collection phase.
    
    This endpoint manages the conversational collection of user information
    through the LLM without hardcoded form logic.
    """
    
    try:
        # Detect user language for error messages
        user_language = detect_language_from_text(request.message)
        
        # Get response from Azure OpenAI
        ai_response = await azure_openai_service.user_info_collection_chat(
            system_prompt=USER_INFO_COLLECTION_PROMPT,
            conversation_history=request.conversation_history,
            user_message=request.message
        )
        
        if not ai_response:
            raise HTTPException(
                status_code=500, 
                detail=error_messages.get("AZURE_CONNECTION_ERROR", user_language)
            )
        
        # Parse the AI response
        parsed_response = azure_openai_service.parse_user_info_response(ai_response)
        
        # Update conversation history
        updated_history: List[ChatMessage] = request.conversation_history.copy()
        
        # Add user message
        updated_history.append(ChatMessage(
            role="user",
            content=request.message,
            timestamp=datetime.now().isoformat()
        ))
        
        # Add assistant response
        updated_history.append(ChatMessage(
            role="assistant",
            content=parsed_response.get("response", ai_response),
            timestamp=datetime.now().isoformat()
        ))
        
        # Build response
        response = UserInfoCollectionResponse(
            status=parsed_response.get("status", "collecting"),
            response=parsed_response.get("response", ai_response),
            collected_fields=parsed_response.get("collected_fields", []),
            missing_fields=parsed_response.get("missing_fields", []),
            conversation_history=updated_history
        )
        
        # If status is completed, try to parse user info
        if parsed_response.get("status") == "completed" and "user_info" in parsed_response:
            try:
                user_info_data = parsed_response["user_info"]
                response.user_info = UserInfo(**user_info_data)
            except Exception as e:
                print(f"Error parsing user info: {e}")
                # If parsing fails, change status back to error
                response.status = "error"
                response.response = error_messages.get("PROCESSING_ERROR", user_language)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in collect_user_info: {e}")
        # Use settings default for error response
        user_language = settings.DEFAULT_LANGUAGE
        
        raise HTTPException(
            status_code=500,
            detail=error_messages.get("SERVER_ERROR", user_language)
        )