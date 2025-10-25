# OAuth "invalid_client" Error - Fix Guide

## Problem
You're getting `❌ OAuth error: (invalid_client) Unauthorized` when trying to authenticate with YouTube.

## Root Cause
The `invalid_client` error means Google's OAuth server is rejecting your client credentials. This happens when:
1. The redirect URI in Google Cloud Console doesn't match what your app is using
2. The client_secret.json file is outdated or incorrect
3. The OAuth client has been deleted or disabled in Google Cloud Console

## Solution Steps

### Step 1: Verify Google Cloud Console Configuration

1. Go to [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
2. Find your OAuth 2.0 Client ID (the one matching your client_secret.json)
3. Click on it to edit
4. Under **Authorized redirect URIs**, make sure you have BOTH:
   ```
   http://127.0.0.1:8000/oauth2callback/
   http://localhost:8000/oauth2callback/
   ```
5. Click **Save**

### Step 2: Verify client_secret.json

Your `client_secret.json` should look like this:
```json
{
  "web": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": [
      "http://127.0.0.1:8000/oauth2callback/"
    ]
  }
}
```

**Important**: Make sure it says `"web"` not `"installed"`. If it says `"installed"`, you need to create a new OAuth client as a **Web application**.

### Step 3: Download Fresh Credentials (Recommended)

If the above doesn't work, create fresh credentials:

1. Go to [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Select **Web application**
4. Give it a name (e.g., "YouTube Shorts Uploader")
5. Under **Authorized redirect URIs**, add:
   ```
   http://127.0.0.1:8000/oauth2callback/
   http://localhost:8000/oauth2callback/
   ```
6. Click **Create**
7. Download the JSON file
8. Replace your current `client_secret.json` with the downloaded file

### Step 4: Clear Django Sessions

After updating credentials, clear your Django sessions:

```bash
python manage.py clearsessions
```

Or delete the session files manually if using file-based sessions.

### Step 5: Test Again

1. Restart your Django server
2. Try uploading a video again
3. The OAuth flow should now work

## Common Mistakes to Avoid

❌ **Don't use "Desktop app" or "Installed app" credentials** - Use "Web application"
❌ **Don't forget the trailing slash** in redirect URIs - `http://127.0.0.1:8000/oauth2callback/` (with slash)
❌ **Don't mix http and https** - For local development, use `http://` not `https://`
❌ **Don't forget to click Save** in Google Cloud Console after making changes

## Still Not Working?

If you're still getting the error:

1. Check if the YouTube Data API v3 is enabled in your Google Cloud project
2. Make sure your OAuth consent screen is configured
3. Verify your Google Cloud project is not suspended
4. Try creating a completely new OAuth client from scratch

## Need More Help?

Run this diagnostic script to check your configuration:
```bash
python check_oauth_config.py
```
