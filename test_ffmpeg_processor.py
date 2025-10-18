"""
Quick test to verify FFmpeg-based video processing works
"""
from video_processor import VideoProcessor
from pathlib import Path

def test_ffmpeg_processing():
    """Test the new FFmpeg-based video processor"""
    
    print("🧪 Testing FFmpeg Video Processor\n")
    
    # Initialize processor
    processor = VideoProcessor()
    
    # Test URL (short video for quick testing)
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video
    
    print(f"📥 Downloading test video: {test_url}")
    
    try:
        # Test the complete workflow
        result = processor.process_youtube_video(
            url=test_url,
            start_time="0:00",
            end_time="0:10",  # Just 10 seconds for quick test
            output_filename='test_short.mp4',
            make_shorts_format=True
        )
        
        print("\n✅ SUCCESS!")
        print(f"   Output: {result['output_path']}")
        print(f"   Title: {result['original_title']}")
        print(f"   Duration: {result['duration']}s")
        
        # Check if file exists
        output_file = Path(result['output_path'])
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"   File size: {size_mb:.2f} MB")
            print("\n🎉 FFmpeg processing is working correctly!")
        else:
            print("\n⚠️  Output file not found!")
        
        # Cleanup
        processor.cleanup(keep_outputs=False)
        print("\n🧹 Cleaned up test files")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ffmpeg_processing()
