"""
Main Preprocessing Runner

This script runs the complete data preprocessing pipeline:
1. Converts HTML files to structured JSON format
2. Generates user-specific text files for all HMO + tier combinations
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.html_to_json import process_all_html_files
from preprocessing.generate_user_data import create_all_user_files


def run_complete_preprocessing():
    """Run the complete preprocessing pipeline"""
    
    print("=" * 60)
    print("MEDICAL CHATBOT DATA PREPROCESSING PIPELINE")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Convert HTML to JSON
        print("STEP 1: Converting HTML files to JSON format...")
        print("-" * 40)
        json_files = process_all_html_files()
        print(f"SUCCESS: Processed {len(json_files)} HTML files")
        print()
        
        # Step 2: Generate user-specific data files
        print("STEP 2: Generating user-specific data files...")
        print("-" * 40)
        user_files = create_all_user_files()
        print(f"SUCCESS: Generated {len(user_files)} user-specific files")
        print()
        
        # Summary
        print("=" * 60)
        print("PREPROCESSING COMPLETE!")
        print("=" * 60)
        print(f"JSON files: {len(json_files)} files in 'preprocessing/jsons/' directory")
        print(f"User files: {len(user_files)} files in 'user_specific_data/' directory")
        
        return {
            'success': True,
            'json_files': json_files,
            'user_files': user_files
        }
        
    except Exception as e:
        print(f"ERROR during preprocessing: {str(e)}")
        print("Please check the error and try again.")
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    result = run_complete_preprocessing()
    
    if not result['success']:
        sys.exit(1)
    else:
        print("Preprocessing pipeline completed successfully!")
        sys.exit(0)