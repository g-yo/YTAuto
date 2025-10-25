# Quick Fix Checklist for "invalid_client" Error

## The Problem
You're getting: `❌ OAuth error: (invalid_client) Unauthorized`

## The Solution (Follow in Order)

### ✅ Step 1: Check Google Cloud Console

1. Open: https://console.cloud.google.com/apis/credentials
2. Find your OAuth 2.0 Client ID
3. Click on it to edit
4. Scroll to **Authorized redirect URIs**
5. Make sure this EXACT URI is listed:
   ```
   http://127.0.0.1:8000/oauth2callback/
   ```
   ⚠️ **Important**: Must include the trailing slash `/`
6. Click **SAVE**

### ✅ Step 2: Verify Your client_secret.json

Your `client_secret.json` should have this structure:
```json
{
  "web": {
    "client_id": "YOUR_ID.apps.googleusercontent.com",
    "client_secret": "YOUR_SECRET",
    "redirect_uris": ["http://127.0.0.1:8000/oauth2callback/"]
  }
}
```

**Check these:**
- [ ] It says `"web"` not `"installed"`
- [ ] The redirect URI matches exactly: `http://127.0.0.1:8000/oauth2callback/`
- [ ] The file is in the project root directory

### ✅ Step 3: If Still Not Working - Download Fresh Credentials

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Choose **Web application**
4. Name it: "YouTube Shorts Uploader"
5. Under **Authorized redirect URIs**, add:
   ```
   http://127.0.0.1:8000/oauth2callback/
   ```
6. Click **CREATE**
7. Click **DOWNLOAD JSON**
8. Replace your `client_secret.json` with the downloaded file
9. Rename it to `client_secret.json` if needed

### ✅ Step 4: Clear Sessions and Restart

Run these commands:
```bash
python manage.py clearsessions
```

Then restart your Django server.

### ✅ Step 5: Test Again

1. Go to your app
2. Try uploading a video
3. The OAuth flow should now work

## Common Mistakes

❌ **Wrong redirect URI** - Must be exactly: `http://127.0.0.1:8000/oauth2callback/`
❌ **Missing trailing slash** - Don't forget the `/` at the end
❌ **Using "Desktop app" credentials** - Must use "Web application"
❌ **Forgot to click Save** in Google Cloud Console
❌ **Using https instead of http** for local development

## Still Not Working?

The redirect URI in your Google Cloud Console MUST EXACTLY match what your app is using.

Your app is using: `http://127.0.0.1:8000/oauth2callback/`

Double-check in Google Cloud Console that this exact URI is listed.

## Need the Full Guide?

See `OAUTH_FIX_GUIDE.md` for detailed explanations.
