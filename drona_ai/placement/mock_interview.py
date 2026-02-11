# Mock interview with role-based questions

import random
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class MockInterview:
    def __init__(self):
        # Role-specific question banks
        self.role_questions = self._initialize_role_questions()
        
        # Track asked questions per role to avoid repetition
        self.asked_questions_history = {}  # {role: {set of asked questions}}
        
        # Interview session data
        self.current_session = None
        
        # Available job roles
        self.available_roles = list(self.role_questions.keys()) + ["Other"]
    
    def _initialize_role_questions(self) -> Dict:
        return {
            'Software Engineer': {
                'technical_beginner': [
                    "What are the four pillars of Object-Oriented Programming?",
                    "Explain the difference between an array and a linked list.",
                    "What is the time complexity of binary search?",
                    "What is a REST API and how does it work?",
                    "Explain what version control is and why it's important.",
                    "What is the difference between SQL and NoSQL databases?",
                    "What are data structures? Name at least 3 examples.",
                    "Explain what recursion is with an example.",
                ],
                'technical_intermediate': [
                    "How would you detect a cycle in a linked list?",
                    "Implement a function to reverse a string without using built-in methods.",
                    "Explain the difference between process and thread.",
                    "What is dependency injection and why is it useful?",
                    "How would you design a URL shortener like bit.ly?",
                    "Explain the SOLID principles with examples.",
                    "What is the difference between authentication and authorization?",
                    "How do you handle race conditions in multithreading?",
                    "Explain microservices architecture and its benefits.",
                ],
                'technical_advanced': [
                    "Design and implement an LRU cache with O(1) operations.",
                    "How would you design a distributed messaging system like Kafka?",
                    "Explain eventual consistency and CAP theorem.",
                    "Design a rate limiter for an API gateway.",
                    "How would you optimize a database with millions of records?",
                    "Implement a thread-safe singleton pattern in your preferred language.",
                    "Design a real-time collaborative editing system like Google Docs.",
                ],
                'behavioral': [
                    "Tell me about a time you debugged a complex issue.",
                    "Describe a situation where you had to learn a new technology quickly.",
                    "How do you prioritize tasks when working on multiple features?",
                    "Tell me about a time you disagreed with a technical decision.",
                    "Describe your most challenging software project and how you handled it.",
                ]
            },
            
            'Data Scientist': {
                'technical_beginner': [
                    "What is the difference between supervised and unsupervised learning?",
                    "Explain what overfitting is and how to prevent it.",
                    "What is a p-value in statistics?",
                    "Explain the bias-variance tradeoff.",
                    "What is the difference between classification and regression?",
                    "What is feature engineering and why is it important?",
                    "Explain what a confusion matrix is.",
                ],
                'technical_intermediate': [
                    "How would you handle imbalanced datasets?",
                    "Explain different types of cross-validation techniques.",
                    "What is regularization? Explain L1 and L2 regularization.",
                    "How do you evaluate a classification model?",
                    "Explain gradient descent and its variants.",
                    "What is the curse of dimensionality?",
                    "How do decision trees work? What are their pros and cons?",
                    "Explain the difference between bagging and boosting.",
                ],
                'technical_advanced': [
                    "Design a recommendation system for an e-commerce platform.",
                    "How would you build a fraud detection system?",
                    "Explain transformers and attention mechanism in NLP.",
                    "How would you deploy a machine learning model in production?",
                    "Design an A/B testing framework for a company.",
                    "Explain how you'd handle concept drift in production models.",
                    "How would you build a real-time anomaly detection system?",
                ],
                'behavioral': [
                    "Tell me about a time your model performed poorly in production.",
                    "Describe how you communicated complex technical results to non-technical stakeholders.",
                    "How do you stay updated with the latest ML research?",
                    "Tell me about a time you had to make a trade-off between model accuracy and interpretability.",
                ]
            },
            
            'Frontend Developer': {
                'technical_beginner': [
                    "What is the DOM and how does JavaScript interact with it?",
                    "Explain the CSS box model.",
                    "What is the difference between var, let, and const in JavaScript?",
                    "What are semantic HTML tags?",
                    "Explain event bubbling and event capturing.",
                    "What is the difference between == and === in JavaScript?",
                ],
                'technical_intermediate': [
                    "Explain React's virtual DOM and its benefits.",
                    "What are React hooks? Explain useState and useEffect.",
                    "How would you optimize the performance of a React application?",
                    "Explain the difference between controlled and uncontrolled components.",
                    "What is state management? Compare Redux, Context API, and Zustand.",
                    "How do you handle responsive design?",
                    "Explain asynchronous JavaScript (promises, async/await).",
                ],
                'technical_advanced': [
                    "How would you implement server-side rendering (SSR) in React?",
                    "Design a component library for your organization.",
                    "How would you optimize a web app with slow rendering performance?",
                    "Explain code splitting and lazy loading strategies.",
                    "How would you implement micro-frontends architecture?",
                    "Design an accessible form with complex validation.",
                ],
                'behavioral': [
                    "Tell me about a time you improved user experience on a website.",
                    "How do you balance design requirements with technical constraints?",
                    "Describe a situation where you had to optimize for different browsers.",
                ]
            },
            
            'Backend Developer': {
                'technical_beginner': [
                    "What is an API and what are REST principles?",
                    "Explain the difference between GET and POST requests.",
                    "What is a database index and why is it important?",
                    "What is authentication vs authorization?",
                    "Explain what middleware is in backend frameworks.",
                    "What is CORS and why does it exist?",
                ],
                'technical_intermediate': [
                    "How would you design a RESTful API for a blog application?",
                    "Explain database normalization and its forms.",
                    "What is connection pooling and why is it important?",
                    "How do you handle database transactions?",
                    "Explain different types of database joins.",
                    "What is caching and where would you implement it?",
                    "How would you implement rate limiting for an API?",
                    "Explain the difference between SQL and NoSQL. When would you use each?",
                ],
                'technical_advanced': [
                    "Design a scalable notification system.",
                    "How would you implement distributed transactions?",
                    "Explain database sharding and partitioning strategies.",
                    "Design an API gateway for microservices.",
                    "How would you handle millions of concurrent connections?",
                    "Implement an event-driven architecture for order processing.",
                ],
                'behavioral': [
                    "Tell me about a time you optimized a slow API endpoint.",
                    "Describe how you handled a production database issue.",
                    "How do you ensure API security and prevent common vulnerabilities?",
                ]
            },
            
'DevOps Engineer': {
                'technical_beginner': [
                    "What is CI/CD and why is it important?",
                    "Explain the difference between Docker containers and virtual machines.",
                    "What is Infrastructure as Code (IaC)?",
                    "What is the purpose of a load balancer?",
                    "Explain what Jenkins is used for.",
                ],
                'technical_intermediate': [
                    "How would you set up a CI/CD pipeline for a web application?",
                    "Explain Kubernetes pods, deployments, and services.",
                    "What is blue-green deployment vs canary deployment?",
                    "How do you monitor application performance and logs?",
                    "Explain the concept of immutable infrastructure.",
                    "What is service mesh and when would you use it?",
                    "How do you handle secrets management in deployments?",
                ],
                'technical_advanced': [
                    "Design a highly available architecture for a global application.",
                    "How would you implement disaster recovery for a production system?",
                    "Design an auto-scaling strategy for unpredictable traffic.",
                    "How would you migrate a monolith to microservices with zero downtime?",
                    "Implement a multi-region deployment strategy.",
                ],
                'behavioral': [
                    "Tell me about a time you handled a production outage.",
                    "Describe how you improved deployment speed or reliability.",
                    "How do you balance automation with security?",
                ]
            },
            
            'Data Analyst': {
                'technical_beginner': [
                    "What is the difference between a primary key and foreign key?",
                    "Explain what a JOIN is in SQL.",
                    "What is data visualization and why is it important?",
                    "What is the difference between qualitative and quantitative data?",
                    "Explain what Excel pivot tables do.",
                ],
                'technical_intermediate': [
                    "How would you identify and handle outliers in a dataset?",
                    "Explain window functions in SQL with examples.",
                    "What metrics would you track for an e-commerce business?",
                    "How do you validate data quality?",
                    "Explain cohort analysis and when you'd use it.",
                    "What is the difference between OLTP and OLAP?",
                    "How would you build a dashboard for executives?",
                ],
                'technical_advanced': [
                    "Design a data warehouse for a multi-product company.",
                    "How would you perform RFM analysis for customer segmentation?",
                    "Design an ETL pipeline for daily sales data.",
                    "How would you measure the impact of a marketing campaign?",
                    "Explain how you'd build predictive models for sales forecasting.",
                ],
                'behavioral': [
                    "Tell me about a time your analysis led to a business decision.",
                    "Describe how you presented complex data insights to stakeholders.",
                    "How do you prioritize multiple analysis requests?",
                ]
            },
            
            'Full Stack Developer': {
                'technical_beginner': [
                    "What is the difference between frontend and backend?",
                    "Explain the request-response cycle in web applications.",
                    "What is JSON and why is it used?",
                    "What is a cookie vs session vs local storage?",
                    "Explain what an ORM is.",
                ],
                'technical_intermediate': [
                    "How would you build authentication for a web application?",
                    "Explain the MVC architecture pattern.",
                    "How do you optimize website performance (both frontend and backend)?",
                    "What is WebSocket and when would you use it?",
                    "How would you implement file upload functionality?",
                    "Explain server-side vs client-side rendering.",
                    "How do you handle state management in full-stack apps?",
                ],
                'technical_advanced': [
                    "Design a real-time multiplayer game architecture.",
                    "How would you build a scalable social media platform?",
                    "Design a payment processing system with fraud detection.",
                    "How would you implement real-time collaboration features?",
                    "Design a multi-tenant SaaS application.",
                ],
                'behavioral': [
                    "Tell me about a full-stack project you built from scratch.",
                    "How do you decide where to implement business logic (frontend vs backend)?",
                    "Describe a time you had to debug an issue across the full stack.",
                ]
            },
            
            'Machine Learning Engineer': {
                'technical_beginner': [
                    "What is the difference between ML Engineer and Data Scientist?",
                    "Explain training, validation, and test sets.",
                    "What is a neural network?",
                    "What is transfer learning?",
                    "Explain what hyperparameters are.",
                ],
                'technical_intermediate': [
                    "How would you deploy a machine learning model to production?",
                    "Explain model versioning and experiment tracking.",
                    "What is model drift and how do you detect it?",
                    "How do you optimize inference latency?",
                    "Explain the ML pipeline: data preprocessing to model serving.",
                    "What is feature store and why is it important?",
                    "How do you handle real-time ML predictions?",
                ],
                'technical_advanced': [
                    "Design an end-to-end ML platform for a company.",
                    "How would you build a real-time recommendation system?",
                    "Design an A/B testing framework for ML models.",
                    "How would you implement federated learning?",
                    "Design a model monitoring and observability system.",
                ],
                'behavioral': [
                    "Tell me about a time you optimized model performance for production.",
                    "Describe how you collaborated with data scientists and engineers.",
                    "How do you balance model accuracy with latency requirements?",
                ]
            },
        }
    
    def get_available_roles(self) -> List[str]:
        return self.available_roles
    
    def _get_fresh_questions(self, role: str, difficulty: str, count: int) -> List[str]:
        # Initialize history for this role if not exists
        if role not in self.asked_questions_history:
            self.asked_questions_history[role] = set()
        
        # Get question pool based on role and difficulty
        if role == "Other" or role not in self.role_questions:
            # For "Other" role, use general software engineering questions
            question_pool = self.role_questions.get('Software Engineer', {})
        else:
            question_pool = self.role_questions[role]
        
        # Collect all available questions for this difficulty
        all_questions = []
        if f'technical_{difficulty.lower()}' in question_pool:
            all_questions.extend(question_pool[f'technical_{difficulty.lower()}'])
        if 'behavioral' in question_pool:
            all_questions.extend(question_pool['behavioral'])
        
        # Filter out already asked questions
        fresh_questions = [q for q in all_questions if q not in self.asked_questions_history[role]]
        
        # If we've asked all questions, reset history for this role
        if len(fresh_questions) < count:
            self.asked_questions_history[role].clear()
            fresh_questions = all_questions.copy()
        
        # Select random questions
        selected = random.sample(fresh_questions, min(count, len(fresh_questions)))
        
        # Mark as asked
        self.asked_questions_history[role].update(selected)
        
        return selected
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
                       difficulty: str = "Intermediate",
                       num_questions: int = 5) -> Dict:
        # Initialize a new interview session
        questions = []
        for _ in range(num_questions):
            q = self.get_question(role, difficulty)
            if q:
                questions.append(q)
        
        self.current_session = {
            'role': role,
            'difficulty': difficulty,
            'questions': questions,
            'answers': [],
            'current_question_index': 0,
            'started_at': datetime.now().isoformat()
        }
        
        return self.current_session
    
    def get_next_question(self) -> Optional[Dict]:
        if not self.current_session:
            return None
        
        idx = self.current_session['current_question_index']
        if idx < len(self.current_session['questions']):
            return self.current_session['questions'][idx]
        return None
    
    def submit_answer(self, answer: str):
        if not self.current_session:
            return
        
        idx = self.current_session['current_question_index']
        
        if idx < len(self.current_session['questions']):
            # Store answer with metadata
            self.current_session['answers'].append({
                'question': self.current_session['questions'][idx],
                'answer': answer,
                'question_number': idx + 1
            })
            
            # Move to next question
            self.current_session['current_question_index'] += 1
    
    def is_interview_complete(self) -> bool:
        if not self.current_session:
            return True
        
        return (self.current_session['current_question_index'] >= 
                len(self.current_session['questions']))
    
    def get_interview_summary(self) -> Dict:
        if not self.current_session:
            return {}
        
        return {
            'role': self.current_session['role'],
            'difficulty': self.current_session['difficulty'],
            'total_questions': len(self.current_session['questions']),
            'questions_answered': len(self.current_session['answers']),
            'completion_rate': f"{(len(self.current_session['answers']) / len(self.current_session['questions']) * 100):.0f}%",
            'all_questions': self.current_session['questions'],
            'all_answers': self.current_session['answers']
        }
    
    def get_role_interview_stats(self, role: str) -> Dict:
        if role not in self.asked_questions_history:
            return {
                'role': role,
                'questions_asked': 0,
                'message': f'No interview history for {role} yet'
            }
        
        return {
            'role': role,
            'questions_asked': len(self.asked_questions_history[role]),
            'total_available': len(self._get_all_questions_for_role(role)),
            'fresh_questions_remaining': len(self._get_all_questions_for_role(role)) - len(self.asked_questions_history[role])
        }
    
    def _get_all_questions_for_role(self, role: str) -> List[str]:
        if role == "Other" or role not in self.role_questions:
            question_pool = self.role_questions.get('Software Engineer', {})
        else:
            question_pool = self.role_questions[role]
        
        all_questions = []
        for key, questions in question_pool.items():
            if isinstance(questions, list):
                all_questions.extend(questions)
        
        return all_questions
    
    def reset_role_history(self, role: str):
        if role in self.asked_questions_history:
            self.asked_questions_history[role].clear()
    
    def get_tips_for_role(self, role: str) -> List[str]:
        tips_by_role = {
            'Software Engineer': [
                "✓ Master data structures: arrays, linked lists, trees, graphs, hash tables",
                "✓ Practice algorithmic problem-solving on LeetCode/HackerRank",
                "✓ Understand time and space complexity (Big O notation)",
                "✓ Study system design fundamentals (scalability, caching, load balancing)",
                "✓ Be ready to code on a whiteboard or shared screen",
                "✓ Prepare STAR method stories for behavioral questions"
            ],
            'Data Scientist': [
                "✓ Master statistics and probability fundamentals",
                "✓ Understand ML algorithms: regression, classification, clustering",
                "✓ Practice feature engineering and model evaluation",
                "✓ Prepare case studies showing end-to-end ML projects",
                "✓ Be ready to explain your work to non-technical stakeholders",
                "✓ Study SQL and data manipulation with pandas"
            ],
            'Frontend Developer': [
                "✓ Master JavaScript ES6+ features and async programming",
                "✓ Deep dive into React/Angular/Vue (whichever you use)",
                "✓ Understand CSS (flexbox, grid, responsive design)",
                "✓ Practice building components from scratch",
                "✓ Study web performance optimization techniques",
                "✓ Understand accessibility (WCAG standards)"
            ],
            'Backend Developer': [
                "✓ Master RESTful API design principles",
                "✓ Understand database design and SQL optimization",
                "✓ Study authentication & authorization (JWT, OAuth)",
                "✓ Learn about caching strategies (Redis, Memcached)",
                "✓ Understand microservices vs monolithic architecture",
                "✓ Practice designing scalable backend systems"
            ],
            'DevOps Engineer': [
                "✓ Master Docker and container orchestration (Kubernetes)",
                "✓ Understand CI/CD pipeline tools (Jenkins, GitLab CI, GitHub Actions)",
                "✓ Study Infrastructure as Code (Terraform, CloudFormation)",
                "✓ Learn monitoring and logging (Prometheus, Grafana, ELK)",
                "✓ Understand cloud platforms (AWS, Azure, or GCP)",
                "✓ Practice automation scripting (Bash, Python)"
            ],
            'Data Analyst': [
                "✓ Master SQL - practice complex queries and window functions",
                "✓ Learn visualization tools (Tableau, Power BI, or Looker)",
                "✓ Understand business metrics and KPIs",
                "✓ Practice telling stories with data",
                "✓ Study statistical analysis and hypothesis testing",
                "✓ Prepare case studies with real business impact"
            ],
            'Full Stack Developer': [
                "✓ Be strong in both frontend AND backend technologies",
                "✓ Understand the full request-response cycle",
                "✓ Master at least one full stack framework (MERN, MEAN, Django+React)",
                "✓ Study database design and API development",
                "✓ Understand deployment and CI/CD processes",
                "✓ Be ready to discuss trade-offs in architecture decisions"
            ],
            'Machine Learning Engineer': [
                "✓ Understand ML lifecycle: training, deployment, monitoring",
                "✓ Master ML frameworks (TensorFlow, PyTorch, scikit-learn)",
                "✓ Study model deployment (Docker, Kubernetes, cloud services)",
                "✓ Learn about model monitoring and drift detection",
                "✓ Understand MLOps practices and tools",
                "✓ Practice optimizing models for production (latency, throughput)"
            ]
        }
        
        return tips_by_role.get(role, [
            "✓ Research the company and role thoroughly",
            "✓ Practice coding problems relevant to the position",
            "✓ Prepare examples of your past work and projects",
            "✓ Study the job description and match your skills",
            "✓ Be ready with thoughtful questions for the interviewer"
        ])
    
    def get_question(self, role: str = "Software Engineer", difficulty: str = "Intermediate") -> str:
        # Get fresh questions for this role
        questions = self._get_fresh_questions(role, difficulty, 1)
        
        if questions:
            return questions[0]
        
        # Fallback
        return "Tell me about a challenging project you've worked on in your role and how you overcame obstacles."
