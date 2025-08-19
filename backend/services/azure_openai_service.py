"""
Azure OpenAI Service

Service layer for Azure OpenAI API interactions.
"""

import json
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
from config.settings import settings
from backend.models.schemas import ChatMessage

class AzureOpenAIService:
    """Service for Azure OpenAI API interactions."""
    
    def __init__(self):
        """Initialize Azure OpenAI client."""
        self.client = AzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION
        )
        
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model_deployment: str,
        temperature: float,
        max_tokens: int
    ) -> Optional[str]:
        """
        Get chat completion from Azure OpenAI.
        
        Args:
            messages: List of message dictionaries
            model_deployment: Azure deployment name
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Assistant response content or None if error
        """
        
        try:
            response = self.client.chat.completions.create(
                model=model_deployment,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                print("No response choices returned from Azure OpenAI")
                return None
                
        except Exception as e:
            print(f"Error in Azure OpenAI chat completion: {str(e)}")
            return None
    
    async def user_info_collection_chat(
        self, 
        system_prompt: str, 
        conversation_history: List[ChatMessage], 
        user_message: str
    ) -> Optional[str]:
        """
        Handle user information collection conversation.
        
        Args:
            system_prompt: System prompt for user info collection
            conversation_history: Previous conversation messages
            user_message: Current user message
            
        Returns:
            Assistant response or None if error
        """
        
        # Build messages list
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Use GPT-4o Mini with configured parameters for user info collection
        return await self.chat_completion(
            messages=messages,
            model_deployment=settings.GPT_4O_MINI_DEPLOYMENT_NAME,
            temperature=settings.USER_INFO_TEMPERATURE,
            max_tokens=settings.USER_INFO_MAX_TOKENS
        )
    
    async def medical_qa_chat(
        self, 
        system_prompt: str, 
        conversation_history: List[ChatMessage], 
        user_message: str
    ) -> Optional[str]:
        """
        Handle medical Q&A conversation.
        
        Args:
            system_prompt: System prompt with user context
            conversation_history: Previous conversation messages
            user_message: Current user message
            
        Returns:
            Assistant response or None if error
        """
        
        # Build messages list
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Use GPT-4o with configured parameters for medical Q&A
        return await self.chat_completion(
            messages=messages,
            model_deployment=settings.GPT_4O_DEPLOYMENT_NAME,
            temperature=settings.MEDICAL_QA_TEMPERATURE,
            max_tokens=settings.MEDICAL_QA_MAX_TOKENS
        )
    
    def parse_user_info_response(self, response: str) -> Dict[str, Any]:
        """
        Parse user information collection response.
        
        Args:
            response: Raw response from Azure OpenAI
            
        Returns:
            Parsed response dictionary
        """
        
        try:
            # Try to extract JSON from response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                # No JSON found, treat as regular response
                return {
                    "status": "collecting",
                    "response": response,
                    "collected_fields": [],
                    "missing_fields": []
                }
            
            parsed = json.loads(json_str)
            
            # Validate parsed response structure
            if "status" not in parsed:
                parsed["status"] = "collecting"
            
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {
                "status": "collecting",
                "response": response,
                "collected_fields": [],
                "missing_fields": []
            }
        except Exception as e:
            print(f"Error in parse_user_info_response: {e}")
            return {
                "status": "error",
                "response": "שגיאה בעיבוד התגובה. אנא נסה שוב.",
                "collected_fields": [],
                "missing_fields": []
            }

# Create global service instance
azure_openai_service = AzureOpenAIService()