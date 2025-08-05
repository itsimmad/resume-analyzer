# 🚀 Deployment Guide: Resume Analyzer to Streamlit Cloud

## 📋 Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Streamlit Cloud Account** - Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **OpenAI API Key** (Optional) - For full AI features

## 🔧 Step-by-Step Deployment

### Step 1: Push to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Resume Analyzer app"
   ```

2. **Create GitHub Repository**:
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `resume-analyzer-app`
   - Make it public (required for free Streamlit Cloud)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/resume-analyzer-app.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

2. **Deploy New App**:
   - Click "New app"
   - Select your repository: `resume-analyzer-app`
   - Set main file path: `frontend/app.py`
   - Click "Deploy!"

### Step 3: Configure Secrets (Optional)

For full AI features, add your OpenAI API key:

1. **In Streamlit Cloud**:
   - Go to your app settings
   - Click "Secrets"
   - Add your secrets in TOML format:

   ```toml
   OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
   ```

2. **Or update `.streamlit/secrets.toml`**:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
   ```

## 🌐 Your App URL

After deployment, your app will be available at:
```
https://resume-analyzer-app-YOUR_USERNAME.streamlit.app
```

## 🔄 Automatic Updates

- Every time you push changes to your GitHub repository, Streamlit Cloud will automatically redeploy your app
- No manual intervention needed!

## 📱 App Features

✅ **Bilingual Support** - English & Arabic  
✅ **Resume Upload** - PDF & DOCX  
✅ **AI Analysis** - Scoring & suggestions  
✅ **Job Matching** - Dubai opportunities  
✅ **PDF Reports** - Downloadable analysis  

## 🛠️ Troubleshooting

### Common Issues:

1. **Import Errors**:
   - Make sure all dependencies are in `requirements.txt`
   - Check that `packages.txt` includes system dependencies

2. **API Key Issues**:
   - Verify your OpenAI API key in Streamlit secrets
   - App works without API key (uses fallback analysis)

3. **Memory Issues**:
   - Streamlit Cloud has memory limits
   - Large files might cause issues

### Performance Tips:

- Keep uploaded files under 10MB
- The app uses caching for better performance
- AI analysis is optional (fallback available)

## 🔒 Security Notes

- Never commit API keys to GitHub
- Use Streamlit secrets for sensitive data
- The app doesn't store uploaded files permanently

## 📞 Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Verify all dependencies are installed
3. Test locally first with `streamlit run frontend/app.py`

---

🎉 **Congratulations!** Your Resume Analyzer is now live on the web! 