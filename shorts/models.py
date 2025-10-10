from django.db import models


class VideoShort(models.Model):
    """Model to store information about generated video shorts."""
    
    youtube_url = models.URLField(max_length=500)
    original_title = models.CharField(max_length=500)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    video_file = models.FileField(upload_to='shorts/', blank=True, null=True)
    
    # AI-generated content
    generated_title = models.CharField(max_length=200, blank=True)
    generated_hashtags = models.TextField(blank=True)
    
    # YouTube upload info
    uploaded_to_youtube = models.BooleanField(default=False)
    youtube_video_id = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.original_title} ({self.start_time} - {self.end_time})"
