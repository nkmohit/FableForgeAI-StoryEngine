#!/usr/bin/env python3
"""
FableForge AI Story Engine - Automated Installation Script
This script helps you set up FableForge AI with all required dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print the welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           🧠 FableForge AI - Story Engine 2.0               ║
    ║                                                              ║
    ║         Automated Installation & Setup Script               ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Not compatible!")
        print("⚠️  Python 3.9 or higher is required.")
        return False

def install_pip_packages():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    packages = [
        "streamlit>=1.45.0",
        "python-dotenv>=1.0.0",
        "Pillow>=10.0.0",
        "requests>=2.32.0",
        "google-generativeai>=0.8.5",
        "gradio-client>=1.4.0",
        "plotly>=5.22.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0"
    ]
    
    try:
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("✅ All packages installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n⚙️ Setting up environment file...")
    
    env_path = Path(".env")
    
    if env_path.exists():
        print("✅ .env file already exists!")
        return True
    
    env_content = """# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Hugging Face Configuration  
HUGGING_FACE_AUTH_TOKEN=your_hugging_face_token_here

# Instructions:
# 1. Get your Google API key from: https://aistudio.google.com/app/apikey
# 2. Get your Hugging Face token from: https://huggingface.co/settings/tokens
# 3. Replace the placeholder values with your actual API keys
# 4. Save this file and restart the application
"""
    
    try:
        with open(env_path, "w") as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("⚠️  Please edit .env file and add your API keys before running the app.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_api_keys():
    """Check if API keys are configured"""
    print("\n🔑 Checking API keys...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    google_key = os.getenv("GOOGLE_API_KEY")
    hf_token = os.getenv("HUGGING_FACE_AUTH_TOKEN")
    
    if google_key and google_key != "your_google_api_key_here":
        print("✅ Google API key found!")
        google_ok = True
    else:
        print("⚠️  Google API key not configured")
        google_ok = False
    
    if hf_token and hf_token != "your_hugging_face_token_here":
        print("✅ Hugging Face token found!")
        hf_ok = True
    else:
        print("⚠️  Hugging Face token not configured")
        hf_ok = False
    
    return google_ok, hf_ok

def test_installation():
    """Test if installation is working"""
    print("\n🧪 Testing installation...")
    
    try:
        import streamlit
        import google.generativeai as genai
        import plotly
        import pandas
        import numpy
        
        print("✅ All core packages imported successfully!")
        
        # Test Streamlit version
        st_version = streamlit.__version__
        print(f"✅ Streamlit version: {st_version}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_application():
    """Launch the Streamlit application"""
    print("\n🚀 Launching FableForge AI...")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Thanks for using FableForge AI!")
    except Exception as e:
        print(f"❌ Failed to launch application: {e}")

def main():
    """Main installation process"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install packages
    if not install_pip_packages():
        print("❌ Installation failed. Please check error messages above.")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed.")
        sys.exit(1)
    
    # Check API keys
    google_ok, hf_ok = check_api_keys()
    
    if not google_ok:
        print("""
        📋 Setup Required:
        1. Get your Google API key: https://aistudio.google.com/app/apikey
        2. Edit the .env file and replace 'your_google_api_key_here' with your actual key
        3. Run the script again or start the app manually with: streamlit run main.py
        """)
        
        response = input("\nWould you like to continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    print("""
    🎉 Installation completed successfully!
    
    📋 Next Steps:
    1. Make sure your API keys are configured in .env file
    2. The application will start automatically
    3. Open your browser to http://localhost:8501
    
    📚 Features:
    • 🤖 Enhanced ChatBot with streaming
    • 📚 Advanced Story Generator  
    • 🎬 Comic Video Generator
    • 🎯 AI Assistant Hub
    • 📊 Analytics Dashboard
    
    Happy storytelling! 🚀
    """)
    
    # Ask if user wants to run the app
    response = input("Would you like to start the application now? (y/n): ")
    if response.lower() == 'y':
        run_application()
    else:
        print("👋 You can start the app later with: streamlit run main.py")

if __name__ == "__main__":
    main() 