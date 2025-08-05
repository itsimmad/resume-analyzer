@echo off
echo 🚀 Resume Analyzer - Streamlit Cloud Deployment
echo ================================================

REM Check if git is initialized
if not exist ".git" (
    echo 📁 Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit: Resume Analyzer app"
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

REM Check if remote exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo.
    echo 🌐 GitHub Repository Setup
    echo ==========================
    echo Please create a GitHub repository and then run:
    echo.
    echo git remote add origin https://github.com/YOUR_USERNAME/resume-analyzer-app.git
    echo git branch -M main
    echo git push -u origin main
    echo.
    echo Then deploy to Streamlit Cloud at: https://share.streamlit.io
    echo.
    echo 📋 Deployment Steps:
    echo 1. Go to https://share.streamlit.io
    echo 2. Sign in with GitHub
    echo 3. Click 'New app'
    echo 4. Select your repository
    echo 5. Set main file path: frontend/app.py
    echo 6. Click 'Deploy!'
    echo.
    echo 🔑 Optional: Add OpenAI API key in Streamlit Cloud secrets
) else (
    echo ✅ Remote repository already configured
    echo.
    echo 🔄 Pushing latest changes...
    git add .
    git commit -m "Update: Resume Analyzer app"
    git push
    echo ✅ Changes pushed to GitHub
    echo.
    echo 🌐 Your app should auto-deploy on Streamlit Cloud!
)

echo.
echo 📚 For detailed instructions, see DEPLOYMENT.md
echo 🎉 Happy deploying!
pause 