# 🚀 Install and Run - Quick Guide

## ⚡ 3-Step Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

**What this installs:**
- Django (web framework)
- yt-dlp (video downloader)
- moviepy (video processing)
- Google APIs (YouTube, Gemini)
- librosa (audio analysis) ← NEW!
- numpy, scipy (calculations) ← NEW!

### Step 2: Setup Database
```bash
python manage.py migrate
```

### Step 3: Run Server
```bash
python manage.py runserver
```

**Open:** http://localhost:8000

---

## 🎬 Create Your First Animated Short

### Fully Automated Mode

1. **Paste YouTube URL**
2. **Enable both checkboxes:**
   - ☑ AI Auto-Detect Best Segment
   - ☑ Create Audio-Reactive Animation
3. **Click "Generate Short"**
4. **Wait 1-2 minutes**
5. **Upload to YouTube!**

---

## 🎨 What You Get

**Input:** Any YouTube URL

**Output:** 
- Vibrant animated video (9:16 vertical)
- Synchronized to audio beats
- AI-suggested visual style
- Copyright-free content
- Ready for YouTube Shorts

---

## 📋 Requirements

### Minimum
- ✅ Python 3.8+
- ✅ FFmpeg installed
- ✅ Internet connection

### For Full Features
- ⚠️ Gemini API key (AI features)
- ⚠️ `client_secret.json` (YouTube upload)

---

## 🐛 Troubleshooting

### "librosa not installed"
```bash
pip install librosa numpy scipy
```

### "FFmpeg not found"
- **Windows:** Download from https://www.gyan.dev/ffmpeg/builds/
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt-get install ffmpeg`

### Server won't start
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## ✅ Verify Installation

```bash
# Check Python
python --version  # Should be 3.8+

# Check FFmpeg
ffmpeg -version

# Check librosa
python -c "import librosa; print('✅ librosa OK')"

# Check Django
python manage.py check
```

---

## 🎉 You're Ready!

**Your YouTube Shorts automation with AI animation is ready to use!**

Open http://localhost:8000 and start creating! 🚀
