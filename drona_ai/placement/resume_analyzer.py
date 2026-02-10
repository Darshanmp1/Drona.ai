"""
Resume Analyzer Module
Analyzes resume text and provides suggestions for improvement.
Checks for key sections, keywords, and formatting issues.
"""

import re
from typing import Dict, List


class ResumeAnalyzer:
    """
    Analyzes resume content and provides feedback and suggestions.
    Helps users improve their resumes for better interview chances.
    """
    
    def __init__(self):
        """Initialize resume analyzer with keyword banks."""
        self.technical_keywords = self._load_technical_keywords()
        self.action_verbs = self._load_action_verbs()
        self.required_sections = [
            'education', 'experience', 'skills', 'projects'
        ]
    
    def _load_technical_keywords(self) -> Dict[str, List[str]]:
        """
        Load technical keywords by category.
        
        Returns:
            Dictionary of keywords by category
        """
        return {
            'programming': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go',
                'typescript', 'php', 'swift', 'kotlin', 'rust', 'scala'
            ],
            'web': [
                'react', 'angular', 'vue', 'node.js', 'express', 'django',
                'flask', 'spring', 'html', 'css', 'rest api', 'graphql'
            ],
            'data': [
                'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
                'data analysis', 'pandas', 'numpy', 'machine learning', 'tensorflow'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
                'ci/cd', 'terraform', 'cloudformation'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'jira', 'agile', 'scrum',
                'linux', 'bash', 'vim'
            ]
        }
    
    def _load_action_verbs(self) -> List[str]:
        """
        Load strong action verbs for resume bullet points.
        
        Returns:
            List of action verbs
        """
        return [
            'achieved', 'developed', 'designed', 'implemented', 'created',
            'built', 'led', 'managed', 'improved', 'optimized', 'reduced',
            'increased', 'launched', 'delivered', 'architected', 'engineered',
            'collaborated', 'analyzed', 'streamlined', 'automated', 'spearheaded'
        ]
    
    def analyze(self, resume_text: str) -> Dict:
        """
        Perform comprehensive resume analysis.
        
        Args:
            resume_text: Full resume text content
            
        Returns:
            Dictionary with analysis results and suggestions
        """
        resume_lower = resume_text.lower()
        
        # Perform various checks
        sections_analysis = self._check_sections(resume_lower)
        keywords_analysis = self._analyze_keywords(resume_lower)
        length_analysis = self._check_length(resume_text)
        formatting_analysis = self._check_formatting(resume_text)
        action_verbs_analysis = self._check_action_verbs(resume_lower)
        
        # Calculate overall score
        overall_score = self._calculate_score(
            sections_analysis,
            keywords_analysis,
            length_analysis,
            formatting_analysis,
            action_verbs_analysis
        )
        
        return {
            'overall_score': overall_score,
            'sections': sections_analysis,
            'keywords': keywords_analysis,
            'length': length_analysis,
            'formatting': formatting_analysis,
            'action_verbs': action_verbs_analysis,
            'suggestions': self._generate_suggestions(resume_lower, overall_score)
        }
    
    def _check_sections(self, resume_text: str) -> Dict:
        """
        Check if resume contains essential sections.
        
        Args:
            resume_text: Resume text (lowercase)
            
        Returns:
            Dictionary with section analysis
        """
        found_sections = []
        missing_sections = []
        
        for section in self.required_sections:
            if section in resume_text:
                found_sections.append(section)
            else:
                missing_sections.append(section)
        
        return {
            'found': found_sections,
            'missing': missing_sections,
            'score': len(found_sections) / len(self.required_sections) * 100
        }
    
    def _analyze_keywords(self, resume_text: str) -> Dict:
        """
        Analyze technical keywords present in resume.
        
        Args:
            resume_text: Resume text (lowercase)
            
        Returns:
            Dictionary with keyword analysis
        """
        found_keywords = {category: [] for category in self.technical_keywords}
        total_found = 0
        
        for category, keywords in self.technical_keywords.items():
            for keyword in keywords:
                if keyword in resume_text:
                    found_keywords[category].append(keyword)
                    total_found += 1
        
        return {
            'by_category': found_keywords,
            'total_count': total_found,
            'categories_covered': [cat for cat, kws in found_keywords.items() if kws]
        }
    
    def _check_length(self, resume_text: str) -> Dict:
        """
        Check resume length and word count.
        
        Args:
            resume_text: Resume text
            
        Returns:
            Dictionary with length analysis
        """
        words = resume_text.split()
        word_count = len(words)
        
        # Ideal range: 400-800 words (roughly 1-2 pages)
        if word_count < 300:
            feedback = "Resume is too short. Add more details about your experience."
        elif word_count > 1000:
            feedback = "Resume is too long. Try to be more concise."
        else:
            feedback = "Resume length is good."
        
        return {
            'word_count': word_count,
            'feedback': feedback,
            'is_optimal': 300 <= word_count <= 1000
        }
    
    def _check_formatting(self, resume_text: str) -> Dict:
        """
        Check formatting elements in resume.
        
        Args:
            resume_text: Resume text
            
        Returns:
            Dictionary with formatting analysis
        """
        # Check for various formatting elements
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text))
        has_phone = bool(re.search(r'\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', resume_text))
        has_linkedin = 'linkedin' in resume_text.lower()
        has_github = 'github' in resume_text.lower()
        has_bullet_points = '•' in resume_text or '-' in resume_text
        
        issues = []
        if not has_email:
            issues.append("Add your email address")
        if not has_phone:
            issues.append("Add your phone number")
        if not has_linkedin:
            issues.append("Consider adding LinkedIn profile")
        if not has_github:
            issues.append("Consider adding GitHub profile (for tech roles)")
        if not has_bullet_points:
            issues.append("Use bullet points for better readability")
        
        return {
            'has_email': has_email,
            'has_phone': has_phone,
            'has_linkedin': has_linkedin,
            'has_github': has_github,
            'has_bullet_points': has_bullet_points,
            'issues': issues
        }
    
    def _check_action_verbs(self, resume_text: str) -> Dict:
        """
        Check usage of strong action verbs.
        
        Args:
            resume_text: Resume text (lowercase)
            
        Returns:
            Dictionary with action verb analysis
        """
        found_verbs = []
        
        for verb in self.action_verbs:
            if verb in resume_text:
                found_verbs.append(verb)
        
        weak_verbs = ['did', 'made', 'worked on', 'was responsible for', 'helped with']
        found_weak = [verb for verb in weak_verbs if verb in resume_text]
        
        return {
            'strong_verbs_found': found_verbs,
            'strong_verbs_count': len(found_verbs),
            'weak_verbs_found': found_weak,
            'recommendation': 'Good use of action verbs!' if len(found_verbs) >= 5 else 'Use more strong action verbs'
        }
    
    def _calculate_score(self, sections, keywords, length, formatting, action_verbs) -> int:
        """
        Calculate overall resume score (0-100).
        
        Args:
            Various analysis results
            
        Returns:
            Overall score as integer
        """
        score = 0
        
        # Sections (30 points)
        score += sections['score'] * 0.3
        
        # Keywords (20 points)
        keyword_score = min(20, keywords['total_count'] * 2)
        score += keyword_score
        
        # Length (10 points)
        score += 10 if length['is_optimal'] else 5
        
        # Formatting (25 points)
        formatting_score = sum([
            formatting['has_email'],
            formatting['has_phone'],
            formatting['has_linkedin'],
            formatting['has_github'],
            formatting['has_bullet_points']
        ]) * 5
        score += formatting_score
        
        # Action verbs (15 points)
        action_score = min(15, action_verbs['strong_verbs_count'] * 2)
        score += action_score
        
        return int(score)
    
    def _generate_suggestions(self, resume_text: str, score: int) -> List[str]:
        """
        Generate improvement suggestions based on analysis.
        
        Args:
            resume_text: Resume text (lowercase)
            score: Overall score
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Score-based suggestions
        if score < 50:
            suggestions.append("⚠️ Your resume needs significant improvement. Focus on adding key sections and technical skills.")
        elif score < 70:
            suggestions.append("📝 Your resume is decent but has room for improvement. See specific suggestions below.")
        else:
            suggestions.append("✓ Your resume looks good! Fine-tune based on the suggestions below.")
        
        # Specific suggestions
        suggestions.extend([
            "Start bullet points with strong action verbs (achieved, developed, implemented)",
            "Quantify your achievements with numbers and metrics",
            "Tailor your resume to the specific job you're applying for",
            "Keep formatting clean and consistent throughout",
            "Proofread carefully for spelling and grammar errors",
            "Include relevant technical keywords for ATS (Applicant Tracking Systems)",
            "List your most impressive/relevant experience first"
        ])
        
        return suggestions
    
    def get_quick_tips(self) -> List[str]:
        """
        Get general resume tips.
        
        Returns:
            List of tips
        """
        return [
            "1. Keep it concise: 1-2 pages maximum",
            "2. Use action verbs: developed, implemented, achieved, etc.",
            "3. Quantify results: 'Increased efficiency by 30%'",
            "4. Tailor for each job: Match keywords from job description",
            "5. No typos: Proofread multiple times",
            "6. Clean format: Consistent fonts, spacing, and style",
            "7. Include projects: Especially for students/recent grads",
            "8. Add links: LinkedIn, GitHub, portfolio website",
            "9. Skills section: List relevant technical skills",
            "10. Keep it honest: Don't exaggerate or lie"
        ]
