"""
User-Specific Data Generator

This module generates user-specific text files containing all medical service
information tailored to specific HMO and membership tier combinations.
"""

import os
import json
import glob


def load_all_json_files(jsons_folder="preprocessing/jsons"):
    """Load all JSON files from the jsons folder"""
    json_files = glob.glob(os.path.join(jsons_folder, "*.json"))
    all_data = {}
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            filename = os.path.splitext(os.path.basename(json_file))[0]
            all_data[filename] = json.load(f)
    
    return all_data


def generate_user_specific_text(all_data, hmo, tier, output_dir):
    """Generate user-specific text file for given HMO and tier combination"""
    
    content_lines = []
    content_lines.append(f"=== נתוני שירותים רפואיים עבור {hmo} - {tier} ===\n")
    
    # Process each medical service category
    for service_category, data in all_data.items():
        content_lines.append(f"## {data['title']}")
        content_lines.append("")
        
        # Add general description
        content_lines.append("### תיאור כללי:")
        content_lines.append(data['general_description'])

        if hmo in data['specific_description']:
            content_lines.append(data['specific_description'][hmo])
        content_lines.append("")
        
        # Add services details
        content_lines.append("### פירוט שירותים:")
        
        if 'services_descriptions' in data and 'services_details' in data:
            for service_name, description in data['services_descriptions'].items():
                content_lines.append(f"**{service_name}:**")
                content_lines.append(f"תיאור: {description}")
                
                # Get tier-specific benefits for this HMO
                if (hmo in data['services_details'] and 
                    tier in data['services_details'][hmo] and 
                    service_name in data['services_details'][hmo][tier]):
                    
                    benefits = data['services_details'][hmo][tier][service_name]
                    content_lines.append(f"הטבות: {benefits}")
                else:
                    content_lines.append("הטבות: לא זמין")
                
                content_lines.append("")
        
        # Add phone numbers
        if 'phone_numbers' in data:
            content_lines.append("### מספרי טלפון:")
            content_lines.append(data['phone_numbers']['title'])
            
            if (hmo in data['phone_numbers']['contact_info']):
                contact_info = data['phone_numbers']['contact_info'][hmo]
                content_lines.append(f"{hmo}: {contact_info}")
            content_lines.append("")
        
        # Add additional information
        if 'additional_information' in data:
            content_lines.append("### מידע נוסף:")
            content_lines.append(data['additional_information']['title'])
            
            if (hmo in data['additional_information']['details']):
                details = data['additional_information']['details'][hmo]
                if 'phone' in details:
                    content_lines.append(f"טלפון: {details['phone']}")
                if 'website' in details:
                    content_lines.append(f"אתר: {details['website']}")
            content_lines.append("")
        
        content_lines.append("=" * 50)
        content_lines.append("")
    
    # Save to text file
    filename = f"{hmo}_{tier}.txt"
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_lines))
    
    return filename


def create_all_user_files():
    """Generate all user-specific data files for all HMO and tier combinations"""
    # Define paths
    jsons_folder = "preprocessing/jsons"
    output_folder = "user_specific_data"
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load all JSON data
    print("Loading JSON files...")
    all_data = load_all_json_files(jsons_folder)
    print(f"Loaded {len(all_data)} medical service categories")
    
    # Define HMO and tier combinations
    hmos = ["מכבי", "מאוחדת", "כללית"]
    tiers = ["זהב", "כסף", "ארד"]
    
    # Generate text files for each combination
    print("\nGenerating user-specific data files...")
    
    generated_files = []
    for hmo in hmos:
        for tier in tiers:
            filename = generate_user_specific_text(all_data, hmo, tier, output_folder)
            generated_files.append(filename)
            print(f"Generated: file #{len(generated_files)}")
    
    print(f"\nUser-specific data generation complete!")
    print(f"Generated {len(generated_files)} files in '{output_folder}' directory.")
    return generated_files


def generate_user_specific_data(hmo, tier, jsons_folder="jsons", output_dir="user_specific_data"):
    """Generate a single user-specific data file for given HMO and tier"""
    all_data = load_all_json_files(jsons_folder)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    return generate_user_specific_text(all_data, hmo, tier, output_dir)


if __name__ == "__main__":
    create_all_user_files()