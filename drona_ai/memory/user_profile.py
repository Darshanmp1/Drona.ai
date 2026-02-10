"""
User Profile Module
Stores user learning preferences, goals, and personalization data.
Uses JSON for simple local storage.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class UserProfile:
    """
    Manages user profile data including learning preferences,
    goals, weak areas, and personalization settings.
    """
    
    def __init__(self, profile_file: str = "user_profile.json"):
        """
        Initialize user profile.
        
        Args:
            profile_file: Path to JSON file for storing profile
        """
        # Store profile in data directory
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.profile_file = os.path.join(self.data_dir, profile_file)
        
        # Load existing profile or create default
        self.profile = self._load_profile()
    
    def _load_profile(self) -> Dict:
        """
        Load user profile from JSON file.
        
        Returns:
            Profile dictionary
        """
        try:
            if os.path.exists(self.profile_file):
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._create_default_profile()
        except Exception as e:
            print(f"Warning: Could not load profile: {e}")
            return self._create_default_profile()
    
    def _create_default_profile(self) -> Dict:
        """
        Create a default user profile structure.
        
        Returns:
            Default profile dictionary
        """
        return {
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'name': 'User',
            'learning_preferences': {
                'preferred_topics': [],  # Topics user is interested in
                'difficulty_level': 'intermediate',  # beginner, intermediate, advanced
                'learning_style': 'balanced',  # visual, auditory, reading, kinesthetic, balanced
            },
            'goals': {
                'target_role': '',  # e.g., "Software Engineer", "Data Scientist"
                'target_companies': [],  # List of target companies
                'preparation_deadline': '',  # ISO format date
                'focus_areas': []  # e.g., ["algorithms", "system design"]
            },
            'weak_areas': [],  # Topics user struggles with
            'strong_areas': [],  # Topics user is good at
            'study_stats': {
                'total_questions_asked': 0,
                'topics_covered': [],
                'last_active': datetime.now().isoformat()
            }
        }
    
    def _save_profile(self):
        """Save profile to JSON file."""
        try:
            self.profile['updated_at'] = datetime.now().isoformat()
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save profile: {e}")
    
    def set_name(self, name: str):
        """Set or update user's name."""
        self.profile['name'] = name
        self._save_profile()
    
    def get_name(self) -> str:
        """Get user's name."""
        return self.profile.get('name', 'User')
    
    def add_preferred_topic(self, topic: str):
        """
        Add a topic to user's preferred topics.
        
        Args:
            topic: Topic name (e.g., "Machine Learning", "Python")
        """
        if topic not in self.profile['learning_preferences']['preferred_topics']:
            self.profile['learning_preferences']['preferred_topics'].append(topic)
            self._save_profile()
    
    def set_difficulty_level(self, level: str):
        """
        Set user's preferred difficulty level.
        
        Args:
            level: 'beginner', 'intermediate', or 'advanced'
        """
        valid_levels = ['beginner', 'intermediate', 'advanced']
        if level.lower() in valid_levels:
            self.profile['learning_preferences']['difficulty_level'] = level.lower()
            self._save_profile()
    
    def set_target_role(self, role: str):
        """
        Set target job role for placement preparation.
        
        Args:
            role: Target role (e.g., "Software Engineer")
        """
        self.profile['goals']['target_role'] = role
        self._save_profile()
    
    def add_target_company(self, company: str):
        """Add a company to target companies list."""
        if company not in self.profile['goals']['target_companies']:
            self.profile['goals']['target_companies'].append(company)
            self._save_profile()
    
    def add_focus_area(self, area: str):
        """Add a focus area for study preparation."""
        if area not in self.profile['goals']['focus_areas']:
            self.profile['goals']['focus_areas'].append(area)
            self._save_profile()
    
    def add_weak_area(self, topic: str):
        """
        Mark a topic as a weak area.
        
        Args:
            topic: Topic where user needs improvement
        """
        if topic not in self.profile['weak_areas']:
            self.profile['weak_areas'].append(topic)
            self._save_profile()
    
    def add_strong_area(self, topic: str):
        """
        Mark a topic as a strong area.
        
        Args:
            topic: Topic user is proficient in
        """
        if topic not in self.profile['strong_areas']:
            self.profile['strong_areas'].append(topic)
            self._save_profile()
    
    def increment_questions_asked(self):
        """Increment the counter for questions asked."""
        self.profile['study_stats']['total_questions_asked'] += 1
        self.profile['study_stats']['last_active'] = datetime.now().isoformat()
        self._save_profile()
    
    def add_topic_covered(self, topic: str):
        """Add a topic to the list of covered topics."""
        if topic not in self.profile['study_stats']['topics_covered']:
            self.profile['study_stats']['topics_covered'].append(topic)
            self._save_profile()
    
    def get_profile_summary(self) -> Dict:
        """
        Get a summary of user profile.
        
        Returns:
            Dictionary with key profile information
        """
        return {
            'name': self.profile['name'],
            'difficulty_level': self.profile['learning_preferences']['difficulty_level'],
            'target_role': self.profile['goals']['target_role'],
            'focus_areas': self.profile['goals']['focus_areas'],
            'weak_areas': self.profile['weak_areas'],
            'total_questions': self.profile['study_stats']['total_questions_asked'],
            'topics_covered': len(self.profile['study_stats']['topics_covered'])
        }
    
    def get_full_profile(self) -> Dict:
        """Get complete profile data."""
        return self.profile.copy()
    
    def reset_profile(self):
        """Reset profile to default (use with caution!)."""
        self.profile = self._create_default_profile()
        self._save_profile()
        print("✓ Profile reset to default")
    
    def export_profile(self, output_file: str):
        """
        Export profile to a file.
        
        Args:
            output_file: Path to export file
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
            print(f"✓ Profile exported to {output_file}")
        except Exception as e:
            print(f"Error exporting profile: {e}")
