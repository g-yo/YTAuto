# 🎥 YouTube API Setup - Final Steps

## You've Downloaded client_secret JSON - Now What?

### Step 1: Rename and Move the File

1. **Find your downloaded file**
   - Usually in: `Downloads/client_secret_XXXXX.json`

2. **Rename it to exactly:**
   ```
   client_secret.json
   ```

3. **Move it to your project root:**
   ```
   YtAut/
   ├── client_secret.json  ← Place it here!
   ├── manage.py
   ├── requirements.txt
   └── ...
   ```

### Step 2: Verify the File Format

Your `client_secret.json` should look like this:

```json
{
  "web": {
    "client_id": "xxxxx.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-xxxxx",
    "redirect_uris": ["http://localhost:8000/oauth2callback/"]
  }
}
```

### Step 3: Security Check

⚠️ **IMPORTANT:** Never commit this file to Git!

The `.gitignore` already includes it, but double-check:
```bash
# Check if it's ignored
git status
# Should NOT show client_secret.json
```

---

## 🎬 How to Use YouTube Upload

### Complete Workflow:

1. **Generate a Short**
   - Go to http://localhost:8000
   - Paste YouTube URL
   - Set start/end times
   - Click "Generate Short"

2. **Review the Result**
   - Video preview appears
   - AI-generated title and hashtags shown
   - Click "Upload to YouTube" button

3. **First-Time Authentication**
   - Browser redirects to Google login
   - Sign in with your YouTube account
   - Google shows permission request:
     - "YouTube Shorts Automation wants to upload videos"
   - Click "Allow"

4. **Automatic Upload**
   - Redirects back to your app
   - Video uploads automatically
   - Success message appears
   - Video ID displayed

5. **View on YouTube**
   - Click "View on YouTube" button
   - Or go to: https://studio.youtube.com

### Subsequent Uploads:

After first authentication, you won't need to login again!
- Just click "Upload to YouTube"
- Video uploads immediately
- Credentials saved in session

---

## 🔍 What Happens Behind the Scenes

### OAuth 2.0 Flow:

```
User clicks "Upload to YouTube"
    ↓
App checks for credentials
    ↓
No credentials? → Redirect to Google
    ↓
User grants permission
    ↓
Google sends authorization code
    ↓
App exchanges code for access token
    ↓
Token saved in session
    ↓
App uploads video using token
    ↓
Success! Video on YouTube
```

### AI Title Generation:

```
Original video title: "Amazing Python Tutorial"
    ↓
Sent to Gemini API
    ↓
AI analyzes and generates:
    Title: "Python Magic in 30 Seconds! 🐍"
    Hashtags: "#Python #Coding #Programming #Tutorial #LearnToCode"
    ↓
Used for YouTube upload
```

---

## 📊 API Quotas & Limits

### YouTube Data API v3
- **Default Quota:** 10,000 units/day
- **Upload Cost:** 1,600 units per video
- **Daily Uploads:** ~6 videos (with default quota)
- **Reset:** Daily at midnight Pacific Time

### Quota Breakdown:
- Video upload: 1,600 units
- Video list: 1 unit
- Video update: 50 units

### Need More Quota?
1. Go to Google Cloud Console
2. APIs & Services → YouTube Data API v3
3. Click "QUOTAS"
4. Request increase (explain your use case)

### Gemini API
- **Free Tier:** 60 requests/minute
- **Cost:** Free for moderate use
- **Rate Limit:** Automatic retry on limit

---

## ✅ Testing Checklist

After setup, test these:

- [ ] `client_secret.json` in project root
- [ ] Server running: `python manage.py runserver`
- [ ] Generate a short successfully
- [ ] Click "Upload to YouTube"
- [ ] Google login page appears
- [ ] Grant permissions
- [ ] Redirect back to app
- [ ] Video uploads successfully
- [ ] Video appears in YouTube Studio

---

## 🐛 Common Issues

### "client_secret.json not found"
- Check file is in project root (same folder as manage.py)
- Check filename is exactly `client_secret.json`
- Restart the server

### "Redirect URI mismatch"
- In Google Cloud Console, check redirect URI is exactly:
  `http://localhost:8000/oauth2callback/`
- No trailing spaces or extra characters
- Must match exactly

### "Access blocked: This app's request is invalid"
- Add yourself as a test user in OAuth consent screen
- Make sure YouTube Data API v3 is enabled
- Check scopes include youtube.upload

### "The app is not verified"
- This is normal for testing
- Click "Advanced" → "Go to [app name] (unsafe)"
- Only you can access (test user)

### "Quota exceeded"
- Wait until midnight Pacific Time
- Or request quota increase
- Each upload = 1,600 units

---

## 🎯 Quick Reference

### Important URLs:
- **Google Cloud Console:** https://console.cloud.google.com/
- **API Library:** https://console.cloud.google.com/apis/library
- **Credentials:** https://console.cloud.google.com/apis/credentials
- **YouTube Studio:** https://studio.youtube.com
- **Gemini API:** https://makersuite.google.com/app/apikey

### File Locations:
- **Credentials:** `YtAut/client_secret.json`
- **Environment:** `YtAut/.env.example` (copy to `.env`)
- **Settings:** `YtAut/youtube_shorts_app/settings.py`

### Commands:
```bash
# Start server
python manage.py runserver

# Check if file exists
dir client_secret.json

# Test video processor
python test_video_processor.py
```

---

## 🎉 You're All Set!

Once `client_secret.json` is in place:

1. Restart your server (Ctrl+C, then `python manage.py runserver`)
2. Generate a short
3. Click "Upload to YouTube"
4. Authenticate once
5. Enjoy automatic uploads! 🚀

**The AI will automatically generate titles and hashtags for every short!**
