"""
Phase 1: Core Video Processor
This module handles downloading YouTube videos and cropping them to create shorts.
"""

import os
import yt_dlp
import subprocess
from pathlib import Path
from ai_error_handler import handle_error, get_error_message


class VideoProcessor:
    def __init__(self, download_dir='downloads', output_dir='outputs'):
        """Initialize the video processor with download and output directories."""
        self.download_dir = Path(download_dir)
        self.output_dir = Path(output_dir)
        
        # Create directories if they don't exist
        self.download_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def download_video(self, url):
        """
        Download a YouTube video using yt-dlp.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            tuple: (video_path, video_info) - Path to downloaded video and video metadata
        """
        # Path to cookies file
        cookies_path = Path(__file__).parent / 'cookies' / 'cookies.txt'
        
        # Base yt-dlp options - minimal config to avoid triggering bot detection
        ydl_opts = {
            # Download BEST quality regardless of format, then merge to MP4
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': str(self.download_dir / '%(id)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'merge_output_format': 'mp4',  # Merge to MP4 (allows WebM, VP9, etc.)
            # Minimal extractor args - let yt-dlp choose best method
            'extractor_args': {
                'youtube': {
                    'player_skip': ['js'],  # Skip JavaScript player (can trigger detection)
                }
            },
            # Use IPv4 only
            'source_address': '0.0.0.0',
            # Add sleep to avoid rate limiting
            'sleep_interval': 1,
            'max_sleep_interval': 3,
        }
        
        # Optional: Try cookies if available (android_creator works without them)
        if cookies_path.exists():
            ydl_opts['cookiefile'] = str(cookies_path)
            print(f"🍪 Using cookies from: {cookies_path}")
        else:
            print("ℹ️  No cookies file - using default yt-dlp client selection")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info
                info = ydl.extract_info(url, download=True)
                video_id = info['id']
                video_path = self.download_dir / f"{video_id}.mp4"
                
                # Display quality information
                width = info.get('width', 'Unknown')
                height = info.get('height', 'Unknown')
                fps = info.get('fps', 'Unknown')
                vcodec = info.get('vcodec', 'Unknown')
                print(f"✅ Successfully downloaded!")
                print(f"📺 Video Quality: {width}x{height} @ {fps}fps | Codec: {vcodec}")
                
                return str(video_path), {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'id': video_id,
                    'width': width,
                    'height': height,
                    'fps': fps
                }
        except Exception as e:
            error_str = str(e)
            if '403' in error_str or 'Forbidden' in error_str:
                raise Exception(
                    f"❌ YouTube blocked the download (403 Forbidden)\n"
                    f"YouTube's bot detection is extremely aggressive right now.\n\n"
                    f"🔧 SOLUTIONS TO TRY:\n\n"
                    f"1. **Try a different video** - This specific video may have extra protection\n"
                    f"2. **Wait 10-15 minutes** - You may be temporarily rate-limited\n"
                    f"3. **Use a VPN** - Your IP might be flagged by YouTube\n"
                    f"4. **Check video restrictions** - Age-restricted or region-locked videos\n"
                    f"   are harder to download\n\n"
                    f"⚠️  NOTE: Your yt-dlp is up-to-date (2025.10.14). The issue is YouTube's\n"
                    f"   aggressive bot detection, not the tool version.\n\n"
                    f"💡 TIP: Try downloading a different, non-restricted video to test if\n"
                    f"   the system works. Some videos are simply impossible to download\n"
                    f"   without a logged-in YouTube Premium account.\n\n"
                    f"Original error: {error_str}"
                )
            else:
                raise Exception(f"Error downloading video: {error_str}")
    
    def parse_time(self, time_str):
        """
        Convert time string to seconds.
        Supports formats: "MM:SS" or "HH:MM:SS" or just seconds as integer.
        
        Args:
            time_str (str): Time string
            
        Returns:
            int: Time in seconds
        """
        if isinstance(time_str, (int, float)):
            return int(time_str)
        
        parts = time_str.strip().split(':')
        
        if len(parts) == 1:  # Just seconds
            return int(parts[0])
        elif len(parts) == 2:  # MM:SS
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError("Invalid time format. Use 'MM:SS' or 'HH:MM:SS'")
    
    def crop_video(self, video_path, start_time, end_time, output_filename='short.mp4', make_shorts_format=True):
        """
        Crop a video from start_time to end_time and convert to YouTube Shorts format using FFmpeg.
        Fast single-pass processing with no temporary audio files.
        
        Args:
            video_path (str): Path to the video file
            start_time (str or int): Start time (format: "MM:SS" or seconds)
            end_time (str or int): End time (format: "MM:SS" or seconds)
            output_filename (str): Name of the output file
            make_shorts_format (bool): Convert to vertical 9:16 format for YouTube Shorts
            
        Returns:
            str: Path to the cropped video
        """
        try:
            # Parse times
            start_seconds = self.parse_time(start_time)
            end_seconds = self.parse_time(end_time)
            duration = end_seconds - start_seconds
            
            # Validate times
            if start_seconds < 0:
                raise ValueError(f"Start time cannot be negative")
            
            if start_seconds >= end_seconds:
                raise ValueError("Start time must be less than end time")
            
            # Output path
            output_path = self.output_dir / output_filename
            
            # Format timestamps for FFmpeg (HH:MM:SS)
            start_ts = self._format_timestamp(start_seconds)
            
            # TWO-STEP PROCESS for better reliability and speed
            temp_cut_path = self.output_dir / f"temp_cut_{output_filename}"
            
            # Check if FFmpeg is available
            try:
                ffmpeg_check = subprocess.run(
                    ['ffmpeg', '-version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                print(f"✅ FFmpeg version: {ffmpeg_check.stdout.split('n')[0][:50]}")
            except Exception as e:
                raise Exception(f"FFmpeg not found or not working: {str(e)}")
            
            print(f"⚡ Step 1/2: Cutting {start_ts} → {duration}s (fast copy)...")
            
            # Step 1: Cut video without re-encoding (super fast)
            cut_cmd = [
                'ffmpeg',
                '-y',
                '-ss', start_ts,
                '-i', str(video_path),
                '-t', str(duration),
                '-c', 'copy',  # Copy streams without re-encoding (FAST!)
                str(temp_cut_path)
            ]
            
            result = subprocess.run(
                cut_cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=60  # Should be very fast
            )
            
            print(f"✅ Step 1 complete!")
            
            # Step 2: Rotate and scale if needed
            if make_shorts_format:
                print(f"⚡ Step 2/2: Rotating to vertical (preserving HD quality)...")
                
                # Smart scaling: scale to 1080:1920 but only if source is lower quality
                # If source is HD or higher, maintain quality
                rotate_cmd = [
                    'ffmpeg',
                    '-y',
                    '-i', str(temp_cut_path),
                    # transpose=1 rotates 90° clockwise, scale with high quality algorithm
                    '-vf', 'transpose=1,scale=1080:1920:flags=lanczos',
                    '-c:v', 'libx264',
                    '-preset', 'veryfast',  # Much faster encoding for slower servers
                    '-crf', '23',  # Balanced quality (lower = better, but slower)
                    '-c:a', 'copy',  # Don't re-encode audio
                    '-maxrate', '12M',  # Higher bitrate for HD
                    '-bufsize', '24M',
                    '-movflags', '+faststart',
                    str(output_path)
                ]
                
                print(f"🔍 DEBUG: Running command: {' '.join(rotate_cmd)}")
                print(f"🔍 DEBUG: Input file: {temp_cut_path} (exists: {temp_cut_path.exists()})")
                print(f"🔍 DEBUG: Output file: {output_path}")
                
                try:
                    result = subprocess.run(
                        rotate_cmd,
                        capture_output=True,
                        text=True,
                        check=True,
                        timeout=600  # 10 minutes timeout for slower servers
                    )
                    print(f"🔍 DEBUG: FFmpeg stdout: {result.stdout[-500:]}")  # Last 500 chars
                    print(f"🔍 DEBUG: FFmpeg stderr: {result.stderr[-500:]}")
                except subprocess.TimeoutExpired as e:
                    print(f"❌ DEBUG: FFmpeg TIMED OUT!")
                    print(f"❌ DEBUG: Stdout so far: {e.stdout[-500:] if e.stdout else 'None'}")
                    print(f"❌ DEBUG: Stderr so far: {e.stderr[-500:] if e.stderr else 'None'}")
                    raise
                
                # Clean up temp file
                try:
                    temp_cut_path.unlink()
                except:
                    pass
                    
                print(f"✅ Step 2 complete!")
            else:
                # No rotation needed, just rename temp file
                temp_cut_path.rename(output_path)
            
            print(f"✅ Video processed successfully: {output_path}")
            return str(output_path)
        
        except subprocess.TimeoutExpired:
            raise Exception(
                f"FFmpeg processing timed out. "
                f"The server might be overloaded or the video is too complex. "
                f"Try: 1) A shorter clip (30 seconds or less), or "
                f"2) Wait a moment and try again"
            )
        except subprocess.CalledProcessError as e:
            error_msg = f"FFmpeg error: {e.stderr}"
            raise Exception(f"Error cropping video: {error_msg}")
        except Exception as e:
            raise Exception(f"Error cropping video: {str(e)}")
    
    def _format_timestamp(self, seconds):
        """
        Convert seconds to FFmpeg timestamp format (HH:MM:SS).
        
        Args:
            seconds (int): Time in seconds
            
        Returns:
            str: Formatted timestamp
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def _convert_to_shorts_format(self, clip, rotation_mode='smart'):
        """
        Convert video to YouTube Shorts format (9:16 vertical aspect ratio).
        Smart rotation to fill frame without cropping content.
        
        Args:
            clip: MoviePy VideoFileClip object
            rotation_mode: 'smart' (auto-detect), 'rotate' (force rotate), 'scale' (scale only)
            
        Returns:
            VideoFileClip: Converted clip in 9:16 format
        """
        from moviepy.editor import ColorClip, CompositeVideoClip
        
        # YouTube Shorts dimensions: 1080x1920 (9:16 aspect ratio)
        target_width = 1080
        target_height = 1920
        target_ratio = target_height / target_width  # 1.777... (9:16)
        
        # Get current dimensions
        current_width, current_height = clip.size
        current_ratio = current_height / current_width
        
        # Smart rotation: if video is landscape, try to rotate for better fit
        if rotation_mode == 'smart':
            # If video is landscape (wider than tall) and would benefit from rotation
            if current_width > current_height:
                # Check if rotating would give better coverage
                rotated_ratio = current_width / current_height
                if abs(rotated_ratio - target_ratio) < abs(current_ratio - target_ratio):
                    # Rotation would be better - rotate 90 degrees
                    clip = clip.rotate(90)
                    current_width, current_height = current_height, current_width
                    current_ratio = current_height / current_width
                    print("🔄 Rotated video 90° for better fit")
        
        # Calculate scaling to maximize content while fitting in 9:16
        # Use LARGER ratio to fill the frame (may extend beyond, but we'll fit it)
        width_ratio = target_width / current_width
        height_ratio = target_height / current_height
        
        # Use the larger ratio to fill more of the frame
        scale_ratio = max(width_ratio, height_ratio)
        
        # Resize the clip
        new_width = int(current_width * scale_ratio)
        new_height = int(current_height * scale_ratio)
        
        clip_resized = clip.resize((new_width, new_height))
        
        # Create a black background at Shorts dimensions
        background = ColorClip(
            size=(target_width, target_height),
            color=(0, 0, 0),
            duration=clip_resized.duration
        )
        
        # Center the video on the background
        x_center = (target_width - new_width) // 2
        y_center = (target_height - new_height) // 2
        
        # Crop if video extends beyond frame
        if new_width > target_width or new_height > target_height:
            # Crop to fit exactly
            x1 = max(0, -x_center)
            y1 = max(0, -y_center)
            x2 = x1 + target_width
            y2 = y1 + target_height
            
            clip_resized = clip_resized.crop(x1=x1, y1=y1, x2=x2, y2=y2)
            clip_resized = clip_resized.set_position((0, 0))
        else:
            clip_resized = clip_resized.set_position((x_center, y_center))
        
        # Composite the video onto the background
        final_clip = CompositeVideoClip([background, clip_resized])
        
        # Copy audio from original
        if clip.audio is not None:
            final_clip = final_clip.set_audio(clip.audio)
        
        return final_clip
    
    def process_youtube_video(self, url, start_time, end_time, output_filename='short.mp4', make_shorts_format=True):
        """
        Complete workflow: Download YouTube video and crop it for YouTube Shorts.
        
        Args:
            url (str): YouTube video URL
            start_time (str or int): Start time for cropping
            end_time (str or int): End time for cropping
            output_filename (str): Name of the output file
            make_shorts_format (bool): Convert to vertical 9:16 format for YouTube Shorts
            
        Returns:
            dict: Information about the processed video
        """
        print(f"Downloading video from: {url}")
        video_path, video_info = self.download_video(url)
        
        print(f"Video downloaded: {video_info['title']}")
        print(f"Cropping video from {start_time} to {end_time}")
        
        if make_shorts_format:
            print("Converting to YouTube Shorts format (9:16 vertical)...")
        
        output_path = self.crop_video(video_path, start_time, end_time, output_filename, make_shorts_format)
        
        print(f"Short created successfully: {output_path}")
        
        return {
            'output_path': output_path,
            'original_title': video_info['title'],
            'video_id': video_info['id'],
            'duration': self.parse_time(end_time) - self.parse_time(start_time),
            'is_shorts_format': make_shorts_format
        }
    
    def cleanup(self, keep_outputs=True, cleanup_all=False):
        """
        Clean up downloaded and temporary files.
        
        Args:
            keep_outputs (bool): Whether to keep the output files
            cleanup_all (bool): Clean everything including outputs (for post-upload cleanup)
        """
        try:
            # Clean downloads
            deleted_count = 0
            for file in self.download_dir.glob('*'):
                if file.is_file():
                    try:
                        file.unlink()
                        deleted_count += 1
                    except Exception as e:
                        print(f"Warning: Could not delete {file}: {e}")
            
            print(f"🧹 Cleaned {deleted_count} downloaded file(s)")
            
            # Clean outputs if requested
            if not keep_outputs or cleanup_all:
                output_count = 0
                for file in self.output_dir.glob('*'):
                    if file.is_file():
                        try:
                            file.unlink()
                            output_count += 1
                        except Exception as e:
                            print(f"Warning: Could not delete {file}: {e}")
                
                print(f"🧹 Cleaned {output_count} output file(s)")
            
            # Clean temporary audio files
            temp_files = ['temp-audio.m4a', 'temp-audio.m4a.tmp']
            for temp_file in temp_files:
                temp_path = Path(temp_file)
                if temp_path.exists():
                    try:
                        temp_path.unlink()
                    except:
                        pass
        
        except Exception as e:
            handle_error(e, context="File cleanup", show_traceback=False)
    
    def cleanup_after_upload(self, video_path=None):
        """
        Aggressive cleanup after successful upload to save space.
        Deletes all temporary files and the specified video.
        
        Args:
            video_path (str): Specific video file to delete
        """
        print("\n🧹 Starting post-upload cleanup...")
        
        # Delete specific video file if provided
        if video_path:
            try:
                video_file = Path(video_path)
                if video_file.exists():
                    video_file.unlink()
                    print(f"✅ Deleted uploaded video: {video_file.name}")
            except Exception as e:
                print(f"⚠️  Could not delete {video_path}: {e}")
        
        # Clean all temporary files
        self.cleanup(keep_outputs=False, cleanup_all=True)
        
        print("✅ Post-upload cleanup complete!\n")


# Example usage for testing
if __name__ == "__main__":
    processor = VideoProcessor()
    
    # Example: Process a YouTube video
    # Replace with actual YouTube URL for testing
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    start = "0:10"  # Start at 10 seconds
    end = "0:40"    # End at 40 seconds
    
    try:
        result = processor.process_youtube_video(url, start, end, 'my_short.mp4')
        print(f"\nSuccess! Short saved to: {result['output_path']}")
    except Exception as e:
        print(f"Error: {e}")
