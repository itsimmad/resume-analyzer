"""
Job matching module for matching resumes to Dubai job listings.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


class JobMatcher:
    """Matches resumes to job listings using various algorithms."""
    
    def __init__(self, jobs_data: pd.DataFrame = None):
        """
        Initialize the job matcher.
        
        Args:
            jobs_data (pd.DataFrame): Job listings data
        """
        self.jobs_data = jobs_data or self._load_default_jobs()
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
        self._prepare_jobs_data()
    
    def _load_default_jobs(self) -> pd.DataFrame:
        """Load default Dubai job listings."""
        # Create sample Dubai job data
        jobs = [
            {
                'title': 'Senior Software Engineer',
                'company': 'TechCorp Dubai',
                'location': 'Dubai, UAE',
                'salary': 'AED 25,000 - 35,000',
                'experience': '5-8 years',
                'description': 'We are looking for a Senior Software Engineer with expertise in Python, JavaScript, and cloud technologies. Experience with AWS, Docker, and microservices architecture is required.',
                'requirements': 'Python, JavaScript, AWS, Docker, Microservices, React, Node.js, MongoDB, PostgreSQL',
                'job_type': 'Full-time',
                'industry': 'Technology'
            },
            {
                'title': 'Data Scientist',
                'company': 'DataFlow Analytics',
                'location': 'Dubai, UAE',
                'salary': 'AED 20,000 - 30,000',
                'experience': '3-6 years',
                'description': 'Join our data science team to develop machine learning models and analytics solutions. Work with large datasets and implement predictive models.',
                'requirements': 'Python, Machine Learning, Statistics, SQL, Pandas, Scikit-learn, TensorFlow, Data Analysis',
                'job_type': 'Full-time',
                'industry': 'Technology'
            },
            {
                'title': 'Marketing Manager',
                'company': 'Global Marketing Solutions',
                'location': 'Dubai, UAE',
                'salary': 'AED 18,000 - 25,000',
                'experience': '4-7 years',
                'description': 'Lead marketing campaigns and strategies for our clients in the MENA region. Experience in digital marketing and brand management required.',
                'requirements': 'Digital Marketing, Brand Management, Social Media, Google Ads, Analytics, Campaign Management',
                'job_type': 'Full-time',
                'industry': 'Marketing'
            },
            {
                'title': 'Financial Analyst',
                'company': 'Dubai Financial Services',
                'location': 'Dubai, UAE',
                'salary': 'AED 15,000 - 22,000',
                'experience': '2-5 years',
                'description': 'Analyze financial data, prepare reports, and provide insights for investment decisions. CFA or similar certification preferred.',
                'requirements': 'Financial Analysis, Excel, Financial Modeling, CFA, Investment Analysis, Risk Management',
                'job_type': 'Full-time',
                'industry': 'Finance'
            },
            {
                'title': 'UX/UI Designer',
                'company': 'Creative Design Studio',
                'location': 'Dubai, UAE',
                'salary': 'AED 16,000 - 24,000',
                'experience': '3-6 years',
                'description': 'Create user-centered designs for web and mobile applications. Experience with design tools and user research methods required.',
                'requirements': 'Figma, Adobe Creative Suite, User Research, Prototyping, Wireframing, Design Systems',
                'job_type': 'Full-time',
                'industry': 'Design'
            },
            {
                'title': 'Project Manager',
                'company': 'Construction Solutions Ltd',
                'location': 'Dubai, UAE',
                'salary': 'AED 20,000 - 28,000',
                'experience': '5-8 years',
                'description': 'Manage construction projects from inception to completion. PMP certification and experience in the UAE market preferred.',
                'requirements': 'Project Management, PMP, Construction, Budget Management, Team Leadership, Risk Management',
                'job_type': 'Full-time',
                'industry': 'Construction'
            },
            {
                'title': 'Sales Executive',
                'company': 'Dubai Trading Company',
                'location': 'Dubai, UAE',
                'salary': 'AED 8,000 - 15,000',
                'experience': '1-3 years',
                'description': 'Generate new business opportunities and maintain relationships with existing clients. Strong communication skills required.',
                'requirements': 'Sales, Customer Relationship Management, Communication, Negotiation, B2B Sales',
                'job_type': 'Full-time',
                'industry': 'Sales'
            },
            {
                'title': 'Human Resources Specialist',
                'company': 'HR Solutions UAE',
                'location': 'Dubai, UAE',
                'salary': 'AED 12,000 - 18,000',
                'experience': '3-5 years',
                'description': 'Handle recruitment, employee relations, and HR operations. Knowledge of UAE labor law required.',
                'requirements': 'HR Management, Recruitment, Employee Relations, UAE Labor Law, HRIS, Performance Management',
                'job_type': 'Full-time',
                'industry': 'Human Resources'
            },
            {
                'title': 'Business Development Manager',
                'company': 'Innovation Hub Dubai',
                'location': 'Dubai, UAE',
                'salary': 'AED 22,000 - 32,000',
                'experience': '4-7 years',
                'description': 'Develop strategic partnerships and identify new business opportunities in the technology sector.',
                'requirements': 'Business Development, Strategic Partnerships, Market Analysis, Negotiation, Technology Industry',
                'job_type': 'Full-time',
                'industry': 'Business Development'
            },
            {
                'title': 'Content Writer',
                'company': 'Digital Content Agency',
                'location': 'Dubai, UAE',
                'salary': 'AED 8,000 - 12,000',
                'experience': '2-4 years',
                'description': 'Create engaging content for websites, blogs, and social media platforms. Experience in SEO and content marketing preferred.',
                'requirements': 'Content Writing, SEO, Social Media, Copywriting, Content Marketing, WordPress',
                'job_type': 'Full-time',
                'industry': 'Marketing'
            }
        ]
        
        return pd.DataFrame(jobs)
    
    def _prepare_jobs_data(self):
        """Prepare job data for matching."""
        if self.jobs_data is not None and not self.jobs_data.empty:
            # Combine text fields for vectorization
            self.jobs_data['combined_text'] = (
                self.jobs_data['title'].fillna('') + ' ' +
                self.jobs_data['description'].fillna('') + ' ' +
                self.jobs_data['requirements'].fillna('') + ' ' +
                self.jobs_data['company'].fillna('')
            )
            
            # Create TF-IDF vectors for jobs
            try:
                self.job_vectors = self.vectorizer.fit_transform(self.jobs_data['combined_text'])
            except:
                # Fallback if vectorization fails
                self.job_vectors = None
    
    def match_resume_to_jobs(self, resume_data: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Match resume to job listings.
        
        Args:
            resume_data (Dict[str, Any]): Parsed resume data
            top_n (int): Number of top matches to return
            
        Returns:
            List[Dict[str, Any]]: Top job matches with scores
        """
        if self.jobs_data is None or self.jobs_data.empty:
            return []
        
        # Prepare resume text for matching
        resume_text = self._prepare_resume_text(resume_data)
        
        # Calculate matching scores
        matches = []
        
        for idx, job in self.jobs_data.iterrows():
            score = self._calculate_job_match_score(resume_text, job)
            
            match_info = {
                'job_id': idx,
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'salary': job['salary'],
                'experience': job['experience'],
                'description': job['description'],
                'requirements': job['requirements'],
                'job_type': job['job_type'],
                'industry': job['industry'],
                'match_score': score,
                'match_percentage': round(score * 100, 1)
            }
            
            matches.append(match_info)
        
        # Sort by match score and return top matches
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches[:top_n]
    
    def _prepare_resume_text(self, resume_data: Dict[str, Any]) -> str:
        """Prepare resume text for matching."""
        text_parts = []
        
        # Add name
        if resume_data.get('name'):
            text_parts.append(resume_data['name'])
        
        # Add summary
        if resume_data.get('summary'):
            text_parts.append(resume_data['summary'])
        
        # Add skills
        if resume_data.get('skills'):
            text_parts.extend(resume_data['skills'])
        
        # Add experience descriptions
        for exp in resume_data.get('experience', []):
            if isinstance(exp, dict):
                text_parts.append(exp.get('title', ''))
                text_parts.append(exp.get('description', ''))
            else:
                text_parts.append(str(exp))
        
        # Add education
        for edu in resume_data.get('education', []):
            if isinstance(edu, dict):
                text_parts.append(edu.get('degree', ''))
                text_parts.append(edu.get('institution', ''))
            else:
                text_parts.append(str(edu))
        
        # Add projects
        for proj in resume_data.get('projects', []):
            if isinstance(proj, dict):
                text_parts.append(proj.get('title', ''))
                text_parts.append(proj.get('description', ''))
            else:
                text_parts.append(str(proj))
        
        # Add raw text
        if resume_data.get('raw_text'):
            text_parts.append(resume_data['raw_text'])
        
        return ' '.join(text_parts)
    
    def _calculate_job_match_score(self, resume_text: str, job: pd.Series) -> float:
        """
        Calculate match score between resume and job.
        
        Args:
            resume_text (str): Resume text
            job (pd.Series): Job information
            
        Returns:
            float: Match score (0-1)
        """
        score = 0.0
        
        # Keyword matching (40% weight)
        keyword_score = self._calculate_keyword_score(resume_text, job)
        score += keyword_score * 0.4
        
        # Title matching (20% weight)
        title_score = self._calculate_title_match(resume_text, job['title'])
        score += title_score * 0.2
        
        # Skills matching (25% weight)
        skills_score = self._calculate_skills_match(resume_text, job['requirements'])
        score += skills_score * 0.25
        
        # Experience level matching (15% weight)
        experience_score = self._calculate_experience_match(resume_text, job['experience'])
        score += experience_score * 0.15
        
        return min(1.0, max(0.0, score))
    
    def _calculate_keyword_score(self, resume_text: str, job: pd.Series) -> float:
        """Calculate keyword matching score."""
        # Extract keywords from job requirements
        requirements = job['requirements'].lower()
        keywords = re.findall(r'\b\w+\b', requirements)
        
        if not keywords:
            return 0.0
        
        # Count matches in resume
        resume_lower = resume_text.lower()
        matches = sum(1 for keyword in keywords if keyword in resume_lower)
        
        return matches / len(keywords)
    
    def _calculate_title_match(self, resume_text: str, job_title: str) -> float:
        """Calculate title matching score."""
        # Extract job title keywords
        title_keywords = re.findall(r'\b\w+\b', job_title.lower())
        
        if not title_keywords:
            return 0.0
        
        # Check for title matches in resume
        resume_lower = resume_text.lower()
        matches = sum(1 for keyword in title_keywords if keyword in resume_lower)
        
        return matches / len(title_keywords)
    
    def _calculate_skills_match(self, resume_text: str, job_requirements: str) -> float:
        """Calculate skills matching score."""
        # Common technical skills
        technical_skills = [
            'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
            'flask', 'spring', 'laravel', 'sql', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'jenkins',
            'machine learning', 'ai', 'data science', 'analytics', 'tableau',
            'excel', 'power bi', 'spark', 'hadoop', 'tensorflow', 'pytorch'
        ]
        
        # Extract skills from job requirements
        req_lower = job_requirements.lower()
        job_skills = [skill for skill in technical_skills if skill in req_lower]
        
        if not job_skills:
            return 0.0
        
        # Check for skill matches in resume
        resume_lower = resume_text.lower()
        matches = sum(1 for skill in job_skills if skill in resume_lower)
        
        return matches / len(job_skills)
    
    def _calculate_experience_match(self, resume_text: str, job_experience: str) -> float:
        """Calculate experience level matching score."""
        # Extract years from job experience requirement
        exp_match = re.search(r'(\d+)[\-\s]*(\d+)?\s*years?', job_experience.lower())
        if not exp_match:
            return 0.5  # Default score if no experience requirement found
        
        min_years = int(exp_match.group(1))
        max_years = int(exp_match.group(2)) if exp_match.group(2) else min_years + 2
        
        # Look for experience indicators in resume
        experience_indicators = [
            'years of experience', 'years experience', 'worked for', 'employed for',
            'experience in', 'professional experience', 'work history'
        ]
        
        resume_lower = resume_text.lower()
        has_experience = any(indicator in resume_lower for indicator in experience_indicators)
        
        if not has_experience:
            return 0.0
        
        # Simple scoring based on experience presence
        return 0.8  # Assume candidate has some experience
    
    def get_job_details(self, job_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific job.
        
        Args:
            job_id (int): Job ID
            
        Returns:
            Dict[str, Any]: Job details
        """
        if self.jobs_data is None or job_id >= len(self.jobs_data):
            return {}
        
        job = self.jobs_data.iloc[job_id]
        return {
            'title': job['title'],
            'company': job['company'],
            'location': job['location'],
            'salary': job['salary'],
            'experience': job['experience'],
            'description': job['description'],
            'requirements': job['requirements'],
            'job_type': job['job_type'],
            'industry': job['industry']
        }
    
    def search_jobs(self, query: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Search jobs by query.
        
        Args:
            query (str): Search query
            top_n (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: Matching jobs
        """
        if self.jobs_data is None or self.jobs_data.empty:
            return []
        
        query_lower = query.lower()
        matches = []
        
        for idx, job in self.jobs_data.iterrows():
            # Check if query matches job title, company, or description
            title_match = query_lower in job['title'].lower()
            company_match = query_lower in job['company'].lower()
            desc_match = query_lower in job['description'].lower()
            req_match = query_lower in job['requirements'].lower()
            
            if title_match or company_match or desc_match or req_match:
                match_info = {
                    'job_id': idx,
                    'title': job['title'],
                    'company': job['company'],
                    'location': job['location'],
                    'salary': job['salary'],
                    'experience': job['experience'],
                    'description': job['description'],
                    'requirements': job['requirements'],
                    'job_type': job['job_type'],
                    'industry': job['industry']
                }
                matches.append(match_info)
        
        return matches[:top_n]
    
    def get_jobs_by_industry(self, industry: str) -> List[Dict[str, Any]]:
        """
        Get jobs filtered by industry.
        
        Args:
            industry (str): Industry name
            
        Returns:
            List[Dict[str, Any]]: Jobs in the specified industry
        """
        if self.jobs_data is None or self.jobs_data.empty:
            return []
        
        industry_jobs = self.jobs_data[
            self.jobs_data['industry'].str.lower() == industry.lower()
        ]
        
        return industry_jobs.to_dict('records')
    
    def get_available_industries(self) -> List[str]:
        """
        Get list of available industries.
        
        Returns:
            List[str]: List of industries
        """
        if self.jobs_data is None or self.jobs_data.empty:
            return []
        
        return self.jobs_data['industry'].unique().tolist() 