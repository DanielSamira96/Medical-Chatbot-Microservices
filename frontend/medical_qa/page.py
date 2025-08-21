"""
Medical Q&A Phase - Page
"""

import streamlit as st
from datetime import datetime
from config.settings import settings
from frontend.utils.utils import call_backend_api, display_message
from frontend.medical_qa.messages import MEDICAL_QA_TEXTS
from frontend.utils.translations import COMMON_TEXTS


def medical_qa_phase():
    """Handle medical Q&A phase."""
    # Page title
    st.title(MEDICAL_QA_TEXTS["page_title"][st.session_state.language])
    st.markdown("---")
    
    # User info display in sidebar
    with st.sidebar:
        st.markdown(f"### {COMMON_TEXTS['user_info_header'][st.session_state.language]}")
        if st.session_state.user_info:
            user_info = st.session_state.user_info
            st.write(f"**{COMMON_TEXTS['name_label'][st.session_state.language]}** {user_info.get('first_name', '')} {user_info.get('last_name', '')}")
            st.write(f"**{COMMON_TEXTS['hmo_label'][st.session_state.language]}** {user_info.get('hmo_name', '')}")
            st.write(f"**{COMMON_TEXTS['tier_label'][st.session_state.language]}** {user_info.get('membership_tier', '')}")
            st.write(f"**{COMMON_TEXTS['age_label'][st.session_state.language]}** {user_info.get('age', '')}")
        
        if st.button(COMMON_TEXTS["start_over"][st.session_state.language]):
            # Reset session state
            st.session_state.phase = "user_info"
            st.session_state.user_info = None
            st.session_state.conversation_history = []
            st.session_state.user_info_messages = []
            st.rerun()
    
    # Instructions
    st.markdown(MEDICAL_QA_TEXTS["instructions"][st.session_state.language])
    
    # Chat interface for medical Q&A
    st.markdown(f"### {MEDICAL_QA_TEXTS['chat_header'][st.session_state.language]}")
    
    # Display conversation history
    for msg in st.session_state.conversation_history:
        display_message(msg["content"], msg["is_user"], msg["timestamp"])
    
    # User input
    user_question = st.chat_input(MEDICAL_QA_TEXTS["chat_placeholder"][st.session_state.language])
    
    if user_question:
        # Add user message to history
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.conversation_history.append({
            "content": user_question,
            "is_user": True,
            "timestamp": timestamp
        })
        
        # Display user message
        display_message(user_question, True, timestamp)
        
        # Prepare conversation history for API
        conversation_history = [
            {"role": "user" if msg["is_user"] else "assistant", "content": msg["content"]}
            for msg in st.session_state.conversation_history[:-1]  # Exclude the just-added message
        ]
        
        # Call backend for medical Q&A
        with st.spinner(MEDICAL_QA_TEXTS["searching"][st.session_state.language]):
            response = call_backend_api(settings.ENDPOINTS["medical_qa"], {
                "message": user_question,
                "user_info": st.session_state.user_info,
                "conversation_history": conversation_history,
                "ui_language": st.session_state.language  # Send UI preference
            })
        
        if "error" not in response:
            # Add assistant response to history
            assistant_timestamp = datetime.now().strftime("%H:%M")
            st.session_state.conversation_history.append({
                "content": response["response"],
                "is_user": False,
                "timestamp": assistant_timestamp
            })
            
            # Display assistant message
            display_message(response["response"], False, assistant_timestamp)