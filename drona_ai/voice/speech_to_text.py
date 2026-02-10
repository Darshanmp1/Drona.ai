"""
Speech to Text Module
Captures microphone input and converts speech to text using SpeechRecognition
"""

import speech_recognition as sr
from typing import Optional


class SpeechToText:
    """
    Class to handle speech recognition from microphone.
    Uses Google's speech recognition API (requires internet connection).
    """
    
    def __init__(self, language: str = "en-US"):
        """
        Initialize speech recognizer.
        
        Args:
            language: Language code for recognition (default: "en-US")
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        
        # Adjust these for better recognition
        # Energy threshold: minimum audio energy to consider for recording
        self.recognizer.energy_threshold = 4000
        
        # Dynamic energy adjustment helps with different environments
        self.recognizer.dynamic_energy_threshold = True
        
        # How long to wait for phrase to start (in seconds)
        self.recognizer.pause_threshold = 0.8
        
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen to microphone and convert speech to text.
        
        Args:
            timeout: How long to wait for speech to start (seconds)
            phrase_time_limit: Maximum time for a phrase (seconds)
            
        Returns:
            Recognized text as string, or None if recognition fails
        """
        try:
            # Use microphone as audio source
            with sr.Microphone() as source:
                print("\n🎤 Listening... (speak now)")
                
                # Adjust for ambient noise (helps filter background noise)
                # This calibrates the energy threshold
                print("   Calibrating for background noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("   Ready! Speak your question.")
                
                # Listen for audio input
                # timeout: wait this long for speech to start
                # phrase_time_limit: maximum length of phrase
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("   Processing speech...")
                
                # Recognize speech using Google Speech Recognition
                # This sends audio to Google's servers for processing
                text = self.recognizer.recognize_google(
                    audio,
                    language=self.language
                )
                
                print(f"   ✓ You said: '{text}'")
                return text
                
        except sr.WaitTimeoutError:
            print("   ⚠️  No speech detected. Please try again.")
            return None
            
        except sr.UnknownValueError:
            print("   ⚠️  Could not understand audio. Please speak clearly.")
            return None
            
        except sr.RequestError as e:
            print(f"   ❌ Error with speech recognition service: {e}")
            print("   (Check your internet connection)")
            return None
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None
    
    def test_microphone(self) -> bool:
        """
        Test if microphone is available and working.
        
        Returns:
            True if microphone is accessible, False otherwise
        """
        try:
            # Check if we can access microphone
            with sr.Microphone() as source:
                print("✓ Microphone is accessible")
                
                # Show available microphones
                mic_list = sr.Microphone.list_microphone_names()
                print(f"  Available microphones: {len(mic_list)}")
                
                return True
                
        except Exception as e:
            print(f"✗ Microphone error: {str(e)}")
            return False
    
    def listen_with_wake_word(self, wake_word: str = "drona") -> Optional[str]:
        """
        Listen for a wake word, then capture the actual query.
        
        Args:
            wake_word: Word to activate listening (default: "drona")
            
        Returns:
            Recognized query text, or None if fails
        """
        print(f"\n🎤 Say '{wake_word}' to start, then ask your question...")
        
        try:
            with sr.Microphone() as source:
                # Wait for wake word
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for activation
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio, language=self.language)
                
                # Check if wake word was said
                if wake_word.lower() in text.lower():
                    print(f"   ✓ Activated! Listening for your question...")
                    
                    # Now listen for actual query
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    query = self.recognizer.recognize_google(audio, language=self.language)
                    
                    print(f"   ✓ Query: '{query}'")
                    return query
                else:
                    print(f"   Wake word '{wake_word}' not detected.")
                    return None
                    
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None


# Convenience function for quick usage
def listen_for_speech(timeout: int = 5, language: str = "en-US") -> Optional[str]:
    """
    Quick function to listen for speech and return text.
    
    Args:
        timeout: Seconds to wait for speech to start
        language: Language code for recognition
        
    Returns:
        Recognized text or None
    """
    stt = SpeechToText(language=language)
    return stt.listen(timeout=timeout)
