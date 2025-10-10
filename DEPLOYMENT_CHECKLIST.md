# 🚀 Deployment Checklist

Use this checklist before deploying to production or sharing your application.

## 🔒 Security

- [ ] Change `SECRET_KEY` in settings.py (generate new one)
- [ ] Set `DEBUG = False` in production
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Never commit `client_secret.json` to version control
- [ ] Never commit `.env` files with real API keys
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS in production
- [ ] Set secure cookie settings for production

## 📦 Dependencies

- [ ] All packages in requirements.txt are installed
- [ ] FFmpeg is installed on production server
- [ ] Python version is 3.8 or higher
- [ ] Database is properly configured

## 🗄️ Database

- [ ] Run all migrations: `python manage.py migrate`
- [ ] Create superuser for admin access
- [ ] Backup database regularly
- [ ] Set up database for production (PostgreSQL recommended)

## 🔑 API Configuration

- [ ] YouTube API credentials configured
- [ ] OAuth consent screen published (not in testing mode)
- [ ] Redirect URIs updated for production domain
- [ ] Gemini API key set in environment
- [ ] API quotas are sufficient for expected usage

## 📁 Files & Directories

- [ ] All required directories exist (downloads, outputs, media)
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] Media directory has proper permissions
- [ ] Temporary files are cleaned up regularly

## 🌐 Web Server

- [ ] Configure production web server (Gunicorn, uWSGI)
- [ ] Set up reverse proxy (Nginx, Apache)
- [ ] Configure SSL/TLS certificates
- [ ] Set up domain name and DNS
- [ ] Configure firewall rules

## 📊 Monitoring

- [ ] Set up error logging
- [ ] Configure application monitoring
- [ ] Set up disk space alerts (videos can be large)
- [ ] Monitor API quota usage
- [ ] Set up backup system

## 🧪 Testing

- [ ] Test video download functionality
- [ ] Test video cropping with various time formats
- [ ] Test YouTube upload with OAuth flow
- [ ] Test AI title generation
- [ ] Test on different browsers
- [ ] Test error handling

## 📝 Documentation

- [ ] README.md is up to date
- [ ] API setup instructions are clear
- [ ] Troubleshooting guide is complete
- [ ] User guide is available

## ⚡ Performance

- [ ] Set up caching if needed
- [ ] Optimize video processing settings
- [ ] Consider background task queue (Celery) for long operations
- [ ] Set up CDN for media files if needed

## 🔄 Maintenance

- [ ] Set up automated cleanup of old downloads
- [ ] Plan for database backups
- [ ] Document update procedures
- [ ] Set up monitoring for disk space

---

## Production Settings Example

```python
# settings.py for production

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Database (PostgreSQL recommended)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

# Static and Media
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# API Keys from environment
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
```

---

## Environment Variables for Production

Create a `.env` file (never commit this):

```bash
DJANGO_SECRET_KEY=your-production-secret-key
GEMINI_API_KEY=your-gemini-api-key
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

---

## Quick Deploy Commands

```bash
# 1. Pull latest code
git pull origin main

# 2. Install/update dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Restart application server
# (depends on your setup - Gunicorn, uWSGI, etc.)
sudo systemctl restart gunicorn
```

---

## 🎯 Pre-Launch Checklist

Final checks before going live:

1. [ ] All security settings enabled
2. [ ] All API keys working
3. [ ] Test upload to YouTube works
4. [ ] Error pages are user-friendly
5. [ ] Backup system is active
6. [ ] Monitoring is configured
7. [ ] Documentation is complete
8. [ ] Team is trained on the system

---

**Ready to deploy? Double-check everything above!** 🚀
