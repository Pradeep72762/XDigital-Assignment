"""
Quick verification script to check if all dependencies are installed correctly
"""
import sys
import os

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')  # Set UTF-8 encoding

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"[OK] Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"[FAIL] Python version {version.major}.{version.minor}.{version.micro} is below 3.10")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'pytest': 'pytest',
        'playwright': 'playwright',
        'pytest_html': 'pytest-html'
    }
    
    missing = []
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"[OK] {package_name} is installed")
        except ImportError:
            print(f"[FAIL] {package_name} is NOT installed")
            missing.append(package_name)
    
    return len(missing) == 0

if __name__ == "__main__":
    print("=" * 50)
    print("U-Ask Test Framework Setup Verification")
    print("=" * 50)
    print()
    
    python_ok = check_python_version()
    print()
    deps_ok = check_dependencies()
    print()
    
    if python_ok and deps_ok:
        print("=" * 50)
        print("[SUCCESS] All checks passed! Framework is ready to use.")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Run 'py -m playwright install' to install browsers")
        print("2. Run 'py -m pytest' to execute tests")
    else:
        print("=" * 50)
        print("[FAIL] Some checks failed. Please install missing dependencies.")
        print("=" * 50)
        print("\nRun: py -m pip install -r requirements.txt")

