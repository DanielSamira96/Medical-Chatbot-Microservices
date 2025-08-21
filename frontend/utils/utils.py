"""
Frontend utility functions.
"""

import streamlit as st
import requests
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
from config.settings import settings


def call_backend_api(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Call backend API with error handling."""
    try:
        # breakpoint()
        url = f"{settings.BACKEND_URL}{endpoint}"
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Backend connection error: {str(e)}")
        return {"error": str(e)}
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return {"error": str(e)}


def check_backend_health() -> bool:
    """Check if backend is running."""
    try:
        url = f"{settings.BACKEND_URL}{settings.ENDPOINTS['health']}"
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False


def initialize_session_state():
    """Initialize session state variables."""
    if "phase" not in st.session_state:
        st.session_state.phase = "user_info"  # "user_info" or "medical_qa"
    
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "user_info_messages" not in st.session_state:
        st.session_state.user_info_messages = []
    
    if "language" not in st.session_state:
        st.session_state.language = settings.DEFAULT_LANGUAGE


def load_css_for_language(language: str):
    """Load CSS for RTL support if Hebrew is selected."""
    if language == "he":
        try:
            css_path = Path(__file__).parent / "styles.css"
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        except Exception as e:
            # Fallback to no styling if CSS file is not found
            st.warning(f"Could not load CSS file: {str(e)}")


def display_message(message: str, is_user: bool = True, timestamp: str = None):
    """Display a chat message with proper styling."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    if is_user:
        st.chat_message("user").write(f"**[{timestamp}]** {message}")
    else:
        st.chat_message("assistant").write(f"**[{timestamp}]** {message}")