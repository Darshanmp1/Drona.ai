# YouTube subtitle/transcript extraction

import re
import time
from typing import Optional, List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def extract_video_id(url: str) -> Optional[str]:
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',  # YouTube Shorts
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    
    return None


def extract_youtube(url: str, languages: List[str] = ['en']) -> Optional[str]:
    try:
        video_id = extract_video_id(url)
        
        if not video_id:
            print(f"Error: Invalid YouTube URL or video ID: {url}")
            return None
        
        print(f"Fetching transcript for video: {video_id}")
        
        # Fetch transcript using YouTube Transcript API
        # Try multiple approaches to handle rate limiting
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=languages
            )
        except Exception as e:
            error_str = str(e)
            # Check for rate limiting
            if '429' in error_str or 'Too Many Requests' in error_str:
                print("Waiting 3 seconds due to rate limit...")
                time.sleep(3)
                # Retry once
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id, 
                    languages=languages
                )
            else:
                # Not rate limiting, re-raise
                raise
        
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
        
        print(f"Successfully extracted transcript ({len(full_transcript)} characters)")
        return full_transcript
        
    except TranscriptsDisabled:
        print("Error: Transcripts are disabled for this video")
        return None
        
    except NoTranscriptFound:
        print(f"Error: No transcript found in languages: {languages}")
        print("Tip: Try different language codes or check if video has captions")
        return None
        
    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'Too Many Requests' in error_msg:
            print("YouTube rate limit exceeded. Please wait a few minutes and try again.")
            print("Tip: YouTube restricts transcript requests to prevent abuse.")
        else:
            print(f"Error extracting YouTube transcript: {error_msg[:200]}")
        return None


def extract_youtube_with_timestamps(url: str, languages: List[str] = ['en']) -> Optional[List[Dict]]:
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
        print(f"Error extracting timestamped transcript: {str(e)[:200]}")
        return None


def list_available_transcripts(url: str) -> Optional[List[str]]:
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
        print(f"Error listing transcripts: {str(e)[:200]}")
        return None
