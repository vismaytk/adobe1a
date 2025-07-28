# solution/utils.py
# Essential utility functions for Adobe Hackathon Solution - Round 1A Only

import os
import json
from typing import List, Dict, Any

def ensure_directory_exists(directory_path: str) -> None:
    """Ensure that a directory exists, create it if it doesn't."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def save_json_output(data: Dict[str, Any], output_path: str) -> None:
    """Save data to a JSON file with proper formatting."""
    ensure_directory_exists(os.path.dirname(output_path))
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_pdf_files(directory: str) -> List[str]:
    """Get all PDF files from a directory."""
    pdf_files = []
    for file in os.listdir(directory):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(directory, file))
    return pdf_files

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize line breaks
    text = ' '.join(text.split())
    return text.strip()

def validate_pdf_file(file_path: str) -> bool:
    """Validate that a file is a readable PDF."""
    try:
        import fitz
        doc = fitz.open(file_path)
        page_count = doc.page_count
        doc.close()
        return page_count > 0
    except Exception:
        return False 