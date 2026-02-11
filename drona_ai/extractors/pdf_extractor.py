# PDF text extraction

import os
from typing import Optional
from PyPDF2 import PdfReader


def extract_pdf(pdf_path: str) -> Optional[str]:
    try:
        if not os.path.exists(pdf_path):
            print(f"Error: File not found at {pdf_path}")
            return None
        
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
