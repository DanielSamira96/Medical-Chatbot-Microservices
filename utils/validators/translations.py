"""
Validator error message translations.
"""

VALIDATOR_MESSAGES = {
    # Required field errors
    "field_required": {
        "he": "{field} נדרש",
        "en": "{field} is required"
    },
    "missing_required_fields": {
        "he": "חסרים שדות נדרשים",
        "en": "Missing required fields"
    },
    
    # ID validation
    "id_only_digits": {
        "he": "תעודת זהות חייבת להכיל רק ספרות",
        "en": "ID must contain only digits"
    },
    "id_nine_digits": {
        "he": "תעודת זהות חייבת להיות בדיוק 9 ספרות",
        "en": "ID must be exactly 9 digits"
    },
    "id_invalid_format": {
        "he": "פורמט תעודת זהות לא תקין",
        "en": "Invalid ID format"
    },
    "id_invalid_checksum": {
        "he": "ספרת ביקורת של תעודת זהות לא תקינה",
        "en": "Invalid ID checksum"
    },
    
    # HMO card validation
    "hmo_card_nine_chars": {
        "he": "מספר כרטיס קופת חולים חייב להיות בדיוק 9 תווים",
        "en": "HMO card number must be exactly 9 characters"
    },
    
    # Name validation
    "name_min_length": {
        "he": "{field} חייב להיות לפחות 2 תווים",
        "en": "{field} must be at least 2 characters"
    },
    "name_max_length": {
        "he": "{field} לא יכול לעלות על 50 תווים",
        "en": "{field} cannot exceed 50 characters"
    },
    "name_invalid_chars": {
        "he": "{field} יכול להכיל רק אותיות, רווחים, מקפים ואפוסטרופים",
        "en": "{field} can only contain letters, spaces, hyphens, and apostrophes"
    },
    
    # Age validation
    "age_must_be_number": {
        "he": "גיל חייב להיות מספר",
        "en": "Age must be a number"
    },
    "age_cannot_be_negative": {
        "he": "גיל לא יכול להיות שלילי",
        "en": "Age cannot be negative"
    },
    "age_max_120": {
        "he": "גיל לא יכול לעלות על 120",
        "en": "Age cannot exceed 120"
    },
    
    # Gender validation
    "gender_required": {
        "he": "מין נדרש",
        "en": "Gender is required"
    },
    "gender_must_be_specified": {
        "he": "יש לציין מין",
        "en": "Gender must be specified"
    },
    
    # HMO validation
    "hmo_name_required": {
        "he": "שם קופת חולים נדרש",
        "en": "HMO name is required"
    },
    "hmo_name_invalid": {
        "he": "קופת חולים חייבת להיות אחת מ: {options}",
        "en": "HMO must be one of: {options}"
    },
    
    # Membership tier validation
    "membership_tier_required": {
        "he": "דרג חברות נדרש",
        "en": "Membership tier is required"
    },
    "membership_tier_invalid": {
        "he": "דרג חברות חייב להיות אחד מ: {options}",
        "en": "Membership tier must be one of: {options}"
    },
    
    # General validation
    "validation_failed_for": {
        "he": "אימות נכשל עבור: {fields}",
        "en": "Validation failed for: {fields}"
    },
    "invalid_hmo_card": {
        "he": "מספר כרטיס קופת חולים לא תקין: {error}",
        "en": "Invalid HMO card number: {error}"
    }
}

# Field name translations
FIELD_NAMES = {
    "first_name": {
        "he": "שם פרטי",
        "en": "First name"
    },
    "last_name": {
        "he": "שם משפחה",
        "en": "Last name"
    },
    "id_number": {
        "he": "תעודת זהות",
        "en": "ID number"
    },
    "gender": {
        "he": "מין",
        "en": "Gender"
    },
    "age": {
        "he": "גיל",
        "en": "Age"
    },
    "hmo_name": {
        "he": "קופת חולים",
        "en": "HMO name"
    },
    "hmo_card_number": {
        "he": "מספר כרטיס קופת חולים",
        "en": "HMO card number"
    },
    "membership_tier": {
        "he": "דרג חברות",
        "en": "Membership tier"
    }
}


def get_validator_message(key: str, language: str = "en", **kwargs):
    """Get validator message in specified language."""
    if key not in VALIDATOR_MESSAGES:
        return f"[Missing: {key}]"
    
    message_dict = VALIDATOR_MESSAGES[key]
    message = message_dict.get(language, message_dict.get("en", f"[Missing: {key}]"))
    
    # Format with variables if provided
    try:
        return message.format(**kwargs)
    except (KeyError, ValueError):
        return message


def get_field_name(field: str, language: str = "en"):
    """Get field name in specified language."""
    if field not in FIELD_NAMES:
        return field
    
    field_dict = FIELD_NAMES[field]
    return field_dict.get(language, field_dict.get("en", field))