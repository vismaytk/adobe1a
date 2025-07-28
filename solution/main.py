# solution/main.py
# Main orchestration script for Adobe Hackathon Solution - Round 1A Only

import os
import json
import sys
from typing import List, Dict, Any

# Add the solution directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from round_1a import extract_outline

# Constants
INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def run_round_1a(pdf_path: str, output_path: str) -> bool:
    """
    Run Round 1A: Document Outline Extraction
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path for the output JSON file
        
    Returns:
        True if successful, False otherwise
    """
    print(f"Processing Round 1A: {os.path.basename(pdf_path)}")
    
    try:
        result = extract_outline(pdf_path)
        
        if result and isinstance(result, dict):
            # Ensure output format matches requirements
            output = {
                "title": result.get("title", "Untitled Document"),
                "outline": result.get("outline", [])
            }
            
            # Validate outline format
            for item in output["outline"]:
                if not all(key in item for key in ["level", "text", "page"]):
                    print(f"Warning: Invalid outline item format in {pdf_path}")
                    return False
            
            # Write output
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Successfully generated outline: {os.path.basename(output_path)}")
            return True
        else:
            print(f"❌ Failed to extract outline from {pdf_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")
        return False

def main():
    """Main execution function for Round 1A only."""
    print("🚀 Adobe Hackathon Solution - Round 1A")
    print("=" * 40)
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get all PDF files from input directory
    try:
        files = os.listdir(INPUT_DIR)
        pdf_files = [f for f in files if f.lower().endswith(".pdf")]
        
        if not pdf_files:
            print("❌ No PDF files found in input directory")
            print("Please add PDF files to the input directory and try again.")
            sys.exit(1)
        
        print(f"📋 Found {len(pdf_files)} PDF file(s) to process")
        
        # Process each PDF individually
        success_count = 0
        total_count = len(pdf_files)
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(INPUT_DIR, pdf_file)
            output_filename = os.path.splitext(pdf_file)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            if run_round_1a(pdf_path, output_path):
                success_count += 1
        
        print(f"\n📊 Round 1A Results: {success_count}/{total_count} files processed successfully")
        
        if success_count == total_count:
            print("🎉 All PDFs processed successfully!")
        else:
            print("⚠️  Some files failed to process. Check the output above for details.")
        
    except Exception as e:
        print(f"❌ Error accessing input directory: {e}")
        sys.exit(1)
    
    print("\n🎉 Processing complete!")

if __name__ == "__main__":
    main() 