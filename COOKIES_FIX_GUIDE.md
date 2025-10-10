# 🍪 Cookie Authentication Fix Guide

## Problem
YouTube is blocking video downloads with "Sign in to confirm you're not a bot" error when using a public IP address.

## Solution
Use authenticated cookies to bypass the bot detection.

---

## ✅ Changes Made

### 1. Updated `video_processor.py`
Added cookie support to the `download_video()` method:
- Tries to use cookies from `cookies/cookies.txt` file first
- Falls back to browser cookies if file doesn't exist

### 2. Updated `video_analyzer.py`
Added cookie support to the `_get_video_info()` method:
- Same cookie loading logic as video_processor
- Enables AI auto-detection to work with restricted videos

---

## 🚀 Deployment Steps (Ubuntu Server)

### Step 1: Upload Changes to Server

```bash
# On your local machine (Windows)
# Option A: Use git
git add video_processor.py video_analyzer.py
git commit -m "Add cookie authentication for yt-dlp"
git push

# Then on server
cd /home/ubuntu/YTAuto
git pull

# Option B: Use SCP/SFTP
# Upload video_processor.py and video_analyzer.py to /home/ubuntu/YTAuto/
```

### Step 2: Export Fresh Cookies

**On your Windows machine:**

1. Install browser extension:
   - Chrome/Edge: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. Go to `youtube.com` and **make sure you're logged in**

3. Click the extension icon → Export cookies for `youtube.com`

4. Save the exported file as `cookies.txt`

### Step 3: Upload Cookies to Server

```bash
# On your local machine
scp cookies.txt ubuntu@your-server-ip:/home/ubuntu/YTAuto/cookies/cookies.txt

# Or use SFTP client (FileZilla, WinSCP, etc.)
# Upload to: /home/ubuntu/YTAuto/cookies/cookies.txt
```

### Step 4: Set Correct Permissions

```bash
# On the server
cd /home/ubuntu/YTAuto
chmod 600 cookies/cookies.txt  # Secure the cookies file
```

### Step 5: Restart Django Server

```bash
# On the server
# If using systemd service
sudo systemctl restart ytauto

# Or if running manually
# Stop the current process (Ctrl+C) and restart:
source .ytauto/bin/activate
python manage.py runserver 0.0.0.0:8000
```

---

## 🧪 Testing

### Test 1: Check if cookies file exists
```bash
# On server
ls -la /home/ubuntu/YTAuto/cookies/cookies.txt
```

### Test 2: Test with the problematic video
Try downloading the video that was failing:
```
https://www.youtube.com/watch?v=dmjp2bM346M
```

You should see:
```
🍪 Using cookies from: /home/ubuntu/YTAuto/cookies/cookies.txt
```

---

## 🔍 Troubleshooting

### Issue: Still getting "Sign in to confirm you're not a bot"

**Cause 1: Cookies are expired**
- Solution: Export fresh cookies (cookies expire after a few weeks)

**Cause 2: Cookies file format is wrong**
- Solution: Make sure you're using the Netscape format (the browser extension does this automatically)
- First line should be: `# Netscape HTTP Cookie File`

**Cause 3: Cookies file not found**
- Solution: Check the file path and permissions
```bash
ls -la /home/ubuntu/YTAuto/cookies/cookies.txt
```

**Cause 4: YouTube account not logged in**
- Solution: Make sure you're logged into YouTube when exporting cookies

### Issue: Code changes not taking effect

**Solution: Restart the Django server**
```bash
sudo systemctl restart ytauto
# or
pkill -f "python manage.py runserver"
python manage.py runserver 0.0.0.0:8000
```

---

## 📝 Cookie File Format

Your cookies file should look like this:

```
# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	1775077987	LOGIN_INFO	AFmmF2swRQIg...
.youtube.com	TRUE	/	FALSE	1775077987	HSID	A1lh-B0wqlH5KXXLR
.youtube.com	TRUE	/	TRUE	1775077987	SSID	A-2LRayLFD2r4_nGU
...
```

**Important:** The expiration dates (5th column) should be in the **future**!

---

## 🔐 Security Notes

1. **Never commit cookies to git** - They contain your authentication tokens
2. **Set restrictive permissions**: `chmod 600 cookies/cookies.txt`
3. **Refresh cookies regularly** - They expire after a few weeks
4. **Don't share cookies** - They're tied to your YouTube account

---

## 🎯 Alternative: Use Browser Cookies Directly

If you have Chrome installed on the server, the code will automatically try to use browser cookies as a fallback:

```python
ydl_opts['cookiesfrombrowser'] = ('chrome',)
```

However, this requires:
- Chrome browser installed on the server
- You to be logged into YouTube in that browser
- Proper permissions to access Chrome's cookie database

**For servers, using a cookies.txt file is more reliable.**

---

## ✅ Verification

After deploying, you should see this in your server logs:

```
🍪 Using cookies from: /home/ubuntu/YTAuto/cookies/cookies.txt
[download] Downloading video...
✅ Video downloaded successfully
```

Instead of:

```
❌ ERROR: [youtube] dmjp2bM346M: Sign in to confirm you're not a bot
```

---

## 📚 References

- [yt-dlp Cookie Documentation](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)
- [Exporting YouTube Cookies](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies)
