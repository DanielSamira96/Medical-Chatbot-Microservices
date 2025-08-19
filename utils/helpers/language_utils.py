"""
Simple language detection and multilingual error messages.
"""

import re
from typing import List, Optional
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
    detected = 'hebrew' if hebrew_chars > english_chars else 'english'
    
    # IMPORTANT: Validate against supported languages
    if detected in settings.SUPPORTED_LANGUAGES:
        return detected
    else:
        return settings.DEFAULT_LANGUAGE  # Fallback to default for unsupported languages


class ErrorMessages:
    """Multilingual error messages."""
    
    PROCESSING_ERROR = {
        'hebrew': 'שגיאה בעיבוד הנתונים. אנא בדוק את הפרטים ונסה שוב.',
        'english': 'Error processing data. Please check the details and try again.'
    }
    
    SERVER_ERROR = {
        'hebrew': 'שגיאה בשרת. אנא נסה שוב מאוחר יותר.',
        'english': 'Server error. Please try again later.'
    }
    
    AZURE_CONNECTION_ERROR = {
        'hebrew': 'שגיאה בחיבור לשירות. אנא נסה שוב.',
        'english': 'Service connection error. Please try again.'
    }
    
    INVALID_USER_INFO = {
        'hebrew': 'הנתונים שסופקו אינם תקינים. אנא בדוק ונסה שוב.',
        'english': 'The provided information is invalid. Please check and try again.'
    }
    
    CONTEXT_LOAD_ERROR = {
        'hebrew': 'שגיאה בטעינת נתוני השירותים הרפואיים.',
        'english': 'Error loading medical services data.'
    }
    
    @classmethod
    def get(cls, message_type: str, language: str) -> str:
        """
        Get error message in specified language.
        
        Args:
            message_type: Error message type (e.g., 'PROCESSING_ERROR')
            language: Language code
            
        Returns:
            Error message in requested language
        """
        
        message_dict = getattr(cls, message_type, cls.SERVER_ERROR)
        return message_dict.get(language, message_dict.get('hebrew', 'Unknown error'))

# Global instance
error_messages = ErrorMessages()