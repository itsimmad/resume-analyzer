"""
Main Streamlit application for the Bilingual Resume Analyzer & Job Matcher.
"""

import streamlit as st
import sys
import os
import tempfile
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent.parent / 'backend')
sys.path.insert(0, backend_path)

from resume_parser import ResumeParser
from ai_analyzer import AIAnalyzer
from job_matcher import JobMatcher
from language_utils import LanguageProcessor
from pdf_generator import PDFGenerator

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer & Job Matcher",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .job-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .suggestion-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    .strength-card {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .weakness-card {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    .match-badge {
        background: #007bff;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .language-toggle {
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0;
    }
    .analysis-section {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .job-matches-section {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .download-section {
        text-align: center;
        margin: 2rem 0;
    }
    .rtl {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize all backend components."""
    return {
        'resume_parser': ResumeParser(),
        'ai_analyzer': AIAnalyzer(),
        'job_matcher': JobMatcher(),
        'language_processor': LanguageProcessor(),
        'pdf_generator': PDFGenerator()
    }

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'job_matches' not in st.session_state:
    st.session_state.job_matches = None

def main():
    """Main application function."""
    # Initialize components
    components = initialize_components()
    
    # Language selection
    language = st.sidebar.selectbox(
        "🌐 Language / اللغة",
        ["English", "العربية"],
        index=0
    )
    
    # Get UI texts
    lang_code = 'ar' if language == "العربية" else 'en'
    texts = components['language_processor'].get_ui_texts(lang_code)
    
    # Main header
    if lang_code == 'ar':
        st.markdown(f'<div class="main-header rtl">{texts["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-header rtl">{texts["subtitle"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="main-header">{texts["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-header">{texts["subtitle"]}</div>', unsafe_allow_html=True)
    
    # File upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    if lang_code == 'ar':
        st.markdown(f'<h3 class="rtl">{texts["upload_label"]}</h3>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h3>{texts["upload_label"]}</h3>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=['pdf', 'docx'],
        help="Upload your resume in PDF or DOCX format"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analyze button
    if uploaded_file is not None:
        if st.button(texts["analyze_button"], type="primary"):
            with st.spinner(texts["loading"]):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_file.name.split(".")[-1]}') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # Parse resume
                    resume_data = components['resume_parser'].parse_resume(tmp_file_path)
                    
                    # Detect language of resume content
                    resume_language = components['language_processor'].detect_language(resume_data.get('raw_text', ''))
                    
                    # Analyze resume
                    analysis_results = components['ai_analyzer'].analyze_resume(resume_data, resume_language)
                    
                    # Match jobs
                    job_matches = components['job_matcher'].match_resume_to_jobs(resume_data, top_n=5)
                    
                    # Store results in session state
                    st.session_state.resume_data = resume_data
                    st.session_state.analysis_results = analysis_results
                    st.session_state.job_matches = job_matches
                    st.session_state.analysis_complete = True
                    
                    # Clean up temporary file
                    os.unlink(tmp_file_path)
                    
                    st.success("Analysis completed successfully!" if lang_code == 'en' else "تم إكمال التحليل بنجاح!")
                    
                except Exception as e:
                    st.error(f"{texts['error_message']}: {str(e)}")
                    st.session_state.analysis_complete = False
    
    # Display results if analysis is complete
    if st.session_state.analysis_complete and st.session_state.analysis_results:
        display_results(components, texts, lang_code)
    
    # Sidebar information
    with st.sidebar:
        st.markdown("### 📊 Features")
        if lang_code == 'ar':
            st.markdown("""
            - تحليل السيرة الذاتية بالذكاء الاصطناعي
            - مطابقة الوظائف في دبي
            - تقييم شامل من 0-100
            - اقتراحات تحسين محددة
            - تقرير PDF احترافي
            """)
        else:
            st.markdown("""
            - AI-powered resume analysis
            - Dubai job matching
            - Comprehensive 0-100 scoring
            - Specific improvement suggestions
            - Professional PDF report
            """)
        
        st.markdown("### 🔧 Supported Formats")
        st.markdown("- PDF files")
        st.markdown("- DOCX files")
        
        st.markdown("### 🌍 Languages")
        st.markdown("- English")
        st.markdown("- العربية")

def display_results(components, texts, lang_code):
    """Display analysis results."""
    resume_data = st.session_state.resume_data
    analysis_results = st.session_state.analysis_results
    job_matches = st.session_state.job_matches
    
    # Overall Score Section
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    
    if lang_code == 'ar':
        st.markdown(f'<h2 class="rtl">{texts["overall_score"]}</h2>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h2>{texts["overall_score"]}</h2>', unsafe_allow_html=True)
    
    score = analysis_results.get('score', 0)
    score_description = components['language_processor'].format_score_description(score, lang_code)
    
    # Create score visualization
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f'''
        <div class="score-card">
            <h1 style="font-size: 3rem; margin: 0;">{score}</h1>
            <p style="font-size: 1.2rem; margin: 0;">/ 100</p>
            <p style="font-size: 1rem; margin-top: 0.5rem;">{score_description}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed Analysis Section
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    
    if lang_code == 'ar':
        st.markdown(f'<h2 class="rtl">{texts["resume_analysis"]}</h2>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h2>{texts["resume_analysis"]}</h2>', unsafe_allow_html=True)
    
    # Strengths
    strengths = analysis_results.get('strengths', [])
    if strengths:
        if lang_code == 'ar':
            st.markdown(f'<h3 class="rtl">{texts["strengths"]}</h3>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h3>{texts["strengths"]}</h3>', unsafe_allow_html=True)
        
        for strength in strengths:
            if lang_code == 'ar':
                st.markdown(f'<div class="strength-card rtl">✅ {strength}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="strength-card">✅ {strength}</div>', unsafe_allow_html=True)
    
    # Weaknesses
    weaknesses = analysis_results.get('weaknesses', [])
    if weaknesses:
        if lang_code == 'ar':
            st.markdown(f'<h3 class="rtl">{texts["weaknesses"]}</h3>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h3>{texts["weaknesses"]}</h3>', unsafe_allow_html=True)
        
        for weakness in weaknesses:
            if lang_code == 'ar':
                st.markdown(f'<div class="weakness-card rtl">⚠️ {weakness}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="weakness-card">⚠️ {weakness}</div>', unsafe_allow_html=True)
    
    # Improved Summary
    improved_summary = analysis_results.get('improved_summary', '')
    if improved_summary:
        if lang_code == 'ar':
            st.markdown(f'<h3 class="rtl">{texts["summary"]}</h3>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h3>{texts["summary"]}</h3>', unsafe_allow_html=True)
        
        if lang_code == 'ar':
            st.markdown(f'<div class="suggestion-card rtl">{improved_summary}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="suggestion-card">{improved_summary}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Suggestions Section
    suggestions = analysis_results.get('suggestions', [])
    if suggestions:
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        
        if lang_code == 'ar':
            st.markdown(f'<h2 class="rtl">{texts["suggestions"]}</h2>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h2>{texts["suggestions"]}</h2>', unsafe_allow_html=True)
        
        for i, suggestion in enumerate(suggestions, 1):
            if lang_code == 'ar':
                st.markdown(f'<div class="suggestion-card rtl">{i}. {suggestion}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="suggestion-card">{i}. {suggestion}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Job Matches Section
    if job_matches:
        st.markdown('<div class="job-matches-section">', unsafe_allow_html=True)
        
        if lang_code == 'ar':
            st.markdown(f'<h2 class="rtl">{texts["job_matches"]}</h2>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h2>{texts["job_matches"]}</h2>', unsafe_allow_html=True)
        
        for job in job_matches:
            if lang_code == 'ar':
                st.markdown(f'''
                <div class="job-card rtl">
                    <h4>{job['title']}</h4>
                    <p><strong>{texts["company"]}:</strong> {job['company']}</p>
                    <p><strong>{texts["location"]}:</strong> {job['location']}</p>
                    <p><strong>{texts["salary"]}:</strong> {job['salary']}</p>
                    <p><strong>{texts["experience"]}:</strong> {job['experience']}</p>
                    <span class="match-badge">{texts["match_percentage"]}: {job['match_percentage']}%</span>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="job-card">
                    <h4>{job['title']}</h4>
                    <p><strong>{texts["company"]}:</strong> {job['company']}</p>
                    <p><strong>{texts["location"]}:</strong> {job['location']}</p>
                    <p><strong>{texts["salary"]}:</strong> {job['salary']}</p>
                    <p><strong>{texts["experience"]}:</strong> {job['experience']}</p>
                    <span class="match-badge">{texts["match_percentage"]}: {job['match_percentage']}%</span>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Download Section
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    
    if st.button(texts["download_report"], type="secondary"):
        try:
            with st.spinner("Generating PDF report..." if lang_code == 'en' else "جاري إنشاء تقرير PDF..."):
                # Generate PDF report
                pdf_path = components['pdf_generator'].generate_analysis_report(
                    resume_data=resume_data,
                    analysis_results=analysis_results,
                    job_matches=job_matches,
                    language=lang_code,
                    output_path='resume_analysis_report.pdf'
                )
                
                # Read PDF file
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_bytes = pdf_file.read()
                
                # Create download button
                st.download_button(
                    label="📄 Download PDF Report" if lang_code == 'en' else "📄 تحميل تقرير PDF",
                    data=pdf_bytes,
                    file_name="resume_analysis_report.pdf",
                    mime="application/pdf"
                )
                
                # Clean up PDF file
                os.unlink(pdf_path)
                
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 