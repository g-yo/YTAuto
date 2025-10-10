"""
AI-Powered Error Handler with Gemini Explanations
Provides detailed, human-readable error messages and solutions.
"""

import google.generativeai as genai
from django.conf import settings
import traceback
import sys


class AIErrorHandler:
    """Handle errors with AI-generated explanations using Gemini."""
    
    def __init__(self):
        """Initialize the AI error handler."""
        self.gemini_available = bool(settings.GEMINI_API_KEY)
        if self.gemini_available:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
    
    def format_error(self, error, context=""):
        """
        Format error with bold text and AI explanation.
        
        Args:
            error: The exception object
            context: Additional context about where the error occurred
            
        Returns:
            dict: Formatted error information
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        # Get AI explanation
        explanation = self._get_ai_explanation(error_type, error_message, context)
        
        return {
            'error_type': error_type,
            'error_message': error_message,
            'explanation': explanation,
            'context': context,
            'traceback': traceback.format_exc()
        }
    
    def _get_ai_explanation(self, error_type, error_message, context):
        """
        Get AI-generated explanation for the error.
        
        Args:
            error_type: Type of error (e.g., FileNotFoundError)
            error_message: The error message
            context: Where the error occurred
            
        Returns:
            str: AI-generated explanation and fix suggestion
        """
        if not self.gemini_available:
            return self._get_fallback_explanation(error_type, error_message)
        
        try:
            prompt = f"""
            You are a helpful debugging assistant for a YouTube Shorts automation application.
            
            An error occurred:
            Error Type: {error_type}
            Error Message: {error_message}
            Context: {context}
            
            Provide a clear, concise explanation in 2-3 sentences that:
            1. Explains what went wrong in simple terms
            2. Suggests a specific fix or solution
            3. Is helpful for someone who may not be a developer
            
            Format: Just the explanation, no extra formatting or labels.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"AI explanation failed: {e}")
            return self._get_fallback_explanation(error_type, error_message)
    
    def _get_fallback_explanation(self, error_type, error_message):
        """
        Provide fallback explanations when AI is unavailable.
        
        Args:
            error_type: Type of error
            error_message: The error message
            
        Returns:
            str: Fallback explanation
        """
        explanations = {
            'FileNotFoundError': 'The system could not locate the required file. Check if the file path is correct and the file exists.',
            'PermissionError': 'The application does not have permission to access this file or directory. Check file permissions.',
            'ValueError': 'Invalid input value provided. Check that all inputs are in the correct format.',
            'ConnectionError': 'Could not connect to the required service. Check your internet connection.',
            'TimeoutError': 'The operation took too long to complete. Try again or check your internet speed.',
            'KeyError': 'Required configuration or data is missing. Check your settings.',
            'ImportError': 'Required Python package is not installed. Run: pip install -r requirements.txt',
            'AttributeError': 'Trying to access a property that does not exist. This may be a code issue.',
            'TypeError': 'Wrong data type provided. Check that inputs match expected types.',
            'OSError': 'Operating system error occurred. Check system resources and permissions.',
        }
        
        base_explanation = explanations.get(
            error_type,
            f'An unexpected {error_type} occurred. Check the error message for details.'
        )
        
        return f"{base_explanation} Error details: {error_message}"
    
    def print_error(self, error, context="", show_traceback=False):
        """
        Print formatted error to console.
        
        Args:
            error: The exception object
            context: Additional context
            show_traceback: Whether to show full traceback
        """
        error_info = self.format_error(error, context)
        
        print("\n" + "=" * 80)
        print(f"❌ ERROR: {error_info['error_type']}")
        print("=" * 80)
        print(f"\n📝 Message: {error_info['error_message']}")
        
        if context:
            print(f"\n📍 Context: {context}")
        
        print(f"\n🤖 AI Explanation:")
        print(f"   {error_info['explanation']}")
        
        if show_traceback:
            print(f"\n📋 Traceback:")
            print(error_info['traceback'])
        
        print("\n" + "=" * 80 + "\n")
    
    def get_user_friendly_message(self, error, context=""):
        """
        Get a user-friendly error message for display in UI.
        
        Args:
            error: The exception object
            context: Additional context
            
        Returns:
            str: User-friendly error message
        """
        error_info = self.format_error(error, context)
        return f"❌ {error_info['error_type']}: {error_info['explanation']}"


# Global error handler instance
error_handler = AIErrorHandler()


def handle_error(error, context="", show_traceback=False):
    """
    Convenience function to handle errors.
    
    Args:
        error: The exception object
        context: Additional context
        show_traceback: Whether to show full traceback
    """
    error_handler.print_error(error, context, show_traceback)


def get_error_message(error, context=""):
    """
    Get user-friendly error message.
    
    Args:
        error: The exception object
        context: Additional context
        
    Returns:
        str: User-friendly error message
    """
    return error_handler.get_user_friendly_message(error, context)


# Example usage
if __name__ == "__main__":
    # Test the error handler
    try:
        # Simulate an error
        open('nonexistent_file.txt', 'r')
    except Exception as e:
        handle_error(e, context="Testing file operations", show_traceback=True)
