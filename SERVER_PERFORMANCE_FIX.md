# Server Performance Fix - FFmpeg Timeout

## Problem
Your Azure server is timing out during video processing because it's too slow.

**Symptoms:**
- FFmpeg runs at 0.2x speed (should be 1x+)
- Times out after 180 seconds
- Error: "FFmpeg processing timed out"

## Root Cause
Your Azure server has limited CPU resources, and the FFmpeg settings were optimized for quality, not speed.

## Changes Made

### 1. Increased Timeout
- **Before**: 180 seconds (3 minutes)
- **After**: 600 seconds (10 minutes)

### 2. Faster FFmpeg Preset
- **Before**: `-preset medium` (slower, better quality)
- **After**: `-preset veryfast` (much faster, good quality)

### 3. Adjusted Quality
- **Before**: `-crf 18` (very high quality, slow)
- **After**: `-crf 23` (good quality, faster)

## Performance Impact

**Expected speed improvement:**
- `veryfast` preset is ~5-10x faster than `medium`
- Your 0.2x speed should become ~1-2x speed
- 60-second video should process in 30-60 seconds instead of 5 minutes

## Deploy to Server

```bash
# On Windows
git add video_processor.py
git commit -m "Optimize FFmpeg for slower servers"
git push

# On server
cd ~/GyoPi/YTAuto
git pull
sudo systemctl restart your-service  # Or restart your Django app
```

## Alternative: Upgrade Server

If still too slow, consider:

1. **Upgrade Azure VM**:
   - Current: Likely B1s or B2s (1-2 vCPU)
   - Recommended: B2ms or B4ms (2-4 vCPU)

2. **Use Hardware Acceleration**:
   - Add `-hwaccel auto` to FFmpeg
   - Requires GPU-enabled VM (more expensive)

3. **Process Videos Asynchronously**:
   - Use Celery + Redis for background processing
   - User doesn't wait for video to finish

## Test After Fix

Try generating a short again. It should:
- ✅ Complete within 10 minutes
- ✅ Process at ~1x speed or faster
- ✅ No timeout errors

## Current Server Specs

Check your server:
```bash
# CPU info
lscpu | grep "Model name"
lscpu | grep "CPU(s):"

# Memory
free -h

# Load average
uptime
```

If load average is consistently > 1.0, your server is overloaded.

## Summary

**Quick fix**: Changed FFmpeg to use faster settings
**Long-term**: Consider upgrading server if still slow

The changes prioritize speed over quality, but quality is still good for YouTube Shorts.
