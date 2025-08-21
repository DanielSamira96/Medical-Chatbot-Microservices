"""
Comprehensive user information validation.
"""

from typing import Dict, List, Any
from utils.validators.conditions import (
    validate_israeli_id,
    validate_hmo_card_number,
    validate_hmo_name,
    validate_membership_tier,
    validate_age,
    validate_name,
    validate_gender
)
from utils.logging import log_error
from .translations import get_validator_message, get_field_name


def translate_english_to_hebrew(user_info: Dict[str, Any]) -> Dict[str, Any]:
    """Translate English HMO names and membership tiers to Hebrew."""
    translated_data = user_info.copy()
    
    # HMO name translations
    hmo_translations = {
        "maccabi": "מכבי",
        "meuhedet": "מאוחדת", 
        "clalit": "כללית"
    }
    
    # Membership tier translations
    tier_translations = {
        "gold": "זהב",
        "silver": "כסף",
        "bronze": "ארד"
    }
    
    if "hmo_name" in translated_data:
        hmo_lower = translated_data["hmo_name"].lower()
        if hmo_lower in hmo_translations:
            translated_data["hmo_name"] = hmo_translations[hmo_lower]
    
    if "membership_tier" in translated_data:
        tier_lower = translated_data["membership_tier"].lower()
        if tier_lower in tier_translations:
            translated_data["membership_tier"] = tier_translations[tier_lower]
    
    return translated_data


def validate_user_info(user_info: Dict[str, Any], chat_content_language: str = "hebrew") -> Dict[str, Any]:
    """
    Validate complete user information.
    
    Args:
        user_info: Dictionary containing user information
        
    Returns:
        Dictionary with validation results:
        {
            "is_valid": bool,
            "errors": List[str],
            "field_errors": Dict[str, str],
            "cleaned_data": Dict[str, Any]
        }
    """
    errors = []
    field_errors = {}
    cleaned_data = {}
    
    # Required fields
    required_fields = [
        "first_name", "last_name", "id_number", "gender", 
        "age", "hmo_name", "hmo_card_number", "membership_tier"
    ]
    
    # Check for missing required fields
    for field in required_fields:
        if field not in user_info or user_info[field] is None:
            translated_field = get_field_name(field, chat_content_language)
            field_errors[field] = get_validator_message("field_required", chat_content_language, field=translated_field)
            continue
        
        # Clean the field value
        value = user_info[field]
        if isinstance(value, str):
            value = value.strip()
        
        cleaned_data[field] = value
    
    # If any required fields are missing, return early
    if field_errors:
        return {
            "is_valid": False,
            "errors": [get_validator_message("missing_required_fields", chat_content_language)],
            "field_errors": field_errors,
            "cleaned_data": cleaned_data
        }
    
    # Validate first name
    is_valid, error = validate_name(cleaned_data["first_name"], "First name", chat_content_language)
    if not is_valid:
        field_errors["first_name"] = error
    
    # Validate last name
    is_valid, error = validate_name(cleaned_data["last_name"], "Last name", chat_content_language)
    if not is_valid:
        field_errors["last_name"] = error
    
    # Validate Israeli ID
    is_valid, error = validate_israeli_id(cleaned_data["id_number"], chat_content_language)
    if not is_valid:
        field_errors["id_number"] = error
    
    # Validate HMO card number (check length is 9)
    is_valid, error = validate_hmo_card_number(cleaned_data["hmo_card_number"], chat_content_language)
    if not is_valid:
        field_errors["hmo_card_number"] = get_validator_message("invalid_hmo_card", chat_content_language, error=error)
    
    # Validate gender
    is_valid, error = validate_gender(cleaned_data["gender"], chat_content_language)
    if not is_valid:
        field_errors["gender"] = error
    
    # Validate age
    try:
        age_int = int(cleaned_data["age"])
        cleaned_data["age"] = age_int
        is_valid, error = validate_age(age_int, chat_content_language)
        if not is_valid:
            field_errors["age"] = error
    except (ValueError, TypeError):
        field_errors["age"] = get_validator_message("age_must_be_number", chat_content_language)
    
    # Validate HMO name
    is_valid, error = validate_hmo_name(cleaned_data["hmo_name"], chat_content_language)
    if not is_valid:
        field_errors["hmo_name"] = error
    
    # Validate membership tier
    is_valid, error = validate_membership_tier(cleaned_data["membership_tier"], chat_content_language)
    if not is_valid:
        field_errors["membership_tier"] = error
    
    # Compile overall result
    is_overall_valid = len(field_errors) == 0
    
    # If validation passed, translate English values to Hebrew
    if is_overall_valid:
        cleaned_data = translate_english_to_hebrew(cleaned_data)
    
    if field_errors:
        errors = [get_validator_message("validation_failed_for", chat_content_language, fields=', '.join(field_errors.keys()))]
        
        # Log validation errors for monitoring
        log_error(
            "User info validation failed",
            field_errors=field_errors,
            user_hmo=cleaned_data.get("hmo_name"),
            validation_fields_failed=list(field_errors.keys())
        )
    
    return {
        "is_valid": is_overall_valid,
        "errors": errors,
        "field_errors": field_errors,
        "cleaned_data": cleaned_data
    }