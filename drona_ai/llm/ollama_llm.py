# Ollama integration for local LLM (LLaMA 3.2)

import requests
import json
from typing import Optional, List, Dict


class OllamaLLM:
    # Connects to Ollama for LLaMA model inference
    
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.chat_url = f"{base_url}/api/chat"
        
    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
    
    def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        # Build the full prompt with context
        if context:
            full_prompt = f"""You are a helpful AI assistant. Use the provided context information to answer the user's question accurately.

CONTEXT FROM DOCUMENTS:
{context}

USER QUESTION: {prompt}

INSTRUCTIONS:
- Answer ONLY using information from the context above
- If the context contains relevant information, provide a detailed answer
- Be specific and reference the source document
- If the context lacks information, clearly state "The uploaded documents don't contain information about this"

ANSWER:"""
        else:
            full_prompt = prompt
        
        # Prepare request
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": stream,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                # Parse response
                if stream:
                    return self._handle_stream(response)
                else:
                    data = response.json()
                    return data.get('response', '').strip()
            else:
                return f"Error: Ollama returned status {response.status_code}"
        
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Ollama might be processing a large request."
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure it's running (ollama serve)."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """
        Chat-style interaction with conversation history.
        
        Args:
            messages: List of {"role": "user"/"assistant", "content": "..."}
            max_tokens: Maximum response length
            temperature: Creativity
        
        Returns:
            Generated response
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }
        
        try:
            response = requests.post(
                self.chat_url,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('message', {}).get('content', '').strip()
            else:
                return f"Error: Ollama returned status {response.status_code}"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _handle_stream(self, response):
        full_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                full_response += data.get('response', '')
                if data.get('done', False):
                    break
        return full_response.strip()


def get_ollama_status() -> Dict:
    llm = OllamaLLM()
    
    status = {
        "installed": llm.is_available(),
        "models": llm.list_models() if llm.is_available() else [],
        "url": llm.base_url
    }
    
    return status


# Installation instructions
OLLAMA_SETUP = """
🚀 To use Llama 3.2 with Drona AI:

1. Install Ollama:
   - Windows: Download from https://ollama.ai/download
   - Run the installer

2. Start Ollama:
   - Open terminal/PowerShell
   - Run: ollama serve

3. Download Llama 3.2:
   - Open another terminal
   - Run: ollama pull llama3.2

4. Verify installation:
   - Run: ollama list
   - You should see llama3.2 in the list

5. Test it:
   - Run: ollama run llama3.2
   - Type a question and press Enter

Once Ollama is running, refresh this app and it will automatically use Llama 3.2!

📝 Note: Llama 3.2 runs entirely on your PC - no internet required, completely private!
"""
