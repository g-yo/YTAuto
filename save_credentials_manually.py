"""
Manual script to save OAuth credentials from session to file
Run this AFTER successfully completing OAuth authorization
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_shorts_app.settings')
django.setup()

from django.contrib.sessions.models import Session
from shorts.youtube_uploader import YouTubeUploader
from google.oauth2.credentials import Credentials
import json

def save_credentials_from_session():
    """Extract credentials from Django session and save to file"""
    print("🔍 Looking for OAuth credentials in sessions...\n")
    
    uploader = YouTubeUploader()
    found = False
    
    # Check all active sessions
    sessions = Session.objects.filter(expire_date__gte=django.utils.timezone.now())
    print(f"Found {sessions.count()} active session(s)")
    
    for session in sessions:
        session_data = session.get_decoded()
        
        if 'credentials' in session_data:
            print(f"\n✅ Found credentials in session: {session.session_key}")
            
            creds_data = session_data['credentials']
            print(f"   Token: {creds_data.get('token', 'N/A')[:50]}...")
            print(f"   Refresh token: {'Yes' if creds_data.get('refresh_token') else 'No'}")
            print(f"   Scopes: {', '.join(creds_data.get('scopes', []))}")
            
            # Create credentials object
            credentials = Credentials(**creds_data)
            
            # Save to file
            print(f"\n💾 Saving to file...")
            uploader.save_credentials_to_file(credentials)
            
            found = True
            break
    
    if not found:
        print("\n❌ No credentials found in any session")
        print("\nThis means:")
        print("1. You haven't completed OAuth authorization yet, OR")
        print("2. The OAuth flow failed (check for 'invalid_client' error), OR")
        print("3. Sessions have expired")
        print("\n📝 To fix:")
        print("1. First fix the 'invalid_client' error (see README_OAUTH_FIX.md)")
        print("2. Then upload a video to trigger OAuth")
        print("3. Run this script again")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = save_credentials_from_session()
        if success:
            print("\n" + "=" * 60)
            print("✅ SUCCESS!")
            print("Credentials saved to youtube_credentials.json")
            print("You can now copy this file to your server.")
            print("=" * 60)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
