"""
PDF generator for creating professional resume analysis reports.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from typing import Dict, List, Any
import os
from datetime import datetime


class PDFGenerator:
    """Generates professional PDF reports for resume analysis."""
    
    def __init__(self):
        """Initialize the PDF generator."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'CustomSection',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        )
        
        # Subsection style
        self.subsection_style = ParagraphStyle(
            'CustomSubsection',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.darkgreen
        )
        
        # Normal text style
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leading=14
        )
        
        # Score style
        self.score_style = ParagraphStyle(
            'CustomScore',
            parent=self.styles['Normal'],
            fontSize=18,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
    
    def generate_analysis_report(self, 
                                resume_data: Dict[str, Any], 
                                analysis_results: Dict[str, Any], 
                                job_matches: List[Dict[str, Any]], 
                                language: str = 'en',
                                output_path: str = 'resume_analysis_report.pdf') -> str:
        """
        Generate a comprehensive PDF report.
        
        Args:
            resume_data (Dict[str, Any]): Parsed resume data
            analysis_results (Dict[str, Any]): AI analysis results
            job_matches (List[Dict[str, Any]]): Job matches
            language (str): Language code ('en' or 'ar')
            output_path (str): Output file path
            
        Returns:
            str: Path to generated PDF file
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Add title
        title_text = "Resume Analysis Report" if language == 'en' else "تقرير تحليل السيرة الذاتية"
        story.append(Paragraph(title_text, self.title_style))
        story.append(Spacer(1, 20))
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_text = f"Generated on: {timestamp}" if language == 'en' else f"تم إنشاؤه في: {timestamp}"
        story.append(Paragraph(timestamp_text, self.normal_style))
        story.append(Spacer(1, 30))
        
        # Add candidate information
        story.extend(self._add_candidate_info(resume_data, language))
        
        # Add overall score
        story.extend(self._add_overall_score(analysis_results, language))
        
        # Add detailed analysis
        story.extend(self._add_detailed_analysis(analysis_results, language))
        
        # Add job matches
        story.extend(self._add_job_matches(job_matches, language))
        
        # Add recommendations
        story.extend(self._add_recommendations(analysis_results, language))
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def _add_candidate_info(self, resume_data: Dict[str, Any], language: str) -> List:
        """Add candidate information section."""
        elements = []
        
        # Section header
        section_title = "Candidate Information" if language == 'en' else "معلومات المرشح"
        elements.append(Paragraph(section_title, self.section_style))
        
        # Create candidate info table
        candidate_data = []
        
        # Name
        name_label = "Name" if language == 'en' else "الاسم"
        name_value = resume_data.get('name', 'Not specified') if language == 'en' else resume_data.get('name', 'غير محدد')
        candidate_data.append([name_label, name_value])
        
        # Contact information
        contact_info = resume_data.get('contact_info', {})
        if contact_info.get('email'):
            email_label = "Email" if language == 'en' else "البريد الإلكتروني"
            candidate_data.append([email_label, contact_info['email']])
        
        if contact_info.get('phone'):
            phone_label = "Phone" if language == 'en' else "الهاتف"
            candidate_data.append([phone_label, contact_info['phone']])
        
        # Skills
        if resume_data.get('skills'):
            skills_label = "Skills" if language == 'en' else "المهارات"
            skills_value = ', '.join(resume_data['skills'][:10])  # Limit to first 10 skills
            candidate_data.append([skills_label, skills_value])
        
        # Create table
        if candidate_data:
            table = Table(candidate_data, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _add_overall_score(self, analysis_results: Dict[str, Any], language: str) -> List:
        """Add overall score section."""
        elements = []
        
        # Section header
        section_title = "Overall Score" if language == 'en' else "الدرجة الإجمالية"
        elements.append(Paragraph(section_title, self.section_style))
        
        # Score
        score = analysis_results.get('score', 0)
        score_text = f"{score}/100" if language == 'en' else f"{score}/100"
        elements.append(Paragraph(score_text, self.score_style))
        
        # Score description
        if score >= 85:
            description = "Excellent" if language == 'en' else "ممتاز"
        elif score >= 70:
            description = "Good" if language == 'en' else "جيد"
        elif score >= 50:
            description = "Fair" if language == 'en' else "مقبول"
        else:
            description = "Needs Improvement" if language == 'en' else "يحتاج تحسين"
        
        elements.append(Paragraph(description, self.normal_style))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _add_detailed_analysis(self, analysis_results: Dict[str, Any], language: str) -> List:
        """Add detailed analysis section."""
        elements = []
        
        # Section header
        section_title = "Detailed Analysis" if language == 'en' else "التحليل المفصل"
        elements.append(Paragraph(section_title, self.section_style))
        
        # Strengths
        strengths = analysis_results.get('strengths', [])
        if strengths:
            strengths_title = "Strengths" if language == 'en' else "نقاط القوة"
            elements.append(Paragraph(strengths_title, self.subsection_style))
            
            for strength in strengths:
                elements.append(Paragraph(f"• {strength}", self.normal_style))
            elements.append(Spacer(1, 10))
        
        # Weaknesses
        weaknesses = analysis_results.get('weaknesses', [])
        if weaknesses:
            weaknesses_title = "Areas for Improvement" if language == 'en' else "مجالات التحسين"
            elements.append(Paragraph(weaknesses_title, self.subsection_style))
            
            for weakness in weaknesses:
                elements.append(Paragraph(f"• {weakness}", self.normal_style))
            elements.append(Spacer(1, 10))
        
        # Improved summary
        improved_summary = analysis_results.get('improved_summary', '')
        if improved_summary:
            summary_title = "Enhanced Professional Summary" if language == 'en' else "الملخص المهني المحسن"
            elements.append(Paragraph(summary_title, self.subsection_style))
            elements.append(Paragraph(improved_summary, self.normal_style))
            elements.append(Spacer(1, 10))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _add_job_matches(self, job_matches: List[Dict[str, Any]], language: str) -> List:
        """Add job matches section."""
        elements = []
        
        # Section header
        section_title = "Job Matches" if language == 'en' else "الوظائف المطابقة"
        elements.append(Paragraph(section_title, self.section_style))
        
        if not job_matches:
            no_matches = "No job matches found." if language == 'en' else "لم يتم العثور على وظائف مطابقة."
            elements.append(Paragraph(no_matches, self.normal_style))
        else:
            # Create job matches table
            job_data = []
            
            # Table headers
            if language == 'en':
                headers = ['Job Title', 'Company', 'Match %', 'Salary', 'Experience']
            else:
                headers = ['المسمى الوظيفي', 'الشركة', 'نسبة المطابقة', 'الراتب', 'الخبرة']
            
            job_data.append(headers)
            
            # Add job matches
            for job in job_matches[:5]:  # Limit to top 5 matches
                job_data.append([
                    job['title'],
                    job['company'],
                    f"{job['match_percentage']}%",
                    job['salary'],
                    job['experience']
                ])
            
            # Create table
            table = Table(job_data, colWidths=[1.5*inch, 1.5*inch, 0.8*inch, 1.2*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            elements.append(table)
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _add_recommendations(self, analysis_results: Dict[str, Any], language: str) -> List:
        """Add recommendations section."""
        elements = []
        
        # Section header
        section_title = "Recommendations" if language == 'en' else "التوصيات"
        elements.append(Paragraph(section_title, self.section_style))
        
        # Suggestions
        suggestions = analysis_results.get('suggestions', [])
        if suggestions:
            suggestions_title = "Improvement Suggestions" if language == 'en' else "اقتراحات التحسين"
            elements.append(Paragraph(suggestions_title, self.subsection_style))
            
            for i, suggestion in enumerate(suggestions, 1):
                elements.append(Paragraph(f"{i}. {suggestion}", self.normal_style))
        else:
            no_suggestions = "No specific suggestions available." if language == 'en' else "لا توجد اقتراحات محددة متاحة."
            elements.append(Paragraph(no_suggestions, self.normal_style))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def generate_simple_report(self, 
                              resume_data: Dict[str, Any], 
                              analysis_results: Dict[str, Any], 
                              language: str = 'en',
                              output_path: str = 'simple_report.pdf') -> str:
        """
        Generate a simple PDF report.
        
        Args:
            resume_data (Dict[str, Any]): Parsed resume data
            analysis_results (Dict[str, Any]): AI analysis results
            language (str): Language code ('en' or 'ar')
            output_path (str): Output file path
            
        Returns:
            str: Path to generated PDF file
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Add title
        title_text = "Resume Analysis Summary" if language == 'en' else "ملخص تحليل السيرة الذاتية"
        story.append(Paragraph(title_text, self.title_style))
        story.append(Spacer(1, 30))
        
        # Add score
        score = analysis_results.get('score', 0)
        score_text = f"Score: {score}/100" if language == 'en' else f"الدرجة: {score}/100"
        story.append(Paragraph(score_text, self.score_style))
        story.append(Spacer(1, 20))
        
        # Add key points
        key_points_title = "Key Points" if language == 'en' else "النقاط الرئيسية"
        story.append(Paragraph(key_points_title, self.section_style))
        
        # Strengths
        strengths = analysis_results.get('strengths', [])
        if strengths:
            strengths_title = "Strengths:" if language == 'en' else "نقاط القوة:"
            story.append(Paragraph(strengths_title, self.subsection_style))
            for strength in strengths[:3]:  # Limit to 3
                story.append(Paragraph(f"• {strength}", self.normal_style))
            story.append(Spacer(1, 10))
        
        # Suggestions
        suggestions = analysis_results.get('suggestions', [])
        if suggestions:
            suggestions_title = "Suggestions:" if language == 'en' else "الاقتراحات:"
            story.append(Paragraph(suggestions_title, self.subsection_style))
            for suggestion in suggestions[:3]:  # Limit to 3
                story.append(Paragraph(f"• {suggestion}", self.normal_style))
        
        # Build PDF
        doc.build(story)
        return output_path 