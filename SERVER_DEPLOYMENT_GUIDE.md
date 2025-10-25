# Deploy OAuth to Ubuntu Azure Server (Headless)

## Problem
Your Azure Ubuntu server has no GUI/browser, so OAuth browser-based authentication won't work directly.

## Solution: Pre-Authorize Locally, Deploy Credentials

I've updated the code to automatically save credentials to a file that can be deployed to your server.

---

## Step-by-Step Deployment

### 1️⃣ Authorize OAuth Locally (Windows)

1. **Make sure your local server is running**:
   ```bash
   python manage.py runserver
   ```

2. **Upload a video** to trigger OAuth flow
   - Go to http://127.0.0.1:8000/
   - Generate a short
   - Click "Upload to YouTube"
   - Complete the Google authorization in your browser

3. **Verify credentials file was created**:
   - Check that `youtube_credentials.json` now exists in your project root
   - This file contains your OAuth tokens

### 2️⃣ Copy Files to Azure Server

Copy both credential files to your server:

```bash
# Replace with your actual server details
scp client_secret.json your-user@your-azure-server:/home/your-user/YtAut/
scp youtube_credentials.json your-user@your-azure-server:/home/your-user/YtAut/
```

**Alternative using Git (if you want to track client_secret.json):**
```bash
# On local machine
git add client_secret.json  # Only if you want to track it
# Note: youtube_credentials.json should NOT be committed (it's in .gitignore)

# On server
git pull
# Then manually copy youtube_credentials.json
```

### 3️⃣ Verify on Server

SSH into your server and check:

```bash
ssh your-user@your-azure-server
cd /home/your-user/YtAut

# Check files exist
ls -la client_secret.json
ls -la youtube_credentials.json

# Check permissions (should be readable)
chmod 600 youtube_credentials.json
chmod 600 client_secret.json
```

### 4️⃣ Update Server Settings (if needed)

Make sure your server's `settings.py` has the correct configuration:

```python
# In youtube_shorts_app/settings.py
YOUTUBE_CLIENT_SECRETS_FILE = BASE_DIR / 'client_secret.json'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
```

### 5️⃣ Test on Server

```bash
# Restart your Django app on the server
sudo systemctl restart your-django-service
# OR if using gunicorn/supervisor
sudo supervisorctl restart ytaut

# Check logs
tail -f /path/to/your/logs/django.log
```

Try uploading a video - it should now work without requiring browser authentication!

---

## How It Works

The updated code now:

1. **Saves credentials to file** when you authorize locally
2. **Checks file first** before checking session
3. **Auto-refreshes** expired tokens using the refresh token
4. **Falls back to session** for local development

This means:
- ✅ Local dev: Uses browser OAuth (normal flow)
- ✅ Server: Uses pre-authorized credentials from file
- ✅ Tokens auto-refresh when expired (no re-authorization needed)

---

## Important Security Notes

### ⚠️ DO NOT commit `youtube_credentials.json` to Git
This file contains sensitive OAuth tokens. It's already in `.gitignore`.

### ✅ Secure file permissions on server
```bash
chmod 600 youtube_credentials.json
chmod 600 client_secret.json
```

### 🔄 Token Refresh
The OAuth tokens will auto-refresh using the refresh token. You only need to re-authorize if:
- The refresh token expires (rare, usually 6 months+)
- You revoke access in Google account settings
- The credentials file gets corrupted

---

## Troubleshooting

### "No credentials found" on server

**Check:**
```bash
# On server
cd /path/to/YtAut
ls -la youtube_credentials.json
cat youtube_credentials.json  # Should show JSON with tokens
```

**Fix:** Copy the file again from local machine

### "Credentials expired" error

The code should auto-refresh, but if it fails:

1. Delete `youtube_credentials.json` on server
2. Re-authorize locally (upload a video)
3. Copy the new `youtube_credentials.json` to server

### "invalid_client" error on server

This means `client_secret.json` is missing or incorrect on server.

**Fix:**
```bash
# Copy from local to server
scp client_secret.json your-user@your-server:/path/to/YtAut/
```

---

## Alternative: Using Environment Variables

If you prefer, you can also set credentials as environment variables on the server:

```bash
# On server, add to ~/.bashrc or systemd service file
export YOUTUBE_OAUTH_TOKEN="your-token"
export YOUTUBE_OAUTH_REFRESH_TOKEN="your-refresh-token"
# ... etc
```

But the file-based approach is simpler and more standard.

---

## Quick Reference

**Files needed on server:**
- ✅ `client_secret.json` - OAuth client credentials
- ✅ `youtube_credentials.json` - Your authorized tokens

**Commands:**
```bash
# Copy to server
scp client_secret.json youtube_credentials.json user@server:/path/to/YtAut/

# Set permissions
chmod 600 youtube_credentials.json client_secret.json

# Test
python manage.py shell
>>> from shorts.youtube_uploader import YouTubeUploader
>>> uploader = YouTubeUploader()
>>> creds = uploader.load_credentials_from_file()
>>> print(creds.valid if creds else "No credentials")
```

---

## Summary

✅ **No browser needed on server**
✅ **Authorize once locally**
✅ **Deploy credentials file**
✅ **Tokens auto-refresh**
✅ **Works on headless Ubuntu**

The OAuth flow now works seamlessly on your headless Azure server!
