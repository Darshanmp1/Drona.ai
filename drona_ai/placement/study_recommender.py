"""
Study Recommender Module
Suggests study topics and resources based on weak areas and goals.
Provides personalized learning paths for placement preparation.
"""

from typing import List, Dict, Optional


class StudyRecommender:
    """
    Recommends study topics, resources, and learning paths
    based on user's weak areas, goals, and target role.
    """
    
    def __init__(self):
        """Initialize study recommender with resource database."""
        self.topic_resources = self._load_topic_resources()
        self.role_requirements = self._load_role_requirements()
        self.study_paths = self._load_study_paths()
    
    def _load_topic_resources(self) -> Dict:
        """
        Load study resources for different topics.
        
        Returns:
            Dictionary mapping topics to resources
        """
        return {
            'data_structures': {
                'priority': 'high',
                'estimated_time': '2-3 weeks',
                'resources': [
                    'LeetCode - Top Interview Questions (Arrays, Linked Lists)',
                    'GeeksforGeeks - Data Structures Tutorial',
                    'YouTube - MyCodeSchool Data Structures Playlist',
                    'Book: "Cracking the Coding Interview" - Chapter 1-4'
                ],
                'practice_problems': [
                    'Implement linked list from scratch',
                    'Solve array rotation problems',
                    'Tree traversal problems (BFS, DFS)',
                    'Hash table collision handling'
                ]
            },
            'algorithms': {
                'priority': 'high',
                'estimated_time': '3-4 weeks',
                'resources': [
                    'LeetCode - Algorithm Problems (Easy to Medium)',
                    'Coursera - Algorithms Specialization',
                    'HackerRank - Algorithm Track',
                    'Book: "Introduction to Algorithms" (CLRS)'
                ],
                'practice_problems': [
                    'Sorting algorithms implementation',
                    'Binary search variations',
                    'Dynamic programming classics (Knapsack, LCS)',
                    'Graph algorithms (BFS, DFS, Dijkstra)'
                ]
            },
            'system_design': {
                'priority': 'medium',
                'estimated_time': '2-3 weeks',
                'resources': [
                    'YouTube - System Design Primer',
                    'Educative.io - Grokking System Design',
                    'Book: "Designing Data-Intensive Applications"',
                    'GitHub - System Design Interview Guide'
                ],
                'practice_problems': [
                    'Design URL shortener',
                    'Design Twitter feed',
                    'Design ride-sharing service',
                    'Design notification system'
                ]
            },
            'python': {
                'priority': 'medium',
                'estimated_time': '2 weeks',
                'resources': [
                    'Python.org - Official Tutorial',
                    'Codecademy - Learn Python 3',
                    'Real Python - Tutorials',
                    'Book: "Python Crash Course"'
                ],
                'practice_problems': [
                    'List comprehensions and generators',
                    'Decorators and context managers',
                    'OOP concepts in Python',
                    'File handling and exceptions'
                ]
            },
            'javascript': {
                'priority': 'medium',
                'estimated_time': '2 weeks',
                'resources': [
                    'JavaScript.info - Modern JavaScript Tutorial',
                    'FreeCodeCamp - JavaScript Course',
                    'MDN Web Docs - JavaScript Guide',
                    'Book: "Eloquent JavaScript"'
                ],
                'practice_problems': [
                    'Closures and scope',
                    'Promises and async/await',
                    'DOM manipulation',
                    'ES6+ features'
                ]
            },
            'databases': {
                'priority': 'medium',
                'estimated_time': '1-2 weeks',
                'resources': [
                    'Mode Analytics - SQL Tutorial',
                    'MongoDB University - Free Courses',
                    'SQLZoo - Interactive SQL Tutorial',
                    'Book: "SQL in 10 Minutes"'
                ],
                'practice_problems': [
                    'Complex JOIN queries',
                    'Indexing and optimization',
                    'NoSQL vs SQL tradeoffs',
                    'Database normalization'
                ]
            },
            'web_development': {
                'priority': 'medium',
                'estimated_time': '3-4 weeks',
                'resources': [
                    'FreeCodeCamp - Responsive Web Design',
                    'MDN Web Docs - HTML/CSS/JavaScript',
                    'Web.dev - Learn Web Development',
                    'YouTube - Traversy Media Web Dev Tutorials'
                ],
                'practice_problems': [
                    'Build responsive landing page',
                    'Create REST API with Express',
                    'Implement authentication system',
                    'Build full-stack CRUD application'
                ]
            },
            'machine_learning': {
                'priority': 'low',
                'estimated_time': '4-6 weeks',
                'resources': [
                    'Coursera - Andrew Ng Machine Learning',
                    'Fast.ai - Practical Deep Learning',
                    'Kaggle - Learn Machine Learning',
                    'Book: "Hands-On Machine Learning"'
                ],
                'practice_problems': [
                    'Linear regression from scratch',
                    'Build classification model',
                    'Feature engineering exercises',
                    'Kaggle beginner competitions'
                ]
            }
        }
    
    def _load_role_requirements(self) -> Dict:
        """
        Load typical requirements for different roles.
        
        Returns:
            Dictionary mapping roles to required skills
        """
        return {
            'Software Engineer': {
                'must_have': ['data_structures', 'algorithms', 'python'],
                'good_to_have': ['system_design', 'databases', 'web_development'],
                'optional': ['machine_learning']
            },
            'Frontend Developer': {
                'must_have': ['javascript', 'web_development'],
                'good_to_have': ['algorithms', 'databases'],
                'optional': ['python']
            },
            'Backend Developer': {
                'must_have': ['python', 'databases', 'algorithms'],
                'good_to_have': ['system_design', 'data_structures'],
                'optional': ['web_development']
            },
            'Full Stack Developer': {
                'must_have': ['javascript', 'web_development', 'databases'],
                'good_to_have': ['python', 'algorithms', 'system_design'],
                'optional': ['machine_learning']
            },
            'Data Scientist': {
                'must_have': ['python', 'machine_learning', 'algorithms'],
                'good_to_have': ['databases'],
                'optional': ['web_development']
            }
        }
    
    def _load_study_paths(self) -> Dict:
        """
        Load recommended study paths for different time frames.
        
        Returns:
            Dictionary with study plans
        """
        return {
            '1_month': {
                'weeks': [
                    ['data_structures', 'Arrays and Strings'],
                    ['data_structures', 'Linked Lists and Trees'],
                    ['algorithms', 'Sorting and Searching'],
                    ['algorithms', 'Dynamic Programming Basics']
                ]
            },
            '2_months': {
                'weeks': [
                    ['data_structures', 'Arrays and Linked Lists'],
                    ['data_structures', 'Stacks, Queues, Trees'],
                    ['algorithms', 'Sorting Algorithms'],
                    ['algorithms', 'Searching and Binary Search'],
                    ['algorithms', 'Dynamic Programming'],
                    ['algorithms', 'Graph Algorithms'],
                    ['system_design', 'Basics and Scalability'],
                    ['practice', 'Mock Interviews and Review']
                ]
            },
            '3_months': {
                'description': 'Comprehensive preparation for top companies',
                'focus': 'Deep dive into all core topics with extensive practice'
            }
        }
    
    def recommend_topics(self, weak_areas: List[str], target_role: Optional[str] = None) -> Dict:
        """
        Recommend topics to study based on weak areas and target role.
        
        Args:
            weak_areas: List of topics user struggles with
            target_role: Target job role
            
        Returns:
            Dictionary with recommendations
        """
        recommendations = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'role_specific': []
        }
        
        # Add weak areas as high priority
        for topic in weak_areas:
            if topic in self.topic_resources:
                recommendations['high_priority'].append({
                    'topic': topic,
                    'reason': 'Identified weak area',
                    'resources': self.topic_resources[topic]
                })
        
        # Add role-specific recommendations if role provided
        if target_role and target_role in self.role_requirements:
            role_reqs = self.role_requirements[target_role]
            
            for topic in role_reqs['must_have']:
                if topic not in weak_areas:  # Don't duplicate
                    if topic in self.topic_resources:
                        recommendations['role_specific'].append({
                            'topic': topic,
                            'reason': f'Must-have for {target_role}',
                            'resources': self.topic_resources[topic]
                        })
        
        return recommendations
    
    def create_study_plan(self, timeframe: str, weak_areas: List[str], 
                         target_role: Optional[str] = None) -> Dict:
        """
        Create a personalized study plan.
        
        Args:
            timeframe: '1_month', '2_months', or '3_months'
            weak_areas: Topics to focus on
            target_role: Target job role
            
        Returns:
            Dictionary with detailed study plan
        """
        plan = {
            'timeframe': timeframe,
            'target_role': target_role,
            'weekly_schedule': [],
            'total_topics': 0,
            'daily_commitment': '2-3 hours recommended'
        }
        
        # Start with weak areas
        priority_topics = weak_areas.copy()
        
        # Add role requirements if specified
        if target_role and target_role in self.role_requirements:
            role_reqs = self.role_requirements[target_role]
            for topic in role_reqs['must_have']:
                if topic not in priority_topics:
                    priority_topics.append(topic)
        
        # If no priorities specified, use common interview topics
        if not priority_topics:
            priority_topics = ['data_structures', 'algorithms', 'python']
        
        # Create week-by-week plan
        weeks_available = {
            '1_month': 4,
            '2_months': 8,
            '3_months': 12
        }.get(timeframe, 4)
        
        week_index = 0
        for topic in priority_topics[:weeks_available]:
            if topic in self.topic_resources:
                plan['weekly_schedule'].append({
                    'week': week_index + 1,
                    'topic': topic,
                    'estimated_time': self.topic_resources[topic]['estimated_time'],
                    'resources': self.topic_resources[topic]['resources'][:2],  # Top 2 resources
                    'practice': self.topic_resources[topic]['practice_problems'][:3]  # Top 3 problems
                })
                week_index += 1
        
        plan['total_topics'] = len(plan['weekly_schedule'])
        
        return plan
    
    def get_daily_practice_suggestions(self, focus_topic: str) -> List[str]:
        """
        Get daily practice suggestions for a specific topic.
        
        Args:
            focus_topic: Topic to practice
            
        Returns:
            List of practice suggestions
        """
        if focus_topic not in self.topic_resources:
            return ["Practice coding problems on LeetCode or HackerRank"]
        
        return self.topic_resources[focus_topic]['practice_problems']
    
    def get_resource_links(self, topic: str) -> List[str]:
        """
        Get learning resources for a specific topic.
        
        Args:
            topic: Topic to get resources for
            
        Returns:
            List of resource links/names
        """
        if topic not in self.topic_resources:
            return []
        
        return self.topic_resources[topic]['resources']
    
    def suggest_next_topic(self, completed_topics: List[str], 
                          target_role: Optional[str] = None) -> Optional[str]:
        """
        Suggest the next topic to study based on what's been completed.
        
        Args:
            completed_topics: Topics already covered
            target_role: Target job role
            
        Returns:
            Next recommended topic
        """
        # Get role requirements if specified
        if target_role and target_role in self.role_requirements:
            must_have = self.role_requirements[target_role]['must_have']
            
            # Find first must-have topic not yet completed
            for topic in must_have:
                if topic not in completed_topics:
                    return topic
        
        # Default progression for general preparation
        default_order = ['data_structures', 'algorithms', 'python', 
                        'system_design', 'databases']
        
        for topic in default_order:
            if topic not in completed_topics:
                return topic
        
        return None  # All topics covered!
