# 🔧 Fix FFmpeg Hanging on Azure

## ❌ Problem
FFmpeg gets stuck during video processing on Azure server but works fine locally.

## ✅ Solutions Applied

### 1. Code Changes (Already Done)
- ✅ Simplified video filter (removed complex crop operations)
- ✅ Changed preset from 'medium' to 'fast' for faster encoding
- ✅ Added 5-minute timeout to prevent infinite hanging
- ✅ Added better error messages

### 2. Deploy to Azure

```bash
# On your PC - commit and push
cd C:\Users\geoau\OneDrive\Desktop\YtAut
git add video_processor.py
git commit -m "Fix FFmpeg hanging - add timeout and simplify filter"
git push

# On Azure - pull and restart
ssh -i "C:\Users\geoau\Downloads\ytauto.pem" azureuser@<your-azure-ip>
cd /home/azureuser/GyoPi/YTAuto
git pull origin main

# Kill any stuck FFmpeg processes
pkill -9 ffmpeg

# Restart Django
python manage.py runserver 0.0.0.0:8000
```

### 3. Verify FFmpeg Installation on Azure

```bash
# SSH to Azure
ssh -i "C:\Users\geoau\Downloads\ytauto.pem" azureuser@<your-azure-ip>

# Check FFmpeg version
ffmpeg -version

# If not installed or old version:
sudo apt update
sudo apt install ffmpeg -y

# Verify it works
ffmpeg -version
```

### 4. Check System Resources

FFmpeg might hang due to low resources:

```bash
# Check memory
free -h

# Check disk space
df -h

# Check CPU
top

# If low on resources, consider:
# - Upgrading Azure VM size
# - Using faster preset (already changed to 'fast')
# - Processing shorter clips
```

## 🐛 Troubleshooting

### If Still Hanging

**1. Check FFmpeg Process:**
```bash
# See if FFmpeg is running
ps aux | grep ffmpeg

# Kill stuck process
pkill -9 ffmpeg
```

**2. Test FFmpeg Manually:**
```bash
cd /home/azureuser/GyoPi/YTAuto/downloads

# Test simple conversion (should work quickly)
ffmpeg -i *.mp4 -t 5 -c:v libx264 -preset fast test.mp4

# If this hangs, FFmpeg installation is broken
```

**3. Check FFmpeg Logs:**
```bash
# Run FFmpeg with verbose output
ffmpeg -i input.mp4 -vf "transpose=1,scale=1080:1920" -t 10 output.mp4 -v debug
```

**4. Try Even Simpler Filter:**

If still hanging, edit `video_processor.py` line 210:

```python
# Ultra-simple filter (no padding)
video_filter = "transpose=1,scale=1080:1920"
```

### Common Causes

1. **FFmpeg not installed** - Install with `sudo apt install ffmpeg`
2. **Low memory** - Upgrade VM or use 'ultrafast' preset
3. **Corrupted video** - Try different video
4. **Missing codecs** - Install: `sudo apt install ubuntu-restricted-extras`
5. **Network issues** - If reading from network storage

## 📊 Performance Comparison

| Setting | Speed | Quality | Use Case |
|---------|-------|---------|----------|
| ultrafast | Fastest | Lower | Testing |
| fast | Fast | Good | **Azure (Current)** |
| medium | Moderate | Better | Local PC |
| slow | Slow | Best | Final production |

## 🎯 What Changed

**Before:**
- Complex crop filter: `crop=min(iw\\,ih*9/16):min(ih\\,iw*16/9),scale=1080:1920`
- Preset: `medium`
- No timeout (could hang forever)

**After:**
- Simple scale+pad filter: `transpose=1,scale=1080:1920:...,pad=...`
- Preset: `fast` (2-3x faster)
- Timeout: 300 seconds (5 minutes)
- Better error messages

## ✅ Quick Test

After deploying, test with a short video:

1. Go to your app
2. Enter a YouTube URL
3. Set times: Start `0:10`, End `0:20` (only 10 seconds)
4. Should complete in under 30 seconds

If 10-second clip works but longer clips hang:
- It's a resource issue
- Consider upgrading Azure VM
- Or process shorter clips (max 30-45 seconds)

---

**The changes should fix the hanging issue! 🎉**
