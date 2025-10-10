# 📦 Complete Installation Guide

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Python 3.8 or higher** installed
- [ ] **pip** (Python package manager) installed
- [ ] **FFmpeg** installed and added to PATH
- [ ] **Git** (optional, for version control)
- [ ] **Google Account** (for YouTube API features)

---

## Step-by-Step Installation

### 1️⃣ Install Python Dependencies

Open your terminal/PowerShell in the project directory and run:

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Django-4.2.7 yt-dlp-2023.11.16 moviepy-1.0.3 ...
```

### 2️⃣ Install FFmpeg

FFmpeg is required for video processing.

#### Windows:
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" under System Variables
   - Add new entry: `C:\ffmpeg\bin`
   - Restart terminal

#### Mac:
```bash
brew install ffmpeg
```

#### Linux:
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### 3️⃣ Initialize the Database

Run migrations to create the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, shorts
Running migrations:
  Applying contenttypes.0001_initial... OK
  ...
```

### 4️⃣ Create Required Directories

The app needs these directories:

```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path downloads, outputs, media, media\shorts, static

# Mac/Linux
mkdir -p downloads outputs media/shorts static
```

Or simply run:
```bash
python setup.py
```

### 5️⃣ Create Admin User (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

---

## 🔑 API Configuration (Optional)

### YouTube Data API Setup

#### Step 1: Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name: "YouTube Shorts Automation"
4. Click "Create"

#### Step 2: Enable YouTube Data API v3
1. In the Cloud Console, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click on it and press "Enable"

#### Step 3: Create OAuth 2.0 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: YouTube Shorts Automation
   - User support email: Your email
   - Developer contact: Your email
   - Scopes: Leave default
   - Test users: Add your email
   - Save and continue

4. Back to Create OAuth client ID:
   - Application type: **Web application**
   - Name: YouTube Shorts App
   - Authorized redirect URIs: `http://localhost:8000/oauth2callback/`
   - Click "Create"

5. Download the JSON file
6. Rename it to `client_secret.json`
7. Place it in your project root directory (YtAut/)

#### Step 4: Add Test Users
1. Go to "APIs & Services" → "OAuth consent screen"
2. Scroll to "Test users"
3. Click "Add Users"
4. Add your Google account email
5. Save

### Google Gemini API Setup (AI Features)

#### Step 1: Get API Key
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the generated key

#### Step 2: Set Environment Variable

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Permanent Setup (Windows):**
1. Search "Environment Variables" in Windows
2. Click "Environment Variables"
3. Under "User variables", click "New"
4. Variable name: `GEMINI_API_KEY`
5. Variable value: Your API key
6. Click OK

---

## 🚀 Running the Application

### Start the Development Server

```bash
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Access the Application

Open your browser and navigate to:
- **Main App:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **History:** http://localhost:8000/history/

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Server starts without errors
- [ ] Home page loads at http://localhost:8000
- [ ] Can access admin panel (if superuser created)
- [ ] FFmpeg is detected (check terminal output)
- [ ] Directories created (downloads/, outputs/, media/)
- [ ] Database file exists (db.sqlite3)

---

## 🧪 Testing the Installation

### Quick Test (No APIs Required)

1. Go to http://localhost:8000
2. Enter a YouTube URL: `https://www.youtube.com/watch?v=jNQXAC9IVRw`
3. Start time: `0:05`
4. End time: `0:35`
5. Click "Generate Short"
6. Wait for processing (may take 1-2 minutes)
7. Video should appear on the result page

### Test with APIs

1. Complete API setup above
2. Generate a short
3. Click "Upload to YouTube"
4. Authenticate with Google
5. Video uploads to your channel

---

## 🐛 Troubleshooting

### "FFmpeg not found"
- Ensure FFmpeg is in your PATH
- Restart terminal after installation
- Run `ffmpeg -version` to verify

### "No module named 'django'"
- Activate virtual environment
- Run `pip install -r requirements.txt`

### "Port already in use"
- Another app is using port 8000
- Run: `python manage.py runserver 8080`
- Access at http://localhost:8080

### "OAuth error"
- Check redirect URI matches exactly
- Ensure you're added as test user
- Clear browser cookies

### "API quota exceeded"
- YouTube API has daily limits
- Wait 24 hours or request quota increase
- Each upload costs 1600 units (default: 10,000/day)

### Video download fails
- Check internet connection
- Try a different YouTube URL
- Some videos may be restricted

---

## 📁 Project Structure After Installation

```
YtAut/
├── db.sqlite3              # Database (created after migration)
├── downloads/              # Temporary video downloads
├── outputs/                # Processed video outputs
├── media/                  # Django media files
│   └── shorts/            # Uploaded shorts
├── static/                # Static files
├── client_secret.json     # YouTube API credentials (you add this)
└── [other project files]
```

---

## 🔄 Updating the Application

If you pull new changes:

```bash
# Install any new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files (if needed)
python manage.py collectstatic
```

---

## 🎉 You're Ready!

Your YouTube Shorts Automation app is now installed and ready to use!

**Next steps:**
1. Start the server: `python manage.py runserver`
2. Open http://localhost:8000
3. Create your first short!

For usage instructions, see **QUICKSTART.md**
For detailed documentation, see **README.md**

---

**Need help?** Check the troubleshooting section or create an issue in the repository.
