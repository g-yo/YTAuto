# Quick Server Setup (Ubuntu Azure - No GUI)

## TL;DR

Your server has no browser, so you need to authorize OAuth locally first, then copy the credentials.

## 3 Simple Steps

### 1. Authorize Locally (Do this now on Windows)

```bash
python manage.py runserver
```

- Upload a video
- Complete Google authorization
- This creates `youtube_credentials.json`

### 2. Copy to Server

```bash
scp client_secret.json youtube_credentials.json user@your-server:/path/to/YtAut/
```

### 3. Test on Server

```bash
# On server
cd /path/to/YtAut
python test_credentials.py
```

Done! Your server can now upload to YouTube without a browser.

---

## Files You Need

| File | What It Is | Where to Get |
|------|-----------|--------------|
| `client_secret.json` | OAuth client config | Google Cloud Console |
| `youtube_credentials.json` | Your auth tokens | Created after first OAuth |

---

## How to Get Files

### `client_secret.json`
1. Go to: https://console.cloud.google.com/apis/credentials
2. Download your OAuth 2.0 Client ID
3. Rename to `client_secret.json`

### `youtube_credentials.json`
1. Run app locally
2. Upload a video (triggers OAuth)
3. File is auto-created in project root

---

## Copy to Server

```bash
# Replace with your actual details
scp client_secret.json youtube_credentials.json \
    your-user@your-azure-ip:/home/your-user/YtAut/
```

Or use your preferred method (SFTP, rsync, etc.)

---

## Verify It Works

**On server:**
```bash
python test_credentials.py
```

Should show:
```
✅ ALL TESTS PASSED!
Your OAuth setup is working correctly.
```

---

## Troubleshooting

**"youtube_credentials.json not found"**
→ You need to authorize locally first

**"invalid_client" error**
→ Copy `client_secret.json` to server

**"Credentials expired"**
→ Should auto-refresh. If not, re-authorize locally and copy again

---

## Full Details

See `SERVER_DEPLOYMENT_GUIDE.md` for complete instructions.
