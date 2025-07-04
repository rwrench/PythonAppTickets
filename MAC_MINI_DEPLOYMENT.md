# 🍎 Mac Mini Deployment Guide

## Step 1: On Windows (Push to GitHub)

1. **Initialize Git Repository:**
   ```powershell
   .\setup_git.bat
   ```

2. **Create GitHub Repository:**
   - Go to [GitHub.com](https://github.com)
   - Click "New repository"
   - Name it `stock-ticker-app` (or your preferred name)
   - Don't initialize with README (we already have files)
   - Copy the repository URL

3. **Push to GitHub:**
   ```powershell
   .\push_to_github.bat
   ```
   - Enter your GitHub repository URL when prompted

## Step 2: On Mac Mini (Clone and Setup)

1. **Open Terminal on Mac Mini**

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

3. **Make Scripts Executable:**
   ```bash
   chmod +x make_executable.sh && ./make_executable.sh
   ```

4. **Run Setup:**
   ```bash
   ./setup_macos.sh
   ```

5. **Start the App:**
   ```bash
   # Choose one:
   ./start_simple_webapp_mac.sh     # Recommended: Standalone app on port 5001
   ./start_api_mac.sh               # API server on port 10000
   ./start_webapp_mac.sh            # Full web app on port 5000
   ```

## Step 3: Access Your App

- **Simple Fresh App**: `http://YOUR_MAC_MINI_IP:5001`
- **API Documentation**: `http://YOUR_MAC_MINI_IP:10000/docs`
- **Web App**: `http://YOUR_MAC_MINI_IP:5000`

## Future Updates

### On Windows:
```powershell
git add .
git commit -m "Your update message"
git push
```

### On Mac Mini:
```bash
git pull
# Restart your chosen app
```

## Troubleshooting

- **Python Version**: Ensure Python 3.11+ is installed on Mac Mini
- **Firewall**: Make sure ports 5000, 5001, and 10000 are open if accessing from other devices
- **Dependencies**: If you get import errors, re-run `./setup_macos.sh`

## Network Access

To access from other devices on your network, find your Mac Mini's IP address:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Then use `http://MAC_MINI_IP:PORT` instead of `localhost`.
