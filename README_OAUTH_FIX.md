# OAuth "invalid_client" Error - Complete Fix Guide

## 🔴 The Error You're Seeing

```
❌ OAuth error: (invalid_client) Unauthorized
```

## 🎯 Root Cause

The `invalid_client` error means Google's OAuth server is rejecting your client credentials. This happens when:

1. **Redirect URI mismatch** - The URI in Google Cloud Console doesn't match your app's URI
2. **Wrong credentials** - The `client_secret.json` file is incorrect or outdated
3. **Wrong client type** - Using "Desktop app" instead of "Web application"

## ✅ Solution (3 Steps)

### Step 1: Fix Google Cloud Console Configuration

1. Go to: **https://console.cloud.google.com/apis/credentials**
2. Find your OAuth 2.0 Client ID (should match the client_id in your `client_secret.json`)
3. Click on it to edit
4. Under **Authorized redirect URIs**, add this EXACT URI:
   ```
   http://127.0.0.1:8000/oauth2callback/
   ```
   ⚠️ **Critical**: Must include the trailing slash `/`
5. Click **SAVE** (don't forget this!)

### Step 2: Verify client_secret.json

Your `client_secret.json` should look like this:

```json
{
  "web": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "your-project",
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

**Important checks:**
- ✅ Must say `"web"` not `"installed"`
- ✅ Must have `redirect_uris` array
- ✅ Must be in project root directory

### Step 3: Test Your Configuration

1. **Check configuration** - Visit: http://127.0.0.1:8000/debug-oauth/
   - This will show you if there are any configuration issues
   
2. **Clear sessions**:
   ```bash
   python manage.py clearsessions
   ```

3. **Restart Django server**:
   ```bash
   python manage.py runserver
   ```

4. **Try OAuth flow again** - Upload a video and authorize

## 🔧 If Still Not Working - Create Fresh Credentials

If the above doesn't work, create completely new credentials:

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Select **Web application** (NOT Desktop app)
4. Name: "YouTube Shorts Uploader"
5. Under **Authorized redirect URIs**, add:
   ```
   http://127.0.0.1:8000/oauth2callback/
   ```
6. Click **CREATE**
7. Click **DOWNLOAD JSON**
8. Replace your `client_secret.json` with the downloaded file
9. Restart your Django server

## 🛠️ Diagnostic Tools

I've created several tools to help you:

1. **Check configuration**:
   ```bash
   python check_oauth_config.py
   ```

2. **Verify setup**:
   ```bash
   python verify_oauth_setup.py
   ```

3. **Web debug endpoint**:
   - Visit: http://127.0.0.1:8000/debug-oauth/
   - Shows real-time configuration status

## ❌ Common Mistakes to Avoid

| Mistake | Correct Way |
|---------|-------------|
| ❌ Using "Desktop app" credentials | ✅ Use "Web application" |
| ❌ `http://127.0.0.1:8000/oauth2callback` (no slash) | ✅ `http://127.0.0.1:8000/oauth2callback/` (with slash) |
| ❌ Using `https://` for local dev | ✅ Use `http://` for local dev |
| ❌ Forgetting to click "Save" in Console | ✅ Always click "Save" |
| ❌ Wrong `client_secret.json` file | ✅ Download fresh from Console |

## 🔍 Understanding the Error

Your logs show:
```
🔐 OAuth Authorization:
   Generated state: 5gAun9v8yuwwl4vqS5pLMie644Nerw
   Redirect URI: http://127.0.0.1:8000/oauth2callback/
   
🔍 OAuth Callback Debug:
   Stored state: 5gAun9v8yuwwl4vqS5pLMie644Nerw
   Received state: 5gAun9v8yuwwl4vqS5pLMie644Nerw
   ✅ States match!
   
❌ OAuth error: (invalid_client) Unauthorized
```

The state verification is working correctly, which means:
- ✅ Sessions are working
- ✅ OAuth flow is correct
- ❌ **Problem is with Google Cloud Console configuration**

This confirms the issue is with the redirect URI or client credentials in Google Cloud Console.

## 📝 Quick Checklist

Before trying again, verify:

- [ ] Redirect URI in Google Cloud Console is exactly: `http://127.0.0.1:8000/oauth2callback/`
- [ ] Redirect URI includes the trailing slash `/`
- [ ] You clicked "Save" in Google Cloud Console
- [ ] Your `client_secret.json` says `"web"` not `"installed"`
- [ ] You've cleared Django sessions
- [ ] You've restarted the Django server

## 🆘 Still Need Help?

1. Run the diagnostic: `python check_oauth_config.py`
2. Visit: http://127.0.0.1:8000/debug-oauth/
3. Check the console output for detailed error messages
4. Verify YouTube Data API v3 is enabled in your Google Cloud project

## 📚 Additional Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- See `QUICK_FIX_CHECKLIST.md` for a simple step-by-step guide
- See `OAUTH_FIX_GUIDE.md` for detailed explanations

---

**TL;DR**: Go to Google Cloud Console, make sure the redirect URI is exactly `http://127.0.0.1:8000/oauth2callback/` (with trailing slash), click Save, restart your server, try again.
