"""
Phase 3: YouTube API Integration
Handles OAuth 2.0 authentication and video uploads to YouTube.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings
from django.urls import reverse

# Allow insecure transport for local development (HTTP instead of HTTPS)
# WARNING: Only use this for local development, never in production!
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class YouTubeUploader:
    """Handle YouTube API authentication and video uploads."""
    
    def __init__(self):
        self.client_secrets_file = settings.YOUTUBE_CLIENT_SECRETS_FILE
        self.scopes = settings.YOUTUBE_SCOPES
        self.api_service_name = settings.YOUTUBE_API_SERVICE_NAME
        self.api_version = settings.YOUTUBE_API_VERSION
    
    def get_credentials_from_session(self, request):
        """Retrieve credentials from session."""
        if 'credentials' in request.session:
            return Credentials(**request.session['credentials'])
        return None
    
    def save_credentials_to_session(self, request, credentials):
        """Save credentials to session."""
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
    
    def has_credentials(self, request):
        """Check if valid credentials exist."""
        credentials = self.get_credentials_from_session(request)
        
        if not credentials:
            return False
        
        # Check if credentials are expired and refresh if needed
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                self.save_credentials_to_session(request, credentials)
                return True
            except Exception:
                return False
        
        return credentials.valid
    
    def get_authorization_url(self, request):
        """Generate OAuth 2.0 authorization URL."""
        # Build the redirect URI
        redirect_uri = request.build_absolute_uri(reverse('shorts:oauth2callback'))
        
        # Ensure insecure transport is allowed for local development
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        
        # Create the flow
        flow = Flow.from_client_secrets_file(
            str(self.client_secrets_file),
            scopes=self.scopes,
            redirect_uri=redirect_uri
        )
        
        # Generate authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Store state in session for verification
        request.session['oauth_state'] = state
        
        return authorization_url
    
    def handle_oauth_callback(self, request):
        """Handle OAuth 2.0 callback and exchange code for credentials."""
        # Verify state
        state = request.session.get('oauth_state')
        if not state:
            raise Exception("Invalid OAuth state")
        
        # Build redirect URI
        redirect_uri = request.build_absolute_uri(reverse('shorts:oauth2callback'))
        
        # Ensure insecure transport is allowed for local development
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        
        # Create flow
        flow = Flow.from_client_secrets_file(
            str(self.client_secrets_file),
            scopes=self.scopes,
            redirect_uri=redirect_uri,
            state=state
        )
        
        # Exchange authorization code for credentials
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)
        
        # Save credentials
        credentials = flow.credentials
        self.save_credentials_to_session(request, credentials)
        
        # Clean up state
        del request.session['oauth_state']
    
    def upload_video(self, request, video_path, title, description, category='22', privacy_status='public', is_shorts=True):
        """
        Upload a video to YouTube as a Short.
        
        Args:
            request: Django request object with credentials
            video_path: Path to the video file
            title: Video title (max 100 chars for Shorts)
            description: Video description
            category: YouTube category ID (22 = People & Blogs)
            privacy_status: 'public', 'private', or 'unlisted'
            is_shorts: Upload as YouTube Short (adds #Shorts tag)
        
        Returns:
            str: YouTube video ID
        """
        # Get credentials
        credentials = self.get_credentials_from_session(request)
        if not credentials:
            raise Exception("No valid credentials found")
        
        # Build YouTube API client
        youtube = build(
            self.api_service_name,
            self.api_version,
            credentials=credentials
        )
        
        # Prepare video metadata for YouTube Shorts
        # Ensure title is not too long (YouTube Shorts recommendation: max 100 chars)
        shorts_title = title[:100] if len(title) > 100 else title
        
        # Add #Shorts tag to description for YouTube Shorts algorithm
        shorts_description = self._prepare_shorts_description(description, is_shorts)
        
        # Extract and prepare tags
        tags = self._extract_hashtags(description)
        if is_shorts and 'Shorts' not in tags:
            tags.insert(0, 'Shorts')  # Add Shorts tag first
        
        body = {
            'snippet': {
                'title': shorts_title,
                'description': shorts_description,
                'tags': tags,
                'categoryId': category
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create media upload
        media = MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True,
            mimetype='video/mp4'
        )
        
        # Execute upload
        request_obj = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request_obj.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")
        
        return response['id']
    
    def _prepare_shorts_description(self, description, is_shorts=True):
        """
        Prepare description for YouTube Shorts.
        Adds #Shorts tag if not present.
        
        Args:
            description (str): Original description
            is_shorts (bool): Whether this is a YouTube Short
            
        Returns:
            str: Description with #Shorts tag
        """
        if not is_shorts:
            return description
        
        # Check if #Shorts is already in description
        if '#Shorts' not in description and '#shorts' not in description:
            # Add #Shorts at the beginning
            description = f"#Shorts\n\n{description}"
        
        return description
    
    def _extract_hashtags(self, description):
        """Extract hashtags from description text."""
        words = description.split()
        hashtags = [word[1:] for word in words if word.startswith('#')]
        
        # Ensure Shorts tag is included
        if not hashtags:
            hashtags = ['Shorts', 'YouTubeShorts']
        elif 'Shorts' not in hashtags and 'shorts' not in hashtags:
            hashtags.insert(0, 'Shorts')
        
        return hashtags


# Standalone function for testing
def test_upload():
    """Test function for uploading a video (requires manual OAuth flow)."""
    print("YouTube uploader module loaded successfully!")
    print("To use this, you need to:")
    print("1. Set up a Google Cloud project")
    print("2. Enable YouTube Data API v3")
    print("3. Create OAuth 2.0 credentials")
    print("4. Download client_secret.json to the project root")


if __name__ == "__main__":
    test_upload()
