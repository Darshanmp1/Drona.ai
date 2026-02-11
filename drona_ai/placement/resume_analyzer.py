"""
Resume Analyzer Module - Enhanced Version
Analyzes resume text and provides comprehensive feedback including:
- ATS (Applicant Tracking System) Score
- Personalized suggestions based on target role
- Grammar and formatting mistake detection
- Industry-specific keyword optimization
- Detailed improvement recommendations
"""

import re
from typing import Dict, List, Tuple


class ResumeAnalyzer:
    def __init__(self):
        self.technical_keywords = self._load_technical_keywords()
        self.action_verbs = self._load_action_verbs()
        self.weak_phrases = self._load_weak_phrases()
        self.role_keywords = self._load_role_specific_keywords()
        self.required_sections = [
            'education', 'experience', 'skills', 'projects'
        ]
        self.common_mistakes = self._load_common_mistakes()
    
    def _load_technical_keywords(self) -> Dict[str, List[str]]:
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
        return [
            'achieved', 'developed', 'designed', 'implemented', 'created',
            'built', 'led', 'managed', 'improved', 'optimized', 'reduced',
            'increased', 'launched', 'delivered', 'architected', 'engineered',
            'collaborated', 'analyzed', 'streamlined', 'automated', 'spearheaded',
            'executed', 'accelerated', 'enhanced', 'transformed', 'pioneered',
            'established', 'resolved', 'coordinated', 'facilitated', 'generated'
        ]
    
    def _load_weak_phrases(self) -> List[str]:
        return [
            'responsible for', 'worked on', 'helped with', 'was part of',
            'duties included', 'assisted with', 'did', 'made', 'tried to',
            'hard worker', 'team player', 'detail-oriented', 'self-motivated'
        ]
    
    def _load_role_specific_keywords(self) -> Dict[str, List[str]]:
        return {
            'software engineer': [
                'algorithms', 'data structures', 'system design', 'debugging',
                'code review', 'testing', 'ci/cd', 'agile', 'scrum', 'api',
                'microservices', 'scalability', 'performance optimization'
            ],
            'data scientist': [
                'machine learning', 'deep learning', 'statistics', 'modeling',
                'visualization', 'python', 'r', 'sql', 'tensorflow', 'pytorch',
                'data mining', 'predictive analytics', 'feature engineering'
            ],
            'data analyst': [
                'excel', 'sql', 'tableau', 'power bi', 'dashboards', 'reporting',
                'data visualization', 'statistics', 'kpi', 'metrics', 'insights'
            ],
            'frontend developer': [
                'react', 'angular', 'vue', 'html', 'css', 'javascript', 'typescript',
                'responsive design', 'ui/ux', 'webpack', 'accessibility', 'sass'
            ],
            'backend developer': [
                'api', 'database', 'server', 'node.js', 'spring', 'django',
                'rest', 'graphql', 'authentication', 'caching', 'load balancing'
            ],
            'devops': [
                'docker', 'kubernetes', 'jenkins', 'terraform', 'aws', 'azure',
                'ci/cd', 'monitoring', 'logging', 'automation', 'infrastructure'
            ]
        }
    
    def _load_common_mistakes(self) -> List[Dict]:
        return [
            {'pattern': r'\bi\b', 'issue': 'First person pronoun "I"', 'fix': 'Remove "I" - use action verbs directly'},
            {'pattern': r'\bmy\b', 'issue': 'Possessive pronoun "my"', 'fix': 'Remove "my" - make it more professional'},
            {'pattern': r'\breferences available upon request\b', 'issue': 'Outdated phrase', 'fix': 'Remove - this is assumed'},
            {'pattern': r'\b(etc|and so on)\b', 'issue': 'Vague ending', 'fix': 'Be specific instead of using "etc"'},
            {'pattern': r'  +', 'issue': 'Multiple spaces', 'fix': 'Use single space'},
        ]
    
    def analyze(self, resume_text: str, target_role: str = "") -> Dict:
        resume_lower = resume_text.lower()
        
        # Perform comprehensive analysis
        sections_analysis = self._check_sections(resume_lower)
        keywords_analysis = self._analyze_keywords(resume_lower, target_role)
        length_analysis = self._check_length(resume_text)
        formatting_analysis = self._check_formatting(resume_text)
        action_verbs_analysis = self._check_action_verbs(resume_lower)
        ats_analysis = self._calculate_ats_score(resume_text, resume_lower, target_role)
        mistakes = self._detect_mistakes(resume_text, resume_lower)
        quantification = self._check_quantification(resume_text)
        
        # Calculate overall score
        overall_score = self._calculate_score(
            sections_analysis,
            keywords_analysis,
            length_analysis,
            formatting_analysis,
            action_verbs_analysis,
            quantification
        )
        
        # Generate personalized suggestions
        personalized_tips = self._generate_personalized_tips(
            target_role, keywords_analysis, overall_score
        )
        
        return {
            'ats_score': ats_analysis['score'],
            'overall_score': overall_score,
            'sections': sections_analysis,
            'keywords': keywords_analysis,
            'length': length_analysis,
            'formatting': formatting_analysis,
            'action_verbs': action_verbs_analysis,
            'quantification': quantification,
            'mistakes': mistakes,
            'ats_details': ats_analysis,
            'personalized_tips': personalized_tips,
            'suggestions': self._generate_suggestions(resume_lower, overall_score, target_role)
        }
    
    def _check_sections(self, resume_text: str) -> Dict:
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
    
    def _analyze_keywords(self, resume_text: str, target_role: str = "") -> Dict:
        found_keywords = {category: [] for category in self.technical_keywords}
        total_found = 0
        
        for category, keywords in self.technical_keywords.items():
            for keyword in keywords:
                if keyword in resume_text:
                    found_keywords[category].append(keyword)
                    total_found += 1
        
        # Check role-specific keywords
        role_match_score = 0
        missing_role_keywords = []
        if target_role:
            role_lower = target_role.lower()
            role_keywords = self.role_keywords.get(role_lower, [])
            if role_keywords:
                found_role_keywords = [kw for kw in role_keywords if kw in resume_text]
                role_match_score = (len(found_role_keywords) / len(role_keywords)) * 100
                missing_role_keywords = [kw for kw in role_keywords if kw not in resume_text]
        
        return {
            'by_category': found_keywords,
            'total_count': total_found,
            'categories_covered': [cat for cat, kws in found_keywords.items() if kws],
            'role_match_score': role_match_score,
            'missing_role_keywords': missing_role_keywords[:5]  # Top 5 missing
        }
    
    def _check_length(self, resume_text: str) -> Dict:
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
    
    def _calculate_score(self, sections, keywords, length, formatting, action_verbs, quantification) -> int:
        score = 0
        
        # Sections (25 points)
        score += sections['score'] * 0.25
        
        # Keywords (20 points)
        keyword_score = min(20, keywords['total_count'] * 2)
        score += keyword_score
        
        # Length (10 points)
        score += 10 if length['is_optimal'] else 5
        
        # Formatting (20 points)
        formatting_score = sum([
            formatting['has_email'],
            formatting['has_phone'],
            formatting['has_linkedin'],
            formatting['has_github'],
            formatting['has_bullet_points']
        ]) * 4
        score += formatting_score
        
        # Action verbs (15 points)
        action_score = min(15, action_verbs['strong_verbs_count'] * 2)
        score += action_score
        
        # Quantification (10 points)
        score += min(10, quantification['count'] * 2)
        
        return int(score)
    
    def _calculate_ats_score(self, resume_text: str, resume_lower: str, target_role: str = "") -> Dict:
        ats_score = 0
        issues = []
        strengths = []
        
        # 1. Check for standard section headers (20 points)
        standard_headers = ['experience', 'education', 'skills', 'projects', 'summary', 'certifications']
        found_headers = sum(1 for header in standard_headers if header in resume_lower)
        header_score = (found_headers / len(standard_headers)) * 20
        ats_score += header_score
        
        if found_headers >= 4:
            strengths.append("✓ Has standard section headers")
        else:
            issues.append("× Add standard section headers (Education, Experience, Skills)")
        
        # 2. Check for simple formatting (no tables/columns) (15 points)
        has_complex_formatting = '|' in resume_text or '\t' in resume_text
        if not has_complex_formatting:
            ats_score += 15
            strengths.append("✓ Clean, ATS-friendly formatting")
        else:
            issues.append("× Avoid tables and complex formatting - use simple text")
        
        # 3. Check for keywords (25 points)
        keyword_count = len(re.findall(r'\b(python|java|sql|javascript|react|aws|docker|agile|scrum)\b', resume_lower))
        keyword_score = min(25, keyword_count * 3)
        ats_score += keyword_score
        
        if keyword_count >= 5:
            strengths.append(f"✓ Contains {keyword_count} relevant technical keywords")
        else:
            issues.append(f"× Only {keyword_count} technical keywords found - add more relevant skills")
        
        # 4. Check for contact information (15 points)
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text))
        has_phone = bool(re.search(r'\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', resume_text))
        
        if has_email and has_phone:
            ats_score += 15
            strengths.append("✓ Complete contact information")
        else:
            missing = []
            if not has_email: missing.append("email")
            if not has_phone: missing.append("phone")
            issues.append(f"× Missing: {', '.join(missing)}")
        
        # 5. File format compatibility (10 points) - Assume good if we can read it
        ats_score += 10
        strengths.append("✓ File format is readable")
        
        # 6. Check for action verbs (15 points)
        action_verb_count = sum(1 for verb in self.action_verbs if verb in resume_lower)
        verb_score = min(15, action_verb_count * 2)
        ats_score += verb_score
        
        if action_verb_count >= 5:
            strengths.append(f"✓ Uses {action_verb_count} strong action verbs")
        else:
            issues.append("× Use more action verbs (developed, implemented, achieved)")
        
        return {
            'score': int(ats_score),
            'issues': issues,
            'strengths': strengths,
            'recommendation': self._get_ats_recommendation(int(ats_score))
        }
    
    def _get_ats_recommendation(self, score: int) -> str:
        if score >= 80:
            return "🎯 Excellent! Your resume is highly ATS-compatible"
        elif score >= 60:
            return "✓ Good ATS compatibility with room for improvement"
        else:
            return "⚠️ Poor ATS compatibility - high risk of being filtered out"
    
    def _detect_mistakes(self, resume_text: str, resume_lower: str) -> List[Dict]:
        mistakes = []
        
        # Check for common mistakes from database
        for mistake_pattern in self.common_mistakes:
            matches = re.findall(mistake_pattern['pattern'], resume_lower)
            if matches:
                mistakes.append({
                    'type': 'formatting',
                    'issue': mistake_pattern['issue'],
                    'fix': mistake_pattern['fix'],
                    'occurrences': len(matches)
                })
        
        # Check for weak phrases
        for phrase in self.weak_phrases:
            if phrase in resume_lower:
                mistakes.append({
                    'type': 'weak_language',
                    'issue': f'Weak phrase: "{phrase}"',
                    'fix': 'Replace with strong action verb',
                    'occurrences': resume_lower.count(phrase)
                })
        
        # Check for typos in common words
        common_typos = {
            'recieved': 'received', 'managment': 'management',
            'experiance': 'experience', 'responsability': 'responsibility',
            'acheivement': 'achievement', 'analisys': 'analysis'
        }
        for typo, correct in common_typos.items():
            if typo in resume_lower:
                mistakes.append({
                    'type': 'spelling',
                    'issue': f'Spelling error: "{typo}"',
                    'fix': f'Correct spelling: "{correct}"',
                    'occurrences': 1
                })
        
        # Check for inconsistent date formats
        date_formats_found = []
        if re.search(r'\d{4}-\d{4}', resume_text):
            date_formats_found.append('YYYY-YYYY')
        if re.search(r'\d{2}/\d{4}', resume_text):
            date_formats_found.append('MM/YYYY')
        if re.search(r'[A-Za-z]{3}\s+\d{4}', resume_text):
            date_formats_found.append('Mon YYYY')
        
        if len(date_formats_found) > 1:
            mistakes.append({
                'type': 'inconsistency',
                'issue': 'Inconsistent date formats',
                'fix': f'Use one format throughout (found: {", ".join(date_formats_found)})',
                'occurrences': 1
            })
        
        return mistakes
    
    def _check_quantification(self, resume_text: str) -> Dict:
        # Find numbers with context (percentages, dollar amounts, time periods, quantities)
        patterns = [
            r'\d+%',  # 20%, 50%
            r'\$\d+[KMB]?',  # $100K, $5M
            r'\d+\+?\s*(?:years?|months?|weeks?)',  # 5 years, 3+ months
            r'(?:increased|decreased|reduced|improved|grew)\s+(?:by\s+)?\d+',  # increased by 30
            r'\d+[KM]?\+?\s+(?:users|customers|clients|projects)',  # 100K users, 50+ projects
        ]
        
        quantified_achievements = []
        for pattern in patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            quantified_achievements.extend(matches)
        
        count = len(quantified_achievements)
        
        return {
            'count': count,
            'examples': quantified_achievements[:5],  # Top 5 examples
            'has_metrics': count > 0,
            'feedback': f'Found {count} quantified achievements' if count > 0 else 'Add numbers and metrics to show impact'
        }
    
    def _generate_personalized_tips(self, target_role: str, keywords_analysis: Dict, score: int) -> List[str]:
        tips = []
        
        if not target_role:
            tips.append("💡 Pro tip: Enter a target role (e.g., 'Software Engineer') for personalized suggestions")
            return tips
        
        role_lower = target_role.lower()
        
        # Role-specific tips
        if 'software' in role_lower or 'developer' in role_lower or 'engineer' in role_lower:
            tips.append("🎯 For Software Engineer roles:")
            tips.append("  • Include 2-3 technical projects with GitHub links")
            tips.append("  • Highlight specific technologies (React, Python, AWS, etc.)")
            tips.append("  • Quantify impact (reduced load time by 40%, improved performance by 2x)")
            tips.append("  • Mention code quality practices (testing, code review, CI/CD)")
        
        elif 'data scientist' in role_lower or 'machine learning' in role_lower:
            tips.append("🎯 For Data Science roles:")
            tips.append("  • Showcase ML projects with metrics (accuracy, F1 score, ROC-AUC)")
            tips.append("  • List specific libraries (TensorFlow, PyTorch, scikit-learn)")
            tips.append("  • Include Kaggle profile or competition rankings if applicable")
            tips.append("  • Mention business impact of your models")
        
        elif 'data analyst' in role_lower:
            tips.append("🎯 For Data Analyst roles:")
            tips.append("  • Highlight dashboard and reporting tools (Tableau, Power BI)")
            tips.append("  • Showcase SQL proficiency with complex query examples")
            tips.append("  • Include examples of insights that drove business decisions")
            tips.append("  • Mention stakeholder collaboration and presentation skills")
        
        # Add missing keyword suggestions
        if keywords_analysis.get('missing_role_keywords'):
            missing = keywords_analysis['missing_role_keywords']
            tips.append(f"\n📌 Consider adding these {target_role} keywords:")
            for keyword in missing:
                tips.append(f"  • {keyword}")
        
        return tips
    
    def _generate_suggestions(self, resume_text: str, score: int, target_role: str = "") -> List[str]:
        suggestions = []
        
        # Score-based priority suggestions
        if score < 50:
            suggestions.append("🚨 CRITICAL: Your resume needs major improvements to pass ATS screening")
            suggestions.append("Priority: Fix missing sections, add contact info, include technical keywords")
        elif score < 70:
            suggestions.append("⚠️ Your resume has potential but needs improvement to be competitive")
            suggestions.append("Focus on: Adding metrics, using stronger action verbs, improving formatting")
        else:
            suggestions.append("✓ Strong resume! Fine-tune these areas for maximum impact:")
        
        # Specific actionable suggestions (prioritized)
        suggestions.extend([
            "",
            "📝 Content Improvements:",
            "  1. Start EVERY bullet point with a strong action verb (Developed, Implemented, Led)",
            "  2. Add numbers to show impact: 'Increased efficiency by 40%', 'Managed team of 5'",
            "  3. Follow the STAR method: Situation, Task, Action, Result",
            "  4. Remove weak phrases: 'responsible for', 'worked on', 'helped with'",
            "",
            "🎯 ATS Optimization:",
            "  • Use standard section headers (Education, Experience, Skills, Projects)",
            "  • Include relevant keywords from job description (copy exact terms)",
            "  • Avoid tables, text boxes, headers/footers - use simple text format",
            "  • Save as .docx or .pdf (NOT scanned image PDF)",
            "",
            "✨ Formatting Best Practices:",
            "  • Use consistent date format throughout (e.g., Jan 2023 - Present)",
            "  • Keep font size 10-12pt, use standard fonts (Arial, Calibri, Times New Roman)",
            "  • Maintain 0.5-1 inch margins on all sides",
            "  • Use bullet points, not paragraphs",
            "",
            "🚀 Make It Stand Out:",
            "  • Add a 2-3 line summary at top highlighting your value proposition",
            "  • Include links: GitHub, LinkedIn, portfolio website",
            "  • Tailor resume for each application (customize keywords)",
            "  • List most relevant/impressive experience first",
            "",
            "❌ What to Remove:",
            "  • Objective statement (outdated - use summary instead)",
            "  • Personal info: photo, age, marital status, religion",
            "  • 'References available upon request' (assumed)",
            "  • Soft skills without proof (use examples instead)",
            "",
            "✅ Final Checklist:",
            "  ☐ Proofread 3 times (zero typos allowed)",
            "  ☐ Have someone else review it",
            "  ☐ Test with ATS checker tools online",
            "  ☐ Customize for each job application",
            "  ☐ Keep it to 1-2 pages maximum"
        ])
        
        return suggestions
    
    def get_quick_tips(self) -> List[str]:
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
