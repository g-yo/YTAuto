# YouTube Cookies Setup Guide

This folder is for storing YouTube cookies to bypass bot detection when downloading videos.

## Why Do I Need This?

YouTube sometimes blocks automated downloads with a "Sign in to confirm you're not a bot" error. Using cookies from your browser allows yt-dlp to authenticate as if you're logged in.

## Quick Setup (Recommended)

### Method 1: Browser Extension (Easiest)

1. **Install a Cookie Extension:**
   - Chrome/Edge: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **Export YouTube Cookies:**
   - Go to [youtube.com](https://youtube.com) and make sure you're logged in
   - Click the extension icon
   - Click "Export" or "Download"
   - Save the file as `cookies.txt` in this folder

3. **Done!** The application will automatically use these cookies.

### Method 2: Automatic Browser Cookies (No File Needed)

The application will automatically try to extract cookies from these browsers in order:
1. Chrome
2. Edge
3. Firefox
4. Brave
5. Opera

**Requirements:**
- You must be logged into YouTube in the browser
- The browser must be closed when running the application (for some browsers)

## Advanced Options

### Using yt-dlp Command Line

If you prefer to use yt-dlp directly:

```bash
# Use cookies from browser
yt-dlp --cookies-from-browser chrome "VIDEO_URL"

# Use cookies.txt file
yt-dlp --cookies cookies/cookies.txt "VIDEO_URL"
```

### Manual Cookie Export (Advanced)

1. Open YouTube in your browser while logged in
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies → https://youtube.com
4. Export all cookies in Netscape format
5. Save as `cookies.txt` in this folder

## File Format

The `cookies.txt` file should be in Netscape HTTP Cookie File format:

```
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	TRUE	0	CONSENT	YES+
.youtube.com	TRUE	/	FALSE	1234567890	VISITOR_INFO1_LIVE	xxxxx
```

## Security Notes

⚠️ **IMPORTANT:**
- Never share your `cookies.txt` file - it contains your login session
- Add `cookies.txt` to `.gitignore` to prevent accidental commits
- Cookies expire after some time - re-export if downloads start failing

## Troubleshooting

### Still Getting Bot Detection Error?

1. **Update yt-dlp:**
   ```bash
   pip install --upgrade yt-dlp
   ```

2. **Re-export cookies** (they may have expired)

3. **Try a different browser** - some browsers work better than others

4. **Clear browser cache** and log in to YouTube again before exporting

5. **Use a VPN** if your IP is flagged

### Cookies Not Working?

- Make sure you're logged into YouTube in the browser
- Check that the cookies.txt file is in the correct format
- Try exporting from a different browser
- Ensure the file is named exactly `cookies.txt` (not `cookies.txt.txt`)

## Files in This Folder

- `cookies.txt` - Your YouTube cookies (create this file)
- `README.md` - This help file

---

**Need Help?** Check the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)
