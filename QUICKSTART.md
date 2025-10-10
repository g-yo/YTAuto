# 🚀 Quick Start Guide

## Get Started in 5 Minutes!

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Setup
```bash
python setup.py
```

### Step 3: Start the Server
```bash
python manage.py runserver
```

### Step 4: Open Your Browser
Navigate to: **http://localhost:8000**

---

## 🎯 Test the App

### Basic Test (No API Keys Required)
1. Go to http://localhost:8000
2. Paste a YouTube URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
3. Enter start time: `0:10`
4. Enter end time: `0:40`
5. Click "Generate Short"
6. Watch your generated short!

### With YouTube Upload (Requires Setup)
1. Follow the Google Cloud setup in README.md
2. Place `client_secret.json` in project root
3. Click "Upload to YouTube" on any generated short
4. Authenticate with Google
5. Your short will be uploaded automatically!

### With AI Features (Optional)
1. Get Gemini API key from https://makersuite.google.com/app/apikey
2. Set environment variable:
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your-key-here"
   
   # Mac/Linux
   export GEMINI_API_KEY="your-key-here"
   ```
3. Restart the server
4. AI will now generate titles and hashtags automatically!

---

## 📁 Project Features

✅ **Phase 1 Complete**: Core video processor with yt-dlp and MoviePy
✅ **Phase 2 Complete**: Beautiful Django web interface with Bootstrap 5
✅ **Phase 3 Complete**: YouTube API integration with OAuth 2.0
✅ **Bonus**: AI-powered title and hashtag generation with Gemini

---

## 🎨 What You Get

- **Modern UI**: Gradient backgrounds, smooth animations, responsive design
- **Video Processing**: Download and crop any YouTube video
- **AI Integration**: Smart titles and hashtags
- **YouTube Upload**: One-click upload to your channel
- **History Tracking**: View all your generated shorts
- **Admin Panel**: Django admin at http://localhost:8000/admin

---

## ⚡ Common Commands

```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Run setup
python setup.py
```

---

## 🆘 Need Help?

Check the full **README.md** for:
- Detailed setup instructions
- API configuration guides
- Troubleshooting tips
- Project structure explanation

**Happy Creating! 🎬✨**
