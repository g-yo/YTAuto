"""
Test script for the video processor module.
This allows you to test video downloading and cropping without running the full Django app.
"""

from video_processor import VideoProcessor
import sys


def test_basic_functionality():
    """Test basic video processing functionality."""
    print("=" * 60)
    print("YouTube Shorts Automation - Video Processor Test")
    print("=" * 60)
    
    # Initialize processor
    processor = VideoProcessor()
    print("\n✓ Video processor initialized")
    print(f"  Download directory: {processor.download_dir}")
    print(f"  Output directory: {processor.output_dir}")
    
    # Test time parsing
    print("\n📝 Testing time parsing...")
    test_times = ["0:30", "1:45", "01:30:45", "90"]
    for time_str in test_times:
        seconds = processor.parse_time(time_str)
        print(f"  '{time_str}' → {seconds} seconds")
    
    print("\n✓ Time parsing works correctly!")
    
    return processor


def test_download_and_crop():
    """Test downloading and cropping a video."""
    processor = VideoProcessor()
    
    print("\n" + "=" * 60)
    print("Video Download & Crop Test")
    print("=" * 60)
    
    # Get user input
    print("\nEnter a YouTube URL to test (or press Enter to skip):")
    url = input("> ").strip()
    
    if not url:
        print("\nSkipping video test. To test with a real video:")
        print("1. Run this script again")
        print("2. Provide a YouTube URL")
        print("3. Specify start and end times")
        return
    
    print("\nEnter start time (e.g., 0:10):")
    start_time = input("> ").strip() or "0:10"
    
    print("Enter end time (e.g., 0:40):")
    end_time = input("> ").strip() or "0:40"
    
    try:
        print(f"\n🎬 Processing video...")
        print(f"  URL: {url}")
        print(f"  Time range: {start_time} to {end_time}")
        
        result = processor.process_youtube_video(
            url=url,
            start_time=start_time,
            end_time=end_time,
            output_filename='test_short.mp4'
        )
        
        print("\n✅ SUCCESS!")
        print(f"  Original title: {result['original_title']}")
        print(f"  Output file: {result['output_path']}")
        print(f"  Duration: {result['duration']} seconds")
        
        # Cleanup
        print("\n🧹 Cleaning up downloaded files...")
        processor.cleanup(keep_outputs=True)
        print("✓ Cleanup complete (outputs preserved)")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if the YouTube URL is valid")
        print("2. Ensure FFmpeg is installed and in PATH")
        print("3. Check your internet connection")
        print("4. Try a different video")


def main():
    """Main test function."""
    print("\n🚀 Starting video processor tests...\n")
    
    # Test basic functionality
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"\n❌ Basic test failed: {e}")
        return
    
    # Ask if user wants to test download
    print("\n" + "=" * 60)
    print("Would you like to test video download and cropping?")
    print("This will download a real YouTube video.")
    print("=" * 60)
    print("\nOptions:")
    print("1. Yes - Test with a video")
    print("2. No - Skip video test")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_download_and_crop()
    else:
        print("\n✓ Skipping video test")
        print("\nTo test video processing:")
        print("1. Run the Django app: python manage.py runserver")
        print("2. Go to http://localhost:8000")
        print("3. Use the web interface to generate shorts")
    
    print("\n" + "=" * 60)
    print("✨ Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
