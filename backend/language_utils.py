"""
Language utilities for detecting and translating between Arabic and English.
"""

import langdetect
from deep_translator import GoogleTranslator
from typing import Dict, Any


class LanguageProcessor:
    """Handles language detection and translation for the resume analyzer."""
    
    def __init__(self):
        self.supported_languages = ['en', 'ar']
        self.translator = GoogleTranslator()
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.
        
        Args:
            text (str): Input text to detect language
            
        Returns:
            str: Language code ('en' for English, 'ar' for Arabic)
        """
        try:
            lang = langdetect.detect(text)
            # Map common variations to our supported languages
            if lang in ['en', 'en-US', 'en-GB']:
                return 'en'
            elif lang in ['ar', 'ar-SA', 'ar-AE']:
                return 'ar'
            else:
                return 'en'  # Default to English
        except:
            return 'en'  # Default to English on error
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """
        Translate text to target language.
        
        Args:
            text (str): Text to translate
            target_lang (str): Target language code ('en' or 'ar')
            
        Returns:
            str: Translated text
        """
        if not text or target_lang not in self.supported_languages:
            return text
        
        try:
            # Detect source language
            source_lang = self.detect_language(text)
            
            # If already in target language, return as is
            if source_lang == target_lang:
                return text
            
            # Translate
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            return translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def get_ui_texts(self, language: str) -> Dict[str, str]:
        """
        Get UI texts in the specified language.
        
        Args:
            language (str): Language code ('en' or 'ar')
            
        Returns:
            Dict[str, str]: Dictionary of UI texts
        """
        texts = {
            'en': {
                'title': 'Resume Analyzer & Job Matcher',
                'subtitle': 'Get Your Resume Analyzed & Matched to Top Dubai Jobs',
                'upload_label': 'Upload your resume (PDF or DOCX)',
                'analyze_button': 'Analyze Resume',
                'overall_score': 'Overall Score',
                'resume_analysis': 'Resume Analysis',
                'suggestions': 'Improvement Suggestions',
                'job_matches': 'Job Matches',
                'download_report': 'Download Report',
                'language_toggle': 'Language',
                'loading': 'Analyzing your resume...',
                'error_message': 'An error occurred. Please try again.',
                'no_file': 'Please upload a resume file.',
                'invalid_format': 'Please upload a PDF or DOCX file.',
                'score_excellent': 'Excellent',
                'score_good': 'Good',
                'score_fair': 'Fair',
                'score_poor': 'Needs Improvement',
                'match_percentage': 'Match',
                'company': 'Company',
                'location': 'Location',
                'salary': 'Salary',
                'experience': 'Experience',
                'skills': 'Skills',
                'education': 'Education',
                'contact': 'Contact Information',
                'summary': 'Professional Summary',
                'strengths': 'Strengths',
                'weaknesses': 'Areas for Improvement',
                'recommendations': 'Recommendations'
            },
            'ar': {
                'title': 'محلل السيرة الذاتية ومطابق الوظائف',
                'subtitle': 'احصل على تحليل سيرتك الذاتية ومطابقتها مع أفضل وظائف دبي',
                'upload_label': 'قم برفع سيرتك الذاتية (PDF أو DOCX)',
                'analyze_button': 'تحليل السيرة الذاتية',
                'overall_score': 'الدرجة الإجمالية',
                'resume_analysis': 'تحليل السيرة الذاتية',
                'suggestions': 'اقتراحات التحسين',
                'job_matches': 'الوظائف المطابقة',
                'download_report': 'تحميل التقرير',
                'language_toggle': 'اللغة',
                'loading': 'جاري تحليل سيرتك الذاتية...',
                'error_message': 'حدث خطأ. يرجى المحاولة مرة أخرى.',
                'no_file': 'يرجى رفع ملف السيرة الذاتية.',
                'invalid_format': 'يرجى رفع ملف PDF أو DOCX.',
                'score_excellent': 'ممتاز',
                'score_good': 'جيد',
                'score_fair': 'مقبول',
                'score_poor': 'يحتاج تحسين',
                'match_percentage': 'مطابقة',
                'company': 'الشركة',
                'location': 'الموقع',
                'salary': 'الراتب',
                'experience': 'الخبرة',
                'skills': 'المهارات',
                'education': 'التعليم',
                'contact': 'معلومات الاتصال',
                'summary': 'الملخص المهني',
                'strengths': 'نقاط القوة',
                'weaknesses': 'مجالات التحسين',
                'recommendations': 'التوصيات'
            }
        }
        
        return texts.get(language, texts['en'])
    
    def format_score_description(self, score: int, language: str) -> str:
        """
        Get score description in the specified language.
        
        Args:
            score (int): Score from 0-100
            language (str): Language code
            
        Returns:
            str: Score description
        """
        texts = self.get_ui_texts(language)
        
        if score >= 85:
            return texts['score_excellent']
        elif score >= 70:
            return texts['score_good']
        elif score >= 50:
            return texts['score_fair']
        else:
            return texts['score_poor'] 