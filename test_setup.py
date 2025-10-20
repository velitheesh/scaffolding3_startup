#!/usr/bin/env python3
"""
test_setup.py
Environment validation script for the warm-up assignment

Run this to verify your environment is set up correctly before starting the assignment.
"""

import sys
import importlib
import subprocess
import platform

def check_python_version():
    """Check if Python version is 3.9+"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.9+ required")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    required_packages = [
        'flask',
        'requests', 
        'bs4',  # beautifulsoup4 imports as bs4
        'nltk',
        'dotenv'  # python-dotenv imports as dotenv
    ]
    
    print("\n📦 Checking required packages...")
    all_installed = True
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Run: pip install {package}")
            all_installed = False
    
    return all_installed

def check_codespace_environment():
    """Check if running in GitHub Codespaces"""
    if 'CODESPACES' in sys.modules or 'CODESPACE_NAME' in sys.modules:
        print("\n🚀 Running in GitHub Codespaces")
        return True
    else:
        print("\n💻 Running in local environment")
        return True  # Not an error, just informational

def test_basic_functionality():
    """Test basic functionality of key libraries"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test requests
        import requests
        print("✅ requests library working")
        
        # Test Flask
        from flask import Flask
        test_app = Flask(__name__)
        print("✅ Flask can create app instance")
        
        # Test text processing
        import re
        text = "Hello, World! This is a test."
        words = text.lower().split()
        print(f"✅ Text processing working: {len(words)} words found")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def test_project_gutenberg_access():
    """Test if we can access Project Gutenberg URLs"""
    print("\n📚 Testing Project Gutenberg access...")
    
    try:
        import requests
        
        # Test with a small file
        test_url = "https://www.gutenberg.org/files/1342/1342-0.txt"
        response = requests.head(test_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Project Gutenberg accessible")
            return True
        else:
            print(f"⚠️  Project Gutenberg returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not reach Project Gutenberg: {e}")
        print("   This might be a temporary network issue")
        return False

def main():
    """Run all setup tests"""
    print("🔍 CSE 510 Warm-Up Assignment - Environment Setup Test")
    print("=" * 60)
    
    tests = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages), 
        ("Basic Functionality", test_basic_functionality),
        ("Project Gutenberg Access", test_project_gutenberg_access)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 SETUP TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:<8} {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ENVIRONMENT SETUP COMPLETE!")
        print("You're ready to start the warm-up assignment!")
        print("\nNext steps:")
        print("1. Read the assignment PDF carefully")
        print("2. Start with Part 2: Extending the TextPreprocessor")
        print("3. Test each part incrementally")
    else:
        print("⚠️  SETUP INCOMPLETE")
        print("Please fix the failed tests before starting the assignment.")
        print("\nTip: Run 'pip install -r requirements.txt' to install missing packages")
    
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)