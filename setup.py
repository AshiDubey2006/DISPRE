"""
Setup script for DISPRE
Run this to set up the project environment
"""

import os
import sys
import subprocess

def create_directories():
    """Create necessary directories"""
    directories = [
        './src',
        './src/data',
        './src/models',
        './src/visualization',
        './src/utils',
        './data',
        './output',
        './logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("⚠️ Warning: Python 3.7+ is recommended")
    else:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")


def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except Exception as e:
        print(f"⚠️ Error installing dependencies: {e}")
        print("Try running: pip install -r requirements.txt")


def test_imports():
    """Test that key modules can be imported"""
    print("\n🧪 Testing imports...")
    
    modules = [
        'numpy',
        'pandas',
        'sklearn',
        'matplotlib',
        'seaborn'
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module}")
            failed.append(module)
    
    if failed:
        print(f"\n⚠️ Failed to import: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
    else:
        print("\n✓ All core modules imported successfully")


def setup_logging():
    """Setup logging configuration"""
    log_dir = './logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Create empty log file
    log_file = os.path.join(log_dir, 'dispre.log')
    open(log_file, 'a').close()
    
    print(f"✓ Logging configured: {log_file}")


def main():
    """Run setup"""
    print("\n" + "="*70)
    print("DISPRE Setup Script")
    print("="*70 + "\n")
    
    # Create directories
    print("📁 Creating directories...")
    create_directories()
    
    # Check Python version
    print("\n🐍 Checking Python version...")
    check_python_version()
    
    # Test imports
    print("\n🧪 Checking existing packages...")
    test_imports()
    
    # Setup logging
    print("\n📝 Setting up logging...")
    setup_logging()
    
    # Optional: Install dependencies
    response = input("\n💾 Install dependencies now? (y/n): ").strip().lower()
    if response == 'y':
        install_dependencies()
    
    print("\n" + "="*70)
    print("✅ Setup Complete!")
    print("="*70)
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the system: python main.py")
    print("3. Check the README.md for detailed documentation")
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    main()
