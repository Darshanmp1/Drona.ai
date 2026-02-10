"""
Mock Interview Module
Generates interview questions dynamically based on role and difficulty.
Provides a practice interview environment for placement preparation.
"""

import random
from typing import List, Dict, Optional


class MockInterview:
    """
    Conducts mock interview sessions with questions across different categories.
    Generates questions based on role, difficulty, and focus areas.
    """
    
    def __init__(self):
        """Initialize mock interview with question banks."""
        # Question bank organized by category and difficulty
        self.question_bank = self._initialize_question_bank()
        
        # Track interview session
        self.current_session = None
    
    def _initialize_question_bank(self) -> Dict:
        """
        Create a comprehensive question bank.
        
        Returns:
            Dictionary with categorized questions
        """
        return {
            'data_structures': {
                'beginner': [
                    "What is an array and how does it differ from a linked list?",
                    "Explain what a stack is and give a real-world example.",
                    "What is the difference between a queue and a stack?",
                    "What is a hash table and what is it used for?",
                    "Explain what a binary tree is."
                ],
                'intermediate': [
                    "Implement a function to reverse a linked list.",
                    "How would you detect a cycle in a linked list?",
                    "Explain how a hash map handles collisions.",
                    "What is the difference between BFS and DFS traversal?",
                    "Implement a stack using two queues."
                ],
                'advanced': [
                    "Design and implement an LRU cache.",
                    "Explain and implement a self-balancing binary search tree.",
                    "How would you design a data structure for a file system?",
                    "Implement a trie and explain its time complexity.",
                    "Design a skip list and explain when you'd use it over a balanced tree."
                ]
            },
            'algorithms': {
                'beginner': [
                    "Explain what Big O notation means.",
                    "What is the difference between O(n) and O(n²) complexity?",
                    "Describe how binary search works.",
                    "What is a sorting algorithm? Name two examples.",
                    "Explain what recursion is with an example."
                ],
                'intermediate': [
                    "Implement merge sort and explain its time complexity.",
                    "Find the kth largest element in an unsorted array.",
                    "How would you find if two strings are anagrams?",
                    "Implement a function to find the longest palindromic substring.",
                    "Explain dynamic programming and give an example problem."
                ],
                'advanced': [
                    "Solve the traveling salesman problem using dynamic programming.",
                    "Implement Dijkstra's shortest path algorithm.",
                    "Design an algorithm to find the median of two sorted arrays.",
                    "Explain and implement the KMP string matching algorithm.",
                    "Solve the coin change problem with optimal approach."
                ]
            },
            'system_design': {
                'beginner': [
                    "What is a client-server architecture?",
                    "Explain what an API is and why it's useful.",
                    "What is the difference between SQL and NoSQL databases?",
                    "What is caching and why is it important?",
                    "Explain what load balancing means."
                ],
                'intermediate': [
                    "Design a URL shortening service like bit.ly.",
                    "How would you design a simple chat application?",
                    "Explain the CAP theorem with examples.",
                    "Design a notification system for a social media app.",
                    "How would you design a rate limiter?"
                ],
                'advanced': [
                    "Design a distributed file storage system like Dropbox.",
                    "How would you design Instagram's feed system?",
                    "Design a global messaging system like WhatsApp.",
                    "Explain how you'd design a recommendation system for Netflix.",
                    "Design a real-time collaborative editing system like Google Docs."
                ]
            },
            'programming': {
                'beginner': [
                    "What are the main features of Python?",
                    "Explain the difference between a list and a tuple in Python.",
                    "What is object-oriented programming?",
                    "Explain what a function is and why we use them.",
                    "What is the difference between == and === in JavaScript?"
                ],
                'intermediate': [
                    "Explain decorators in Python with an example.",
                    "What is the difference between synchronous and asynchronous code?",
                    "How does garbage collection work in JavaScript?",
                    "Explain closures in programming with an example.",
                    "What are promises in JavaScript and how do you use them?"
                ],
                'advanced': [
                    "Explain the event loop in Node.js.",
                    "How would you optimize a slow database query?",
                    "Explain metaclasses in Python.",
                    "What are generators and when would you use them?",
                    "Implement a thread-safe singleton pattern."
                ]
            },
            'behavioral': {
                'general': [
                    "Tell me about yourself and your journey in tech.",
                    "Why do you want to work as a software engineer?",
                    "Describe a challenging project you worked on.",
                    "How do you stay updated with new technologies?",
                    "Tell me about a time you failed and what you learned.",
                    "How do you handle tight deadlines?",
                    "Describe a situation where you had to work in a team.",
                    "What are your strengths and weaknesses?",
                    "Where do you see yourself in 5 years?",
                    "Why do you want to work for our company?"
                ]
            }
        }
    
    def start_interview(self, role: str = "Software Engineer", 
                       difficulty: str = "intermediate",
                       focus_areas: Optional[List[str]] = None,
                       num_questions: int = 5) -> Dict:
        """
        Start a new mock interview session.
        
        Args:
            role: Target role (affects question selection)
            difficulty: Difficulty level (beginner/intermediate/advanced)
            focus_areas: Specific areas to focus on
            num_questions: Number of questions to ask
            
        Returns:
            Interview session data
        """
        # Determine question categories based on role
        categories = focus_areas or ['data_structures', 'algorithms', 'programming']
        
        # Always include behavioral questions
        if 'behavioral' not in categories:
            categories.append('behavioral')
        
        # Generate questions
        questions = self._generate_questions(categories, difficulty, num_questions)
        
        # Create session
        self.current_session = {
            'role': role,
            'difficulty': difficulty,
            'focus_areas': categories,
            'questions': questions,
            'current_question_index': 0,
            'answers': []
        }
        
        return self.current_session
    
    def _generate_questions(self, categories: List[str], difficulty: str, 
                           num_questions: int) -> List[Dict]:
        """
        Generate a mix of questions from different categories.
        
        Args:
            categories: List of question categories
            difficulty: Difficulty level
            num_questions: Total questions to generate
            
        Returns:
            List of question dictionaries
        """
        questions = []
        questions_per_category = max(1, num_questions // len(categories))
        
        for category in categories:
            if category not in self.question_bank:
                continue
            
            # Get questions for this category
            if category == 'behavioral':
                available_questions = self.question_bank[category]['general']
            else:
                # Get questions based on difficulty
                if difficulty in self.question_bank[category]:
                    available_questions = self.question_bank[category][difficulty]
                else:
                    # Default to intermediate if difficulty not found
                    available_questions = self.question_bank[category].get('intermediate', [])
            
            # Randomly select questions
            selected = random.sample(
                available_questions, 
                min(questions_per_category, len(available_questions))
            )
            
            for q in selected:
                questions.append({
                    'category': category,
                    'difficulty': difficulty if category != 'behavioral' else 'general',
                    'question': q
                })
        
        # Shuffle to mix categories
        random.shuffle(questions)
        
        # Return requested number
        return questions[:num_questions]
    
    def get_next_question(self) -> Optional[Dict]:
        """
        Get the next question in the current interview session.
        
        Returns:
            Next question dictionary or None if interview is complete
        """
        if not self.current_session:
            return None
        
        idx = self.current_session['current_question_index']
        questions = self.current_session['questions']
        
        if idx >= len(questions):
            return None  # Interview complete
        
        question = questions[idx].copy()
        question['number'] = idx + 1
        question['total'] = len(questions)
        
        return question
    
    def submit_answer(self, answer: str):
        """
        Submit answer to current question and move to next.
        
        Args:
            answer: User's answer
        """
        if not self.current_session:
            return
        
        idx = self.current_session['current_question_index']
        
        if idx < len(self.current_session['questions']):
            # Store answer
            self.current_session['answers'].append({
                'question': self.current_session['questions'][idx]['question'],
                'answer': answer
            })
            
            # Move to next question
            self.current_session['current_question_index'] += 1
    
    def is_interview_complete(self) -> bool:
        """Check if the interview session is complete."""
        if not self.current_session:
            return True
        
        return (self.current_session['current_question_index'] >= 
                len(self.current_session['questions']))
    
    def get_interview_summary(self) -> Dict:
        """
        Get summary of completed interview.
        
        Returns:
            Dictionary with interview statistics
        """
        if not self.current_session:
            return {}
        
        return {
            'role': self.current_session['role'],
            'difficulty': self.current_session['difficulty'],
            'total_questions': len(self.current_session['questions']),
            'questions_answered': len(self.current_session['answers']),
            'categories_covered': list(set(q['category'] for q in self.current_session['questions']))
        }
    
    def get_tips_for_category(self, category: str) -> List[str]:
        """
        Get preparation tips for a specific category.
        
        Args:
            category: Question category
            
        Returns:
            List of tips
        """
        tips = {
            'data_structures': [
                "Practice implementing common data structures from scratch",
                "Understand time and space complexity for each operation",
                "Know when to use each data structure in real scenarios",
                "Practice on platforms like LeetCode and HackerRank"
            ],
            'algorithms': [
                "Master sorting and searching algorithms",
                "Practice dynamic programming problems regularly",
                "Understand graph algorithms (BFS, DFS, Dijkstra)",
                "Learn to recognize patterns in problems"
            ],
            'system_design': [
                "Start with defining requirements and constraints",
                "Think about scalability from the beginning",
                "Understand trade-offs between different approaches",
                "Practice designing real-world systems"
            ],
            'programming': [
                "Write clean, readable code with good naming",
                "Master at least one programming language deeply",
                "Understand language-specific features and idioms",
                "Practice explaining your code clearly"
            ],
            'behavioral': [
                "Prepare stories using the STAR method",
                "Be honest and authentic in your answers",
                "Show enthusiasm and passion for technology",
                "Research the company before the interview"
            ]
        }
        
        return tips.get(category, ["Practice regularly and stay confident!"])
