"""
Medical Context Loader

Utility to load user-specific medical service data for prompt injection.
"""

import os
from typing import Optional

def load_user_medical_context(hmo_name: str, membership_tier: str, data_folder: str = "user_specific_data") -> Optional[str]:
    """
    Load user-specific medical context from preprocessed text files.
    
    Args:
        hmo_name: HMO name (מכבי, מאוחדת, כללית)
        membership_tier: Membership tier (זהב, כסף, ארד)
        data_folder: Folder containing user-specific data files
        
    Returns:
        Medical context string or None if file not found
    """
    
    try:
        # Construct filename based on user's HMO and tier
        filename = f"{hmo_name}_{membership_tier}.txt"
        file_path = os.path.join(data_folder, filename)
        
        # Load the context file
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print(f"Warning: Context file not found: {file_path}")
            return None
            
    except Exception as e:
        print(f"Error loading medical context: {str(e)}")
        return None

def get_available_contexts(data_folder: str = "user_specific_data") -> list:
    """
    Get list of available user context combinations.
    
    Returns:
        List of (hmo, tier) tuples for available contexts
    """
    
    contexts = []
    
    try:
        if os.path.exists(data_folder):
            for filename in os.listdir(data_folder):
                if filename.endswith('.txt'):
                    # Parse filename: hmo_tier.txt
                    name_parts = filename.replace('.txt', '').split('_')
                    if len(name_parts) == 2:
                        hmo, tier = name_parts
                        contexts.append((hmo, tier))
                        
    except Exception as e:
        print(f"Error getting available contexts: {str(e)}")
        
    return contexts

def validate_user_context(hmo_name: str, membership_tier: str) -> bool:
    """
    Validate that a user's HMO and tier combination is supported.
    
    Args:
        hmo_name: HMO name
        membership_tier: Membership tier
        
    Returns:
        True if combination is valid, False otherwise
    """
    
    valid_hmos = ["מכבי", "מאוחדת", "כללית"]
    valid_tiers = ["זהב", "כסף", "ארד"]
    
    return hmo_name in valid_hmos and membership_tier in valid_tiers