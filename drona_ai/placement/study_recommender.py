"""
Study Recommender Module
Suggests study topics and resources based on weak areas and goals.
Provides personalized learning paths for placement preparation.
"""

from typing import List, Dict, Optional


class StudyRecommender:
    def __init__(self):
        self.topic_resources = self._load_topic_resources()
        self.role_requirements = self._load_role_requirements()
        self.study_paths = self._load_study_paths()
        self.level_configs = self._load_level_configs()
        self.daily_schedules = self._load_daily_schedules()
    
    def _load_topic_resources(self) -> Dict:
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
                ],
                'beginner_problems': [
                    'LeetCode #1 Two Sum',
                    'LeetCode #206 Reverse Linked List',
                    'LeetCode #104 Maximum Depth Binary Tree',
                    'Build basic stack and queue'
                ],
                'intermediate_problems': [
                    'LeetCode #146 LRU Cache',
                    'LeetCode #236 Lowest Common Ancestor',
                    'LeetCode #297 Serialize Binary Tree',
                    'Design HashMap from scratch'
                ],
                'advanced_problems': [
                    'LeetCode #295 Median from Stream',
                    'LeetCode #297 Serialize Deserialize Tree',
                    'Design Red-Black Tree',
                    'Implement B+ Tree for database'
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
                'beginner_resources': [
                    'Coursera - Andrew Ng Machine Learning (Start here)',
                    'YouTube - StatQuest Machine Learning',
                    'Kaggle - Intro to Machine Learning',
                    'Python.org - NumPy & Pandas Basics'
                ],
                'intermediate_resources': [
                    'Fast.ai - Practical Deep Learning',
                    'Kaggle - Intermediate ML',
                    'Scikit-learn Documentation',
                    'Book: "Hands-On Machine Learning" Ch 1-8'
                ],
                'advanced_resources': [
                    'Deep Learning Specialization - deeplearning.ai',
                    'Papers with Code - Latest Research',
                    'Book: "Deep Learning" - Goodfellow',
                    'Advanced Kaggle Competitions'
                ],
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
    
    def _load_level_configs(self) -> Dict:
        return {
            'Beginner': {
                'daily_hours': '1.5-2 hours',
                'practice_problems_per_day': 2,
                'theory_practice_ratio': '60:40',  # More theory
                'project_complexity': 'Simple console apps',
                'focus': 'Understanding fundamentals deeply',
                'pace': 'Slow and steady'
            },
            'Intermediate': {
                'daily_hours': '2-3 hours',
                'practice_problems_per_day': 3,
                'theory_practice_ratio': '40:60',  # More practice
                'project_complexity': 'Web apps with databases',
                'focus': 'Problem-solving patterns',
                'pace': 'Moderate with challenges'
            },
            'Advanced': {
                'daily_hours': '3-4 hours',
                'practice_problems_per_day': 5,
                'theory_practice_ratio': '20:80',  # Mostly practice
                'project_complexity': 'Production-ready systems',
                'focus': 'Optimization and architecture',
                'pace': 'Fast-paced with hard problems'
            }
        }
    
    def _load_daily_schedules(self) -> Dict:
        return {
            'Beginner': {
                '1 week': '1.5 hrs/day: 30min theory, 45min coding, 15min review',
                '1 month': '2 hrs/day: 45min theory, 60min practice, 15min projects',
                '3 months': '2 hrs/day: 40min concepts, 60min problems, 20min projects'
            },
            'Intermediate': {
                '1 week': '2.5 hrs/day: 30min theory, 1.5hr practice, 30min projects',
                '1 month': '2.5 hrs/day: 45min concepts, 1hr coding, 45min projects',
                '3 months': '3 hrs/day: 45min theory, 1.5hr practice, 45min building'
            },
            'Advanced': {
                '1 week': '3 hrs/day: 30min architecture, 2hr complex problems, 30min review',
                '1 month': '3.5 hrs/day: 1hr system design, 2hr coding challenges, 30min optimization',
                '3 months': '4 hrs/day: 1hr advanced topics, 2.5hr problem solving, 30min code review'
            }
        }
    
    def recommend_topics(self, weak_areas: List[str], target_role: Optional[str] = None) -> Dict:
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
        if focus_topic not in self.topic_resources:
            return ["Practice coding problems on LeetCode or HackerRank"]
    
    def generate_plan(self, subject: str, current_level: str, goal: str, 
                     timeframe: str, learning_style: List[str]) -> Dict:
        """
        Generate a study plan with more flexible parameters for UI integration.
        
        Args:
            subject: Subject/topic to study
            current_level: Beginner, Intermediate, or Advanced
            goal: Learning goal description
            timeframe: Timeline for study (e.g., "1 month", "3 months")
            learning_style: Preferred learning methods
            
        Returns:
            Dictionary with study plan details
        """
        # Convert timeframe to internal format with correct mapping
        timeframe_map = {
            '1 week': '1_month',      # 1 week = focus on 1-2 core topics
            '1 month': '1_month',     # 1 month = 4 weeks of study
            '3 months': '3_months',   # 3 months = 12 weeks comprehensive
        }
        internal_timeframe = timeframe_map.get(timeframe, '1_month')
        
        # Adjust weeks based on actual timeframe
        weeks_config = {
            '1 week': 1,      # Show only 1 week plan
            '1 month': 4,     # Show 4 weeks
            '3 months': 12,   # Show 12 weeks
        }
        num_weeks = weeks_config.get(timeframe, 4)
        
        # Identify weak areas based on subject AND level
        weak_areas = []
        subject_lower = subject.lower()
        
        if 'machine learning' in subject_lower or 'ml' in subject_lower or 'ai' in subject_lower:
            if current_level == 'Beginner':
                weak_areas = ['python', 'algorithms']  # Start simple
            elif current_level == 'Intermediate':
                weak_areas = ['algorithms', 'python', 'machine_learning']
            else:  # Advanced
                weak_areas = ['machine_learning', 'algorithms', 'system_design']
                
        elif 'data' in subject_lower:
            if current_level == 'Beginner':
                weak_areas = ['python', 'databases']
            elif current_level == 'Intermediate':
                weak_areas = ['algorithms', 'python', 'databases']
            else:  # Advanced
                weak_areas = ['algorithms', 'databases', 'system_design']
                
        elif 'web' in subject_lower or 'frontend' in subject_lower:
            if current_level == 'Beginner':
                weak_areas = ['javascript', 'web_development']
            elif current_level == 'Intermediate':
                weak_areas = ['javascript', 'web_development', 'algorithms']
            else:  # Advanced
                weak_areas = ['web_development', 'system_design', 'javascript']
                
        elif 'backend' in subject_lower:
            if current_level == 'Beginner':
                weak_areas = ['python', 'databases']
            elif current_level == 'Intermediate':
                weak_areas = ['algorithms', 'databases', 'system_design']
            else:  # Advanced
                weak_areas = ['system_design', 'algorithms', 'databases']
        else:
            # Default based on level
            if current_level == 'Beginner':
                weak_areas = ['python', 'data_structures']
            elif current_level == 'Intermediate':
                weak_areas = ['data_structures', 'algorithms', 'python']
            else:  # Advanced
                weak_areas = ['algorithms', 'system_design', 'data_structures']
        
        # Create detailed plan
        plan = self.create_study_plan(internal_timeframe, weak_areas, target_role=None)
        
        # Format for UI display - show appropriate number of weeks
        weekly_breakdown = "\n".join([
            f"**Week {w['week']}:** {w['topic'].replace('_', ' ').title()}\n- Study: {w['estimated_time']}\n- Resources: {', '.join(w['resources'][:2])}"
            for w in plan['weekly_schedule'][:num_weeks]
        ])
        
        resources = "\n".join([
            f"- {style}" for style in learning_style
        ]) if learning_style else "- Online courses\n- Practice problems\n- Documentation"
        
        # Dynamic milestones based on timeframe
        if timeframe == '1 week':
            milestones = f"""
1. **Days 1-2:** Understand core concepts of {subject}
2. **Days 3-5:** Practice with guided tutorials
3. **Days 6-7:** Build a small project and review
1. **Week 1-2:** Master fundamentals of {subject}
2. **Week 3:** Build hands-on projects  
3. **Week 4:** Practice problems and review
1. **Month 1:** Master fundamentals and core concepts
2. **Month 2:** Build real-world projects
3. **Month 3:** Practice interview questions and advanced topics
            """
        
        # Level-specific tips
        if current_level == 'Beginner':
            tips = f"Take your time to understand basics. {plan['daily_commitment']} Practice consistently and don't skip fundamentals."
        elif current_level == 'Intermediate':
            tips = f"Focus on depth over breadth. {plan['daily_commitment']} Build projects to solidify concepts."
        else:  # Advanced
            tips = f"Challenge yourself with complex problems. {plan['daily_commitment']} Focus on system design and optimization."
        
        return {
            'weekly_plan': weekly_breakdown or 'Study consistently with daily practice sessions.',
            'resources': resources,
            'milestones': milestones,
            'tips': tips,
            'timeframe': timeframe,
            'subject': subject,
            'level': current_level,
            'goal': goal
        }
    
    def get_resource_links(self, topic: str) -> List[str]:
        if topic not in self.topic_resources:
            return []
        
        return self.topic_resources[topic]['resources']
    
    def suggest_next_topic(self, completed_topics: List[str], 
                          target_role: Optional[str] = None) -> Optional[str]:
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
