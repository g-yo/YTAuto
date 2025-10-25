from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.files import File
from django.http import JsonResponse
from .models import VideoShort
from video_processor import VideoProcessor
from video_analyzer import VideoAnalyzer
from animation_generator import AnimationGenerator
from ai_error_handler import handle_error, get_error_message
import os
import sys
from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def index(request):
    """Main page with the form to generate shorts."""
    return render(request, 'shorts/index.html')


# def _create_animated_short(processor, youtube_url, start_time, end_time):
#     """
#     Create an animated short with audio from the video.
    
#     Args:
#         processor: VideoProcessor instance
#         youtube_url: YouTube video URL
#         start_time: Start time for audio extraction
#         end_time: End time for audio extraction
        
#     Returns:
#         dict: Result with output_path and metadata
#     """
#     try:
#         # Download video
#         print("📥 Downloading video...")
#         video_path, video_info = processor.download_video(youtube_url)
        
#         # Extract audio from the segment
#         print(f"🎵 Extracting audio from {start_time} to {end_time}...")
#         video_clip = VideoFileClip(video_path)
        
#         start_seconds = processor.parse_time(start_time)
#         end_seconds = processor.parse_time(end_time)
        
#         # Limit duration to 30 seconds max for faster rendering
#         duration = end_seconds - start_seconds
#         if duration > 30:
#             print(f"⚠️  Segment too long ({duration}s). Limiting to 30 seconds for faster rendering.")
#             end_seconds = start_seconds + 30
        
#         audio_clip = video_clip.subclip(start_seconds, end_seconds).audio
#         audio_path = str(processor.output_dir / "temp_audio.mp3")
#         audio_clip.write_audiofile(audio_path, verbose=False, logger=None)
        
#         audio_clip.close()
#         video_clip.close()
        
#         # Generate animation
#         print("🎨 Generating audio-reactive animation...")
#         generator = AnimationGenerator()
        
#         output_filename = f'animated_short_{VideoShort.objects.count() + 1}.mp4'
#         output_path = str(processor.output_dir / output_filename)
        
#         animation_result = generator.create_animated_short(
#             audio_path=audio_path,
#             output_path=output_path,
#             duration=end_seconds - start_seconds
#         )
        
#         if not animation_result['success']:
#             raise Exception(animation_result.get('error', 'Animation generation failed'))
        
#         # Clean up temp audio
#         try:
#             Path(audio_path).unlink()
#         except:
#             pass
        
#         return {
#             'output_path': output_path,
#             'original_title': video_info['title'],
#             'video_id': video_info['id'],
#             'duration': end_seconds - start_seconds,
#             'is_animation': True,
#             'animation_style': animation_result.get('style', {})
#         }
        
#     except Exception as e:
#         handle_error(e, context="Animated short creation", show_traceback=True)
#         raise
def _create_animated_short(processor, youtube_url, start_time, end_time):
    """
    Create an animated short by cutting the required portion of the video
    instead of extracting audio separately.
    """
    try:
        # Download video
        print("📥 Downloading video...")
        video_path, video_info = processor.download_video(youtube_url)
        
        # Parse times
        start_seconds = processor.parse_time(start_time)
        end_seconds = processor.parse_time(end_time)

        # Enforce 45s limit
        duration = end_seconds - start_seconds
        if duration > 45:
            print(f"⚠️  Segment too long ({duration}s). Limiting to 45 seconds.")
            end_seconds = start_seconds + 45

        # Cut only the selected segment (audio + video)
        print(f"✂️ Cutting clip from {start_seconds}s to {end_seconds}s ...")
        clip = VideoFileClip(video_path).subclip(start_seconds, end_seconds)

        # Define output path
        output_filename = f'animated_short_{VideoShort.objects.count() + 1}.mp4'
        output_path = str(processor.output_dir / output_filename)

        # Save the cut video (keep audio)
        clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile=str(processor.output_dir / "temp_cut_audio.m4a"),
            remove_temp=True,
            verbose=False,
            logger=None
        )

        clip.close()

        # (Optional) Run animation overlay — if you want to add visual motion graphics later
        # If your AnimationGenerator adds overlays, you can re-enable this:
        # generator = AnimationGenerator()
        # animation_result = generator.overlay_animation(output_path)

        print("✅ Clip created successfully.")

        return {
            'output_path': output_path,
            'original_title': video_info['title'],
            'video_id': video_info['id'],
            'duration': end_seconds - start_seconds,
            'is_animation': False,  # not a separate animation render
            'animation_style': None
        }

    except Exception as e:
        handle_error(e, context="Animated short creation", show_traceback=True)
        raise


# def generate_short(request):
#     """Handle the video generation request with AI auto-detection and animation."""
#     if request.method == 'POST':
#         youtube_url = request.POST.get('youtube_url')
#         start_time = request.POST.get('start_time')
#         end_time = request.POST.get('end_time')
#         auto_detect = request.POST.get('auto_detect', 'off') == 'on'
#         create_animation = request.POST.get('create_animation', 'off') == 'on'
        
#         # Validate URL is always required
#         if not youtube_url:
#             messages.error(request, 'Please provide a YouTube URL.')
#             return redirect('shorts:index')
        
#         try:
#             # Initialize processors
#             processor = VideoProcessor(
#                 download_dir=str(settings.DOWNLOADS_DIR),
#                 output_dir=str(settings.OUTPUTS_DIR)
#             )
            
#             # AI Auto-Detection Mode
#             if auto_detect or (not start_time or not end_time):
#                 print("\n🤖 AI Auto-Detection Mode Activated")
#                 analyzer = VideoAnalyzer()
#                 analysis = analyzer.analyze_video(youtube_url)
                
#                 if analysis['success']:
#                     # Use AI-detected segment
#                     segment = analysis['suggested_segment']
#                     start_time = f"{segment['start_time'] // 60}:{segment['start_time'] % 60:02d}"
#                     end_time = f"{segment['end_time'] // 60}:{segment['end_time'] % 60:02d}"
                    
#                     print(f"✅ AI detected best segment: {start_time} to {end_time}")
#                     print(f"   Reason: {segment['reason']}")
                    
#                     # Use AI-generated metadata
#                     ai_metadata = analysis['ai_analysis']
#                 else:
#                     # Fallback to manual if auto-detection fails
#                     if not start_time or not end_time:
#                         messages.error(request, analysis.get('error', 'Auto-detection failed. Please provide times manually.'))
#                         return redirect('shorts:index')
#                     ai_metadata = None
#             else:
#                 # Manual mode
#                 if not all([start_time, end_time]):
#                     messages.error(request, 'Please fill in all fields.')
#                     return redirect('shorts:index')
#                 ai_metadata = None
            
#             # Check if animation mode is enabled
#             if create_animation:
#                 # Animation mode: extract audio and create animated video
#                 print(f"\n🎨 Animation Mode: Creating audio-reactive animation")
#                 result = _create_animated_short(
#                     processor, youtube_url, start_time, end_time
#                 )
#             else:
#                 # Normal mode: process video
#                 print(f"\n🎬 Processing video: {youtube_url}")
#                 result = processor.process_youtube_video(
#                     url=youtube_url,
#                     start_time=start_time,
#                     end_time=end_time,
#                     output_filename=f'short_{VideoShort.objects.count() + 1}.mp4',
#                     make_shorts_format=True  # Always create in Shorts format
#                 )
            
#             # Create database record
#             video_short = VideoShort.objects.create(
#                 youtube_url=youtube_url,
#                 original_title=result['original_title'],
#                 start_time=start_time,
#                 end_time=end_time
#             )
            
#             # Save the video file to media
#             output_path = Path(result['output_path'])
#             with open(output_path, 'rb') as f:
#                 video_short.video_file.save(output_path.name, File(f), save=True)
            
#             # Use AI-generated metadata if available from auto-detection
#             if ai_metadata:
#                 video_short.generated_title = ai_metadata['title']
#                 video_short.generated_hashtags = ai_metadata['description']
#                 video_short.save()
#                 print(f"✅ Used AI-generated metadata")
#             # Otherwise generate AI title and hashtags if API key is available
#             elif settings.GEMINI_API_KEY:
#                 try:
#                     from .ai_generator import generate_title_and_hashtags
#                     ai_content = generate_title_and_hashtags(result['original_title'])
#                     video_short.generated_title = ai_content['title']
#                     video_short.generated_hashtags = ai_content['hashtags']
#                     video_short.save()
#                 except Exception as e:
#                     handle_error(e, context="AI metadata generation", show_traceback=False)
            
#             success_msg = 'Short generated successfully!'
#             if auto_detect:
#                 success_msg += ' (AI auto-detected best segment)'
#             if create_animation:
#                 success_msg += ' (Audio-reactive animation created)'
#             messages.success(request, success_msg)
            
#             # Cleanup downloaded file (keep outputs for now)
#             processor.cleanup(keep_outputs=True)
            
#             return render(request, 'shorts/result.html', {
#                 'video_short': video_short,
#                 'video_url': video_short.video_file.url,
#                 'auto_detected': auto_detect
#             })
            
#         except Exception as e:
#             error_msg = get_error_message(e, context="Video generation")
#             messages.error(request, error_msg)
#             handle_error(e, context="Video generation", show_traceback=True)
#             return redirect('shorts:index')
    
#     return redirect('shorts:index')

def generate_short(request):
    """Handle the video generation request with AI auto-detection and animation."""
    if request.method == 'POST':
        youtube_url = request.POST.get('youtube_url')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        auto_detect = request.POST.get('auto_detect', 'off') == 'on'
        create_animation = request.POST.get('create_animation', 'off') == 'on'
        
        if not youtube_url:
            messages.error(request, 'Please provide a YouTube URL.')
            return redirect('shorts:index')
        
        try:
            processor = VideoProcessor(
                download_dir=str(settings.DOWNLOADS_DIR),
                output_dir=str(settings.OUTPUTS_DIR)
            )
            
            # AI Auto-Detection Mode
            if auto_detect or (not start_time or not end_time):
                print("\n🤖 AI Auto-Detection Mode Activated")
                analyzer = VideoAnalyzer()
                analysis = analyzer.analyze_video(youtube_url)
                
                if analysis['success']:
                    segment = analysis['suggested_segment']
                    start_time = f"{segment['start_time'] // 60}:{segment['start_time'] % 60:02d}"
                    end_time = f"{segment['end_time'] // 60}:{segment['end_time'] % 60:02d}"
                    
                    print(f"✅ AI detected best segment: {start_time} to {end_time}")
                    print(f"   Reason: {segment['reason']}")
                    
                    ai_metadata = analysis['ai_analysis']
                else:
                    if not start_time or not end_time:
                        messages.error(request, analysis.get('error', 'Auto-detection failed. Please provide times manually.'))
                        return redirect('shorts:index')
                    ai_metadata = None
            else:
                if not all([start_time, end_time]):
                    messages.error(request, 'Please fill in all fields.')
                    return redirect('shorts:index')
                ai_metadata = None
            
            # 🕒 Enforce 45s limit globally (for both animation and normal modes)
            start_seconds = processor.parse_time(start_time)
            end_seconds = processor.parse_time(end_time)
            duration = end_seconds - start_seconds
            if duration > 45:
                print(f"⚠️  Segment too long ({duration}s). Limiting to 45 seconds.")
                end_seconds = start_seconds + 45
                end_time = f"{end_seconds // 60}:{end_seconds % 60:02d}"
            
            # Animation mode
            if create_animation:
                print(f"\n🎨 Animation Mode: Creating audio-reactive animation")
                result = _create_animated_short(
                    processor, youtube_url, start_time, end_time
                )
            else:
                print(f"\n🎬 Processing video: {youtube_url}")
                result = processor.process_youtube_video(
                    url=youtube_url,
                    start_time=start_time,
                    end_time=end_time,
                    output_filename=f'short_{VideoShort.objects.count() + 1}.mp4',
                    make_shorts_format=True
                )
            
            # Create DB record
            video_short = VideoShort.objects.create(
                youtube_url=youtube_url,
                original_title=result['original_title'],
                start_time=start_time,
                end_time=end_time
            )
            
            output_path = Path(result['output_path'])
            with open(output_path, 'rb') as f:
                video_short.video_file.save(output_path.name, File(f), save=True)
            
            if ai_metadata:
                video_short.generated_title = ai_metadata['title']
                video_short.generated_hashtags = ai_metadata['description']
                video_short.save()
                print(f"✅ Used AI-generated metadata")
            elif settings.GEMINI_API_KEY:
                try:
                    from .ai_generator import generate_title_and_hashtags
                    ai_content = generate_title_and_hashtags(result['original_title'])
                    video_short.generated_title = ai_content['title']
                    video_short.generated_hashtags = ai_content['hashtags']
                    video_short.save()
                except Exception as e:
                    handle_error(e, context="AI metadata generation", show_traceback=False)
            
            success_msg = 'Short generated successfully!'
            if auto_detect:
                success_msg += ' (AI auto-detected best segment)'
            if create_animation:
                success_msg += ' (Audio-reactive animation created)'
            messages.success(request, success_msg)
            
            processor.cleanup(keep_outputs=True)
            
            return render(request, 'shorts/result.html', {
                'video_short': video_short,
                'video_url': video_short.video_file.url,
                'auto_detected': auto_detect
            })
            
        except Exception as e:
            error_msg = get_error_message(e, context="Video generation")
            messages.error(request, error_msg)
            handle_error(e, context="Video generation", show_traceback=True)
            return redirect('shorts:index')
    
    return redirect('shorts:index')


def upload_to_youtube(request, short_id):
    """Handle YouTube upload with OAuth 2.0."""
    video_short = get_object_or_404(VideoShort, id=short_id)
    
    if video_short.uploaded_to_youtube:
        messages.info(request, 'This video has already been uploaded to YouTube.')
        return redirect('shorts:history')
    
    try:
        from .youtube_uploader import YouTubeUploader
        
        uploader = YouTubeUploader()
        
        # Check if we have credentials
        if not uploader.has_credentials(request):
            # Redirect to OAuth flow
            auth_url = uploader.get_authorization_url(request)
            return redirect(auth_url)
        
        # Upload the video as YouTube Short
        title = video_short.generated_title or video_short.original_title
        description = video_short.generated_hashtags or "#Shorts\n\nCreated with YouTube Shorts Automation"
        
        # Ensure #Shorts is in description
        if '#Shorts' not in description and '#shorts' not in description:
            description = f"#Shorts\n\n{description}"
        
        video_id = uploader.upload_video(
            request=request,
            video_path=video_short.video_file.path,
            title=title,
            description=description,
            is_shorts=True  # Always upload as YouTube Short
        )
        
        # Update the record
        video_short.uploaded_to_youtube = True
        video_short.youtube_video_id = video_id
        video_short.save()
        
        # Cleanup after successful upload to save space
        print("\n🧹 Cleaning up after successful upload...")
        processor = VideoProcessor(
            download_dir=str(settings.DOWNLOADS_DIR),
            output_dir=str(settings.OUTPUTS_DIR)
        )
        processor.cleanup_after_upload(video_path=video_short.video_file.path)
        
        messages.success(request, f'Successfully uploaded to YouTube Shorts! Video ID: {video_id} (Files cleaned up)')
        return redirect('shorts:history')
        
    except Exception as e:
        messages.error(request, f'Error uploading to YouTube: {str(e)}')
        return redirect('shorts:history')


def oauth2callback(request):
    """Handle OAuth 2.0 callback from Google."""
    try:
        from .youtube_uploader import YouTubeUploader
        
        uploader = YouTubeUploader()
        uploader.handle_oauth_callback(request)
        
        messages.success(request, 'Successfully connected to YouTube!')
        
        # Redirect back to upload if we have a pending upload
        short_id = request.session.get('pending_upload_id')
        if short_id:
            del request.session['pending_upload_id']
            return redirect('shorts:upload_to_youtube', short_id=short_id)
        
        return redirect('shorts:history')
        
    except Exception as e:
        messages.error(request, f'OAuth error: {str(e)}')
        return redirect('shorts:index')


def history(request):
    """Display history of generated shorts."""
    shorts = VideoShort.objects.all()
    return render(request, 'shorts/history.html', {'shorts': shorts})


def debug_oauth_config(request):
    """Debug endpoint to check OAuth configuration."""
    import json
    from django.urls import reverse
    
    debug_info = {
        'status': 'checking',
        'issues': [],
        'warnings': [],
        'config': {}
    }
    
    # Check client_secret.json
    client_secret_path = settings.YOUTUBE_CLIENT_SECRETS_FILE
    if not client_secret_path.exists():
        debug_info['issues'].append('client_secret.json not found')
        debug_info['status'] = 'error'
    else:
        try:
            with open(client_secret_path, 'r') as f:
                data = json.load(f)
            
            if 'web' in data:
                config = data['web']
                debug_info['config']['client_type'] = 'web'
            elif 'installed' in data:
                config = data['installed']
                debug_info['config']['client_type'] = 'installed'
                debug_info['warnings'].append('Using "installed" app credentials. Should use "Web application"')
            else:
                debug_info['issues'].append('Unknown client type')
                config = {}
            
            # Check redirect URIs
            redirect_uris = config.get('redirect_uris', [])
            expected_uri = request.build_absolute_uri(reverse('shorts:oauth2callback'))
            
            debug_info['config']['expected_redirect_uri'] = expected_uri
            debug_info['config']['configured_redirect_uris'] = redirect_uris
            
            if expected_uri not in redirect_uris:
                debug_info['warnings'].append(
                    f'Expected redirect URI not in client_secret.json: {expected_uri}'
                )
            
            # Mask sensitive data
            if 'client_id' in config:
                debug_info['config']['client_id'] = config['client_id'][:50] + '...'
            
            if not debug_info['issues']:
                debug_info['status'] = 'ok' if not debug_info['warnings'] else 'warning'
                
        except Exception as e:
            debug_info['issues'].append(f'Error reading client_secret.json: {str(e)}')
            debug_info['status'] = 'error'
    
    return JsonResponse(debug_info, json_dumps_params={'indent': 2})
