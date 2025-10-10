# 🚀 Quick Reference Card

## ⚡ Start the App

```bash
python manage.py runserver
```
Then open: **http://localhost:8000**

---

## 🎯 Two Modes Available

### 🤖 AI Auto-Detect Mode (Recommended)
```
1. Paste YouTube URL
2. ☑ Check "AI Auto-Detect Best Segment"
3. Leave times blank
4. Click "Generate Short"
```

**What happens:**
- ✅ AI finds best 30-60 second segment
- ✅ Smart rotation for optimal fit
- ✅ AI generates title & hashtags
- ✅ Uploads as YouTube Short
- ✅ Auto-cleanup after upload

### ✋ Manual Mode
```
1. Paste YouTube URL
2. ☐ Uncheck "AI Auto-Detect"
3. Enter start time (e.g., 1:30)
4. Enter end time (e.g., 2:00)
5. Click "Generate Short"
```

---

## 📋 Features Checklist

✅ **AI Auto-Detection** - Finds most replayed segments
✅ **Smart Rotation** - Optimizes vertical format (9:16)
✅ **AI Error Messages** - Clear explanations + solutions
✅ **Auto Cleanup** - Deletes files after upload
✅ **Context Metadata** - AI-generated titles/descriptions
✅ **YouTube Shorts** - Always uploads as Shorts (not videos)
✅ **#Shorts Tag** - Automatically added

---

## 🔧 Key Files

| File | Purpose |
|------|---------|
| `ai_error_handler.py` | AI error explanations |
| `video_analyzer.py` | Auto-detect best segments |
| `video_processor.py` | Smart rotation & cleanup |
| `shorts/views.py` | Main workflow logic |
| `templates/shorts/index.html` | UI with AI toggle |

---

## 📖 Documentation

| Document | What's Inside |
|----------|---------------|
| `AI_UPDATE_SUMMARY.md` | Complete feature overview |
| `AI_FEATURES_GUIDE.md` | Detailed technical guide |
| `YOUTUBE_SHORTS_FORMAT.md` | Shorts format details |
| `SHORTS_UPDATE_SUMMARY.md` | Shorts configuration |
| `README.md` | Full project documentation |

---

## 🐛 Common Issues

### AI not working?
```bash
# Check API key is set
echo $env:GEMINI_API_KEY

# Set if missing
$env:GEMINI_API_KEY="your-key-here"

# Restart server
python manage.py runserver
```

### Files not cleaning?
- Check file permissions
- Close programs using files
- Check console for cleanup messages

### Video not uploading as Short?
- Verify #Shorts tag in description
- Check video is 9:16 format
- Ensure duration ≤ 60 seconds

---

## 💡 Pro Tips

1. **Use AI mode for unknown videos** - Let AI find the best part
2. **Use manual mode for known segments** - When you know exactly what you want
3. **Keep videos under 60 seconds** - YouTube Shorts limit
4. **Check console output** - See AI decisions and cleanup
5. **Monitor YouTube Studio** - Verify uploads appear as Shorts

---

## 🎬 Example Workflow

```
1. Open http://localhost:8000
2. Paste: https://www.youtube.com/watch?v=example
3. ☑ AI Auto-Detect
4. Click "Generate Short"
5. Wait 1-2 minutes
6. Preview generated short
7. Click "Upload to YouTube"
8. Authenticate (first time only)
9. ✅ Done! Video on YouTube Shorts
10. Files automatically cleaned
```

---

## 📊 What Gets Cleaned

**After Generation:**
- ✅ Downloaded source video
- ❌ Generated short (kept)

**After Upload:**
- ✅ Downloaded source video
- ✅ Generated short
- ✅ Temp audio files
- ✅ All temporary files

**Result:** 0 MB disk usage per short!

---

## 🔑 Required Setup

### Minimum (Works Now)
- ✅ Python 3.8+
- ✅ FFmpeg installed
- ✅ Dependencies installed

### For AI Features
- ⚠️ Gemini API key
- ⚠️ Internet connection

### For YouTube Upload
- ⚠️ `client_secret.json`
- ⚠️ OAuth authentication

---

## 🎯 Success Indicators

**Console Output:**
```
🤖 AI Auto-Detection Mode Activated
✅ AI detected best segment: 2:15 to 2:45
🔄 Rotated video 90° for better fit
✅ Used AI-generated metadata
🧹 Cleaned 1 downloaded file(s)
✅ Post-upload cleanup complete!
```

**YouTube Studio:**
- Shows as "Short" not "Video"
- Appears in Shorts feed
- Has #Shorts tag
- 9:16 vertical format

---

## ⚡ Quick Commands

```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Set API key
$env:GEMINI_API_KEY="your-key"

# Check Python version
python --version

# Check FFmpeg
ffmpeg -version
```

---

## 🆘 Emergency Fixes

**Server won't start:**
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**AI not detecting:**
```bash
# Use manual mode instead
# Uncheck AI Auto-Detect
# Enter times manually
```

**Upload failing:**
```bash
# Check client_secret.json exists
# Re-authenticate with Google
# Try uploading again
```

---

## 📞 Where to Get Help

1. **Check console output** - Errors have AI explanations
2. **Read `AI_FEATURES_GUIDE.md`** - Detailed troubleshooting
3. **Check `README.md`** - Full documentation
4. **Review error messages** - AI provides solutions

---

**Everything you need on one page!** 🚀
