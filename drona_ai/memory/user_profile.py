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
    def __init__(self, profile_file: str = "user_profile.json"):
        # Store profile in data directory
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.profile_file = os.path.join(self.data_dir, profile_file)
        
        # Load existing profile or create default
        self.profile = self._load_profile()
    
    def _load_profile(self) -> Dict:
        try:
            if os.path.exists(self.profile_file):
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._create_default_profile()
        except Exception as e:
            print(f"Warning: Could not load profile: {e}")
            return self._create_default_profile()
    
    def _create_default_profile(self) -> Dict:
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
        try:
            self.profile['updated_at'] = datetime.now().isoformat()
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save profile: {e}")
    
    def set_name(self, name: str):
        self.profile['name'] = name
        self._save_profile()
    
    def get_name(self) -> str:
        return self.profile.get('name', 'User')
    
    def add_preferred_topic(self, topic: str):
        if topic not in self.profile['preferences']['topics']:
            self.profile['preferences']['topics'].append(topic)
            self._save_profile()
    
    def set_difficulty_level(self, level: str):
        self.profile['preferences']['difficulty_level'] = level
        self._save_profile()
    
    def set_target_role(self, role: str):
        self.profile['goals']['target_role'] = role
        self._save_profile()
    
    def add_target_company(self, company: str):
        if company not in self.profile['goals']['target_companies']:
            self.profile['goals']['target_companies'].append(company)
            self._save_profile()
    
    def add_focus_area(self, area: str):
        if area not in self.profile['goals']['focus_areas']:
            self.profile['goals']['focus_areas'].append(area)
            self._save_profile()
    
    def add_weak_area(self, topic: str):
        if topic not in self.profile['weak_areas']:
            self.profile['weak_areas'].append(topic)
            self._save_profile()
    
    def add_strong_area(self, topic: str):
        if topic not in self.profile['strong_areas']:
            self.profile['strong_areas'].append(topic)
            self._save_profile()
    
    def increment_questions_asked(self):
        self.profile['study_stats']['total_questions_asked'] += 1
        self.profile['study_stats']['last_active'] = datetime.now().isoformat()
        self._save_profile()
    
    def add_topic_covered(self, topic: str):
        if topic not in self.profile['study_stats']['topics_covered']:
            self.profile['study_stats']['topics_covered'].append(topic)
            self._save_profile()
    
    def get_profile_summary(self) -> Dict:
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
        return self.profile.copy()
    
    def reset_profile(self):
        self.profile = self._create_default_profile()
        self._save_profile()
        print("✓ Profile reset to default")
    
    def export_profile(self, output_file: str):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
            print(f"✓ Profile exported to {output_file}")
        except Exception as e:
            print(f"Error exporting profile: {e}")
