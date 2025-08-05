"""
AI-powered resume analyzer using LangChain and OpenAI.
"""

import os
import streamlit as st
from typing import Dict, List, Any, Tuple
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import json
import re


class AIAnalyzer:
    """AI-powered resume analyzer for scoring and providing suggestions."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the AI analyzer.
        
        Args:
            api_key (str): OpenAI API key. If None, will try to get from environment or Streamlit secrets.
        """
        # Try to get API key from Streamlit secrets first, then environment
        if api_key:
            self.api_key = api_key
        elif hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            self.api_key = st.secrets['OPENAI_API_KEY']
        else:
            self.api_key = os.getenv('OPENAI_API_KEY')
            
        if self.api_key and self.api_key != "your_openai_api_key_here":
            try:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.3,
                    api_key=self.api_key
                )
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI: {e}")
                self.llm = None
        else:
            self.llm = None
    
    def analyze_resume(self, resume_data: Dict[str, Any], language: str = 'en') -> Dict[str, Any]:
        """
        Analyze resume and provide comprehensive feedback.
        
        Args:
            resume_data (Dict[str, Any]): Parsed resume data
            language (str): Language code ('en' or 'ar')
            
        Returns:
            Dict[str, Any]: Analysis results including score and suggestions
        """
        if not self.llm:
            return self._fallback_analysis(resume_data, language)
        
        try:
            # Create analysis prompt
            prompt = self._create_analysis_prompt(resume_data, language)
            
            # Get AI response
            response = self.llm.invoke(prompt)
            
            # Parse response
            analysis = self._parse_ai_response(response.content, language)
            
            return analysis
            
        except Exception as e:
            print(f"AI analysis error: {e}")
            return self._fallback_analysis(resume_data, language)
    
    def _create_analysis_prompt(self, resume_data: Dict[str, Any], language: str) -> str:
        """Create the analysis prompt for the AI."""
        
        if language == 'ar':
            system_prompt = """أنت محلل سير ذاتية محترف. قم بتحليل السيرة الذاتية المقدمة وتقييمها من 0 إلى 100.
            
            يجب أن تتضمن تحليلك:
            1. تقييم شامل (0-100)
            2. نقاط القوة
            3. مجالات التحسين
            4. اقتراحات محددة للتحسين
            5. ملخص مهني محسن
            
            أعد استجابة بتنسيق JSON يحتوي على:
            {
                "score": عدد من 0-100,
                "strengths": [قائمة نقاط القوة],
                "weaknesses": [قائمة مجالات التحسين],
                "suggestions": [اقتراحات محددة],
                "improved_summary": "ملخص مهني محسن"
            }"""
            
            user_prompt = f"""تحليل السيرة الذاتية التالية:
            
            الاسم: {resume_data.get('name', 'غير محدد')}
            الملخص: {resume_data.get('summary', 'غير محدد')}
            الخبرة: {json.dumps(resume_data.get('experience', []), ensure_ascii=False)}
            التعليم: {json.dumps(resume_data.get('education', []), ensure_ascii=False)}
            المهارات: {resume_data.get('skills', [])}
            اللغات: {resume_data.get('languages', [])}
            الشهادات: {resume_data.get('certifications', [])}
            المشاريع: {json.dumps(resume_data.get('projects', []), ensure_ascii=False)}
            
            النص الكامل: {resume_data.get('raw_text', '')[:2000]}
            """
        else:
            system_prompt = """You are a professional resume analyst. Analyze the provided resume and score it from 0 to 100.
            
            Your analysis should include:
            1. Overall score (0-100)
            2. Key strengths
            3. Areas for improvement
            4. Specific improvement suggestions
            5. Enhanced professional summary
            
            Return a JSON response with:
            {
                "score": number 0-100,
                "strengths": [list of strengths],
                "weaknesses": [list of areas for improvement],
                "suggestions": [specific suggestions],
                "improved_summary": "enhanced professional summary"
            }"""
            
            user_prompt = f"""Analyze the following resume:
            
            Name: {resume_data.get('name', 'Not specified')}
            Summary: {resume_data.get('summary', 'Not specified')}
            Experience: {json.dumps(resume_data.get('experience', []))}
            Education: {json.dumps(resume_data.get('education', []))}
            Skills: {resume_data.get('skills', [])}
            Languages: {resume_data.get('languages', [])}
            Certifications: {resume_data.get('certifications', [])}
            Projects: {json.dumps(resume_data.get('projects', []))}
            
            Full text: {resume_data.get('raw_text', '')[:2000]}
            """
        
        return [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
    
    def _parse_ai_response(self, response: str, language: str) -> Dict[str, Any]:
        """Parse the AI response and extract structured data."""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                # If no JSON found, create structured response from text
                data = self._extract_from_text(response, language)
            
            # Ensure all required fields exist
            analysis = {
                'score': data.get('score', 50),
                'strengths': data.get('strengths', []),
                'weaknesses': data.get('weaknesses', []),
                'suggestions': data.get('suggestions', []),
                'improved_summary': data.get('improved_summary', ''),
                'ai_response': response
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self._extract_from_text(response, language)
    
    def _extract_from_text(self, text: str, language: str) -> Dict[str, Any]:
        """Extract structured data from plain text response."""
        analysis = {
            'score': 50,
            'strengths': [],
            'weaknesses': [],
            'suggestions': [],
            'improved_summary': '',
            'ai_response': text
        }
        
        # Try to extract score
        score_match = re.search(r'(\d+)/100|score[:\s]*(\d+)', text, re.IGNORECASE)
        if score_match:
            score = score_match.group(1) or score_match.group(2)
            analysis['score'] = min(100, max(0, int(score)))
        
        # Extract sections based on language
        if language == 'ar':
            # Extract strengths
            strengths_match = re.search(r'نقاط القوة[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', text, re.DOTALL)
            if strengths_match:
                strengths_text = strengths_match.group(1)
                analysis['strengths'] = [s.strip() for s in strengths_text.split('\n') if s.strip()]
            
            # Extract weaknesses
            weaknesses_match = re.search(r'مجالات التحسين[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', text, re.DOTALL)
            if weaknesses_match:
                weaknesses_text = weaknesses_match.group(1)
                analysis['weaknesses'] = [w.strip() for w in weaknesses_text.split('\n') if w.strip()]
            
            # Extract suggestions
            suggestions_match = re.search(r'اقتراحات[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', text, re.DOTALL)
            if suggestions_match:
                suggestions_text = suggestions_match.group(1)
                analysis['suggestions'] = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
        else:
            # Extract strengths
            strengths_match = re.search(r'strengths[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', text, re.IGNORECASE | re.DOTALL)
            if strengths_match:
                strengths_text = strengths_match.group(1)
                analysis['strengths'] = [s.strip() for s in strengths_text.split('\n') if s.strip()]
            
            # Extract weaknesses
            weaknesses_match = re.search(r'weaknesses[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', text, re.IGNORECASE | re.DOTALL)
            if weaknesses_match:
                weaknesses_text = weaknesses_match.group(1)
                analysis['weaknesses'] = [w.strip() for w in weaknesses_text.split('\n') if w.strip()]
            
            # Extract suggestions
            suggestions_match = re.search(r'suggestions[:\s]*(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', text, re.IGNORECASE | re.DOTALL)
            if suggestions_match:
                suggestions_text = suggestions_match.group(1)
                analysis['suggestions'] = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
        
        return analysis
    
    def _fallback_analysis(self, resume_data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Fallback analysis when AI is not available."""
        
        # Calculate basic score based on resume completeness
        score = 50  # Base score
        
        # Add points for having different sections
        if resume_data.get('name'):
            score += 5
        if resume_data.get('summary'):
            score += 10
        if resume_data.get('experience'):
            score += 15
        if resume_data.get('education'):
            score += 10
        if resume_data.get('skills'):
            score += 10
        
        # Add points for contact information
        contact_info = resume_data.get('contact_info', {})
        if contact_info.get('email'):
            score += 5
        if contact_info.get('phone'):
            score += 5
        
        # Cap score at 100
        score = min(100, score)
        
        if language == 'ar':
            return {
                'score': score,
                'strengths': [
                    'السيرة الذاتية تحتوي على معلومات أساسية',
                    'التنسيق مقبول'
                ] if score > 60 else ['تم رفع الملف بنجاح'],
                'weaknesses': [
                    'يمكن تحسين المحتوى',
                    'يحتاج إلى مزيد من التفاصيل'
                ] if score < 80 else ['تحسينات طفيفة مطلوبة'],
                'suggestions': [
                    'أضف ملخص مهني واضح',
                    'حسن وصف الخبرات العملية',
                    'أضف المزيد من المهارات التقنية'
                ],
                'improved_summary': 'ملخص مهني محسن بناءً على تحليل السيرة الذاتية',
                'ai_response': 'تحليل أساسي تم إجراؤه بدون AI'
            }
        else:
            return {
                'score': score,
                'strengths': [
                    'Resume contains basic information',
                    'Format is acceptable'
                ] if score > 60 else ['File uploaded successfully'],
                'weaknesses': [
                    'Content can be improved',
                    'Needs more details'
                ] if score < 80 else ['Minor improvements needed'],
                'suggestions': [
                    'Add a clear professional summary',
                    'Improve work experience descriptions',
                    'Add more technical skills'
                ],
                'improved_summary': 'Enhanced professional summary based on resume analysis',
                'ai_response': 'Basic analysis performed without AI'
            }
    
    def calculate_keyword_score(self, resume_text: str, job_keywords: List[str]) -> float:
        """
        Calculate keyword matching score between resume and job requirements.
        
        Args:
            resume_text (str): Resume text
            job_keywords (List[str]): Job requirement keywords
            
        Returns:
            float: Matching score (0-1)
        """
        if not job_keywords:
            return 0.0
        
        resume_lower = resume_text.lower()
        matched_keywords = 0
        
        for keyword in job_keywords:
            if keyword.lower() in resume_lower:
                matched_keywords += 1
        
        return matched_keywords / len(job_keywords)
    
    def generate_job_specific_suggestions(self, resume_data: Dict[str, Any], job_title: str, language: str) -> List[str]:
        """
        Generate job-specific improvement suggestions.
        
        Args:
            resume_data (Dict[str, Any]): Resume data
            job_title (str): Target job title
            language (str): Language code
            
        Returns:
            List[str]: Job-specific suggestions
        """
        if not self.llm:
            return []
        
        try:
            if language == 'ar':
                prompt = f"""بناءً على السيرة الذاتية والوظيفة المستهدفة '{job_title}'، قدم اقتراحات محددة لتحسين السيرة الذاتية.
                
                السيرة الذاتية:
                المهارات: {resume_data.get('skills', [])}
                الخبرة: {json.dumps(resume_data.get('experience', []), ensure_ascii=False)}
                
                قدم 3-5 اقتراحات محددة ومفيدة."""
            else:
                prompt = f"""Based on the resume and target job '{job_title}', provide specific suggestions to improve the resume.
                
                Resume:
                Skills: {resume_data.get('skills', [])}
                Experience: {json.dumps(resume_data.get('experience', []))}
                
                Provide 3-5 specific and actionable suggestions."""
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            
            # Extract suggestions from response
            suggestions = []
            lines = response.content.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    suggestion = line.lstrip('-•0123456789. ')
                    if suggestion:
                        suggestions.append(suggestion)
            
            return suggestions[:5]  # Limit to 5 suggestions
            
        except Exception as e:
            print(f"Error generating job-specific suggestions: {e}")
            return [] 