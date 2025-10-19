# Update Django Settings for ngrok

## On your EC2 instance, edit settings.py:

```bash
ssh -i "C:\Users\geoau\Downloads\ytauto.pem" ubuntu@ec2-65-1-131-185.ap-south-1.compute.amazonaws.com

cd /home/ubuntu/GyoPi/YTAuto/youtube_shorts_app
nano settings.py
```

## Update ALLOWED_HOSTS:

Find the line with `ALLOWED_HOSTS` and update it to:

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'domestically-pseudomilitaristic-candis.ngrok-free.dev', 'ec2-65-1-131-185.ap-south-1.compute.amazonaws.com', '*']
```

## Also add CSRF_TRUSTED_ORIGINS (important for ngrok):

Add this line after ALLOWED_HOSTS:

```python
CSRF_TRUSTED_ORIGINS = [
    'https://domestically-pseudomilitaristic-candis.ngrok-free.dev',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

## Save and restart Django:

Press `Ctrl+X`, then `Y`, then `Enter` to save.

Restart Django:
```bash
# If running in terminal, press Ctrl+C then:
python manage.py runserver 0.0.0.0:8000
```

## Test OAuth:

1. Go to: https://domestically-pseudomilitaristic-candis.ngrok-free.dev
2. Try to upload a video
3. Click "Authorize with YouTube"
4. Should redirect to Google OAuth properly
