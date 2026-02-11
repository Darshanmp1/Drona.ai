# Unified file/URL handling

import os
from typing import Optional, Dict
from urllib.parse import urlparse

from .pdf_extractor import extract_pdf
from .image_ocr import extract_image
from .youtube_transcript import extract_youtube, extract_video_id
from .web_scraper import extract_webpage, is_valid_url


class FileHandler:
    # Detects input type and routes to the right extractor
    
    def __init__(self):
        self.pdf_extensions = ['.pdf']
        self.image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']
        
    def detect_input_type(self, input_source: str) -> str:
        if 'youtube.com' in input_source or 'youtu.be' in input_source:
            return 'youtube'
        
        # Check if it's a general web URL
        if is_valid_url(input_source):
            return 'webpage'
        
        # Check if it's a local file path
        if os.path.exists(input_source):
            file_ext = os.path.splitext(input_source)[1].lower()
            
            if file_ext in self.pdf_extensions:
                return 'pdf'
            elif file_ext in self.image_extensions:
                return 'image'
        
        return 'unknown'
    
    def extract(self, input_source: str) -> Optional[Dict]:
        # Detect input type
        input_type = self.detect_input_type(input_source)
        
        print(f"\n{'='*50}")
        print(f"Input Type Detected: {input_type.upper()}")
        print(f"Source: {input_source}")
        print(f"{'='*50}\n")
        
        extracted_text = None
        
        # Route to appropriate extractor based on type
        if input_type == 'pdf':
            extracted_text = extract_pdf(input_source)
            
        elif input_type == 'image':
            extracted_text = extract_image(input_source)
            
        elif input_type == 'youtube':
            extracted_text = extract_youtube(input_source)
            
        elif input_type == 'webpage':
            extracted_text = extract_webpage(input_source)
            
        else:
            print(f"Error: Unknown or unsupported input type")
            print(f"Supported types:")
            print(f"  - PDF files (.pdf)")
            print(f"  - Images (.png, .jpg, .jpeg, .bmp, .tiff, .gif)")
            print(f"  - YouTube URLs")
            print(f"  - Web URLs")
            return None
        
        # Check if extraction was successful
        if extracted_text is None or not extracted_text.strip():
            print(f"\n✗ Extraction failed or no content found")
            return None
        
        # Return result in standardized format
        result = {
            'text': extracted_text,
            'type': input_type,
            'source': input_source,
            'length': len(extracted_text)
        }
        
        print(f"\n{'='*50}")
        print(f"✓ Extraction Complete")
        print(f"Type: {input_type}")
        print(f"Characters extracted: {len(extracted_text)}")
        print(f"{'='*50}\n")
        
        return result
    
    def extract_batch(self, input_sources: list) -> list:
        results = []
        
        print(f"\nProcessing {len(input_sources)} sources...")
        
        for idx, source in enumerate(input_sources, start=1):
            print(f"\n[{idx}/{len(input_sources)}] Processing: {source}")
            
            result = self.extract(source)
            
            if result:
                results.append(result)
            else:
                print(f"  Skipped (extraction failed)")
        
        print(f"\n{'='*50}")
        print(f"Batch Processing Complete")
        print(f"Successful: {len(results)}/{len(input_sources)}")
        print(f"{'='*50}\n")
        
        return results
    
    def get_supported_types(self) -> Dict:
        return {
            'pdf': {
                'description': 'PDF documents',
                'extensions': self.pdf_extensions,
                'example': 'document.pdf'
            },
            'image': {
                'description': 'Image files with OCR',
                'extensions': self.image_extensions,
                'example': 'screenshot.png'
            },
            'youtube': {
                'description': 'YouTube video transcripts',
                'example': 'https://www.youtube.com/watch?v=VIDEO_ID'
            },
            'webpage': {
                'description': 'Web page articles',
                'example': 'https://example.com/article'
            }
        }


# Convenience function for quick extraction
def extract_content(input_source: str) -> Optional[Dict]:
    handler = FileHandler()
    return handler.extract(input_source)
