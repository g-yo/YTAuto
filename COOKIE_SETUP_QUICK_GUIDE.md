# 🍪 Quick Cookie Setup Guide

## The Problem
YouTube is blocking your downloads with: **"Sign in to confirm you're not a bot"**

## The Solution (Choose One)

### ✅ Option 1: Use Browser Extension (EASIEST - 2 minutes)

1. **Install Extension:**
   - **Chrome/Edge**: Install [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - **Firefox**: Install [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **Export Cookies:**
   - Go to [youtube.com](https://youtube.com) (make sure you're logged in)
   - Click the extension icon in your browser toolbar
   - Click "Export" or "Download"
   - Save as `cookies.txt` in the `cookies/` folder

3. **Run your app again** - it will automatically use the cookies!

### ✅ Option 2: Let the App Use Browser Cookies (NO FILE NEEDED)

The app will **automatically** try to extract cookies from your browser if you:
- Are logged into YouTube in Chrome, Edge, Firefox, Brave, or Opera
- Keep the browser closed while running the app (for some browsers)

**Just run the app** - it will try multiple browsers automatically!

### ✅ Option 3: Update yt-dlp (Sometimes Helps)

```bash
pip install --upgrade yt-dlp
```

## What Changed?

The app now has **enhanced bot bypass features**:

1. ✅ **Multiple browser fallback** - tries Chrome, Edge, Firefox, Brave, Opera
2. ✅ **Android player client** - uses mobile API to bypass restrictions  
3. ✅ **Realistic headers** - mimics real browser requests
4. ✅ **Better error messages** - tells you exactly what to do
5. ✅ **Automatic retries** - tries different methods if one fails

## Testing

Just try downloading a video again - the app will:
1. Check for `cookies/cookies.txt` file first
2. If not found, try extracting from Chrome browser
3. If Chrome fails, try Edge, Firefox, Brave, Opera
4. Use enhanced headers and Android client for better success
5. Give you clear instructions if all methods fail

## Need More Help?

Check `cookies/README.md` for detailed instructions and troubleshooting.

---

**TL;DR**: Install browser extension → Export cookies from YouTube → Save to `cookies/cookies.txt` → Done! 🎉
