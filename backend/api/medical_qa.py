"""
Medical Q&A API endpoints.
"""

from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    MedicalQARequest, 
    MedicalQAResponse, 
    ChatMessage
)
from backend.services import azure_openai_service
from config.prompts.medical_qa import build_medical_qa_prompt
from utils.helpers import detect_language_from_text, error_messages, load_user_medical_context
from config.settings import settings

router = APIRouter()

@router.post("/medical-qa", response_model=MedicalQAResponse)
async def medical_question_answer(request: MedicalQARequest):
    """
    Handle medical Q&A phase.
    
    This endpoint provides medical service information based on user-specific
    context and answers questions using the knowledge base.
    """
    
    try:
        # Detect user language for error messages
        user_language = detect_language_from_text(request.message)
        
        # Load user-specific medical context
        medical_context = load_user_medical_context(
            hmo_name=request.user_info.hmo_name,
            membership_tier=request.user_info.membership_tier,
            data_folder=settings.DATA_FOLDER
        )
        
        if not medical_context:
            raise HTTPException(
                status_code=400,
                detail=error_messages.get("CONTEXT_LOAD_ERROR", user_language)
            )
        
        # Build the medical Q&A prompt with user context
        system_prompt = build_medical_qa_prompt(
            user_info=request.user_info.dict(),
            medical_context=medical_context,
            language=user_language
        )
        
        # Get response from Azure OpenAI
        ai_response = await azure_openai_service.medical_qa_chat(
            system_prompt=system_prompt,
            conversation_history=request.conversation_history,
            user_message=request.message
        )
        
        if not ai_response:
            raise HTTPException(
                status_code=500, 
                detail=error_messages.get("AZURE_CONNECTION_ERROR", user_language)
            )
        
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
            content=ai_response,
            timestamp=datetime.now().isoformat()
        ))
        
        # Build response
        response = MedicalQAResponse(
            status="success",
            response=ai_response,
            conversation_history=updated_history
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in medical_question_answer: {e}")
        # Use settings default for error response
        user_language = settings.DEFAULT_LANGUAGE
        
        raise HTTPException(
            status_code=500,
            detail=error_messages.get("SERVER_ERROR", user_language)
        )