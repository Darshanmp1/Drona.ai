# Speech recognition for voice input

import speech_recognition as sr
from typing import Optional


class SpeechToText:
    # Handles microphone input and converts to text
    
    def __init__(self, language: str = "en-US"):
        self.recognizer = sr.Recognizer()
        self.language = language
        
        # Adjust these for better recognition
        # Energy threshold: minimum audio energy to consider for recording
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        try:
            # Use microphone as audio source
            with sr.Microphone() as source:
                print("\n🎤 Listening... (speak now)")
                print("   Calibrating for background noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("   Ready! Speak your question.")
                
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("   Processing speech...")
                
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
        try:
            # Check if we can access microphone
            with sr.Microphone() as source:
                print("✓ Microphone is accessible")
                mic_list = sr.Microphone.list_microphone_names()
                print(f"  Available microphones: {len(mic_list)}")
                
                return True
                
        except Exception as e:
            print(f"✗ Microphone error: {str(e)}")
            return False
    
    def listen_with_wake_word(self, wake_word: str = "drona") -> Optional[str]:
        print(f"\n🎤 Say '{wake_word}' to start, then ask your question...")
        
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio, language=self.language)
                
                if wake_word.lower() in text.lower():
                    print(f"   ✓ Activated! Listening for your question...")
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


def listen_for_speech(timeout: int = 5, language: str = "en-US") -> Optional[str]:
    stt = SpeechToText(language=language)
    return stt.listen(timeout=timeout)
