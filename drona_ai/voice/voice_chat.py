# Voice interaction combining speech input/output

from typing import Optional
from .speech_to_text import SpeechToText
from .text_to_speech import TextToSpeech


class VoiceChat:
    # Voice-based interaction system
    
    def __init__(self, retriever, language: str = "en-US", speech_rate: int = 175):
        self.retriever = retriever
        self.stt = SpeechToText(language=language)
        
        # Initialize text-to-speech
        self.tts = TextToSpeech(rate=speech_rate, volume=0.9)
        
        # Check if components are working
        self.voice_enabled = self.tts.enabled
        
        if not self.voice_enabled:
            print("⚠️  Warning: Text-to-speech not available. Responses will be text-only.")
    
    def greet(self):
        greeting = "Hello! I am Drona, your voice assistant. How can I help you today?"
        print("\n" + "=" * 60)
        print("🎤 Voice Chat Mode Active")
        print("=" * 60)
        
        if self.voice_enabled:
            self.tts.speak(greeting)
        else:
            print(f"\n🔊 Drona: {greeting}\n")
    
    def listen_and_respond(self, top_k: int = 3, timeout: int = 5) -> Optional[str]:
        # Step 1: Listen for user speech
        user_query = self.stt.listen(timeout=timeout)
        
        if not user_query:
            # Listening failed or no speech detected
            return None
        
        # Step 2: Check for exit commands
        exit_commands = ['exit', 'quit', 'goodbye', 'bye', 'stop']
        if user_query.lower() in exit_commands:
            farewell = "Goodbye! Happy learning!"
            if self.voice_enabled:
                self.tts.speak(farewell)
            else:
                print(f"\n🔊 Drona: {farewell}\n")
            return "EXIT"
        
        # Step 3: Process query through RAG retriever
        try:
            print("\n   🤔 Thinking...")
            response = self.retriever.generate_response(user_query, top_k=top_k)
            
            # Step 4: Speak the response
            if self.voice_enabled:
                self.tts.speak(response)
            else:
                print(f"\n🔊 Drona: {response}\n")
            
            return response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            if self.voice_enabled:
                self.tts.speak("Sorry, I encountered an error processing your query.")
            else:
                print(f"\n🔊 Drona: {error_msg}\n")
            return None
    
    def start_conversation(self, max_turns: Optional[int] = None):
        # Greet the user
        self.greet()
        
        print("\n💡 Tips:")
        print("  • Speak clearly into your microphone")
        print("  • Say 'exit', 'quit', or 'goodbye' to end conversation")
        print("  • Press Ctrl+C to force quit")
        print("\n" + "=" * 60 + "\n")
        
        # Test microphone
        if not self.stt.test_microphone():
            print("\n❌ Cannot access microphone. Please check your settings.")
            return
        
        print()
        
        # Conversation loop
        turn_count = 0
        while True:
            # Check if max turns reached
            if max_turns and turn_count >= max_turns:
                farewell = f"We've reached the maximum of {max_turns} questions. Goodbye!"
                if self.voice_enabled:
                    self.tts.speak(farewell)
                else:
                    print(f"\n🔊 Drona: {farewell}\n")
                break
            
            try:
                # Listen and respond
                response = self.listen_and_respond()
                
                # Check for exit
                if response == "EXIT":
                    break
                
                # Count successful turns
                if response:
                    turn_count += 1
                
                print("-" * 60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for chatting.\n")
                break
                
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}\n")
                break
    
    def quick_query(self, question: str, speak_response: bool = True) -> str:
        try:
            print(f"\n📝 Question: {question}")
            
            # Get response from RAG
            response = self.retriever.generate_response(question, top_k=3)
            
            # Speak if requested
            if speak_response and self.voice_enabled:
                self.tts.speak(response)
            else:
                print(f"\n🔊 Drona: {response}\n")
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            print(f"\n❌ {error_msg}\n")
            return error_msg
    
    def set_speech_rate(self, rate: int):
        if self.voice_enabled:
            self.tts.set_rate(rate)
            print(f"Speech rate set to {rate} words per minute")
    
    def set_volume(self, volume: float):
        if self.voice_enabled:
            self.tts.set_volume(volume)
            print(f"Volume set to {volume}")
    
    def test_voice_output(self):
        test_message = "This is a test of the voice output system. Can you hear me clearly?"
        
        if self.voice_enabled:
            print("\n🔊 Testing voice output...")
            self.tts.speak(test_message)
        else:
            print("\n❌ Voice output not available")
