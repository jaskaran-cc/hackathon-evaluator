"""
Test script for PitchIQ integration with hackathon-evaluator
"""

import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the presentation agent
from agents.presentation_agent import evaluate_presentation

def test_presentation_agent():
    print("=" * 60)
    print("Testing PitchIQ Integration")
    print("=" * 60)
    print()
    
    # Test with a sample YouTube video URL
    # Replace with your actual test video URL
    test_video_url = input("Enter a YouTube video URL to test (or press Enter for demo): ").strip()
    
    if not test_video_url:
        print("\n⚠️  No video URL provided.")
        print("Please run the test again with a YouTube video URL.")
        return
    
    print(f"\n🎬 Testing with video: {test_video_url}")
    print("⏳ Evaluating presentation... (this may take 30-90 seconds)\n")
    
    try:
        result = evaluate_presentation(test_video_url)
        
        print("=" * 60)
        print("✅ EVALUATION RESULT")
        print("=" * 60)
        print()
        print(result)
        print()
        print("=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print("=" * 60)
        print("❌ ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        print("=" * 60)
        print("💡 Troubleshooting Tips:")
        print("=" * 60)
        print("1. Ensure PitchIQ is in the parent directory (../PitchIQ)")
        print("2. Check that all dependencies are installed:")
        print("   cd ../PitchIQ && pip install -r requirements.txt")
        print("3. Verify Google Cloud credentials are set:")
        print("   export GOOGLE_CLOUD_PROJECT=your_project_id")
        print("4. Make sure ffmpeg is installed (for video download)")
        print()

if __name__ == "__main__":
    test_presentation_agent()
