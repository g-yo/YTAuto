"""
Audio-Reactive Animation Generator
Creates vibrant, music-synchronized animations for YouTube Shorts.
Uses procedural generation with AI-guided styling from Gemini.
"""

import numpy as np
import google.generativeai as genai
from django.conf import settings
from moviepy.editor import VideoClip, AudioFileClip, CompositeVideoClip, TextClip, ColorClip
from moviepy.video.fx import resize
from ai_error_handler import handle_error, get_error_message
import colorsys
from pathlib import Path
import cv2
import subprocess
import tempfile
import os

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    print("⚠️  librosa not installed. Run: pip install librosa numpy scipy")


class AnimationGenerator:
    """Generate vibrant audio-reactive animations."""
    
    def __init__(self):
        """Initialize the animation generator."""
        self.gemini_available = bool(settings.GEMINI_API_KEY)
        if self.gemini_available:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        
        # Animation settings
        self.width = 1080
        self.height = 1920
        self.fps = 30
    
    def create_animated_short(self, audio_path, output_path, duration=None):
        """
        Create a vibrant animated short synchronized to audio.
        
        Args:
            audio_path (str): Path to audio file
            output_path (str): Path to save output video
            duration (float): Duration in seconds (None = use full audio)
            
        Returns:
            dict: Generation results
        """
        try:
            print(f"\n🎨 Creating animated short from audio...")
            
            # Load and analyze audio
            audio_analysis = self._analyze_audio(audio_path, duration)
            
            if not audio_analysis['success']:
                raise Exception(audio_analysis.get('error', 'Audio analysis failed'))
            
            # Get AI-guided visual style
            visual_style = self._get_visual_style(audio_analysis)
            
            print(f"🎵 Audio: {audio_analysis['tempo']:.0f} BPM, {audio_analysis['mood']} mood")
            print(f"🎨 Style: {visual_style['animation_style']}")
            print(f"🌈 Colors: {', '.join(visual_style['color_scheme'][:3])}")
            
            # Use FAST rendering method (OpenCV + FFmpeg)
            self._generate_animation_fast(audio_analysis, visual_style, output_path, audio_path)
            
            return {
                'success': True,
                'output_path': output_path,
                'duration': audio_analysis['duration'],
                'style': visual_style,
                'audio_analysis': audio_analysis
            }
            
        except Exception as e:
            handle_error(e, context="Animation generation", show_traceback=True)
            return {
                'success': False,
                'error': get_error_message(e, "Animation generation")
            }
    
    def _analyze_audio(self, audio_path, max_duration=None):
        """Analyze audio for tempo, beats, and energy."""
        if not LIBROSA_AVAILABLE:
            return {
                'success': True,
                'tempo': 120.0,
                'beats': [],
                'energy': 0.5,
                'mood': 'energetic',
                'duration': max_duration or 30,
                'fallback': True
            }
        
        try:
            # Load audio
            y, sr = librosa.load(audio_path, duration=max_duration or 60)
            
            # Tempo and beats
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            beat_times = librosa.frames_to_time(beat_frames, sr=sr)
            
            # Energy
            rms = librosa.feature.rms(y=y)[0]
            energy = float(np.mean(rms))
            
            # Spectral features
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            brightness = float(np.mean(spectral_centroid))
            
            # Determine mood
            if tempo < 80:
                mood = "calm" if energy < 0.3 else "dramatic"
            elif tempo < 120:
                mood = "romantic" if energy < 0.5 else "upbeat"
            else:
                mood = "energetic" if energy > 0.6 else "motivational"
            
            return {
                'success': True,
                'tempo': float(tempo),
                'beats': beat_times.tolist(),
                'energy': energy,
                'brightness': brightness,
                'mood': mood,
                'duration': len(y) / sr,
                'sample_rate': sr
            }
            
        except Exception as e:
            print(f"⚠️  Audio analysis error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_visual_style(self, audio_analysis):
        """Get AI-guided visual style based on audio."""
        mood = audio_analysis.get('mood', 'energetic')
        tempo = audio_analysis.get('tempo', 120)
        energy = audio_analysis.get('energy', 0.5)
        
        if not self.gemini_available:
            return self._get_default_style(mood, tempo, energy)
        
        try:
            prompt = f"""
            Create a vibrant visual style for a music animation.
            
            Audio: {tempo:.0f} BPM, {mood} mood, energy {energy:.2f}
            
            Suggest:
            1. Animation style (one sentence describing movement and effects)
            2. 4 hex color codes that match the mood
            3. 3 visual elements (e.g., particles, waves, shapes)
            
            Format:
            STYLE: [description]
            COLORS: #color1, #color2, #color3, #color4
            ELEMENTS: element1, element2, element3
            """
            
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            style = "Dynamic particle motion with vibrant effects"
            colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#F7B731"]
            elements = ["particles", "waves", "glow"]
            
            for line in text.split('\n'):
                if 'STYLE:' in line:
                    style = line.split('STYLE:')[1].strip()
                elif 'COLORS:' in line:
                    color_text = line.split('COLORS:')[1].strip()
                    colors = [c.strip() for c in color_text.replace('#', '').split(',')]
                    colors = ['#' + c if not c.startswith('#') else c for c in colors]
                elif 'ELEMENTS:' in line:
                    elem_text = line.split('ELEMENTS:')[1].strip()
                    elements = [e.strip() for e in elem_text.split(',')]
            
            return {
                'animation_style': style,
                'color_scheme': colors[:4],
                'visual_elements': elements[:3],
                'mood': mood,
                'ai_generated': True
            }
            
        except Exception as e:
            print(f"⚠️  AI style generation failed: {e}")
            return self._get_default_style(mood, tempo, energy)
    
    def _get_default_style(self, mood, tempo, energy):
        """Get default visual style based on mood."""
        styles = {
            'calm': {
                'style': 'Soft flowing gradients with gentle particle motion',
                'colors': ['#667eea', '#764ba2', '#f093fb', '#4facfe'],
                'elements': ['gradients', 'particles', 'waves']
            },
            'energetic': {
                'style': 'Fast-moving neon particles with pulse effects',
                'colors': ['#f093fb', '#f5576c', '#4facfe', '#00f2fe'],
                'elements': ['particles', 'neon', 'pulses']
            },
            'romantic': {
                'style': 'Warm flowing shapes with soft glows',
                'colors': ['#ff9a9e', '#fad0c4', '#ffecd2', '#fcb69f'],
                'elements': ['shapes', 'glows', 'flows']
            },
            'dramatic': {
                'style': 'Bold contrasts with intense pulsing lights',
                'colors': ['#ee0979', '#ff6a00', '#000000', '#ffffff'],
                'elements': ['contrasts', 'pulses', 'lights']
            },
            'upbeat': {
                'style': 'Bouncing colorful shapes with rhythmic motion',
                'colors': ['#43e97b', '#38f9d7', '#ffd89b', '#19d4ae'],
                'elements': ['shapes', 'bounces', 'rhythms']
            },
            'motivational': {
                'style': 'Rising glowing elements with dynamic camera motion',
                'colors': ['#fa709a', '#fee140', '#30cfd0', '#330867'],
                'elements': ['glows', 'rises', 'motion']
            }
        }
        
        style_data = styles.get(mood, styles['energetic'])
        return {
            'animation_style': style_data['style'],
            'color_scheme': style_data['colors'],
            'visual_elements': style_data['elements'],
            'mood': mood,
            'ai_generated': False
        }
    
    def _generate_animation_fast(self, audio_analysis, visual_style, output_path, audio_path):
        """Generate animation using fast batch rendering with OpenCV."""
        duration = audio_analysis['duration']
        beats = audio_analysis.get('beats', [])
        tempo = audio_analysis.get('tempo', 120)
        mood = audio_analysis.get('mood', 'energetic')
        
        # Parse colors
        colors = self._parse_colors(visual_style['color_scheme'])
        
        # Calculate total frames
        total_frames = int(duration * self.fps)
        print(f"⚡ FAST MODE: Rendering {total_frames} frames at {self.fps} FPS...")
        print(f"   Expected time: 3-5 minutes (optimized rendering)")
        
        # Create temporary video file (no audio)
        temp_video = output_path.replace('.mp4', '_temp.mp4')
        
        # Initialize video writer with OpenCV (much faster!)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_video, fourcc, self.fps, (self.width, self.height))
        
        # Render frames in batches
        batch_size = 30  # Render 30 frames at a time
        for i in range(0, total_frames, batch_size):
            batch_end = min(i + batch_size, total_frames)
            
            # Render batch
            for frame_num in range(i, batch_end):
                t = frame_num / self.fps
                frame = self._render_frame(t, duration, beats, tempo, mood, colors)
                
                # Convert RGB to BGR for OpenCV
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            
            # Progress update
            progress = (batch_end / total_frames) * 100
            print(f"   Progress: {progress:.1f}% ({batch_end}/{total_frames} frames)")
        
        out.release()
        print(f"✅ Video frames rendered!")
        
        # Combine with audio using FFmpeg (super fast!)
        print(f"🎵 Adding audio with FFmpeg...")
        subprocess.run([
            'ffmpeg', '-y',
            '-i', temp_video,
            '-i', audio_path,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-shortest',
            '-preset', 'ultrafast',  # Fast encoding
            output_path
        ], capture_output=True, check=True)
        
        # Clean up temp file
        if os.path.exists(temp_video):
            os.remove(temp_video)
        
        print(f"✅ Final video created: {output_path}")
        return output_path
    
    def _render_frame(self, t, duration, beats, tempo, mood, colors):
        """Render a single frame of animation."""
        # Create base image
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Progress through video (0 to 1)
        progress = t / duration if duration > 0 else 0
        
        # Check if on a beat
        on_beat = any(abs(t - beat) < 0.1 for beat in beats) if beats else False
        beat_intensity = 1.5 if on_beat else 1.0
        
        # Render based on mood
        if mood in ['energetic', 'upbeat']:
            frame = self._render_energetic(frame, t, progress, colors, beat_intensity, tempo)
        elif mood in ['calm', 'romantic']:
            frame = self._render_calm(frame, t, progress, colors)
        elif mood in ['dramatic', 'motivational']:
            frame = self._render_dramatic(frame, t, progress, colors, beat_intensity)
        else:
            frame = self._render_energetic(frame, t, progress, colors, beat_intensity, tempo)
        
        return frame
    
    def _render_energetic(self, frame, t, progress, colors, beat_intensity, tempo):
        """Render energetic animation with particles and pulses - OPTIMIZED."""
        # Vectorized gradient background
        y_coords = np.arange(self.height).reshape(-1, 1)
        ratio = (y_coords / self.height + progress) % 1.0
        
        c1 = np.array(colors[0])
        c2 = np.array(colors[1])
        # Broadcast ratio correctly for RGB
        frame[:, :] = (c1 * (1 - ratio[:, :, np.newaxis]) + c2 * ratio[:, :, np.newaxis]).astype(np.uint8)
        
        # Add pulsing circles (minimal for speed)
        num_circles = 2  # Reduced from 3
        for i in range(num_circles):
            angle = (i / num_circles) * 2 * np.pi + t * tempo / 60
            radius = 200 + 100 * np.sin(t * 2 + i)
            cx = int(self.width / 2 + np.cos(angle) * 300)
            cy = int(self.height / 2 + np.sin(angle) * 500)
            
            color = colors[i % len(colors)]
            self._draw_circle(frame, cx, cy, int(radius * beat_intensity), color, alpha=0.3)
        
        return frame
    
    def _render_calm(self, frame, t, progress, colors):
        """Render calm animation with gradients and waves - OPTIMIZED."""
        # Vectorized gradient calculation
        y_coords = np.arange(self.height).reshape(-1, 1)
        x_coords = np.arange(self.width).reshape(1, -1)
        
        # Wave effect
        wave = np.sin(x_coords / 200 + t) * 0.5 + 0.5
        ratio = (y_coords / self.height * 0.7 + wave * 0.3) % 1.0
        
        # Blend colors using vectorized operations
        c1 = np.array(colors[0])
        c2 = np.array(colors[1])
        frame[:, :] = (c1 * (1 - ratio[:, :, np.newaxis]) + c2 * ratio[:, :, np.newaxis]).astype(np.uint8)
        
        # Gentle particles (minimal for speed)
        num_particles = 5  # Reduced from 10
        for i in range(num_particles):
            x = int((np.sin(t * 0.5 + i) * 0.5 + 0.5) * self.width)
            y = int(((t * 50 + i * 100) % self.height))
            color = colors[i % len(colors)]
            self._draw_circle(frame, x, y, 15, color, alpha=0.5)
        
        return frame
    
    def _render_dramatic(self, frame, t, progress, colors, beat_intensity):
        """Render dramatic animation with bold contrasts - OPTIMIZED."""
        # Gradient background (faster than solid + rays)
        y_coords = np.arange(self.height).reshape(-1, 1)
        ratio = (y_coords / self.height * 0.5 + progress * 0.5) % 1.0
        
        c1 = np.array(colors[0])
        c2 = np.array(colors[1] if len(colors) > 1 else colors[0])
        # Broadcast ratio correctly for RGB
        frame[:, :] = (c1 * (1 - ratio[:, :, np.newaxis]) + c2 * ratio[:, :, np.newaxis]).astype(np.uint8)
        
        # Minimal pulsing circles (faster than rays)
        num_circles = 2
        for i in range(num_circles):
            angle = (i / num_circles) * 2 * np.pi + t * 0.5
            radius = int(150 + 100 * beat_intensity)
            cx = int(self.width / 2 + np.cos(angle) * 200)
            cy = int(self.height / 2 + np.sin(angle) * 300)
            
            color = colors[i % len(colors)]
            self._draw_circle(frame, cx, cy, radius, color, alpha=0.4)
        
        return frame
    
    def _parse_colors(self, color_scheme):
        """Parse color scheme to RGB tuples."""
        colors = []
        for color in color_scheme:
            try:
                rgb = self._hex_to_rgb(color)
                colors.append(rgb)
            except:
                colors.append((255, 107, 107))  # Default color
        return colors
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        # If already a tuple, return as-is
        if isinstance(hex_color, (tuple, list)):
            return tuple(hex_color)
        
        # Convert hex string to RGB
        if isinstance(hex_color, str):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Fallback
        return (255, 107, 107)
    
    def _blend_colors(self, color1, color2, ratio):
        """Blend two colors based on ratio (0-1)."""
        c1 = np.array(color1)
        c2 = np.array(color2)
        return (c1 * (1 - ratio) + c2 * ratio).astype(np.uint8)
    
    def _draw_circle(self, frame, cx, cy, radius, color, alpha=1.0):
        """Draw a circle on the frame."""
        y, x = np.ogrid[:self.height, :self.width]
        mask = (x - cx)**2 + (y - cy)**2 <= radius**2
        if alpha < 1.0:
            frame[mask] = (frame[mask] * (1 - alpha) + np.array(color) * alpha).astype(np.uint8)
        else:
            frame[mask] = color
    
    def _draw_line(self, frame, x1, y1, x2, y2, color, alpha=1.0, thickness=5):
        """Draw a line on the frame."""
        # Simple line drawing
        length = int(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        if length == 0:
            return
        
        for i in range(length):
            t = i / length
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)
            if 0 <= x < self.width and 0 <= y < self.height:
                self._draw_circle(frame, x, y, thickness, color, alpha)


# Example usage
if __name__ == "__main__":
    generator = AnimationGenerator()
    
    result = generator.create_animated_short(
        audio_path="test_audio.mp3",
        output_path="animated_short.mp4",
        duration=30
    )
    
    if result['success']:
        print(f"✅ Animation created: {result['output_path']}")
    else:
        print(f"❌ Failed: {result['error']}")
