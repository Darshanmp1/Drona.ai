"""
Advanced Study Recommender - Highly Personalized AI-Powered Learning Plans
Provides adaptive, level-specific, and project-based study recommendations.
"""

from typing import List, Dict


class AdvancedStudyRecommender:
    def __init__(self):
        self.level_configs = self._load_level_configs()
        self.daily_schedules = self._load_daily_schedules()
    
    def generate_advanced_plan(self, subject: str, level: str, timeframe: str) -> Dict:
        level_config = self.level_configs.get(level, self.level_configs['Intermediate'])
        daily_schedule = self.daily_schedules.get(level, {}).get(timeframe, '2-3 hours daily')
        
        weeks_config = {'1 week': 1, '1 month': 4, '3 months': 12}
        num_weeks = weeks_config.get(timeframe, 4)
        
        # Smart topic selection
        topics = self._select_topics(subject.lower(), level, num_weeks)
        
        # Build detailed curriculum
        weekly_plan = self._build_curriculum(topics, level, num_weeks)
        
        # Create personalized content
        milestones = self._create_milestones(subject, level, timeframe, num_weeks)
        tips = self._generate_tips(subject, level, timeframe, level_config)
        projects = self._suggest_projects(subject, level)
        schedule = self._format_schedule(daily_schedule, level_config)
        total_hours = self._calculate_hours(num_weeks, level_config['daily_hours'])
        
        return {
            'weekly_plan': weekly_plan,
            'milestones': milestones,
            'tips': tips,
            'daily_schedule': schedule,
            'projects': projects,
            'total_hours': total_hours,
            'level': level,
            'subject': subject,
            'timeframe': timeframe
        }
    
    def _load_level_configs(self) -> Dict:
        return {
            'Beginner': {
                'daily_hours': '1.5-2 hours',
                'problems_per_day': 2,
                'theory_practice': '60:40',
                'project_complexity': 'Simple console apps',
                'focus': 'Understanding fundamentals',
                'pace': 'Slow and steady'
            },
            'Intermediate': {
                'daily_hours': '2-3 hours',
                'problems_per_day': 3,
                'theory_practice': '40:60',
                'project_complexity': 'Web apps with databases',
                'focus': 'Problem-solving patterns',
                'pace': 'Moderate with challenges'
            },
            'Advanced': {
                'daily_hours': '3-4 hours',
                'problems_per_day': 5,
                'theory_practice': '20:80',
                'project_complexity': 'Production systems',
                'focus': 'Optimization & architecture',
                'pace': 'Fast-paced hard problems'
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
                '1 month': '3.5 hrs/day: 1hr system design, 2hr challenges, 30min optimization',
                '3 months': '4 hrs/day: 1hr advanced topics, 2.5hr problem solving, 30min review'
            }
        }
    
    def _select_topics(self, subject: str, level: str, weeks: int) -> List[str]:
        topic_map = {
            'machine learning': {
                'Beginner': ['Python Basics', 'NumPy & Pandas', 'Linear Regression'],
                'Intermediate':['ML Algorithms', 'Deep Learning Intro', 'Model Deployment'],
                'Advanced': ['Advanced ML', 'System Design for ML', 'Research Papers']
            },
            'ml': {
                'Beginner': ['Python Basics', 'NumPy & Pandas', 'ML Fundamentals'],
                'Intermediate': ['ML Algorithms', 'Deep Learning', 'Feature Engineering'],
                'Advanced': ['Advanced DL', 'MLOps', 'Production ML']
            },
            'data': {
                'Beginner': ['Python Basics', 'SQL Fundamentals', 'Data Cleaning'],
                'Intermediate': ['Advanced SQL', 'Python Data Analysis', 'ETL Pipelines'],
                'Advanced': ['Data Architecture', 'Big Data Technologies', 'Real-time Processing']
            },
            'web': {
                'Beginner': ['HTML/CSS Basics', 'JavaScript Fundamentals', 'DOM Manipulation'],
                'Intermediate': ['React/Vue Basics', 'REST APIs', 'State Management'],
                'Advanced': ['System Architecture', 'Performance Optimization', 'Microservices']
            },
            'frontend': {
                'Beginner': ['HTML/CSS', 'JavaScript ES6', 'Basic React'],
                'Intermediate': ['Advanced React', 'TypeScript', 'Testing'],
                'Advanced': ['Performance', 'Accessibility', 'Design Systems']
            },
            'backend': {
                'Beginner': ['Python/Node Basics', 'Database Fundamentals', 'REST APIs'],
                'Intermediate': ['Advanced APIs', 'Authentication', 'Caching'],
                'Advanced': ['Microservices', 'Scalability', 'System Design']
            }
        }
        
        for key in topic_map:
            if key in subject:
                return topic_map[key].get(level, [])[:weeks]
        
        # Defaults
        defaults = {
            'Beginner': ['Programming Basics', 'Data Structures'],
            'Intermediate': ['Algorithms', 'System Design Basics'],
            'Advanced': ['Advanced Algorithms', 'Distributed Systems']
        }
        return defaults.get(level, ['Programming Fundamentals'])[:weeks]
    
    def _build_curriculum(self, topics: List[str], level: str, num_weeks: int) -> str:
        if not topics:
            return 'Study consistently with daily practice.'
        
        curriculum_parts = []
        resources_by_level = {
            'Beginner': ['📺 Video tutorials', '📖 Interactive courses', '💻 Guided projects'],
            'Intermediate': ['📚 Advanced tutorials', '🎯 Medium difficulty problems', '🔨 Build real apps'],
            'Advanced': ['📄 Research papers', '⚡ Hard problems', '🏗️ System design']
        }
        
        practice_by_level = {
            'Beginner': ['✅ 2 easy problems/day', '🎯 Complete 5 tutorials', '💡 Build 1 small project'],
            'Intermediate': ['✅ 3 medium problems/day', '🎯 Deep dive exercises', '💡 Build production app'],
            'Advanced': ['✅ 5 hard problems/day', '🎯 System design challenges', '💡 Optimize at scale']
        }
        
        for i, topic in enumerate(topics[:num_weeks], 1):
            week_plan = f"""**Week {i}: {topic}**
📖 Learning Focus:
  • {resources_by_level[level][0]} on {topic}
  • {resources_by_level[level][1]}
💻 Practice:
  • {practice_by_level[level][0]}
  • {practice_by_level[level][1]}
🚀 Milestone: {practice_by_level[level][2]}"""
            curriculum_parts.append(week_plan)
        
        return '\n\n'.join(curriculum_parts)
    
    def _create_milestones(self, subject: str, level: str, timeframe: str, weeks: int) -> str:
        if timeframe == '1 week':
            milestones_map = {
                'Beginner': f'🎯 **Day 1-2:** Grasp {subject} basics\n🎯 **Day 3-5:** Complete 5 tutorials + 10 problems\n🎯 **Day 6-7:** Build mini-project + document learnings',
                'Intermediate': f'🎯 **Day 1-2:** Review + solve 8 medium problems\n🎯 **Day 3-5:** Implement 2 real features\n🎯 **Day 6-7:** Production-ready mini-app',
                'Advanced': f'🎯 **Day 1-2:** Solve 10 hard problems + optimize\n🎯 **Day 3-5:** Design scalable system\n🎯 **Day 6-7:** Performance optimization + tests'
            }
        elif timeframe == '1 month':
            milestones_map = {
                'Beginner': f'🎯 **Week 1:** Master {subject} fundamentals\n🎯 **Week 2:** Build 2 console projects\n🎯 **Week 3:** Solve 30 easy problems\n🎯 **Week 4:** Complete portfolio project',
                'Intermediate': f'🎯 **Week 1-2:** Deep dive + 40 medium problems\n🎯 **Week 3:** Full-stack web application\n🎯 **Week 4:** Mock interviews + 50 total problems',
                'Advanced': f'🎯 **Week 1-2:** 60 hard problems + advanced concepts\n🎯 **Week 3:** System design + contribute to OSS\n🎯 **Week 4:** Interview mastery + 80 total problems'
            }
        else:  # 3 months
            milestones_map = {
                'Beginner': f'🎯 **Month 1:** Fundamentals + 60 easy problems\n🎯 **Month 2:** Intermediate concepts + 3 web apps\n🎯 **Month 3:** Interview prep + 150 total problems',
                'Intermediate': f'🎯 **Month 1:** Advanced {subject} + 80 problems\n🎯 **Month 2:** System design + 4 major projects\n🎯 **Month 3:** FAANG prep + 200 total problems',
                'Advanced': f'🎯 **Month 1:** Expert concepts + 100 hard problems\n🎯 **Month 2:** Distributed systems + research\n🎯 **Month 3:** 250+ problems + production system'
            }
        
        return milestones_map.get(level, 'Focus on consistent progress')
    
    def _generate_tips(self, subject: str, level: str, timeframe: str, config: Dict) -> str:
        base = f"⏰ **Commit:** {config['daily_hours']} daily. "
        
        level_tips = {
            'Beginner': '🎓 Master basics before moving ahead. Use debugger extensively. Document your learning.',
            'Intermediate': '🔥 Build while learning. Focus on patterns. Explain concepts to others.',
            'Advanced': '⚡ Optimize for complexity. Study architecture. Practice whiteboard coding daily.'
        }
        
        time_tips = {
            '1 week': ' 🚀 Sprint mode: Eliminate distractions, deep focus sessions.',
            '1 month': ' 📈 Steady growth: Review weekly, adjust based on progress.',
            '3 months': ' 🏆 Marathon mindset: Build sustainable habits, track metrics.'
        }
        
        return base + level_tips[level] + time_tips[timeframe]
    
    def _suggest_projects(self, subject: str, level: str) -> str:
        project_db = {
            ('machine learning', 'Beginner'): '🚀 **Projects:** Iris classifier → House price predictor → Titanic survival model',
            ('machine learning', 'Intermediate'): '🚀 **Projects:** Image classifier (CNN) → Sentiment analyzer → Chatbot',
            ('machine learning', 'Advanced'): '🚀 **Projects:** Object detection → Recommendation engine → AutoML pipeline',
            ('web', 'Beginner'): '🚀 **Projects:** Portfolio site → Todo app → Weather dashboard',
            ('web', 'Intermediate'): '🚀 **Projects:** Blog with auth → E-commerce → Social media clone',
            ('web', 'Advanced'): '🚀 **Projects:** Real-time collab tool → Microservices → CDN-optimized app',
            ('data', 'Beginner'): '🚀 **Projects:** CSV analyzer → SQLite manager → Data visualizer',
            ('data', 'Intermediate'): '🚀 **Projects:** ETL pipeline → Dashboard with charts → API integration',
            ('data', 'Advanced'): '🚀 **Projects:** Real-time analytics → Data warehouse → Streaming pipeline'
        }
        
        subject_lower = subject.lower()
        for (subj, lvl), project in project_db.items():
            if subj in subject_lower and lvl == level:
                return project
        
        defaults = {
            'Beginner': '🚀 **Projects:** Calculator → CRUD app → Simple game',
            'Intermediate': '🚀 **Projects:** Full-stack app → REST API → Real-time feature',
            'Advanced': '🚀 **Projects:** Scalable service → Distributed system → Production app'
        }
        return defaults.get(level, '🚀 **Projects:** Build practical applications')
    
    def _format_schedule(self, schedule: str, config: Dict) -> str:
        return f"""📅 **Daily Routine:** {schedule}

**📊 Study Mix:** {config['theory_practice']} (Theory:Practice)
**💻 Daily Goals:** {config['problems_per_day']} problems/day
**🎯 Project Type:** {config['project_complexity']}
**🔥 Focus Area:** {config['focus']}"""
    
    def _calculate_hours(self, weeks: int, hours_range: str) -> str:
        try:
            parts = hours_range.split('-')
            avg = (float(parts[0]) + float(parts[1].split()[0])) / 2
            total = int(avg * 7 * weeks)
            return f"⏱️ **Total Time:** ~{total} hours ({avg}hrs/day × {weeks} weeks)"
        except:
            return f"⏱️ **Total Time:** ~{weeks * 14} hours"
