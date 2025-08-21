"""
Backend message translations.
"""

BACKEND_MESSAGES = {
    "validation_errors_found": {
        "he": "נמצאו שגיאות בנתונים:"
              "\n{errors}\n\n"
              "אנא תקן את השגיאות ונסה שוב.",
        "en": "Data validation errors found:\n{errors}\n\nPlease correct the errors and try again."
    },
    "processing_error": {
        "he": "שגיאה בעיבוד הנתונים. אנא בדוק את הפרטים ונסה שוב.",
        "en": "Error processing data. Please check the details and try again."
    },
    "server_error": {
        "he": "שגיאה בשרת. אנא נסה שוב מאוחר יותר.",
        "en": "Server error. Please try again later."
    },
    "azure_connection_error": {
        "he": "שגיאה בחיבור לשירות. אנא נסה שוב.",
        "en": "Service connection error. Please try again."
    },
    "context_load_error": {
        "he": "שגיאה בטעינת נתוני השירותים הרפואיים.",
        "en": "Error loading medical services data."
    }
}

def get_message(key: str, language: str = "en"):
    """Get message in specified language."""
    if key not in BACKEND_MESSAGES:
        return f"[Missing: {key}]"
    
    message_dict = BACKEND_MESSAGES[key]
    return message_dict.get(language, message_dict.get("en", f"[Missing: {key}]"))