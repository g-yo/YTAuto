from django.contrib import admin
from .models import VideoShort

@admin.register(VideoShort)
class VideoShortAdmin(admin.ModelAdmin):
    list_display = ('original_title', 'created_at', 'uploaded_to_youtube', 'youtube_video_id')
    list_filter = ('uploaded_to_youtube', 'created_at')
    search_fields = ('original_title', 'youtube_video_id')
    readonly_fields = ('created_at',)
