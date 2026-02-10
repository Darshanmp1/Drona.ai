"""
Text to Speech Module
Converts text responses into speech using pyttsx3
"""

import pyttsx3
from typing import Optional


class TextToSpeech:
    """
    Class to handle text-to-speech conversion.
    Uses pyttsx3 which works offline (no internet required).
    """
    
    def __init__(self, rate: int = 175, volume: float = 0.9):
        """
        Initialize text-to-speech engine.
        
        Args:
            rate: Speech rate (words per minute). Default 175, normal is ~200
            volume: Volume level (0.0 to 1.0). Default 0.9
        """
        try:
            # Initialize pyttsx3 engine
            self.engine = pyttsx3.init()
            
            # Set speech rate (speed)
            # Lower = slower, Higher = faster
            self.engine.setProperty('rate', rate)
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', volume)
            
            # Try to set a good voice (prefer female voice if available)
            self._set_voice()
            
            self.enabled = True
            
        except Exception as e:
            print(f"Warning: Could not initialize text-to-speech: {e}")
            self.enabled = False
    
    def _set_voice(self):
        """Set a pleasant voice for the assistant."""
        try:
            voices = self.engine.getProperty('voices')
            
            # Try to find a female voice (usually sounds better for assistants)
            # On Windows, this might be Microsoft Zira
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    return
            
            # If no female voice, try to find any English voice
            for voice in voices:
                if 'english' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    return
            
            # Otherwise use default (first voice)
            if voices:
                self.engine.setProperty('voice', voices[0].id)
                
        except Exception as e:
            # If voice setting fails, just use default
            pass
    
    def speak(self, text: str, block: bool = True) -> bool:
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to speak
            block: If True, wait until speech finishes. If False, return immediately
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            print("Text-to-speech is not available")
            return False
        
        if not text or not text.strip():
            return False
        
        try:
            print(f"\n🔊 Drona: {text}\n")
            
            # Speak the text
            self.engine.say(text)
            
            if block:
                # Wait until speech is finished
                self.engine.runAndWait()
            else:
                # Start speaking but don't wait
                self.engine.startLoop(False)
                self.engine.iterate()
                self.engine.endLoop()
            
            return True
            
        except Exception as e:
            print(f"Error during speech: {str(e)}")
            return False
    
    def set_rate(self, rate: int):
        """
        Change speech rate.
        
        Args:
            rate: Words per minute (typical range: 100-300)
        """
        if self.enabled:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """
        Change volume level.
        
        Args:
            volume: 0.0 (mute) to 1.0 (maximum)
        """
        if self.enabled:
            # Clamp volume between 0 and 1
            volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', volume)
    
    def list_voices(self):
        """Print all available voices on the system."""
        if not self.enabled:
            print("Text-to-speech is not available")
            return
        
        try:
            voices = self.engine.getProperty('voices')
            print("\n📢 Available voices:")
            for i, voice in enumerate(voices):
                print(f"  {i}. {voice.name} - {voice.id}")
            print()
        except Exception as e:
            print(f"Error listing voices: {e}")
    
    def set_voice_by_index(self, index: int):
        """
        Set voice by index from available voices list.
        
        Args:
            index: Voice index (use list_voices() to see available voices)
        """
        if not self.enabled:
            return
        
        try:
            voices = self.engine.getProperty('voices')
            if 0 <= index < len(voices):
                self.engine.setProperty('voice', voices[index].id)
                print(f"Voice changed to: {voices[index].name}")
            else:
                print(f"Invalid voice index. Use 0-{len(voices)-1}")
        except Exception as e:
            print(f"Error setting voice: {e}")
    
    def stop(self):
        """Stop current speech."""
        if self.enabled:
            try:
                self.engine.stop()
            except:
                pass


# Convenience function for quick usage
def speak_text(text: str, rate: int = 175, volume: float = 0.9) -> bool:
    """
    Quick function to speak text.
    
    Args:
        text: Text to speak
        rate: Speech rate (words per minute)
        volume: Volume level (0.0 to 1.0)
        
    Returns:
        True if successful, False otherwise
    """
    tts = TextToSpeech(rate=rate, volume=volume)
    return tts.speak(text)
