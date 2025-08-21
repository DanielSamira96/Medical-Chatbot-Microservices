"""
Israeli-specific validation functions.
"""

import re
from typing import Tuple, Optional
from .translations import get_validator_message, get_field_name


def validate_israeli_id(id_number: str, language: str = "en") -> Tuple[bool, Optional[str]]:
    """
    Validate Israeli ID number using the official checksum algorithm.
    
    Args:
        id_number: The ID number as string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Clean the input
    id_str = str(id_number).strip()
    
    # Basic format check
    if not id_str.isdigit():
        return False, get_validator_message("id_only_digits", language)
    
    if len(id_str) != 9:
        return False, get_validator_message("id_nine_digits", language)
    
    # Convert to list of integers
    try:
        digits = [int(d) for d in id_str]
    except ValueError:
        return False, get_validator_message("id_invalid_format", language)
    
    # Israeli ID checksum algorithm
    checksum = 0
    for i, digit in enumerate(digits):
        # Multiply by 1 if position is even, by 2 if odd (0-indexed)
        if i % 2 == 0:
            checksum += digit
        else:
            multiplied = digit * 2
            # If result is two digits, add them separately
            checksum += multiplied if multiplied < 10 else multiplied // 10 + multiplied % 10
    
    # Valid if checksum is divisible by 10
    if checksum % 10 != 0:
        return False, get_validator_message("id_invalid_checksum", language)
    
    return True, None


def validate_hmo_card_number(card_number: str, language: str = "en") -> Tuple[bool, Optional[str]]:
    """
    Validate HMO card number (must be exactly 9 characters).
    
    Args:
        card_number: The HMO card number as string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    card_str = str(card_number).strip()
    
    if len(card_str) != 9:
        return False, get_validator_message("hmo_card_nine_chars", language)
    
    return True, None


def validate_hmo_name(hmo_name: str, language: str = "en") -> Tuple[bool, Optional[str]]:
    """
    Validate HMO name against allowed values.
    
    Args:
        hmo_name: The HMO name
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Accept both Hebrew and English HMO names (case-insensitive)
    allowed_hmos = {
        "מכבי", "מאוחדת", "כללית",  # Hebrew
        "maccabi", "meuhedet", "clalit"  # English
    }
    
    if not hmo_name or not hmo_name.strip():
        return False, get_validator_message("hmo_name_required", language)
    
    # Case-insensitive comparison
    if hmo_name.strip().lower() not in [hmo.lower() for hmo in allowed_hmos]:
        display_options = "מכבי, מאוחדת, כללית" if language == "he" else "Maccabi, Meuhedet, Clalit"
        return False, get_validator_message("hmo_name_invalid", language, options=display_options)
    
    return True, None


def validate_membership_tier(tier: str, language: str = "en") -> Tuple[bool, Optional[str]]:
    """
    Validate membership tier against allowed values.
    
    Args:
        tier: The membership tier
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Accept both Hebrew and English membership tiers (case-insensitive)
    allowed_tiers = {
        "זהב", "כסף", "ארד",  # Hebrew
        "gold", "silver", "bronze"  # English
    }
    
    if not tier or not tier.strip():
        return False, get_validator_message("membership_tier_required", language)
    
    # Case-insensitive comparison
    if tier.strip().lower() not in [t.lower() for t in allowed_tiers]:
        display_options = "זהב, כסף, ארד" if language == "he" else "Gold, Silver, Bronze"
        return False, get_validator_message("membership_tier_invalid", language, options=display_options)
    
    return True, None


def validate_age(age: int, language: str = "en") -> Tuple[bool, Optional[str]]:
    """
    Validate age range.
    
    Args:
        age: The age as integer
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(age, int):
        try:
            age = int(age)
        except (ValueError, TypeError):
            return False, get_validator_message("age_must_be_number", language)
    
    if age < 0:
        return False, get_validator_message("age_cannot_be_negative", language)
    
    if age > 120:
        return False, get_validator_message("age_max_120", language)
    
    return True, None


def validate_name(name: str, field_name: str = "Name", language: str = "en") -> Tuple[bool, Optional[str]]:
    """
    Validate name field.
    
    Args:
        name: The name to validate
        field_name: Field name for error messages
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    translated_field = get_field_name(field_name.lower().replace(" ", "_"), language)
    
    if not name or not name.strip():
        return False, get_validator_message("field_required", language, field=translated_field)
    
    # Remove extra spaces
    name = name.strip()
    
    if len(name) < 2:
        return False, get_validator_message("name_min_length", language, field=translated_field)
    
    if len(name) > 50:
        return False, get_validator_message("name_max_length", language, field=translated_field)
    
    # Allow Hebrew, English letters, spaces, hyphens, and apostrophes
    name_pattern = re.compile(r"^[\u0590-\u05FFa-zA-Z\s\-']+$")
    if not name_pattern.match(name):
        return False, get_validator_message("name_invalid_chars", language, field=translated_field)
    
    return True, None


def validate_gender(gender: str, language: str = "en") -> Tuple[bool, Optional[str]]:
    """
    Validate gender field.
    
    Args:
        gender: The gender to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not gender or not gender.strip():
        return False, get_validator_message("gender_required", language)
    
    # Accept common gender values in Hebrew and English
    allowed_genders = {
        "זכר", "נקבה", "אחר",  # Hebrew
        "male", "female", "other", "m", "f",  # English
        "גבר", "אישה"  # Additional Hebrew options
    }
    
    if gender.lower().strip() not in [g.lower() for g in allowed_genders]:
        return False, get_validator_message("gender_must_be_specified", language)
    
    return True, None