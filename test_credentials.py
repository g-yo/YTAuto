"""
⚠️  DEPRECATED: This script is no longer needed.

The app now uses session-based OAuth flow instead of file-based credentials.
No need to test credential files - OAuth works automatically when you upload.

See OAUTH_SESSION_FLOW.md for details on the new authentication flow.

Legacy test script (kept for reference only)
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_shorts_app.settings')
django.setup()

from shorts.youtube_uploader import YouTubeUploader
from pathlib import Path

def test_credentials():
    """Test if credentials are properly configured"""
    print("🔍 Testing OAuth Credentials\n")
    print("=" * 60)
    
    uploader = YouTubeUploader()
    
    # Check client_secret.json
    print("\n1️⃣  Checking client_secret.json...")
    if uploader.client_secrets_file.exists():
        print(f"   ✅ Found: {uploader.client_secrets_file}")
    else:
        print(f"   ❌ NOT FOUND: {uploader.client_secrets_file}")
        print("   You need to download this from Google Cloud Console")
        return False
    
    # Check youtube_credentials.json
    print("\n2️⃣  Checking youtube_credentials.json...")
    if uploader.credentials_file.exists():
        print(f"   ✅ Found: {uploader.credentials_file}")
    else:
        print(f"   ⚠️  NOT FOUND: {uploader.credentials_file}")
        print("   This file is created after first OAuth authorization")
        print("   Run the app and upload a video to create it")
        return False
    
    # Try loading credentials
    print("\n3️⃣  Loading credentials from file...")
    creds = uploader.load_credentials_from_file()
    
    if not creds:
        print("   ❌ Failed to load credentials")
        return False
    
    print("   ✅ Credentials loaded successfully")
    
    # Check if valid
    print("\n4️⃣  Checking credential validity...")
    if creds.valid:
        print("   ✅ Credentials are VALID")
        print(f"   📋 Scopes: {', '.join(creds.scopes)}")
    elif creds.expired and creds.refresh_token:
        print("   ⚠️  Credentials expired, but refresh token available")
        print("   🔄 Attempting to refresh...")
        try:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
            uploader.save_credentials_to_file(creds)
            print("   ✅ Credentials refreshed successfully!")
        except Exception as e:
            print(f"   ❌ Failed to refresh: {e}")
            return False
    else:
        print("   ❌ Credentials are INVALID and cannot be refreshed")
        print("   You need to re-authorize")
        return False
    
    # Test YouTube API connection
    print("\n5️⃣  Testing YouTube API connection...")
    try:
        from googleapiclient.discovery import build
        youtube = build(
            uploader.api_service_name,
            uploader.api_version,
            credentials=creds
        )
        
        # Try to get channel info
        request = youtube.channels().list(
            part="snippet",
            mine=True
        )
        response = request.execute()
        
        if response.get('items'):
            channel = response['items'][0]['snippet']
            print(f"   ✅ Connected to YouTube!")
            print(f"   📺 Channel: {channel.get('title', 'Unknown')}")
        else:
            print("   ⚠️  Connected but no channel found")
        
    except Exception as e:
        print(f"   ❌ API connection failed: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("\n✅ ALL TESTS PASSED!")
    print("\nYour OAuth setup is working correctly.")
    print("You can now upload videos to YouTube from this machine.")
    
    return True

if __name__ == "__main__":
    try:
        success = test_credentials()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
