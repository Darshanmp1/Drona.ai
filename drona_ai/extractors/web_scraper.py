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

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def extract_webpage(url: str, timeout: int = 10) -> Optional[str]:
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
        
        # Try to find main content area FIRST (before removing elements)
        # Look for common content containers (including Wikipedia-specific selectors)
        main_content = None
        
        # Try Wikipedia-specific content first
        if 'wikipedia.org' in url:
            main_content = soup.find('div', {'id': 'mw-content-text'}) or soup.find('div', {'id': 'bodyContent'})
        
        # If not Wikipedia or not found, try generic selectors
        if not main_content:
            content_tags = [
                'article', 
                'main',
                ['div', {'id': re.compile('content|main|article', re.I)}],
                ['div', {'class': re.compile('content|article|post|entry|main', re.I)}]
            ]
            
            for tag in content_tags:
                if isinstance(tag, list):
                    main_content = soup.find(tag[0], tag[1])
                else:
                    main_content = soup.find(tag)
                
                if main_content:
                    break
        
        # If still no main content found, use the entire body
        if not main_content:
            main_content = soup.find('body')
        
        if not main_content:
            print("Warning: Could not find content in webpage")
            return None
        
        # NOW remove unwanted elements FROM the main content area
        unwanted_tags = [
            'script', 'style', 'nav', 'footer', 'header',
            'aside', 'iframe', 'noscript', 'form'
        ]
        
        for tag in unwanted_tags:
            for element in main_content.find_all(tag):
                element.decompose()
        
        # Extract text from the cleaned content
        text = main_content.get_text(separator=' ', strip=True)
        
        # Clean up the text - remove extra whitespace
        text = ' '.join(text.split())
        
        # Basic validation - ensure minimum content length
        if len(text) < 100:
            print("Warning: Extracted text is too short (less than 100 characters)")
            return None
        
        print(f"✓ Successfully extracted {len(text)} characters from webpage")
        return text
        
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {timeout} seconds")
        return None
        
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the website")
        return None
        
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
        return None
        
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {timeout} seconds")
        print("The website is taking too long to respond. Try again or check your internet connection.")
        return None
    
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to {url}")
        print("Check your internet connection or verify the URL is correct.")
        return None
    
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {e.response.status_code} - {e.response.reason}")
        if e.response.status_code == 403:
            print("Access forbidden - website may be blocking automated requests")
        elif e.response.status_code == 404:
            print("Page not found - check if the URL is correct")
        return None
    
    except Exception as e:
        print(f"Error extracting webpage: {str(e)}")
        print(f"URL: {url}")
        return None


def extract_webpage_metadata(url: str) -> dict:
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
