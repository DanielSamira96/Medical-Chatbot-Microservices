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
from config.prompts.user_info_collection import USER_INFO_COLLECTION_PROMPT, USER_INFO_COLLECTION_PROMPT_EN
from utils.helpers import detect_language_from_text, get_error_message
from utils.logging import log_user_action, log_error
from utils.validators.user_info_validator import validate_user_info
from backend.translations import get_message
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
        # Separate language concerns:
        # 1. Chat content language (auto-detected from message)
        chat_content_language = detect_language_from_text(request.message)
        
        # 2. UI language (user preference for interface messages)  
        ui_language = request.ui_language
        
        # Log user interaction (logs always in English)
        log_user_action(
            phase="user_info_collection",
            action="submit_message", 
            ui_language=ui_language,
            chat_content_language=chat_content_language,
            message_length=len(request.message),
            conversation_length=len(request.conversation_history)
        )
        
        # Select appropriate prompt based on detected language
        system_prompt = USER_INFO_COLLECTION_PROMPT_EN if chat_content_language == "en" else USER_INFO_COLLECTION_PROMPT
        
        # Get response from Azure OpenAI
        ai_response = await azure_openai_service.user_info_collection_chat(
            system_prompt=system_prompt,
            conversation_history=request.conversation_history,
            user_message=request.message
        )
        
        if not ai_response:
            raise HTTPException(
                status_code=500, 
                detail=get_error_message("azure_connection_error", ui_language)
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
        
        # If status is completed, try to parse and validate user info
        if parsed_response.get("status") == "completed" and "user_info" in parsed_response:
            try:
                user_info_data = parsed_response["user_info"]
                
                # Validate user information
                validation_result = validate_user_info(user_info_data, chat_content_language)
                
                if validation_result["is_valid"]:
                    # Use cleaned data from validation
                    response.user_info = UserInfo(**validation_result["cleaned_data"])
                    
                    # Log successful user info collection
                    log_user_action(
                        phase="user_info_collection",
                        action="info_collected_successfully",
                        ui_language=ui_language,
                        chat_content_language=chat_content_language,
                        user_hmo=validation_result["cleaned_data"].get("hmo_name"),
                        user_tier=validation_result["cleaned_data"].get("membership_tier")
                    )
                else:
                    # Validation failed - request corrections
                    response.status = "error"
                    error_details = []
                    for field, error_msg in validation_result["field_errors"].items():
                        error_details.append(f"{field}: {error_msg}")
                    
                    error_list = "\n".join([f"• {detail}" for detail in error_details])
                    response.response = get_message("validation_errors_found", ui_language).format(errors=error_list)
                    
                    log_user_action(
                        phase="user_info_collection",
                        action="validation_failed",
                        ui_language=ui_language,
                        chat_content_language=chat_content_language,
                        validation_errors=list(validation_result["field_errors"].keys())
                    )
                
            except Exception as e:
                log_error("Error parsing user info", exception=e, ui_language=ui_language, chat_language=chat_content_language)
                # If parsing fails, change status back to error
                response.status = "error"
                response.response = get_message("processing_error", ui_language)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        log_error("Unexpected error in user info collection", exception=e)
        
        raise HTTPException(
            status_code=500,
            detail=get_message("server_error", settings.DEFAULT_LANGUAGE)
        )