"""
AI-powered title and hashtag generation using Google Gemini API.
"""

import google.generativeai as genai
from django.conf import settings


def generate_title_and_hashtags(original_title):
    """
    Generate a catchy title and relevant hashtags for a YouTube Short.
    
    Args:
        original_title (str): The original video title
        
    Returns:
        dict: {'title': str, 'hashtags': str}
    """
    if not settings.GEMINI_API_KEY:
        # Return default values if no API key
        return {
            'title': f"Short: {original_title[:50]}",
            'hashtags': "#YouTubeShorts #Shorts #Viral"
        }
    
    try:
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # Create prompt
        prompt = f"""
        Based on this YouTube video title: "{original_title}"
        
        Generate:
        1. A short, catchy title (max 60 characters) suitable for a YouTube Short
        2. 5 relevant hashtags
        
        Format your response EXACTLY like this:
        TITLE: [your generated title]
        HASHTAGS: #tag1 #tag2 #tag3 #tag4 #tag5
        """
        
        # Generate content
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Parse response
        lines = text.split('\n')
        title = ""
        hashtags = ""
        
        for line in lines:
            if line.startswith('TITLE:'):
                title = line.replace('TITLE:', '').strip()
            elif line.startswith('HASHTAGS:'):
                hashtags = line.replace('HASHTAGS:', '').strip()
        
        # Fallback if parsing fails
        if not title:
            title = f"Short: {original_title[:50]}"
        if not hashtags:
            hashtags = "#YouTubeShorts #Shorts #Viral"
        
        return {
            'title': title[:100],  # Ensure it's not too long
            'hashtags': hashtags
        }
        
    except Exception as e:
        print(f"Error generating AI content: {e}")
        return {
            'title': f"Short: {original_title[:50]}",
            'hashtags': "#YouTubeShorts #Shorts #Viral"
        }


# Test function
if __name__ == "__main__":
    # Example usage
    test_title = "How to Build Amazing Web Applications with Python Django"
    result = generate_title_and_hashtags(test_title)
    print(f"Generated Title: {result['title']}")
    print(f"Generated Hashtags: {result['hashtags']}")
