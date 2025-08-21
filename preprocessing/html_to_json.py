"""
HTML to JSON Converter

This module parses HTML files containing medical service information
and converts them into structured JSON format.
"""

import os
import json
from bs4 import BeautifulSoup
import re


def parse_html_to_json(html_file_path, output_dir):
    """Parse HTML file and convert to structured JSON format with HMO data organized by keys"""
    
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract title (first h2)
    title = soup.find('h2').get_text().strip()
    
    # Extract first paragraph (general description)
    first_p = soup.find('p').get_text().strip()
    
    # Extract second paragraph (contains HMO reference that needs to be customized)
    paragraphs = soup.find_all('p')
    second_p = paragraphs[1].get_text().strip()
    
    # Extract service descriptions from ul/li
    services_descriptions = {}
    ul_element = soup.find('ul')
    if ul_element:
        for li in ul_element.find_all('li'):
            text = li.get_text().strip()
            if ':' in text:
                service_name, description = text.split(':', 1)
                services_descriptions[service_name.strip()] = description.strip()
    
    # Extract table data
    table = soup.find('table')
    hmo_services_data = {"מכבי": {}, "מאוחדת": {}, "כללית": {}}
    
    if table:
        rows = table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 4:
                service_name = cells[0].get_text().strip()
                
                # Parse each HMO's data
                hmo_names = ["מכבי", "מאוחדת", "כללית"]
                for i, hmo in enumerate(hmo_names, 1):
                    cell_html = str(cells[i])
                    
                    # Extract tier information
                    tiers_data = {}
                    for tier in ["זהב", "כסף", "ארד"]:
                        pattern = rf'<strong>{tier}:</strong>\s*([^<]*(?:<br[^>]*>[^<]*)*)'
                        match = re.search(pattern, cell_html)
                        if match:
                            tier_info = match.group(1).strip()
                            tier_info = re.sub(r'<br[^>]*>', ' ', tier_info).strip()
                            tiers_data[tier] = tier_info
                    
                    hmo_services_data[hmo][service_name] = tiers_data
    
    # Extract phone numbers (first h3 section)
    phone_numbers = {}
    h3_elements = soup.find_all('h3')
    if len(h3_elements) >= 1:
        first_h3_title = h3_elements[0].get_text().strip()
        # Find the ul element after the first h3
        next_ul = h3_elements[0].find_next_sibling('ul')
        if next_ul:
            for li in next_ul.find_all('li'):
                text = li.get_text().strip()
                for hmo in ["מכבי", "מאוחדת", "כללית"]:
                    if text.startswith(hmo):
                        phone_info = text.replace(f"{hmo}:", "").strip()
                        phone_numbers[hmo] = phone_info
    
    # Extract additional information (second h3 section)
    additional_info = {}
    if len(h3_elements) >= 2:
        second_h3_title = h3_elements[1].get_text().strip()
        next_ul = h3_elements[1].find_next_sibling('ul')
        if next_ul:
            for li in next_ul.find_all('li'):
                text = li.get_text()
                for hmo in ["מכבי", "מאוחדת", "כללית"]:
                    if hmo in text:
                        # Extract phone and website info
                        lines = text.split('\n')
                        info = {}
                        for line in lines:
                            line = line.strip()
                            if line.startswith('טלפון:'):
                                info['phone'] = line.replace('טלפון:', '').strip()
                            elif line.startswith('מידע נוסף:'):
                                # Extract URL from a tag
                                a_tag = li.find('a')
                                if a_tag:
                                    info['website'] = a_tag.get('href')
                        additional_info[hmo] = info
    
    # Create single JSON structure with all HMOs
    hmo_names = ["מכבי", "מאוחדת", "כללית"]
    
    # Create specific descriptions for each HMO
    specific_descriptions = {}
    for hmo in hmo_names:
        specific_descriptions[hmo] = second_p.replace(
            'קופות החולים "מכבי", "מאוחדת" ו"כללית"',
            f'קופת החולים "{hmo}"'
        )
    
    # Organize services details by HMO
    organized_services_details = {}
    for hmo in hmo_names:
        organized_services_details[hmo] = {
            "זהב": {},
            "כסף": {},
            "ארד": {}
        }
        
        # Populate services details for each tier
        for service_name, tiers in hmo_services_data[hmo].items():
            for tier in ["זהב", "כסף", "ארד"]:
                if tier in tiers:
                    organized_services_details[hmo][tier][service_name] = tiers[tier]
    
    # Organize phone numbers by HMO
    organized_phone_numbers = {}
    for hmo in hmo_names:
        organized_phone_numbers[hmo] = phone_numbers.get(hmo, "")
    
    # Organize additional information by HMO
    organized_additional_info = {}
    for hmo in hmo_names:
        organized_additional_info[hmo] = additional_info.get(hmo, {})
    
    # Create final JSON structure
    final_json = {
        "title": title,
        "general_description": first_p,
        "specific_description": specific_descriptions,
        "services_descriptions": services_descriptions,
        "services_details": organized_services_details,
        "phone_numbers": {
            "title": first_h3_title if 'first_h3_title' in locals() else "",
            "contact_info": organized_phone_numbers
        },
        "additional_information": {
            "title": second_h3_title if 'second_h3_title' in locals() else "",
            "details": organized_additional_info
        }
    }
    
    # Save single JSON file
    base_name = os.path.splitext(os.path.basename(html_file_path))[0]
    output_filename = f"{base_name}.json"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(final_json, json_file, ensure_ascii=False, indent=2)
    
    return output_filename


def process_all_html_files():
    """Process all HTML files and convert them to JSON format"""
    # Define paths
    html_folder = "phase2_data"
    output_folder = "preprocessing/jsons"
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # List all HTML files
    html_files = [
        "workshops_services.html",
        "alternative_services.html", 
        "communication_clinic_services.html",
        "pragrency_services.html",
        "optometry_services.html",
        "dentel_services.html"
    ]
    
    # Process each HTML file
    processed_files = []
    for html_file in html_files:
        html_path = os.path.join(html_folder, html_file)
        if os.path.exists(html_path):
            print(f"Processing: {html_file}")
            output_filename = parse_html_to_json(html_path, output_folder)
            processed_files.append(output_filename)
        else:
            print(f"File not found: {html_file}")
    
    print(f"\nHTML to JSON conversion complete!")
    print(f"Generated {len(processed_files)} JSON files in '{output_folder}' directory.")
    return processed_files


if __name__ == "__main__":
    process_all_html_files()