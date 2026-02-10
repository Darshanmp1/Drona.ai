"""
Image OCR Module
Extracts text from images using Tesseract OCR via pytesseract
"""

import os
from typing import Optional
from PIL import Image
import pytesseract


def extract_image(image_path: str) -> Optional[str]:
    """
    Extract text from an image using OCR (Optical Character Recognition).
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted text as a string, or None if extraction fails
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at {image_path}")
            return None
        
        # Supported image formats
        supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']
        file_ext = os.path.splitext(image_path)[1].lower()
        
        if file_ext not in supported_formats:
            print(f"Error: Unsupported image format: {file_ext}")
            print(f"Supported formats: {', '.join(supported_formats)}")
            return None
        
        print(f"Processing image: {os.path.basename(image_path)}")
        
        # Open image using PIL
        image = Image.open(image_path)
        
        # Convert image to RGB if needed (handles different color modes)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Perform OCR using pytesseract
        # Note: Tesseract must be installed on your system
        extracted_text = pytesseract.image_to_string(image)
        
        if not extracted_text.strip():
            print("Warning: No text detected in image")
            return None
        
        # Clean up the extracted text
        cleaned_text = extracted_text.strip()
        
        print(f"✓ Successfully extracted {len(cleaned_text)} characters from image")
        return cleaned_text
        
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract OCR is not installed or not in PATH")
        print("Please install Tesseract OCR:")
        print("  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("  - Linux: sudo apt-get install tesseract-ocr")
        print("  - Mac: brew install tesseract")
        return None
        
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        return None


def extract_image_with_config(image_path: str, lang='eng', config='') -> Optional[str]:
    """
    Extract text from image with custom Tesseract configuration.
    
    Args:
        image_path: Path to the image file
        lang: Language code for OCR (default: 'eng')
        config: Custom Tesseract configuration string
        
    Returns:
        Extracted text as a string, or None if extraction fails
    """
    try:
        image = Image.open(image_path)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Use custom configuration if provided
        extracted_text = pytesseract.image_to_string(
            image, 
            lang=lang, 
            config=config
        )
        
        return extracted_text.strip() if extracted_text.strip() else None
        
    except Exception as e:
        print(f"Error extracting text with config: {str(e)}")
        return None
