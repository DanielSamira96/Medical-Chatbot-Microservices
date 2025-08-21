"""
User Information Collection Phase - Page
"""

import streamlit as st
import time
from datetime import datetime
from config.settings import settings
from frontend.utils.utils import call_backend_api, display_message, load_css_for_language
from frontend.user_info.messages import USER_INFO_TEXTS
from frontend.utils.translations import COMMON_TEXTS


def user_info_phase():
    """Handle user information collection phase."""
    # Page title
    st.title(USER_INFO_TEXTS["page_title"][st.session_state.language])
    st.markdown("---")
    
    # Instructions
    st.markdown(USER_INFO_TEXTS["instructions"][st.session_state.language])
    
    # Chat interface for user info collection
    st.markdown(f"### {COMMON_TEXTS['chat_header'][st.session_state.language]}")
    
    # Display conversation history
    for msg in st.session_state.user_info_messages:
        display_message(msg["content"], msg["is_user"], msg["timestamp"])
    
    # User input
    user_input = st.chat_input(USER_INFO_TEXTS["chat_placeholder"][st.session_state.language])
    
    if user_input:
        # Add user message to history
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.user_info_messages.append({
            "content": user_input,
            "is_user": True,
            "timestamp": timestamp
        })
        
        # Display user message
        display_message(user_input, True, timestamp)
        
        # Prepare conversation history for API
        conversation_history = [
            {"role": "user" if msg["is_user"] else "assistant", "content": msg["content"]}
            for msg in st.session_state.user_info_messages[:-1]  # Exclude the just-added message
        ]
        
        # Call backend for user info collection
        with st.spinner(COMMON_TEXTS["processing"][st.session_state.language]):
            response = call_backend_api(settings.ENDPOINTS["user_info"], {
                "message": user_input,
                "conversation_history": conversation_history,
                "ui_language": st.session_state.language  # Send UI preference
            })
        
        if "error" not in response:
            # Add assistant response to history
            assistant_timestamp = datetime.now().strftime("%H:%M")
            st.session_state.user_info_messages.append({
                "content": response["response"],
                "is_user": False,
                "timestamp": assistant_timestamp
            })
            
            # Display assistant message
            display_message(response["response"], False, assistant_timestamp)
            
            # Check if user info is complete
            if response.get("status") == "completed" and response.get("user_info"):
                st.session_state.user_info = response["user_info"]
                st.success(COMMON_TEXTS["info_collected"][st.session_state.language])
                
                # Wait a moment for user to see the success message
                time.sleep(2)
                
                # Clean user info conversation before moving to Q&A
                st.session_state.user_info_messages = []
                
                # Automatically transition to medical Q&A phase
                st.session_state.phase = "medical_qa"
                st.rerun()