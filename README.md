# YouTube Shorts Automation 🎬

A powerful Django web application that automates the creation and uploading of YouTube Shorts. Download any YouTube video, crop it to your desired timeframe, generate AI-powered titles and hashtags, and upload directly to your YouTube channel!

## ✨ Features

### Phase 1: Core Video Processing
- **Download YouTube Videos**: Uses `yt-dlp` for reliable video downloads
- **Smart Video Cropping**: Crop videos using `MoviePy` with flexible time formats (MM:SS or HH:MM:SS)
- **High-Quality Output**: Maintains video quality with H.264 encoding

### Phase 2: Django Web Interface
- **Beautiful Modern UI**: Bootstrap 5-powered responsive design with gradient backgrounds
- **Simple Form Interface**: Easy-to-use form for URL and time inputs
- **Video Preview**: Watch your generated short before uploading
- **History Tracking**: View all your previously generated shorts

### Phase 3: YouTube API Integration
- **OAuth 2.0 Authentication**: Secure Google authentication
- **One-Click Upload**: Upload shorts directly to your YouTube channel
- **AI-Powered Content**: Generate catchy titles and hashtags using Google Gemini AI

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **FFmpeg** installed (required by MoviePy)
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`

### Installation

1. **Clone or navigate to the project directory**
```bash
cd YtAut
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser (optional, for admin access)**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

8. **Open your browser**
Navigate to: `http://localhost:8000`

## 🔑 API Setup (Optional but Recommended)

### Google Cloud Setup for YouTube Upload

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**

2. **Create a new project**
   - Click "Select a project" → "New Project"
   - Name it (e.g., "YouTube Shorts Automation")

3. **Enable YouTube Data API v3**
   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Web application"
   - Authorized redirect URIs: `http://localhost:8000/oauth2callback/`
   - Download the JSON file and save it as `client_secret.json` in the project root

5. **Configure OAuth Consent Screen**
   - Go to "APIs & Services" → "OAuth consent screen"
   - Choose "External" (for testing)
   - Fill in required fields
   - Add your email as a test user

### Google Gemini API Setup (for AI-generated titles)

1. **Get API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create an API key

2. **Set Environment Variable**
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"

# Mac/Linux
export GEMINI_API_KEY="your-api-key-here"
```

Or add it to your system environment variables permanently.

## 📖 Usage Guide

### Creating a YouTube Short

1. **Navigate to the home page**
2. **Paste a YouTube URL**
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

3. **Enter start and end times**
   - Format: `MM:SS` or `HH:MM:SS`
   - Example: Start: `0:10`, End: `0:40` (creates a 30-second short)

4. **Click "Generate Short"**
   - The app will download and crop the video
   - AI will generate a title and hashtags (if API key is set)

5. **Preview your short**
   - Watch the generated video
   - Review AI-generated title and hashtags

6. **Upload to YouTube** (optional)
   - Click "Upload to YouTube"
   - Authenticate with Google (first time only)
   - Video will be uploaded to your channel

### Viewing History

- Click "History" in the navigation
- See all your generated shorts
- Re-upload or view previously created videos

## 🛠️ Project Structure

```
YtAut/
├── youtube_shorts_app/      # Django project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI config
├── shorts/                  # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── urls.py              # App URLs
│   ├── admin.py             # Admin interface
│   ├── ai_generator.py      # AI title generation
│   └── youtube_uploader.py  # YouTube API integration
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── shorts/              # App templates
│       ├── index.html       # Home page
│       ├── result.html      # Result page
│       └── history.html     # History page
├── video_processor.py       # Core video processing logic
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🎯 Key Technologies

- **Django 4.2**: Web framework
- **yt-dlp**: YouTube video downloader
- **MoviePy**: Video editing and processing
- **FFmpeg**: Video encoding (backend for MoviePy)
- **Google YouTube Data API v3**: YouTube uploads
- **Google Gemini API**: AI content generation
- **Bootstrap 5**: Modern, responsive UI
- **SQLite**: Database (default, can be changed)

## 📝 Configuration

### Settings (youtube_shorts_app/settings.py)

```python
# YouTube API Configuration
YOUTUBE_CLIENT_SECRETS_FILE = BASE_DIR / 'client_secret.json'
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Google Gemini API Configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Video processing directories
DOWNLOADS_DIR = BASE_DIR / 'downloads'
OUTPUTS_DIR = BASE_DIR / 'outputs'
```

## 🔒 Security Notes

- **Never commit `client_secret.json`** to version control
- **Never hardcode API keys** in your code
- Use environment variables for sensitive data
- The default `SECRET_KEY` should be changed for production
- Set `DEBUG = False` in production

## 🐛 Troubleshooting

### FFmpeg not found
- Make sure FFmpeg is installed and in your system PATH
- Restart your terminal/IDE after installation

### YouTube API quota exceeded
- YouTube API has daily quotas
- Each upload costs 1600 quota units
- Default quota is 10,000 units per day

### Video download fails
- Check if the YouTube URL is valid
- Some videos may be restricted or unavailable
- Try a different video

### OAuth errors
- Ensure redirect URI matches exactly in Google Cloud Console
- Check that you're added as a test user
- Clear browser cookies and try again

## 🚀 Future Enhancements

- [ ] Support for multiple video formats
- [ ] Batch processing of multiple videos
- [ ] Custom video filters and effects
- [ ] Scheduled uploads
- [ ] Analytics dashboard
- [ ] Support for other platforms (TikTok, Instagram Reels)

## 📄 License

This project is for educational purposes. Make sure to comply with YouTube's Terms of Service and API usage policies.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📧 Support

For issues or questions, please create an issue in the repository.

---

**Happy Short Creating! 🎥✨**
