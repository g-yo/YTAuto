"""
Test script to verify cookies are working with yt-dlp
"""
import yt_dlp
from pathlib import Path

def test_cookies():
    cookies_path = Path(__file__).parent / 'cookies' / 'cookies.txt'
    
    print(f"Cookies file exists: {cookies_path.exists()}")
    print(f"Cookies path: {cookies_path}")
    
    # Test video URL (replace with your actual video)
    test_url = "https://www.youtube.com/watch?v=dmjp2bM346M"
    
    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
        'skip_download': True,  # Don't download, just test authentication
    }
    
    # Try with cookies file
    if cookies_path.exists():
        ydl_opts['cookiefile'] = str(cookies_path)
        print(f"\n🍪 Testing with cookies file...")
    else:
        print(f"\n⚠️  Cookies file not found, trying browser cookies...")
        ydl_opts['cookiesfrombrowser'] = ('chrome',)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            print(f"\n✅ SUCCESS! Video info retrieved:")
            print(f"   Title: {info.get('title', 'Unknown')}")
            print(f"   Duration: {info.get('duration', 0)} seconds")
            print(f"   Uploader: {info.get('uploader', 'Unknown')}")
            return True
    except Exception as e:
        print(f"\n❌ FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    test_cookies()
