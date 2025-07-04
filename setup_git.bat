@echo off
echo 🚀 Setting up Git Repository for GitHub Deployment
echo ===============================================

echo 📁 Navigating to project directory...
cd /d "c:\Users\Richard Wrench\source\repos\PythonAppTickets"

echo 🔧 Initializing git repository...
git init

echo 📝 Adding all files to git...
git add .

echo 💾 Creating initial commit...
git commit -m "Initial commit - Stock Ticker App with macOS deployment scripts

Features:
- FastAPI server for real-time stock data
- Flask web app with modern UI
- Simple standalone webapp (simple_fresh_webapp.py)
- macOS deployment scripts for Mac Mini
- Windows batch files for local development
- Comprehensive documentation

Supports Python 3.11+ and includes:
- Real-time stock price fetching from Yahoo Finance
- YTD performance analysis
- Interactive API documentation
- Multiple deployment options"

echo 🌿 Setting main branch...
git branch -M main

echo ""
echo "✅ Git repository initialized successfully!"
echo ""
echo "🔗 Next steps:"
echo "1. Create a repository on GitHub.com"
echo "2. Copy the repository URL (https://github.com/yourusername/repo-name.git)"
echo "3. Run: git remote add origin YOUR_GITHUB_URL"
echo "4. Run: git push -u origin main"
echo ""
echo "📋 Example commands:"
echo "git remote add origin https://github.com/yourusername/stock-ticker-app.git"
echo "git push -u origin main"
echo ""
pause
