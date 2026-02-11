# Text-to-speech for voice output

import pyttsx3
from typing import Optional


class TextToSpeech:
    # Converts text responses to spoken audio
    
    def __init__(self, rate: int = 175, volume: float = 0.9):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            self._set_voice()
            
            self.enabled = True
            
        except Exception as e:
            print(f"Warning: Could not initialize text-to-speech: {e}")
            self.enabled = False
    
    def _set_voice(self):
        try:
            voices = self.engine.getProperty('voices')
            
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    return
            
            for voice in voices:
                if 'english' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    return
            
            if voices:
                self.engine.setProperty('voice', voices[0].id)
                
        except Exception as e:
            pass
    
    def speak(self, text: str, block: bool = True) -> bool:
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
        if self.enabled:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        if self.enabled:
            # Clamp volume between 0 and 1
            volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', volume)
    
    def list_voices(self):
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
        if self.enabled:
            try:
                self.engine.stop()
            except:
                pass


# Convenience function for quick usage
def speak_text(text: str, rate: int = 175, volume: float = 0.9) -> bool:
    tts = TextToSpeech(rate=rate, volume=volume)
    return tts.speak(text)
