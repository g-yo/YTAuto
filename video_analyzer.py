"""
AI-Powered Video Analyzer
Detects the most engaging/replayed segments of YouTube videos using Gemini AI.
"""

import google.generativeai as genai
from django.conf import settings
import yt_dlp
import json
from ai_error_handler import handle_error, get_error_message


class VideoAnalyzer:
    """Analyze YouTube videos to find the best segments for Shorts."""
    
    def __init__(self):
        """Initialize the video analyzer."""
        self.gemini_available = bool(settings.GEMINI_API_KEY)
        if self.gemini_available:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_video(self, url):
        """
        Analyze a YouTube video to find the best segment for a Short.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            dict: Analysis results with suggested start/end times
        """
        try:
            # Get video metadata
            video_info = self._get_video_info(url)
            
            # Analyze engagement data
            best_segment = self._find_best_segment(video_info)
            
            # Get AI recommendations
            ai_analysis = self._get_ai_recommendations(video_info, best_segment)
            
            return {
                'success': True,
                'video_info': video_info,
                'suggested_segment': best_segment,
                'ai_analysis': ai_analysis,
                'auto_detected': True
            }
            
        except Exception as e:
            handle_error(e, context="Video Analysis", show_traceback=True)
            return {
                'success': False,
                'error': get_error_message(e, "Video Analysis"),
                'auto_detected': False
            }
    
    def _get_video_info(self, url):
        """
        Extract detailed video information from YouTube.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            dict: Video information
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'description': info.get('description', ''),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'comment_count': info.get('comment_count', 0),
                    'tags': info.get('tags', []),
                    'categories': info.get('categories', []),
                    'chapters': info.get('chapters', []),
                    'heatmap': info.get('heatmap', []),  # Most replayed data
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader', 'Unknown')
                }
        except Exception as e:
            raise Exception(f"Failed to fetch video information: {str(e)}")
    
    def _find_best_segment(self, video_info):
        """
        Find the most engaging segment based on heatmap and chapters.
        
        Args:
            video_info (dict): Video information
            
        Returns:
            dict: Best segment with start and end times
        """
        duration = video_info['duration']
        
        # Strategy 1: Use heatmap data (most replayed)
        if video_info.get('heatmap') and len(video_info['heatmap']) > 0:
            return self._analyze_heatmap(video_info['heatmap'], duration)
        
        # Strategy 2: Use chapters (if available)
        if video_info.get('chapters') and len(video_info['chapters']) > 0:
            return self._analyze_chapters(video_info['chapters'], duration)
        
        # Strategy 3: Smart default based on video length
        return self._get_smart_default(duration)
    
    def _analyze_heatmap(self, heatmap, duration):
        """
        Analyze YouTube heatmap to find most replayed segment.
        
        Args:
            heatmap (list): Heatmap data from YouTube
            duration (int): Video duration in seconds
            
        Returns:
            dict: Best segment
        """
        # Find the peak in the heatmap
        max_heat = 0
        peak_time = 0
        
        for point in heatmap:
            heat_value = point.get('value', 0)
            if heat_value > max_heat:
                max_heat = heat_value
                peak_time = point.get('start_time', 0)
        
        # Create 30-60 second segment around peak
        segment_duration = min(60, duration)  # Max 60 seconds for Shorts
        
        # Center the segment on the peak
        start_time = max(0, peak_time - segment_duration // 2)
        end_time = min(duration, start_time + segment_duration)
        
        # Adjust if end goes beyond duration
        if end_time >= duration:
            end_time = duration
            start_time = max(0, end_time - segment_duration)
        
        return {
            'start_time': int(start_time),
            'end_time': int(end_time),
            'method': 'heatmap',
            'confidence': 'high',
            'reason': f'Most replayed segment detected at {self._format_time(peak_time)}'
        }
    
    def _analyze_chapters(self, chapters, duration):
        """
        Analyze video chapters to find the best segment.
        
        Args:
            chapters (list): Chapter data
            duration (int): Video duration
            
        Returns:
            dict: Best segment
        """
        # Find the most interesting chapter based on title keywords
        interesting_keywords = [
            'highlight', 'best', 'amazing', 'epic', 'wow', 'incredible',
            'tutorial', 'how to', 'tip', 'trick', 'secret', 'reveal'
        ]
        
        best_chapter = None
        max_score = 0
        
        for chapter in chapters:
            title = chapter.get('title', '').lower()
            score = sum(1 for keyword in interesting_keywords if keyword in title)
            
            if score > max_score:
                max_score = score
                best_chapter = chapter
        
        # If no interesting chapter found, use the first one
        if not best_chapter and chapters:
            best_chapter = chapters[0]
        
        if best_chapter:
            start_time = best_chapter.get('start_time', 0)
            # Limit to 60 seconds for Shorts
            end_time = min(start_time + 60, duration)
            
            return {
                'start_time': int(start_time),
                'end_time': int(end_time),
                'method': 'chapters',
                'confidence': 'medium',
                'reason': f'Selected chapter: {best_chapter.get("title", "Unknown")}'
            }
        
        return self._get_smart_default(duration)
    
    def _get_smart_default(self, duration):
        """
        Get smart default segment when no heatmap or chapters available.
        
        Args:
            duration (int): Video duration
            
        Returns:
            dict: Default segment
        """
        # For short videos, take from beginning
        if duration <= 60:
            return {
                'start_time': 0,
                'end_time': int(duration),
                'method': 'default',
                'confidence': 'low',
                'reason': 'Video is already short enough'
            }
        
        # For longer videos, skip intro (first 10%) and take 30-60 seconds
        skip_intro = int(duration * 0.1)  # Skip first 10%
        segment_duration = min(45, duration - skip_intro)  # 45 second default
        
        start_time = skip_intro
        end_time = start_time + segment_duration
        
        return {
            'start_time': int(start_time),
            'end_time': int(end_time),
            'method': 'smart_default',
            'confidence': 'medium',
            'reason': 'Selected segment after intro with optimal length'
        }
    
    def _get_ai_recommendations(self, video_info, segment):
        """
        Get AI recommendations for the selected segment.
        
        Args:
            video_info (dict): Video information
            segment (dict): Selected segment
            
        Returns:
            dict: AI recommendations
        """
        if not self.gemini_available:
            return {
                'title': video_info['title'][:100],
                'description': f"#Shorts\n\nClip from: {video_info['title']}",
                'tags': ['Shorts', 'YouTubeShorts']
            }
        
        try:
            prompt = f"""
            You are creating a YouTube Short from this video:
            
            Original Title: {video_info['title']}
            Original Description: {video_info['description'][:500]}
            Video Duration: {video_info['duration']} seconds
            Selected Segment: {self._format_time(segment['start_time'])} to {self._format_time(segment['end_time'])}
            Reason: {segment['reason']}
            
            Generate:
            1. A catchy title for the Short (max 60 characters, engaging and clickable)
            2. A description with #Shorts tag and relevant context (2-3 sentences)
            3. 5 relevant hashtags (comma-separated)
            
            Format your response as:
            TITLE: [your title]
            DESCRIPTION: [your description]
            HASHTAGS: [hashtags]
            """
            
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Parse response
            title = ""
            description = ""
            hashtags = []
            
            for line in text.split('\n'):
                if line.startswith('TITLE:'):
                    title = line.replace('TITLE:', '').strip()[:100]
                elif line.startswith('DESCRIPTION:'):
                    description = line.replace('DESCRIPTION:', '').strip()
                elif line.startswith('HASHTAGS:'):
                    hashtag_text = line.replace('HASHTAGS:', '').strip()
                    hashtags = [tag.strip() for tag in hashtag_text.split(',')]
            
            # Ensure #Shorts is in description
            if '#Shorts' not in description and '#shorts' not in description:
                description = f"#Shorts\n\n{description}"
            
            return {
                'title': title or video_info['title'][:100],
                'description': description or f"#Shorts\n\nClip from: {video_info['title']}",
                'tags': hashtags or ['Shorts', 'YouTubeShorts'],
                'ai_generated': True
            }
            
        except Exception as e:
            print(f"AI recommendation failed: {e}")
            return {
                'title': video_info['title'][:100],
                'description': f"#Shorts\n\nClip from: {video_info['title']}",
                'tags': ['Shorts', 'YouTubeShorts'],
                'ai_generated': False
            }
    
    def _format_time(self, seconds):
        """
        Format seconds as MM:SS.
        
        Args:
            seconds (int): Time in seconds
            
        Returns:
            str: Formatted time
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"


# Example usage
if __name__ == "__main__":
    analyzer = VideoAnalyzer()
    
    # Test with a YouTube URL
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = analyzer.analyze_video(url)
    
    if result['success']:
        print(f"✅ Analysis successful!")
        print(f"Suggested segment: {result['suggested_segment']}")
        print(f"AI recommendations: {result['ai_analysis']}")
    else:
        print(f"❌ Analysis failed: {result['error']}")
