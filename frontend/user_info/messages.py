"""
User Information Collection Phase - Translations
"""

USER_INFO_TEXTS = {
    "page_title": {
        "he": "🏥 צ'אטבוט רפואי - איסוף פרטים",
        "en": "🏥 Medical Chatbot - User Information"
    },
    "instructions": {
        "he": """
        ### שלום! אני כאן לעזור לך עם שאלות על שירותי בריאות
        
        **כדי להתחיל, אני צריך לאסוף כמה פרטים:**
        - שם פרטי ומשפחה
        - מספר תעודת זהות (9 ספרות)
        - מגדר
        - גיל (0-120)
        - שם קופת חולים (מכבי / מאוחדת / כללית)
        - מספר כרטיס קופת חולים (9 ספרות)
        - רמת החברות (זהב / כסף / ארד)
        
        **אנא התחל לספר לי על עצמך...**
        """,
        "en": """
        ### Hello! I'm here to help you with questions about Israeli health services
        
        **To get started, I need to collect some information:**
        - First and last name
        - ID number (9 digits)
        - Gender
        - Age (0-120)
        - HMO name (Maccabi / Meuhedet / Clalit)
        - HMO card number (9 digits)
        - Insurance membership tier (Gold / Silver / Bronze)
        
        **Please start by telling me about yourself...**
        """
    },
    "chat_placeholder": {
        "he": "כתוב את ההודעה שלך כאן...",
        "en": "Type your message here..."
    }
}