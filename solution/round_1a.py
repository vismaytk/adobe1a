# solution/round_1a.py
# Round 1A: Document Outline Extraction - Advanced Font Analysis Approach

import fitz  # PyMuPDF
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Tuple

class DocumentAnalyzer:
    """Advanced document structure analyzer for PDF outline extraction."""
    
    def __init__(self):
        self.title_candidates = []
        self.heading_candidates = []
        self.body_text_samples = []
        
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract structured outline from PDF using advanced font analysis.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with 'title' and 'outline' keys
        """
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"Error opening PDF {pdf_path}: {e}")
            return {"title": "Untitled Document", "outline": []}
        
        # Extract all text elements with metadata
        text_elements = self._extract_text_elements(doc)
        
        if not text_elements:
            return {"title": "Untitled Document", "outline": []}
        
        # Analyze document structure
        title = self._extract_title(text_elements)
        outline = self._extract_headings(text_elements)
        
        doc.close()
        
        return {
            "title": title,
            "outline": outline
        }
    
    def _extract_text_elements(self, doc: fitz.Document) -> List[Dict[str, Any]]:
        """Extract all text elements with comprehensive metadata."""
        elements = []
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # Get text blocks with detailed information
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if block["type"] == 0:  # Text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if not text:
                                continue
                            
                            # Calculate text characteristics
                            word_count = len(text.split())
                            char_count = len(text)
                            is_all_caps = text.isupper()
                            has_numbers = bool(re.search(r'\d', text))
                            
                            element = {
                                "text": text,
                                "font_size": round(span["size"], 1),
                                "font_name": span["font"],
                                "is_bold": "bold" in span["font"].lower() or span.get("flags", 0) & 2**4,
                                "is_italic": "italic" in span["font"].lower() or span.get("flags", 0) & 2**1,
                                "page": page_num + 1,
                                "y_pos": line["bbox"][1],
                                "x_pos": line["bbox"][0],
                                "word_count": word_count,
                                "char_count": char_count,
                                "is_all_caps": is_all_caps,
                                "has_numbers": has_numbers,
                                "line_height": line["bbox"][3] - line["bbox"][1]
                            }
                            
                            elements.append(element)
        
        return elements
    
    def _extract_title(self, elements: List[Dict[str, Any]]) -> str:
        """Extract document title using multiple heuristics."""
        if not elements:
            return "Untitled Document"
        
        # Focus on first page elements
        first_page_elements = [e for e in elements if e["page"] == 1]
        
        if not first_page_elements:
            return "Untitled Document"
        
        # Sort by font size (descending) and position
        first_page_elements.sort(key=lambda x: (x["font_size"], -x["y_pos"]), reverse=True)
        
        # Look for title candidates with specific characteristics
        title_candidates = []
        for element in first_page_elements[:10]:  # Check top 10 largest elements
            text = element["text"]
            
            # Title heuristics
            is_good_title = (
                element["font_size"] >= 12 and  # Reasonable size
                element["word_count"] <= 15 and  # Not too long
                element["word_count"] >= 1 and   # Not empty
                not element["has_numbers"] and   # Usually no numbers in titles
                not text.startswith("Page") and  # Not page numbers
                not text.startswith("Chapter") and
                len(text) > 2  # Minimum length
            )
            
            if is_good_title:
                title_candidates.append(element)
        
        # Return the best candidate or default
        if title_candidates:
            return title_candidates[0]["text"]
        
        # Fallback: largest text on first page
        return first_page_elements[0]["text"] if first_page_elements else "Untitled Document"
    
    def _extract_headings(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract headings using advanced font analysis and clustering."""
        if not elements:
            return []
        
        # Step 1: Identify body text characteristics
        body_stats = self._analyze_body_text(elements)
        
        # Step 2: Identify potential headings
        heading_candidates = self._identify_heading_candidates(elements, body_stats)
        
        # Step 3: Classify heading levels
        classified_headings = self._classify_heading_levels(heading_candidates)
        
        # Step 4: Filter and sort final outline
        final_outline = self._create_final_outline(classified_headings)
        
        return final_outline
    
    def _analyze_body_text(self, elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze body text characteristics to establish baseline."""
        # Find the most common font size (likely body text)
        font_sizes = [e["font_size"] for e in elements]
        size_counter = Counter(font_sizes)
        
        # Get the most common font size and its frequency
        most_common_size = size_counter.most_common(1)[0]
        body_size = most_common_size[0]
        body_frequency = most_common_size[1]
        
        # Calculate body text characteristics
        body_elements = [e for e in elements if e["font_size"] == body_size]
        
        avg_word_count = sum(e["word_count"] for e in body_elements) / len(body_elements) if body_elements else 0
        avg_char_count = sum(e["char_count"] for e in body_elements) / len(body_elements) if body_elements else 0
        
        return {
            "size": body_size,
            "frequency": body_frequency,
            "avg_word_count": avg_word_count,
            "avg_char_count": avg_char_count,
            "total_elements": len(elements)
        }
    
    def _identify_heading_candidates(self, elements: List[Dict[str, Any]], body_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential heading candidates using multiple criteria."""
        candidates = []
        body_size = body_stats["size"]
        
        for element in elements:
            text = element["text"]
            
            # Skip very short text
            if len(text) < 3:
                continue
            
            # Heading detection criteria
            is_larger_than_body = element["font_size"] > body_size
            is_significantly_larger = element["font_size"] >= body_size * 1.1
            is_bold = element["is_bold"]
            is_all_caps = element["is_all_caps"]
            reasonable_length = 3 <= element["word_count"] <= 20
            
            # Heading probability score
            score = 0
            if is_larger_than_body:
                score += 2
            if is_significantly_larger:
                score += 3
            if is_bold:
                score += 2
            if is_all_caps:
                score += 1
            if reasonable_length:
                score += 1
            if not element["has_numbers"]:
                score += 1
            
            # Must meet minimum criteria
            if score >= 3 and is_larger_than_body:
                element["heading_score"] = score
                candidates.append(element)
        
        return candidates
    
    def _classify_heading_levels(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Classify headings into H1, H2, H3 levels using clustering."""
        if not candidates:
            return []
        
        # Group by font size and style
        style_groups = defaultdict(list)
        for candidate in candidates:
            # Create style key based on font size and characteristics
            style_key = (
                candidate["font_size"],
                candidate["is_bold"],
                candidate["is_all_caps"]
            )
            style_groups[style_key].append(candidate)
        
        # Sort styles by font size (descending)
        sorted_styles = sorted(style_groups.keys(), key=lambda x: x[0], reverse=True)
        
        # Map to heading levels (max 3 levels)
        level_mapping = {}
        for i, style in enumerate(sorted_styles[:3]):
            level = f"H{i+1}"
            level_mapping[style] = level
        
        # Apply level mapping
        classified_headings = []
        for candidate in candidates:
            style_key = (
                candidate["font_size"],
                candidate["is_bold"],
                candidate["is_all_caps"]
            )
            
            if style_key in level_mapping:
                heading = {
                    "level": level_mapping[style_key],
                    "text": candidate["text"],
                    "page": candidate["page"]
                }
                classified_headings.append(heading)
        
        return classified_headings
    
    def _create_final_outline(self, classified_headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create final outline with proper sorting and filtering."""
        if not classified_headings:
            return []
        
        # Sort by page number and vertical position
        classified_headings.sort(key=lambda x: (x["page"], x.get("y_pos", 0)))
        
        # Remove duplicates and very similar headings
        final_outline = []
        seen_texts = set()
        
        for heading in classified_headings:
            # Normalize text for comparison
            normalized_text = heading["text"].strip().lower()
            
            if normalized_text not in seen_texts and len(normalized_text) > 2:
                seen_texts.add(normalized_text)
                final_outline.append(heading)
        
        return final_outline


def extract_outline(pdf_path: str) -> Dict[str, Any]:
    """
    Main function to extract document outline.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with 'title' and 'outline' keys
    """
    analyzer = DocumentAnalyzer()
    return analyzer.extract_outline(pdf_path) 