# Deploy OAuth to Headless Server (Ubuntu Azure)

## Problem
OAuth requires browser authentication, but your Azure Ubuntu server has no GUI/browser.

## Solution: Pre-Authorize Locally, Deploy Credentials

### Step 1: Authorize OAuth Locally (Windows)

1. Run your Django app locally:
   ```bash
   python manage.py runserver
   ```

2. Upload a video to trigger OAuth flow
3. Complete the browser authorization
4. This creates credentials in your Django session

### Step 2: Modify Code to Save Credentials to File

We need to save OAuth credentials to a file instead of just session.

Add this to `shorts/youtube_uploader.py`:

```python
def save_credentials_to_file(self, credentials, filepath='youtube_credentials.json'):
    """Save credentials to a JSON file."""
    import json
    creds_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    with open(filepath, 'w') as f:
        json.dump(creds_data, f)
    print(f"✅ Credentials saved to {filepath}")

def load_credentials_from_file(self, filepath='youtube_credentials.json'):
    """Load credentials from a JSON file."""
    import json
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        creds_data = json.load(f)
    return Credentials(**creds_data)
```

### Step 3: Generate Credentials File Locally

Run this script locally after authorizing:

```python
# generate_credentials.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_shorts_app.settings')
django.setup()

from django.test import RequestFactory
from shorts.youtube_uploader import YouTubeUploader

# You need to have completed OAuth flow first
# This script extracts credentials from your session

print("After completing OAuth flow, run this to save credentials")
print("Or use the management command below")
```

### Step 4: Copy Files to Server

Copy these files to your Azure server:

```bash
# On your local machine
scp client_secret.json your-user@your-server:/path/to/YtAut/
scp youtube_credentials.json your-user@your-server:/path/to/YtAut/
```

### Step 5: Update Server Code to Use File Credentials

Modify the code to check for file credentials first:

```python
def get_credentials_from_session(self, request):
    """Retrieve credentials from file first, then session."""
    # Try loading from file first (for server deployment)
    file_creds = self.load_credentials_from_file()
    if file_creds and file_creds.valid:
        return file_creds
    
    # Fall back to session (for local development)
    if 'credentials' in request.session:
        return Credentials(**request.session['credentials'])
    
    return None
```

---

## Alternative: Service Account (More Complex)

Service accounts don't require browser auth, but YouTube API has limitations:
- ❌ Cannot upload to personal YouTube channels
- ✅ Only works with YouTube Brand Accounts with proper delegation
- More complex setup

---

## Recommended Approach for Your Case

**Use Pre-Authorization Method:**

1. Authorize locally (you already did this)
2. Save credentials to file
3. Deploy file to server
4. Server uses saved credentials (they auto-refresh)

This is the standard approach for headless servers with OAuth.
