# 🔧 Fix OAuth State Mismatch Error

## ❌ Error You're Getting:
```
OAuth error: (mismatching_state) CSRF Warning! State not equal in request and response.
```

## 🔍 Root Cause
Django sessions aren't persisting between the OAuth authorization request and callback. This happens when:
- Session cookies aren't being set/read properly
- ngrok is interfering with session cookies
- Session settings aren't configured for HTTPS proxies

## ✅ Complete Fix

### Step 1: Update Files on Your PC

The files have been updated locally. Now commit and push:

```bash
cd C:\Users\geoau\OneDrive\Desktop\YtAut
git add .
git commit -m "Fix OAuth state mismatch - session configuration"
git push
```

### Step 2: Pull Changes on EC2

SSH into EC2 and pull the latest changes:

```bash
ssh -i "C:\Users\geoau\Downloads\ytauto.pem" ubuntu@ec2-65-1-131-185.ap-south-1.compute.amazonaws.com

cd /home/ubuntu/GyoPi/YTAuto
git pull origin main
```

### Step 3: Verify Settings Changes

Check that these settings are in `youtube_shorts_app/settings.py`:

```bash
cat youtube_shorts_app/settings.py | grep -A 15 "Session configuration"
```

You should see:
```python
# Session configuration for OAuth
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_SAVE_EVERY_REQUEST = True

# Security settings for ngrok/OAuth
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Step 4: Ensure Database Migrations

The session table needs to exist:

```bash
cd /home/ubuntu/GyoPi/YTAuto
source /home/ubuntu/GyoPi/.ytauto/bin/activate  # Activate virtual environment
python manage.py migrate
```

### Step 5: Restart Django

```bash
# If Django is running, press Ctrl+C to stop

# Restart Django
python manage.py runserver 0.0.0.0:8000
```

### Step 6: Clear Browser Data

**Important:** Clear your browser cookies and cache:
- Press `Ctrl+Shift+Delete`
- Select "Cookies" and "Cached images"
- Clear data
- Or use Incognito/Private mode

### Step 7: Test OAuth Flow

1. Go to: `https://domestically-pseudomilitaristic-candis.ngrok-free.dev`
2. Try to upload a video or authorize
3. Watch the Django console output for debug messages:
   ```
   🔐 OAuth Authorization:
      Generated state: xxxxx
      Session key: xxxxx
   ```
4. After Google redirects back:
   ```
   🔍 OAuth Callback Debug:
      Stored state in session: xxxxx
      Received state from URL: xxxxx
   ```

---

## 🐛 Troubleshooting

### Still Getting State Mismatch?

**Check Django Console Output:**

Look for the debug messages. If you see:
```
Stored state in session: None
```

This means sessions aren't working. Try:

1. **Check session table exists:**
   ```bash
   python manage.py migrate
   python manage.py shell
   >>> from django.contrib.sessions.models import Session
   >>> Session.objects.all()
   ```

2. **Verify session middleware is active:**
   ```bash
   grep -n "SessionMiddleware" youtube_shorts_app/settings.py
   ```
   Should show it's in MIDDLEWARE list.

3. **Check ngrok isn't blocking cookies:**
   - ngrok free tier should work fine
   - Make sure you're using the HTTPS URL (not HTTP)

### Sessions Work But State Still Mismatches?

If the stored state and received state are DIFFERENT (not None):

1. **Clear all sessions:**
   ```bash
   python manage.py shell
   >>> from django.contrib.sessions.models import Session
   >>> Session.objects.all().delete()
   >>> exit()
   ```

2. **Restart Django**

3. **Clear browser cookies completely**

4. **Try again in Incognito mode**

### Alternative: Disable State Verification (Temporary)

**⚠️ Only for testing - NOT recommended for production!**

If you need to test quickly, you can temporarily disable state verification:

Edit `shorts/youtube_uploader.py` line ~125:

```python
# Temporarily skip state verification for testing
flow = Flow.from_client_secrets_file(
    str(self.client_secrets_file),
    scopes=self.scopes,
    redirect_uri=redirect_uri
    # state=stored_state  # Comment this out temporarily
)
```

**Remember to re-enable it later!**

---

## 📋 Quick Verification Checklist

- [ ] Pushed code changes from PC
- [ ] Pulled changes on EC2
- [ ] Verified session settings in settings.py
- [ ] Ran `python manage.py migrate`
- [ ] Restarted Django on EC2
- [ ] Cleared browser cookies/cache
- [ ] Tested in Incognito mode
- [ ] Checked Django console for debug output
- [ ] Both states match in debug output

---

## 🎯 What Should Happen

**Successful OAuth Flow:**

1. User clicks "Authorize" → Django generates state and saves to session
   ```
   🔐 OAuth Authorization:
      Generated state: abc123xyz
      Session key: session_key_here
   ```

2. User authorizes on Google → Google redirects back with same state

3. Django callback receives state and verifies it matches
   ```
   🔍 OAuth Callback Debug:
      Stored state in session: abc123xyz
      Received state from URL: abc123xyz  ← MUST MATCH!
      Session key: session_key_here  ← MUST BE SAME!
   ```

4. Success!
   ```
   ✅ OAuth callback successful!
   ```

---

## 💡 Key Points

1. **Sessions must persist** between authorization and callback
2. **Same session key** must be used for both requests
3. **ngrok HTTPS** is required for proper cookie handling
4. **Browser cookies** must be enabled
5. **Clear cache** when testing changes

---

**After following these steps, OAuth should work without state mismatch! 🎉**
