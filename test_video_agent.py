"""
Test script for Video Analysis Agent
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.video_analysis_agent import evaluate_video_presentation

def test_video_agent():
    print("=" * 60)
    print("Testing Video Analysis Agent")
    print("=" * 60)
    print()
    
    test_video_url = input("Enter a YouTube video URL to test: ").strip()
    
    if not test_video_url:
        print("\n⚠️  No video URL provided.")
        return
    
    print(f"\n🎬 Testing with video: {test_video_url}")
    print("⏳ This may take 30-90 seconds...\n")
    
    try:
        result = evaluate_video_presentation(test_video_url)
        
        print("\n" + "=" * 60)
        print("✅ EVALUATION RESULT")
        print("=" * 60)
        print()
        print(result)
        print()
        print("=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        print()
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_video_agent()
