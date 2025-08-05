# Bilingual Resume Analyzer + Job Matcher

A comprehensive web application that analyzes resumes and matches them to relevant Dubai job listings, supporting both Arabic and English content.

## Features

- **Bilingual Support**: Full Arabic and English language support
- **Resume Analysis**: AI-powered analysis of resume structure and content
- **Job Matching**: Intelligent matching to Dubai job listings
- **Professional Scoring**: 0-100 score with detailed feedback
- **Improvement Suggestions**: Actionable tips to enhance your resume
- **PDF Export**: Download analysis results as PDF

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python with LangChain/OpenAI
- **Resume Parsing**: pdfplumber, python-docx, spacy, PyMuPDF
- **Language Processing**: langdetect, deep-translator
- **Data Visualization**: Plotly
- **PDF Generation**: ReportLab

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd resume
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
python -m spacy download ar_core_news_sm
```

4. Set up environment variables:
```bash
cp .env.example .env
# Add your OpenAI API key to .env file
```

5. Run the application:
```bash
streamlit run frontend/app.py
```

## Project Structure

```
resume/
├── frontend/
│   ├── app.py                 # Main Streamlit application
│   ├── components/            # UI components
│   └── assets/               # CSS and static files
├── backend/
│   ├── resume_parser.py      # Resume parsing logic
│   ├── ai_analyzer.py        # AI analysis and scoring
│   ├── job_matcher.py        # Job matching algorithm
│   ├── language_utils.py     # Language detection and translation
│   └── pdf_generator.py      # PDF report generation
├── data/
│   └── dubai_jobs.csv        # Job listings database
├── requirements.txt
└── README.md
```

## Usage

1. Open the web application in your browser
2. Toggle between Arabic and English languages
3. Upload your resume (PDF or DOCX format)
4. View the AI analysis and scoring
5. See matched job opportunities
6. Download the analysis report

## 🚀 Deployment

### Quick Deploy to Streamlit Cloud

**Option 1: Automated Script**
```bash
# On Windows
deploy.bat

# On Mac/Linux
chmod +x deploy.sh
./deploy.sh
```

**Option 2: Manual Steps**
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Resume Analyzer app"
   git remote add origin https://github.com/YOUR_USERNAME/resume-analyzer-app.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `frontend/app.py`
   - Click "Deploy!"

3. **Add OpenAI API Key** (Optional):
   - In Streamlit Cloud, go to app settings
   - Click "Secrets"
   - Add: `OPENAI_API_KEY = "your-api-key-here"`

### Your App URL
After deployment: `https://resume-analyzer-app-YOUR_USERNAME.streamlit.app`

### Other Platforms
- **Render**: Use the provided `requirements.txt`
- **Heroku**: Add a `Procfile` with `web: streamlit run frontend/app.py`
- **Replit**: Import the project and run `streamlit run frontend/app.py`

📚 **Detailed deployment guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## License

MIT License 