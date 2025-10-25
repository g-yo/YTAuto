# Why youtube_credentials.json Was Not Created

## The Issue

You triggered OAuth but `youtube_credentials.json` was not created.

## Root Cause

**The credentials file is ONLY created when OAuth succeeds.**

If you're getting the `invalid_client` error, the OAuth flow **fails before** credentials are saved.

## The Flow

```
1. Click "Upload to YouTube"
2. Redirect to Google authorization
3. You authorize
4. Google redirects back with code
5. ❌ FAILS HERE with "invalid_client" error
6. ❌ Credentials never saved (because step 5 failed)
```

## Solution: Fix OAuth First

You MUST fix the `invalid_client` error before credentials can be saved.

### Step 1: Fix the OAuth Error

Follow `README_OAUTH_FIX.md`:

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click your OAuth 2.0 Client ID
3. Add this EXACT redirect URI:
   ```
   http://127.0.0.1:8000/oauth2callback/
   ```
4. Click **SAVE**

### Step 2: Test OAuth Again

1. Restart Django server:
   ```bash
   python manage.py runserver
   ```

2. Upload a video

3. Watch the console output - you should see:
   ```
   🔄 Saving credentials...
      ✅ Saved to session
      📝 Attempting to save to: C:\Users\...\youtube_credentials.json
      ✅ Credentials saved to ...
      ✅ File verified to exist
   💾 Credentials saved to both session and file
   ```

4. Check if file exists:
   ```bash
   dir youtube_credentials.json
   ```

### Step 3: If Still No File

If OAuth succeeds but file still not created, run:

```bash
python save_credentials_manually.py
```

This will extract credentials from your session and save them to file.

## How to Know If OAuth Succeeded

**Success looks like:**
```
🔐 OAuth Authorization:
   Generated state: ...
   Redirect URI: http://127.0.0.1:8000/oauth2callback/

🔍 OAuth Callback Debug:
   Stored state: ...
   Received state: ...
   
🔄 Saving credentials...
   ✅ Saved to session
   📝 Attempting to save to: ...
   ✅ Credentials saved to ...
   ✅ File verified to exist
💾 Credentials saved to both session and file

✅ OAuth callback successful!
```

**Failure looks like:**
```
🔐 OAuth Authorization:
   Generated state: ...
   
🔍 OAuth Callback Debug:
   Stored state: ...
   Received state: ...
   
❌ OAuth error: (invalid_client) Unauthorized
```

## Quick Checklist

- [ ] Fixed `invalid_client` error in Google Cloud Console
- [ ] Restarted Django server
- [ ] Tried OAuth again
- [ ] Checked console output for "Credentials saved" message
- [ ] Verified file exists: `dir youtube_credentials.json`

## Still Not Working?

### Check 1: Is OAuth Actually Succeeding?

Look for this in console output:
```
✅ OAuth callback successful!
```

If you see `❌ OAuth error`, fix that first.

### Check 2: Check File Permissions

```bash
# Windows
icacls youtube_credentials.json
```

### Check 3: Run Manual Save

```bash
python save_credentials_manually.py
```

This will tell you if credentials exist in session.

### Check 4: Check Django Settings

```bash
python manage.py shell
```

```python
from django.conf import settings
print(settings.BASE_DIR)
# Should show: C:\Users\geoau\OneDrive\Desktop\YtAut

from shorts.youtube_uploader import YouTubeUploader
uploader = YouTubeUploader()
print(uploader.credentials_file)
# Should show: C:\Users\geoau\OneDrive\Desktop\YtAut\youtube_credentials.json
```

## Summary

**The file is not created because OAuth is failing.**

Fix the `invalid_client` error first, then the file will be created automatically.

See `README_OAUTH_FIX.md` for how to fix the OAuth error.
