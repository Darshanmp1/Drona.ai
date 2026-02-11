"""
Context Manager Module
Retrieves and combines relevant past context for new queries.
Integrates conversation memory and user profile for personalized responses.
"""

from typing import Dict, List, Optional
from .conversation_memory import ConversationMemory
from .user_profile import UserProfile


class ContextManager:
    def __init__(self, memory: Optional[ConversationMemory] = None, 
                 profile: Optional[UserProfile] = None):
        self.memory = memory or ConversationMemory()
        self.profile = profile or UserProfile()
    
    def get_context_for_query(self, query: str, include_history: bool = True,
                              include_profile: bool = True) -> Dict:
        context = {
            'query': query,
            'history': None,
            'profile_summary': None,
            'personalization_hints': []
        }
        
        # Add conversation history if requested
        if include_history:
            recent_convs = self.memory.get_recent_conversations(count=3)
            if recent_convs:
                context['history'] = recent_convs
        
        # Add profile data if requested
        if include_profile:
            context['profile_summary'] = self.profile.get_profile_summary()
            
            # Generate personalization hints based on profile
            hints = self._generate_personalization_hints()
            context['personalization_hints'] = hints
        
        return context
    
    def _generate_personalization_hints(self) -> List[str]:
        hints = []
        profile_data = self.profile.get_full_profile()
        
        # Difficulty level hint
        difficulty = profile_data['learning_preferences']['difficulty_level']
        hints.append(f"Use {difficulty} level explanations")
        
        # Weak areas hint
        if profile_data['weak_areas']:
            weak_topics = ', '.join(profile_data['weak_areas'][:3])
            hints.append(f"User needs help with: {weak_topics}")
        
        # Target role hint
        target_role = profile_data['goals']['target_role']
        if target_role:
            hints.append(f"Target role: {target_role}")
        
        # Focus areas hint
        if profile_data['goals']['focus_areas']:
            focus = ', '.join(profile_data['goals']['focus_areas'][:3])
            hints.append(f"Focus on: {focus}")
        
        return hints
    
    def add_interaction(self, query: str, response: str, detected_topics: Optional[List[str]] = None):
        # Save to conversation memory
        metadata = {'topics': detected_topics} if detected_topics else {}
        self.memory.add_conversation(query, response, metadata)
        
        # Update user profile statistics
        self.profile.increment_questions_asked()
        
        # Add topics to profile if detected
        if detected_topics:
            for topic in detected_topics:
                self.profile.add_topic_covered(topic)
    
    def search_relevant_context(self, keyword: str, max_results: int = 5) -> List[Dict]:
        return self.memory.search_conversations(keyword, max_results)
    
    def get_user_preferences(self) -> Dict:
        profile_data = self.profile.get_full_profile()
        return {
            'difficulty_level': profile_data['learning_preferences']['difficulty_level'],
            'preferred_topics': profile_data['learning_preferences']['preferred_topics'],
            'learning_style': profile_data['learning_preferences']['learning_style']
        }
    
    def get_preparation_context(self) -> Dict:
        profile_data = self.profile.get_full_profile()
        return {
            'target_role': profile_data['goals']['target_role'],
            'target_companies': profile_data['goals']['target_companies'],
            'focus_areas': profile_data['goals']['focus_areas'],
            'weak_areas': profile_data['weak_areas'],
            'strong_areas': profile_data['strong_areas']
        }
    
    def format_context_summary(self) -> str:
        summary_parts = []
        
        # User info
        name = self.profile.get_name()
        summary_parts.append(f"User: {name}")
        
        # Profile summary
        profile_sum = self.profile.get_profile_summary()
        summary_parts.append(f"Difficulty Level: {profile_sum['difficulty_level']}")
        
        if profile_sum['target_role']:
            summary_parts.append(f"Target Role: {profile_sum['target_role']}")
        
        if profile_sum['weak_areas']:
            weak = ', '.join(profile_sum['weak_areas'][:3])
            summary_parts.append(f"Needs Help With: {weak}")
        
        # Conversation stats
        conv_summary = self.memory.get_conversation_summary()
        summary_parts.append(f"Total Questions: {conv_summary['total_conversations']}")
        
        return '\n'.join(summary_parts)
    
    def clear_all_data(self):
        self.memory.clear_memory()
        self.profile.reset_profile()
        print("✓ All context data cleared")
