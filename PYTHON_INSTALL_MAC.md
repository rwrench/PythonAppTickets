# 🐍 Python Installation Guide for Mac Mini

## Problem: "python not found" error

This happens because macOS doesn't include Python 3.11+ by default.

## ✅ Solution Options:

### Option 1: Official Python Installer (Recommended)

1. **Download Python:**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.11 or newer for macOS
   - Double-click the .pkg file to install

2. **Verify Installation:**
   ```bash
   python3 --version
   # Should show: Python 3.11.x or higher
   ```

### Option 2: Homebrew (If you use package managers)

1. **Install Homebrew (if not installed):**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python:**
   ```bash
   brew install python@3.11
   ```

### Option 3: pyenv (For Python version management)

1. **Install pyenv:**
   ```bash
   curl https://pyenv.run | bash
   ```

2. **Install Python 3.11:**
   ```bash
   pyenv install 3.11.9
   pyenv global 3.11.9
   ```

## 🚀 After Python Installation:

1. **Test Python:**
   ```bash
   python3 --version
   ```

2. **Run the setup script:**
   ```bash
   ./setup_macos.sh
   ```

3. **Start the app:**
   ```bash
   ./start_simple_webapp_mac.sh
   ```

## 🔧 Troubleshooting:

- **If `python3` doesn't work, try `python`**
- **Check PATH:** Make sure `/usr/local/bin` is in your PATH
- **Restart Terminal** after installation

## ⚡ Quick Test:
```bash
# This should work after installation:
python3 -c "print('Python is working!')"
```

If you still have issues, the updated setup script will detect and guide you through the proper installation.
