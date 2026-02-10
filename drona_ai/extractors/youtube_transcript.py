"""
YouTube Transcript Extractor
Extracts subtitles/transcripts from YouTube videos
"""

import re
from typing import Optional, List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from various YouTube URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    
    Args:
        url: YouTube video URL
        
    Returns:
        Video ID string, or None if invalid URL
    """
    # Pattern to match different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If no pattern matched, check if input is already a video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    
    return None


def extract_youtube(url: str, languages: List[str] = ['en']) -> Optional[str]:
    """
    Extract transcript/subtitles from a YouTube video.
    
    Args:
        url: YouTube video URL or video ID
        languages: List of preferred language codes (default: ['en'])
        
    Returns:
        Full transcript as a string, or None if extraction fails
    """
    try:
        # Extract video ID from URL
        video_id = extract_video_id(url)
        
        if not video_id:
            print(f"Error: Invalid YouTube URL or video ID: {url}")
            return None
        
        print(f"Fetching transcript for video: {video_id}")
        
        # Fetch transcript using YouTube Transcript API
        # This tries to get transcript in specified languages
        transcript_list = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=languages
        )
        
        # Extract just the text from each transcript entry
        # Each entry has format: {'text': '...', 'start': 0.0, 'duration': 2.5}
        text_chunks = [entry['text'] for entry in transcript_list]
        
        # Join all text chunks into one string
        full_transcript = ' '.join(text_chunks)
        
        # Clean up extra spaces
        full_transcript = ' '.join(full_transcript.split())
        
        if not full_transcript.strip():
            print("Warning: Transcript is empty")
            return None
        
        print(f"✓ Successfully extracted transcript ({len(full_transcript)} characters)")
        return full_transcript
        
    except TranscriptsDisabled:
        print("Error: Transcripts are disabled for this video")
        return None
        
    except NoTranscriptFound:
        print(f"Error: No transcript found in languages: {languages}")
        print("Tip: Try different language codes or check if video has captions")
        return None
        
    except Exception as e:
        print(f"Error extracting YouTube transcript: {str(e)}")
        return None


def extract_youtube_with_timestamps(url: str, languages: List[str] = ['en']) -> Optional[List[Dict]]:
    """
    Extract transcript with timestamps preserved.
    
    Args:
        url: YouTube video URL or video ID
        languages: List of preferred language codes
        
    Returns:
        List of transcript entries with text, start time, and duration
    """
    try:
        video_id = extract_video_id(url)
        
        if not video_id:
            print(f"Error: Invalid YouTube URL: {url}")
            return None
        
        # Get full transcript with timestamps
        transcript_list = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=languages
        )
        
        return transcript_list
        
    except Exception as e:
        print(f"Error extracting timestamped transcript: {str(e)}")
        return None


def list_available_transcripts(url: str) -> Optional[List[str]]:
    """
    List all available transcript languages for a video.
    
    Args:
        url: YouTube video URL or video ID
        
    Returns:
        List of available language codes
    """
    try:
        video_id = extract_video_id(url)
        
        if not video_id:
            return None
        
        # Get all available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        available_languages = []
        for transcript in transcript_list:
            available_languages.append(transcript.language_code)
        
        return available_languages
        
    except Exception as e:
        print(f"Error listing transcripts: {str(e)}")
        return None
