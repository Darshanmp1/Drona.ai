"""
Conversation Memory Module
Stores and retrieves past user queries and AI responses.
Uses simple JSON file storage for easy access and modification.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class ConversationMemory:
    """
    Manages conversation history between user and AI.
    Stores queries, responses, and timestamps in JSON format.
    """
    
    def __init__(self, memory_file: str = "conversation_history.json"):
        """
        Initialize conversation memory.
        
        Args:
            memory_file: Path to JSON file for storing conversations
        """
        # Store memory file in a data directory
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.memory_file = os.path.join(self.data_dir, memory_file)
        
        # Load existing conversations or create new storage
        self.conversations = self._load_conversations()
    
    def _load_conversations(self) -> List[Dict]:
        """
        Load conversation history from JSON file.
        
        Returns:
            List of conversation dictionaries
        """
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Warning: Could not load conversation history: {e}")
            return []
    
    def _save_conversations(self):
        """Save conversation history to JSON file."""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save conversation history: {e}")
    
    def add_conversation(self, query: str, response: str, metadata: Optional[Dict] = None):
        """
        Add a new conversation exchange to memory.
        
        Args:
            query: User's question or input
            response: AI's response
            metadata: Optional additional information (tags, topics, etc.)
        """
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'metadata': metadata or {}
        }
        
        self.conversations.append(conversation)
        self._save_conversations()
    
    def get_recent_conversations(self, count: int = 5) -> List[Dict]:
        """
        Get the most recent conversations.
        
        Args:
            count: Number of recent conversations to retrieve
            
        Returns:
            List of recent conversation dictionaries
        """
        return self.conversations[-count:] if self.conversations else []
    
    def search_conversations(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        Search conversations containing a specific keyword.
        
        Args:
            keyword: Keyword to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of matching conversations
        """
        keyword_lower = keyword.lower()
        matches = []
        
        # Search from most recent to oldest
        for conv in reversed(self.conversations):
            if (keyword_lower in conv['query'].lower() or 
                keyword_lower in conv['response'].lower()):
                matches.append(conv)
                
                if len(matches) >= max_results:
                    break
        
        return matches
    
    def get_conversation_count(self) -> int:
        """
        Get total number of stored conversations.
        
        Returns:
            Count of conversations
        """
        return len(self.conversations)
    
    def get_conversation_summary(self) -> Dict:
        """
        Get summary statistics about conversations.
        
        Returns:
            Dictionary with conversation statistics
        """
        if not self.conversations:
            return {
                'total_conversations': 0,
                'first_conversation': None,
                'last_conversation': None
            }
        
        return {
            'total_conversations': len(self.conversations),
            'first_conversation': self.conversations[0]['timestamp'],
            'last_conversation': self.conversations[-1]['timestamp']
        }
    
    def clear_memory(self):
        """Clear all stored conversations (use with caution!)."""
        self.conversations = []
        self._save_conversations()
        print("✓ Conversation memory cleared")
    
    def export_conversations(self, output_file: str):
        """
        Export conversations to a separate file.
        
        Args:
            output_file: Path to export file
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, indent=2, ensure_ascii=False)
            print(f"✓ Conversations exported to {output_file}")
        except Exception as e:
            print(f"Error exporting conversations: {e}")
    
    def get_contextual_history(self, current_query: str, max_context: int = 3) -> str:
        """
        Get relevant conversation history as context for new query.
        
        Args:
            current_query: The current user query
            max_context: Maximum number of past conversations to include
            
        Returns:
            Formatted string with relevant past context
        """
        if not self.conversations:
            return ""
        
        # Get recent conversations
        recent = self.get_recent_conversations(max_context)
        
        if not recent:
            return ""
        
        # Format as context string
        context_parts = []
        for conv in recent:
            context_parts.append(f"Previous Q: {conv['query']}")
            context_parts.append(f"Previous A: {conv['response'][:200]}...")  # Truncate long responses
        
        return "\n".join(context_parts)
