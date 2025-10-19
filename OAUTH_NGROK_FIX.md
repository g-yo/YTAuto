# 🔧 Fix OAuth redirect_uri_mismatch Error with ngrok

## ❌ Error You're Getting:
```
Error 400: redirect_uri_mismatch
```

## ✅ Complete Fix (3 Steps)

### Step 1: Google Cloud Console Setup

1. Go to [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
2. Select your project **"YT-Geopi"**
3. Click on your **OAuth 2.0 Client ID**
4. Under **Authorized redirect URIs**, add these **exact** URLs:

```
https://domestically-pseudomilitaristic-candis.ngrok-free.dev/oauth2callback
http://localhost:8000/oauth2callback
http://127.0.0.1:8000/oauth2callback
```

**Important Notes:**
- ❌ NO trailing slash at the end
- ✅ Must be HTTPS for ngrok
- ✅ Must match exactly (case-sensitive)

5. Click **SAVE**
6. Wait 1-2 minutes for changes to propagate

---

### Step 2: Update EC2 Django Settings

SSH into your EC2 instance:

```bash
ssh -i "C:\Users\geoau\Downloads\ytauto.pem" ubuntu@ec2-65-1-131-185.ap-south-1.compute.amazonaws.com
```

Edit the settings file:

```bash
cd /home/ubuntu/GyoPi/YTAuto/youtube_shorts_app
nano settings.py
```

**Find and update these lines:**

```python
# Update ALLOWED_HOSTS (around line 29)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'domestically-pseudomilitaristic-candis.ngrok-free.dev', 'ec2-65-1-131-185.ap-south-1.compute.amazonaws.com', '*']

# Add CSRF_TRUSTED_ORIGINS (add after ALLOWED_HOSTS)
CSRF_TRUSTED_ORIGINS = [
    'https://domestically-pseudomilitaristic-candis.ngrok-free.dev',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

**Save the file:**
- Press `Ctrl+X`
- Press `Y`
- Press `Enter`

---

### Step 3: Restart Django on EC2

```bash
# If Django is running, press Ctrl+C to stop it

# Restart Django
cd /home/ubuntu/GyoPi/YTAuto
python manage.py runserver 0.0.0.0:8000
```

---

## 🧪 Test OAuth Flow

1. **Open your ngrok URL:**
   ```
   https://domestically-pseudomilitaristic-candis.ngrok-free.dev
   ```

2. **Try to upload a video** or click "Authorize with YouTube"

3. **You should be redirected to Google OAuth** without errors

4. **After authorization**, you'll be redirected back to your app

---

## 🐛 Troubleshooting

### Still getting redirect_uri_mismatch?

**Check these:**

1. **Exact URL match in Google Console:**
   ```bash
   # The redirect URI Django sends
   https://domestically-pseudomilitaristic-candis.ngrok-free.dev/oauth2callback
   
   # Must match EXACTLY in Google Console (no trailing slash)
   ```

2. **Wait for Google changes to propagate:**
   - After updating Google Console, wait 2-5 minutes
   - Clear your browser cache
   - Try in incognito/private mode

3. **Check Django logs:**
   ```bash
   # On EC2, watch the Django output
   # It will show the redirect_uri it's trying to use
   ```

4. **Verify ngrok is running:**
   ```bash
   # Make sure ngrok is forwarding to your EC2 Django app
   # ngrok should show: https://domestically-pseudomilitaristic-candis.ngrok-free.dev -> localhost:8000
   ```

### ngrok URL changed?

If your ngrok URL changes (free tier generates new URLs):

1. Update Google Cloud Console with new URL
2. Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in settings.py
3. Restart Django

### OAuth works locally but not on ngrok?

Make sure:
- `OAUTHLIB_INSECURE_TRANSPORT = '1'` is set (already in code)
- ngrok is using HTTPS (free tier should be HTTPS by default)
- Your EC2 security group allows inbound traffic on port 8000

---

## 📋 Quick Verification Checklist

- [ ] Added redirect URI to Google Cloud Console (no trailing slash)
- [ ] Waited 2-5 minutes after updating Google Console
- [ ] Updated `ALLOWED_HOSTS` in settings.py on EC2
- [ ] Added `CSRF_TRUSTED_ORIGINS` in settings.py on EC2
- [ ] Restarted Django on EC2
- [ ] Cleared browser cache / tried incognito mode
- [ ] ngrok URL is accessible and forwarding correctly

---

## 🎯 Expected Flow

1. User clicks "Authorize with YouTube" on your app
2. Django redirects to: `https://accounts.google.com/o/oauth2/auth?...`
3. User logs in and authorizes
4. Google redirects back to: `https://domestically-pseudomilitaristic-candis.ngrok-free.dev/oauth2callback?code=...`
5. Django exchanges code for access token
6. User can now upload videos!

---

**After following these steps, OAuth should work! 🎉**
