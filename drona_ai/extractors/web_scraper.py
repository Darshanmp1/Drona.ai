"""
Web Scraper Module
Extracts clean article text from web URLs using BeautifulSoup
"""

import re
from typing import Optional
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def is_valid_url(url: str) -> bool:
    """
    Check if a string is a valid URL.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def extract_webpage(url: str, timeout: int = 10) -> Optional[str]:
    """
    Extract main text content from a webpage.
    Removes scripts, styles, navigation, ads, and other non-content elements.
    
    Args:
        url: Website URL to scrape
        timeout: Request timeout in seconds (default: 10)
        
    Returns:
        Extracted clean text, or None if extraction fails
    """
    try:
        # Validate URL
        if not is_valid_url(url):
            print(f"Error: Invalid URL: {url}")
            return None
        
        print(f"Fetching webpage: {url}")
        
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Send GET request
        response = requests.get(url, headers=headers, timeout=timeout)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements (scripts, styles, navigation, etc.)
        unwanted_tags = [
            'script', 'style', 'nav', 'footer', 'header',
            'aside', 'iframe', 'noscript', 'form'
        ]
        
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Also remove elements with common ad/navigation class names
        unwanted_classes = [
            'advertisement', 'ad', 'ads', 'sidebar', 'menu',
            'navigation', 'cookie', 'popup', 'modal'
        ]
        
        for class_name in unwanted_classes:
            for element in soup.find_all(class_=re.compile(class_name, re.I)):
                element.decompose()
        
        # Try to find main content area
        # Look for common content containers
        main_content = None
        content_tags = ['article', 'main', ['div', {'class': re.compile('content|article|post|entry', re.I)}]]
        
        for tag in content_tags:
            if isinstance(tag, list):
                main_content = soup.find(tag[0], tag[1])
            else:
                main_content = soup.find(tag)
            
            if main_content:
                break
        
        # If no main content found, use the entire body
        if not main_content:
            main_content = soup.find('body')
        
        if not main_content:
            print("Warning: Could not find content in webpage")
            return None
        
        # Extract text from the content
        text = main_content.get_text(separator=' ', strip=True)
        
        # Clean up the text
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove very short lines (likely navigation/footer remnants)
        lines = text.split('.')
        meaningful_lines = [line.strip() for line in lines if len(line.strip()) > 20]
        cleaned_text = '. '.join(meaningful_lines)
        
        if not cleaned_text.strip():
            print("Warning: No meaningful text extracted from webpage")
            return None
        
        print(f"✓ Successfully extracted {len(cleaned_text)} characters from webpage")
        return cleaned_text
        
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {timeout} seconds")
        return None
        
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the website")
        return None
        
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
        return None
        
    except Exception as e:
        print(f"Error extracting webpage content: {str(e)}")
        return None


def extract_webpage_metadata(url: str) -> dict:
    """
    Extract metadata from webpage (title, description, etc.).
    
    Args:
        url: Website URL
        
    Returns:
        Dictionary containing metadata
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract metadata
        metadata = {
            'title': '',
            'description': '',
            'url': url
        }
        
        # Get title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()
        
        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            metadata['description'] = meta_desc['content'].strip()
        
        return metadata
        
    except Exception as e:
        print(f"Error extracting metadata: {str(e)}")
        return {}
