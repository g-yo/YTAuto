# 🚀 EC2 Deployment Guide - YouTube Shorts App

Complete guide for deploying and running this project on AWS EC2.

## 🎯 Overview

Since EC2 is a headless server (no browser), you need to:
1. Export YouTube cookies on your **local PC**
2. Upload cookies to **EC2 instance**
3. The app will use the cookies file for authentication

---

## 📋 Prerequisites

- AWS EC2 instance (Ubuntu/Amazon Linux recommended)
- SSH access to EC2 instance
- EC2 security group allowing ports: 22 (SSH), 8000 (Django), 80/443 (HTTP/HTTPS)
- Your EC2 SSH key (.pem file)

---

## 🔧 Part 1: Setup on Your Local PC

### Step 1: Export YouTube Cookies

1. **Install Browser Extension:**
   - Chrome/Edge: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **Export Cookies:**
   - Go to [youtube.com](https://youtube.com) and **log in**
   - Click the extension icon
   - Click "Export" or "Download"
   - Save as `cookies.txt` in the `cookies/` folder of this project

3. **Verify:**
   ```powershell
   # Check if file exists
   Test-Path cookies\cookies.txt
   ```

### Step 2: Upload Cookies to EC2

**Option A: Using PowerShell Script (Easiest)**

1. Edit `upload_cookies_to_ec2.ps1`:
   ```powershell
   $EC2_USER = "ubuntu"                    # Your EC2 username
   $EC2_HOST = "3.123.45.67"              # Your EC2 public IP
   $EC2_KEY = "C:\path\to\your-key.pem"   # Path to SSH key
   $PROJECT_PATH = "/home/ubuntu/YtAut"   # Project path on EC2
   ```

2. Run the script:
   ```powershell
   .\upload_cookies_to_ec2.ps1
   ```

**Option B: Manual Upload with SCP**

```powershell
# Windows (with OpenSSH or WSL)
scp -i "path\to\key.pem" cookies\cookies.txt ubuntu@your-ec2-ip:/home/ubuntu/YtAut/cookies/

# Or using WSL
wsl scp -i /mnt/c/path/to/key.pem cookies/cookies.txt ubuntu@your-ec2-ip:/home/ubuntu/YtAut/cookies/
```

**Option C: Manual Upload via SFTP Client**

Use FileZilla, WinSCP, or similar:
- Host: Your EC2 IP
- Protocol: SFTP
- Key file: Your .pem file
- Upload `cookies/cookies.txt` to `/home/ubuntu/YtAut/cookies/`

---

## 🖥️ Part 2: Setup on EC2 Instance

### Step 1: Connect to EC2

```bash
ssh -i "your-key.pem" ubuntu@your-ec2-ip
```

### Step 2: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install FFmpeg (required for video processing)
sudo apt install ffmpeg -y

# Install git (if not already installed)
sudo apt install git -y
```

### Step 3: Clone/Upload Project

**Option A: Clone from Git**
```bash
git clone https://github.com/your-username/YtAut.git
cd YtAut
```

**Option B: Upload from Local PC**
```powershell
# On your PC
scp -i "key.pem" -r C:\Users\geoau\OneDrive\Desktop\YtAut ubuntu@your-ec2-ip:/home/ubuntu/
```

### Step 4: Setup Python Environment

```bash
cd YtAut

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# If requirements.txt doesn't exist, install manually:
pip install django yt-dlp google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### Step 5: Verify Cookies

```bash
# Check if cookies directory exists
ls -la cookies/

# Verify cookies.txt is present
cat cookies/cookies.txt | head -n 5

# Set proper permissions
chmod 600 cookies/cookies.txt
```

### Step 6: Configure Django

```bash
# Create necessary directories
mkdir -p downloads outputs media static

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 7: Test Video Download

```bash
# Test with a simple Python script
python3 << EOF
from video_processor import VideoProcessor

processor = VideoProcessor()
try:
    # Test with a short video
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_path, info = processor.download_video(url)
    print(f"✅ Success! Downloaded: {info['title']}")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

### Step 8: Run Django Server

**For Testing:**
```bash
python manage.py runserver 0.0.0.0:8000
```

**For Production (using Gunicorn):**
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn youtube_shorts_app.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**Using systemd (Recommended for Production):**

Create service file:
```bash
sudo nano /etc/systemd/system/ytaut.service
```

Add this content:
```ini
[Unit]
Description=YouTube Shorts App
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/YtAut
Environment="PATH=/home/ubuntu/YtAut/venv/bin"
ExecStart=/home/ubuntu/YtAut/venv/bin/gunicorn youtube_shorts_app.wsgi:application --bind 0.0.0.0:8000 --workers 3

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ytaut
sudo systemctl start ytaut
sudo systemctl status ytaut
```

---

## 🔒 Security Configuration

### 1. Update Django Settings

Edit `youtube_shorts_app/settings.py`:

```python
# IMPORTANT: Change for production
DEBUG = False
ALLOWED_HOSTS = ['your-ec2-ip', 'your-domain.com']

# Generate new secret key
SECRET_KEY = 'your-new-secret-key-here'
```

### 2. Configure Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000  # Django (if not using reverse proxy)
sudo ufw enable
```

### 3. Setup Nginx (Optional but Recommended)

```bash
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/ytaut
```

Add:
```nginx
server {
    listen 80;
    server_name your-ec2-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /home/ubuntu/YtAut/static/;
    }

    location /media/ {
        alias /home/ubuntu/YtAut/media/;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/ytaut /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔄 Updating Cookies

When cookies expire (usually after a few weeks):

1. **On your PC:** Export fresh cookies from YouTube
2. **Upload to EC2:**
   ```powershell
   .\upload_cookies_to_ec2.ps1
   ```
3. **On EC2:** Restart the service
   ```bash
   sudo systemctl restart ytaut
   ```

---

## 🐛 Troubleshooting

### Cookies Not Working

```bash
# Check if cookies file exists
ls -la /home/ubuntu/YtAut/cookies/cookies.txt

# Check file permissions
chmod 600 /home/ubuntu/YtAut/cookies/cookies.txt

# Test download manually
cd /home/ubuntu/YtAut
source venv/bin/activate
python3 -c "from video_processor import VideoProcessor; VideoProcessor().download_video('https://youtube.com/watch?v=test')"
```

### Port Already in Use

```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>
```

### FFmpeg Not Found

```bash
# Install FFmpeg
sudo apt install ffmpeg -y

# Verify installation
ffmpeg -version
```

### Permission Denied Errors

```bash
# Fix ownership
sudo chown -R ubuntu:ubuntu /home/ubuntu/YtAut

# Fix permissions
chmod -R 755 /home/ubuntu/YtAut
chmod 600 /home/ubuntu/YtAut/cookies/cookies.txt
```

### Django Static Files Not Loading

```bash
cd /home/ubuntu/YtAut
source venv/bin/activate
python manage.py collectstatic --noinput
```

---

## 📊 Monitoring

### Check Logs

```bash
# Django logs (if using systemd)
sudo journalctl -u ytaut -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Check Disk Space

```bash
# Video files can fill up disk quickly
df -h

# Clean up old downloads
cd /home/ubuntu/YtAut
rm -rf downloads/* outputs/*
```

---

## 🎯 Quick Reference Commands

```bash
# SSH to EC2
ssh -i "key.pem" ubuntu@your-ec2-ip

# Activate virtual environment
cd /home/ubuntu/YtAut && source venv/bin/activate

# Restart service
sudo systemctl restart ytaut

# View logs
sudo journalctl -u ytaut -f

# Update code (if using git)
git pull && sudo systemctl restart ytaut

# Upload new cookies (from PC)
.\upload_cookies_to_ec2.ps1
```

---

## 💡 Tips

1. **Set up automatic backups** of your cookies.txt
2. **Use CloudWatch** for monitoring EC2 metrics
3. **Enable auto-scaling** if you expect high traffic
4. **Use S3** for storing processed videos instead of local disk
5. **Set up SSL/HTTPS** using Let's Encrypt for production

---

**Need Help?** Check the main README.md or cookies/README.md for more details.
