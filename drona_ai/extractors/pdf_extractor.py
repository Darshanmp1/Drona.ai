"""
PDF Extractor Module
Extracts text content from PDF files using PyPDF2
"""

import os
from typing import Optional
from PyPDF2 import PdfReader


def extract_pdf(pdf_path: str) -> Optional[str]:
    """
    Extract all text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string, or None if extraction fails
    """
    try:
        # Check if file exists
        if not os.path.exists(pdf_path):
            print(f"Error: File not found at {pdf_path}")
            return None
        
        # Check if file is actually a PDF
        if not pdf_path.lower().endswith('.pdf'):
            print(f"Error: File is not a PDF: {pdf_path}")
            return None
        
        # Initialize PDF reader
        reader = PdfReader(pdf_path)
        
        # Extract text from all pages
        text_content = []
        total_pages = len(reader.pages)
        
        print(f"Processing PDF: {total_pages} pages found")
        
        for page_num, page in enumerate(reader.pages, start=1):
            # Extract text from current page
            page_text = page.extract_text()
            
            if page_text.strip():  # Only add if page has content
                text_content.append(page_text)
                print(f"  - Page {page_num}/{total_pages} extracted")
        
        # Combine all pages with separator
        full_text = "\n\n".join(text_content)
        
        if not full_text.strip():
            print("Warning: No text content found in PDF")
            return None
        
        print(f"✓ Successfully extracted {len(full_text)} characters from PDF")
        return full_text
        
    except Exception as e:
        print(f"Error extracting PDF: {str(e)}")
        return None


def extract_pdf_metadata(pdf_path: str) -> dict:
    """
    Extract metadata from PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing metadata (title, author, pages, etc.)
    """
    try:
        reader = PdfReader(pdf_path)
        metadata = {
            'pages': len(reader.pages),
            'title': reader.metadata.get('/Title', 'Unknown'),
            'author': reader.metadata.get('/Author', 'Unknown'),
        }
        return metadata
    except Exception as e:
        print(f"Error extracting PDF metadata: {str(e)}")
        return {}
