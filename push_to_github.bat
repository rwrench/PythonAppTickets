@echo off
echo 🚀 Pushing to GitHub
echo ==================

echo 📁 Navigating to project directory...
cd /d "c:\Users\Richard Wrench\source\repos\PythonAppTickets"

echo 🔍 Checking git status...
git status

echo ""
set /p GITHUB_URL="Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): "

echo ""
echo 🔗 Adding GitHub remote...
git remote add origin %GITHUB_URL%

echo 📤 Pushing to GitHub...
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "🍎 Now you can clone on your Mac Mini with:"
echo "git clone %GITHUB_URL%"
echo ""
pause
