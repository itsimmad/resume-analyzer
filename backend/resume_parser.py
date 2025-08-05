"""
Resume parser for extracting text and structure from PDF and DOCX files.
"""

import pdfplumber
import fitz  # PyMuPDF
from docx import Document
import re
import spacy
from typing import Dict, List, Any, Optional
import os


class ResumeParser:
    """Parses resumes from PDF and DOCX files and extracts structured information."""
    
    def __init__(self):
        # Load spaCy models for both languages
        try:
            self.nlp_en = spacy.load("en_core_web_sm")
        except:
            self.nlp_en = None
            
        # Arabic model might not be available for all spaCy versions
        try:
            self.nlp_ar = spacy.load("ar_core_news_sm")
        except:
            # Fallback: try to use English model for Arabic text
            self.nlp_ar = self.nlp_en
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume file and extract structured information.
        
        Args:
            file_path (str): Path to the resume file
            
        Returns:
            Dict[str, Any]: Structured resume data
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self._parse_pdf(file_path)
        elif file_extension == '.docx':
            return self._parse_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please upload PDF or DOCX.")
    
    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Parse PDF resume using multiple methods for better extraction."""
        text = ""
        
        # Try pdfplumber first
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except:
            pass
        
        # If pdfplumber fails, try PyMuPDF
        if not text.strip():
            try:
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text() + "\n"
                doc.close()
            except:
                pass
        
        return self._extract_structure(text)
    
    def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Parse DOCX resume."""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return self._extract_structure(text)
        except Exception as e:
            raise ValueError(f"Error parsing DOCX file: {str(e)}")
    
    def _extract_structure(self, text: str) -> Dict[str, Any]:
        """
        Extract structured information from resume text.
        
        Args:
            text (str): Raw resume text
            
        Returns:
            Dict[str, Any]: Structured resume data
        """
        # Clean and normalize text
        text = self._clean_text(text)
        
        # Extract different sections
        resume_data = {
            'raw_text': text,
            'contact_info': self._extract_contact_info(text),
            'name': self._extract_name(text),
            'summary': self._extract_summary(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'skills': self._extract_skills(text),
            'languages': self._extract_languages(text),
            'certifications': self._extract_certifications(text),
            'projects': self._extract_projects(text)
        }
        
        return resume_data
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep Arabic and English
        text = re.sub(r'[^\w\s\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\-\.\,\;\:\!\?\(\)]', '', text)
        return text.strip()
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information."""
        contact_info = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Phone (multiple formats)
        phone_patterns = [
            r'\+?[\d\s\-\(\)]{10,}',  # International format
            r'[\d\s\-\(\)]{10,}',     # Local format
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact_info['phone'] = phone_match.group().strip()
                break
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
        linkedin_match = re.search(linkedin_pattern, text)
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group()
        
        return contact_info
    
    def _extract_name(self, text: str) -> str:
        """Extract candidate name."""
        # Look for name at the beginning of the document
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4:  # Name should be 1-4 words
                # Check if it doesn't contain typical resume keywords
                keywords = ['resume', 'cv', 'curriculum', 'vitae', 'experience', 'education', 'skills']
                if not any(keyword.lower() in line.lower() for keyword in keywords):
                    return line
        return ""
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary."""
        # Look for summary section
        summary_patterns = [
            r'summary[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)',
            r'objective[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)',
            r'profile[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)',
            r'ملخص[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)',
            r'الهدف[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience."""
        experience = []
        
        # Look for experience section
        exp_patterns = [
            r'experience[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'work history[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'employment[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'الخبرة[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'العمل[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                exp_text = match.group(1)
                # Parse individual experiences
                exp_entries = self._parse_experience_entries(exp_text)
                experience.extend(exp_entries)
                break
        
        return experience
    
    def _parse_experience_entries(self, exp_text: str) -> List[Dict[str, str]]:
        """Parse individual experience entries."""
        entries = []
        lines = exp_text.split('\n')
        
        current_entry = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    entries.append(current_entry)
                    current_entry = {}
                continue
            
            # Look for job title patterns
            if re.search(r'(senior|junior|lead|manager|director|engineer|developer|analyst|consultant)', line, re.IGNORECASE):
                if current_entry:
                    entries.append(current_entry)
                current_entry = {'title': line}
            elif current_entry and 'title' in current_entry:
                # Add to description
                if 'description' not in current_entry:
                    current_entry['description'] = line
                else:
                    current_entry['description'] += ' ' + line
        
        if current_entry:
            entries.append(current_entry)
        
        return entries
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information."""
        education = []
        
        # Look for education section
        edu_patterns = [
            r'education[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'academic[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'التعليم[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'الدراسة[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)'
        ]
        
        for pattern in edu_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                edu_text = match.group(1)
                # Parse education entries
                edu_entries = self._parse_education_entries(edu_text)
                education.extend(edu_entries)
                break
        
        return education
    
    def _parse_education_entries(self, edu_text: str) -> List[Dict[str, str]]:
        """Parse individual education entries."""
        entries = []
        lines = edu_text.split('\n')
        
        current_entry = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    entries.append(current_entry)
                    current_entry = {}
                continue
            
            # Look for degree patterns
            if re.search(r'(bachelor|master|phd|diploma|certificate|degree)', line, re.IGNORECASE):
                if current_entry:
                    entries.append(current_entry)
                current_entry = {'degree': line}
            elif current_entry and 'degree' in current_entry:
                # Add to institution
                if 'institution' not in current_entry:
                    current_entry['institution'] = line
                else:
                    current_entry['institution'] += ' ' + line
        
        if current_entry:
            entries.append(current_entry)
        
        return entries
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume."""
        skills = []
        
        # Look for skills section
        skills_patterns = [
            r'skills[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'technical skills[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'competencies[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'المهارات[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'الخبرات[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)'
        ]
        
        for pattern in skills_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                skills_text = match.group(1)
                # Extract individual skills
                skills = self._parse_skills_list(skills_text)
                break
        
        return skills
    
    def _parse_skills_list(self, skills_text: str) -> List[str]:
        """Parse skills from text."""
        skills = []
        
        # Split by common delimiters
        skill_patterns = [
            r'[,\n;]',  # Comma, newline, semicolon
            r'\s+and\s+',  # "and" separator
            r'\s+&\s+',    # "&" separator
        ]
        
        for pattern in skill_patterns:
            if re.search(pattern, skills_text):
                skill_list = re.split(pattern, skills_text)
                skills = [skill.strip() for skill in skill_list if skill.strip()]
                break
        
        if not skills:
            # If no delimiters found, try to extract individual skills
            words = skills_text.split()
            skills = [word.strip() for word in words if len(word.strip()) > 2]
        
        return skills[:20]  # Limit to 20 skills
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extract language skills."""
        languages = []
        
        # Common language patterns
        lang_patterns = [
            r'languages[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'اللغات[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)'
        ]
        
        for pattern in lang_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                lang_text = match.group(1)
                languages = self._parse_skills_list(lang_text)
                break
        
        return languages
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications."""
        certifications = []
        
        # Look for certifications section
        cert_patterns = [
            r'certifications[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'certificates[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'الشهادات[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)'
        ]
        
        for pattern in cert_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                cert_text = match.group(1)
                certifications = self._parse_skills_list(cert_text)
                break
        
        return certifications
    
    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract projects information."""
        projects = []
        
        # Look for projects section
        proj_patterns = [
            r'projects[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)',
            r'المشاريع[:\s]*(.*?)(?=\n\s*\n\s*[A-Z]|$)'
        ]
        
        for pattern in proj_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                proj_text = match.group(1)
                # Parse project entries
                projects = self._parse_project_entries(proj_text)
                break
        
        return projects
    
    def _parse_project_entries(self, proj_text: str) -> List[Dict[str, str]]:
        """Parse individual project entries."""
        entries = []
        lines = proj_text.split('\n')
        
        current_entry = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    entries.append(current_entry)
                    current_entry = {}
                continue
            
            # Look for project title patterns
            if re.search(r'(project|application|system|platform|website|app)', line, re.IGNORECASE):
                if current_entry:
                    entries.append(current_entry)
                current_entry = {'title': line}
            elif current_entry and 'title' in current_entry:
                # Add to description
                if 'description' not in current_entry:
                    current_entry['description'] = line
                else:
                    current_entry['description'] += ' ' + line
        
        if current_entry:
            entries.append(current_entry)
        
        return entries 