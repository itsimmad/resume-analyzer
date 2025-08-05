"""
Test script to verify the Resume Analyzer components are working correctly.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent / 'backend')
sys.path.insert(0, backend_path)

def test_imports():
    """Test that all modules can be imported."""
    try:
        from resume_parser import ResumeParser
        from ai_analyzer import AIAnalyzer
        from job_matcher import JobMatcher
        from language_utils import LanguageProcessor
        from pdf_generator import PDFGenerator
        print("✅ All backend modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_language_processor():
    """Test language processing functionality."""
    try:
        from language_utils import LanguageProcessor
        
        processor = LanguageProcessor()
        
        # Test language detection
        english_text = "This is a sample resume in English"
        arabic_text = "هذه سيرة ذاتية باللغة العربية"
        
        en_detected = processor.detect_language(english_text)
        ar_detected = processor.detect_language(arabic_text)
        
        print(f"✅ Language detection: English detected as {en_detected}, Arabic detected as {ar_detected}")
        
        # Test UI texts
        en_texts = processor.get_ui_texts('en')
        ar_texts = processor.get_ui_texts('ar')
        
        print(f"✅ UI texts loaded: {len(en_texts)} English texts, {len(ar_texts)} Arabic texts")
        
        return True
    except Exception as e:
        print(f"❌ Language processor error: {e}")
        return False

def test_job_matcher():
    """Test job matching functionality."""
    try:
        from job_matcher import JobMatcher
        
        matcher = JobMatcher()
        
        # Test job data loading
        if matcher.jobs_data is not None and not matcher.jobs_data.empty:
            print(f"✅ Job matcher initialized with {len(matcher.jobs_data)} jobs")
            
            # Test available industries
            industries = matcher.get_available_industries()
            print(f"✅ Available industries: {industries}")
            
            return True
        else:
            print("❌ Job matcher failed to load job data")
            return False
    except Exception as e:
        print(f"❌ Job matcher error: {e}")
        return False

def test_resume_parser():
    """Test resume parser functionality."""
    try:
        from resume_parser import ResumeParser
        
        parser = ResumeParser()
        print("✅ Resume parser initialized successfully")
        
        # Test with sample text
        sample_text = """
        John Doe
        Software Engineer
        john.doe@email.com
        +1234567890
        
        SUMMARY
        Experienced software engineer with 5 years of experience in Python and JavaScript.
        
        EXPERIENCE
        Senior Developer at TechCorp (2020-2023)
        - Developed web applications using React and Node.js
        - Led team of 5 developers
        
        SKILLS
        Python, JavaScript, React, Node.js, AWS, Docker
        """
        
        # Create a temporary file for testing
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(sample_text)
            temp_path = f.name
        
        try:
            # Parse the sample text
            resume_data = parser._extract_structure(sample_text)
            
            print(f"✅ Resume parsing successful")
            print(f"   - Name: {resume_data.get('name', 'Not found')}")
            print(f"   - Skills: {len(resume_data.get('skills', []))} skills found")
            print(f"   - Experience: {len(resume_data.get('experience', []))} entries found")
            
            return True
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        print(f"❌ Resume parser error: {e}")
        return False

def test_ai_analyzer():
    """Test AI analyzer functionality."""
    try:
        from ai_analyzer import AIAnalyzer
        
        analyzer = AIAnalyzer()
        print("✅ AI analyzer initialized successfully")
        
        # Test fallback analysis
        sample_resume_data = {
            'name': 'John Doe',
            'summary': 'Experienced software engineer',
            'skills': ['Python', 'JavaScript', 'React'],
            'experience': [{'title': 'Senior Developer', 'description': 'Led development team'}],
            'education': [{'degree': 'Bachelor of Science', 'institution': 'University'}],
            'raw_text': 'Sample resume text for testing'
        }
        
        analysis = analyzer._fallback_analysis(sample_resume_data, 'en')
        
        print(f"✅ Fallback analysis successful")
        print(f"   - Score: {analysis.get('score', 0)}")
        print(f"   - Strengths: {len(analysis.get('strengths', []))}")
        print(f"   - Suggestions: {len(analysis.get('suggestions', []))}")
        
        return True
    except Exception as e:
        print(f"❌ AI analyzer error: {e}")
        return False

def test_pdf_generator():
    """Test PDF generator functionality."""
    try:
        from pdf_generator import PDFGenerator
        
        generator = PDFGenerator()
        print("✅ PDF generator initialized successfully")
        
        # Test simple report generation
        sample_resume_data = {
            'name': 'John Doe',
            'contact_info': {'email': 'john@example.com'},
            'skills': ['Python', 'JavaScript']
        }
        
        sample_analysis = {
            'score': 75,
            'strengths': ['Good technical skills'],
            'weaknesses': ['Needs more experience'],
            'suggestions': ['Add more projects']
        }
        
        # Test simple report generation
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name
        
        try:
            pdf_path = generator.generate_simple_report(
                resume_data=sample_resume_data,
                analysis_results=sample_analysis,
                language='en',
                output_path=temp_path
            )
            
            if os.path.exists(pdf_path):
                print(f"✅ PDF generation successful: {pdf_path}")
                return True
            else:
                print("❌ PDF file not created")
                return False
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        print(f"❌ PDF generator error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Resume Analyzer Components")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Language Processor", test_language_processor),
        ("Job Matcher", test_job_matcher),
        ("Resume Parser", test_resume_parser),
        ("AI Analyzer", test_ai_analyzer),
        ("PDF Generator", test_pdf_generator)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run frontend/app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main() 