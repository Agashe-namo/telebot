#!/usr/bin/env python3
"""
Setup script for BingX Multi-Pair Bot
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install requirements")
        return False

def check_config():
    """Check if config.py has been properly configured"""
    try:
        from config import BINGX_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

        if "your_" in BINGX_API_KEY or "your_" in TELEGRAM_BOT_TOKEN or "your_" in str(TELEGRAM_CHAT_ID):
            print("⚠️  Warning: Please edit config.py with your actual API keys!")
            return False
        else:
            print("✓ Config appears to be set up")
            return True
    except ImportError:
        print("✗ Config file not found or has errors")
        return False

def main():
    print("=== BingX Multi-Pair Bot Setup ===")
    print()

    # Install requirements
    if not install_requirements():
        return

    # Check config
    config_ok = check_config()

    print()
    print("=== Setup Complete ===")
    if config_ok:
        print("✓ Ready to run! Use: python main.py")
    else:
        print("⚠️  Please configure your API keys in config.py before running")

if __name__ == "__main__":
    main()
