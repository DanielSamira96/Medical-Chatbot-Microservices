"""
Simple language detection and multilingual error messages.
"""

import re
from config.settings import settings

def detect_language_from_text(text: str) -> str:
    """
    Detect if text is primarily Hebrew or English, with fallback to default.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Valid language code from SUPPORTED_LANGUAGES, or default language
    """
    
    if not text or len(text.strip()) < 3:
        return settings.DEFAULT_LANGUAGE
    
    # Count Hebrew characters
    hebrew_pattern = r'[\u0590-\u05FF]'
    hebrew_chars = len(re.findall(hebrew_pattern, text))
    
    # Count English characters  
    english_pattern = r'[a-zA-Z]'
    english_chars = len(re.findall(english_pattern, text))
    
    # Need at least some characters to decide
    if hebrew_chars == 0 and english_chars == 0:
        return settings.DEFAULT_LANGUAGE
    
    # Determine detected language
    detected = 'he' if hebrew_chars > english_chars else 'en'
    
    # IMPORTANT: Validate against supported languages
    if detected in settings.SUPPORTED_LANGUAGES:
        return detected
    else:
        return settings.DEFAULT_LANGUAGE  # Fallback to default for unsupported languages


ERROR_MESSAGES = {
    "processing_error": {
        'he': 'שגיאה בעיבוד הנתונים. אנא בדוק את הפרטים ונסה שוב.',
        'en': 'Error processing data. Please check the details and try again.'
    },
    "server_error": {
        'he': 'שגיאה בשרת. אנא נסה שוב מאוחר יותר.',
        'en': 'Server error. Please try again later.'
    },
    "azure_connection_error": {
        'he': 'שגיאה בחיבור לשירות. אנא נסה שוב.',
        'en': 'Service connection error. Please try again.'
    },
    "invalid_user_info": {
        'he': 'הנתונים שסופקו אינם תקינים. אנא בדוק ונסה שוב.',
        'en': 'The provided information is invalid. Please check and try again.'
    },
    "context_load_error": {
        'he': 'שגיאה בטעינת נתוני השירותים הרפואיים.',
        'en': 'Error loading medical services data.'
    }
}

def get_error_message(message_type: str, language: str) -> str:
    """
    Get error message in specified language.
    
    Args:
        message_type: Error message type (e.g., 'processing_error')
        language: Language code
        
    Returns:
        Error message in requested language
    """
    message_dict = ERROR_MESSAGES.get(message_type, ERROR_MESSAGES["server_error"])
    return message_dict.get(language, message_dict.get('he', 'Unknown error'))
