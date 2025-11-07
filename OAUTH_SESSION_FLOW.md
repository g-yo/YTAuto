# OAuth Session-Based Flow

## Overview
The application now uses **traditional OAuth 2.0 session-based authentication** instead of file-based credentials. This change prevents upload quota limitations by distributing API usage across different Google accounts.

## What Changed

### Before (File-Based Approach)
- Credentials were saved to `youtube_credentials.json` file
- All uploads used the same saved credentials
- This caused quota limitations as all requests counted against one account
- Required manual credential file management for server deployment

### After (Session-Based Approach)
- Credentials are stored only in Django session (browser session)
- Each user authenticates via OAuth when needed
- API quota is distributed across multiple Google accounts
- No credential file management required

## How It Works

### 1. First Upload Attempt
When a user tries to upload a video:
1. System checks for valid credentials in session
2. If no credentials found, redirects to Google OAuth
3. User authorizes the app with their Google account
4. Credentials are saved in their browser session

### 2. Subsequent Uploads
During the same browser session:
1. System retrieves credentials from session
2. If credentials expired, automatically refreshes them
3. Upload proceeds without re-authorization

### 3. New Browser Session
When user opens a new browser or session expires:
1. Must re-authorize via OAuth
2. This is the standard OAuth flow behavior
3. Ensures security and distributes quota

## Benefits

### ✅ No More Quota Limitations
- Each user authenticates with their own Google account
- API quota is distributed, not concentrated on one account

### ✅ Better Security
- No credential files to manage or secure
- Credentials only exist in browser session
- Automatic session expiration

### ✅ Standard OAuth Flow
- Uses industry-standard OAuth 2.0 web flow
- Follows Google's best practices
- More reliable and maintainable

### ✅ Simpler Deployment
- No need to copy credential files to servers
- No manual credential management
- Works the same in development and production

## User Experience

### For End Users
1. Click "Upload to YouTube" on a video
2. If not authenticated, redirected to Google login
3. Grant permissions to the app
4. Redirected back, upload proceeds automatically
5. Can upload multiple videos in same session without re-auth

### For Developers
1. No credential file setup needed
2. Standard OAuth flow works out of the box
3. Better debugging with session-based auth
4. Easier to test with multiple accounts

## Files Modified

### Updated Files
- `shorts/youtube_uploader.py` - Removed file-based credential methods
  - Removed `credentials_file` attribute
  - Removed `save_credentials_to_file()` method
  - Removed `load_credentials_from_file()` method
  - Updated `get_credentials_from_session()` to use session only
  - Updated `save_credentials_to_session()` to save to session only

### Deprecated Files (No Longer Needed)
- `save_credentials_manually.py` - No longer needed
- `test_credentials.py` - Update needed for session-based testing
- `youtube_credentials.json` - Can be deleted

## Migration Guide

### If You Have Existing Setup

1. **Delete old credential file** (optional cleanup):
   ```bash
   # Optional: Remove the old credential file
   rm youtube_credentials.json
   ```

2. **Update .gitignore** (already done):
   The file is already gitignored, no action needed

3. **First upload after migration**:
   - Users will need to re-authenticate via OAuth
   - This is expected and by design
   - Each user uses their own Google account

### For Server Deployment

**No special setup needed!**
- Remove any steps copying `youtube_credentials.json` to server
- OAuth flow works automatically
- Each user authenticates with their own account

## FAQ

### Q: Do I need to re-authenticate every time?
**A:** Only when your browser session expires or you use a new browser. During an active session, credentials are cached and automatically refreshed.

### Q: Can multiple users upload simultaneously?
**A:** Yes! Each user authenticates with their own Google account, so uploads are independent and quota is distributed.

### Q: What about headless/server deployment?
**A:** The session-based flow works with web applications. For true headless automation, you'd need service accounts (different use case). For web apps, users authenticate via browser as normal.

### Q: Is this more secure?
**A:** Yes! Credentials exist only in browser sessions, not in files. Sessions expire automatically, and there's no credential file to secure or accidentally expose.

### Q: Will old documentation still work?
**A:** Some deployment guides reference the old file-based approach. Those steps can be skipped. The OAuth flow is now automatic.

## Technical Details

### Session Storage
- Credentials stored in Django session backend
- Default: database-backed sessions (db.sqlite3)
- Configurable in Django settings

### Credential Refresh
- Refresh tokens automatically refresh expired access tokens
- Happens transparently during upload
- No user interaction needed for refresh

### OAuth Scopes
Same as before:
- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube`

## Troubleshooting

### Issue: "No valid credentials found"
**Solution:** Click the upload button again to trigger OAuth flow

### Issue: "Session expired"
**Solution:** Normal behavior. User will be prompted to re-authenticate

### Issue: "Quota exceeded"
**Solution:** This now happens per-user, not globally. User should try with a different Google account or wait for quota reset

## Code Example

### How to Upload (User Perspective)
```python
# In views.py - no changes needed from user perspective
def upload_to_youtube(request, short_id):
    uploader = YouTubeUploader()
    
    # Check credentials - redirects to OAuth if needed
    if not uploader.has_credentials(request):
        auth_url = uploader.get_authorization_url(request)
        return redirect(auth_url)
    
    # Upload proceeds with session credentials
    video_id = uploader.upload_video(...)
```

The OAuth flow is handled automatically!

## Summary

The switch to session-based OAuth provides:
- ✅ Better quota distribution
- ✅ Improved security
- ✅ Simpler deployment
- ✅ Standard OAuth practices
- ✅ Better multi-user support

No more `youtube_credentials.json` file needed!
