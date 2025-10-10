"""
Setup script to initialize the YouTube Shorts Automation project.
Run this after installing requirements.txt
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_shorts_app.settings')
django.setup()

def create_directories():
    """Create necessary directories for the project."""
    directories = [
        BASE_DIR / 'downloads',
        BASE_DIR / 'outputs',
        BASE_DIR / 'media',
        BASE_DIR / 'media' / 'shorts',
        BASE_DIR / 'static',
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def run_migrations():
    """Run Django migrations."""
    print("\n📦 Running database migrations...")
    from django.core.management import call_command
    
    try:
        call_command('makemigrations', 'shorts')
        call_command('migrate')
        print("✓ Migrations completed successfully")
    except Exception as e:
        print(f"✗ Migration error: {e}")

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print("\n🎬 Checking for FFmpeg...")
    import subprocess
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print("✓ FFmpeg is installed")
            return True
        else:
            print("✗ FFmpeg not found")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg not found in PATH")
        print("  Please install FFmpeg:")
        print("  - Windows: Download from https://ffmpeg.org/download.html")
        print("  - Mac: brew install ffmpeg")
        print("  - Linux: sudo apt-get install ffmpeg")
        return False

def check_api_setup():
    """Check if API credentials are configured."""
    print("\n🔑 Checking API configuration...")
    
    # Check for client_secret.json
    client_secret = BASE_DIR / 'client_secret.json'
    if client_secret.exists():
        print("✓ YouTube API credentials found (client_secret.json)")
    else:
        print("⚠ YouTube API credentials not found")
        print("  To enable YouTube uploads:")
        print("  1. Go to https://console.cloud.google.com/")
        print("  2. Create OAuth 2.0 credentials")
        print("  3. Download as 'client_secret.json' in project root")
    
    # Check for Gemini API key
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if gemini_key:
        print("✓ Gemini API key found in environment")
    else:
        print("⚠ Gemini API key not found")
        print("  To enable AI title generation:")
        print("  1. Get API key from https://makersuite.google.com/app/apikey")
        print("  2. Set environment variable: GEMINI_API_KEY")

def main():
    """Main setup function."""
    print("=" * 60)
    print("YouTube Shorts Automation - Setup Script")
    print("=" * 60)
    
    # Create directories
    print("\n📁 Creating project directories...")
    create_directories()
    
    # Run migrations
    run_migrations()
    
    # Check FFmpeg
    check_ffmpeg()
    
    # Check API setup
    check_api_setup()
    
    print("\n" + "=" * 60)
    print("✨ Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Open: http://localhost:8000")
    print("3. Start creating YouTube Shorts!")
    print("\nFor full documentation, see README.md")

if __name__ == "__main__":
    main()
