"""
Medical Chatbot Frontend - Main Streamlit Application
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import streamlit as st
from config.settings import settings
from frontend.utils.utils import initialize_session_state, check_backend_health, load_css_for_language
from frontend.user_info.page import user_info_phase
from frontend.medical_qa.page import medical_qa_phase
from frontend.utils.translations import COMMON_TEXTS


# Page configuration
st.set_page_config(
    page_title="Medical Chatbot - Israeli Health Funds",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def main():
    """Main application function."""
    initialize_session_state()
    
    # Load CSS for current language (RTL for Hebrew)
    load_css_for_language(st.session_state.language)
    
    # Language selection (shared across all phases)
    col1, col2 = st.columns([1, 3])
    with col1:
        language_options = {lang: "עברית" if lang == "he" else "English" 
                           for lang in settings.SUPPORTED_LANGUAGES}
        
        selected_lang = st.selectbox(
            COMMON_TEXTS["language_label"][st.session_state.language],
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=0 if st.session_state.language == "he" else 1
        )
        if st.session_state.language != selected_lang:
            st.session_state.language = selected_lang
            # Reload CSS when language changes and force rerun
            load_css_for_language(selected_lang)
            st.rerun()
    
    st.markdown("---")
    
    # Check backend health
    if not check_backend_health():
        st.error(COMMON_TEXTS["backend_error"][st.session_state.language])
        st.code("python backend/main.py")
        return
    
    # Route to appropriate phase
    if st.session_state.phase == "user_info":
        user_info_phase()
    elif st.session_state.phase == "medical_qa":
        medical_qa_phase()


if __name__ == "__main__":
    main()