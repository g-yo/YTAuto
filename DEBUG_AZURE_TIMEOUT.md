# 🔍 Debug Azure FFmpeg Timeout

## The Mystery

- ✅ Works perfectly on local PC
- ❌ Times out on MORE powerful Azure VM
- ⚠️ This means it's NOT a performance issue!

## Possible Causes

1. **FFmpeg Version Mismatch**
   - Azure might have older FFmpeg without h264 support
   - Or missing libx264 codec

2. **Hardware Encoding Issue**
   - FFmpeg trying to use GPU/hardware encoder that doesn't exist
   - Waiting for non-existent hardware

3. **Storage Latency**
   - Azure using network-attached storage (slower I/O)
   - File operations taking longer

4. **Missing Codecs**
   - libx264 not installed properly
   - AAC audio codec missing

5. **Shell Environment**
   - Different PATH or environment variables
   - FFmpeg can't find libraries

## 🔧 Debug Steps (Added to Code)

I've added debug logging that will show:

```
✅ FFmpeg version: [version info]
⚡ Step 1/2: Cutting...
✅ Step 1 complete!
⚡ Step 2/2: Rotating...
🔍 DEBUG: Running command: [full ffmpeg command]
🔍 DEBUG: Input file: [path] (exists: True/False)
🔍 DEBUG: Output file: [path]
```

If it times out:
```
❌ DEBUG: FFmpeg TIMED OUT!
❌ DEBUG: Stdout so far: [output]
❌ DEBUG: Stderr so far: [error messages]
```

## 📊 Deploy and Test

```bash
git add video_processor.py DEBUG_AZURE_TIMEOUT.md
git commit -m "Add debug logging for Azure timeout"
git push

# On Azure:
cd /home/azureuser/GyoPi/YTAuto
git pull origin main
# Restart Django and try again
```

## 🔍 What to Look For

When you try again, check the console output for:

### 1. FFmpeg Version
```
✅ FFmpeg version: ffmpeg version 4.x.x
```
If this fails → FFmpeg not installed properly

### 2. Step 1 Success
```
✅ Step 1 complete!
```
If Step 1 fails → Basic FFmpeg issue

### 3. Step 2 Command
```
🔍 DEBUG: Running command: ffmpeg -y -i ...
```
This shows the exact command being run

### 4. Input File Exists
```
🔍 DEBUG: Input file: /path/to/file (exists: True)
```
If False → Step 1 didn't create the file

### 5. Timeout Output
If it times out, look at the stderr:
- `Encoder (codec libx264) not found` → Missing codec
- `No such file or directory` → File path issue
- No output at all → FFmpeg hung/waiting for something

## 🎯 Quick Fixes Based on Output

### If "libx264 not found"
```bash
# On Azure
sudo apt update
sudo apt install ffmpeg libx264-dev -y
```

### If "No such file or directory"
```bash
# Check file permissions
ls -la /home/azureuser/GyoPi/YTAuto/outputs/
chmod 755 /home/azureuser/GyoPi/YTAuto/outputs/
```

### If FFmpeg version is old
```bash
# Install newer FFmpeg
sudo apt update
sudo apt install ffmpeg -y
```

### If it hangs with no output
FFmpeg might be waiting for user input or GPU. Try adding:
```python
'-nostdin',  # Don't wait for user input
```
to the ffmpeg command.

## 📝 Next Steps

1. Deploy the debug code
2. Try processing a video on Azure
3. Look at the console output
4. Share the debug output here
5. I'll help fix based on what we see!

---

**The debug output will tell us exactly what's wrong! 🔍**
