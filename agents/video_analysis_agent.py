"""
Video Analysis Agent - Powered by PitchIQ Core Logic

Evaluates hackathon presentation videos using AI-powered multimodal analysis.
Core evaluation logic embedded from PitchIQ platform.
"""

import os
import json
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Cloud imports
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# YouTube downloader
import yt_dlp


def _download_video_internal(url, output_path="downloads"):
    """
    Internal function to download a YouTube video as MP4.
    Embedded from PitchIQ's youtubeDownloader.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the downloaded video
    
    Returns:
        tuple: (success: bool, video_path: str, error: str)
    """
    os.makedirs(output_path, exist_ok=True)
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            print(f"\rDownloading: {percent}", end='')
        elif d['status'] == 'finished':
            print(f"\nProcessing video...")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': False,
        'progress_hooks': [progress_hook],
    }
    
    try:
        print(f"Downloading video from: {url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown')
            print(f"Video: {video_title}")
            
            ydl.download([url])
            video_path = ydl.prepare_filename(info)
            
        print(f"\n✓ Download complete!")
        return True, video_path, None
        
    except Exception as e:
        error_msg = f"Error downloading video: {str(e)}"
        print(f"\n✗ {error_msg}")
        return False, None, error_msg


def _evaluate_with_gemini(video_path):
    """
    Evaluate presentation using Gemini multimodal model.
    Embedded from PitchIQ's presentationEvaluator.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        tuple: (success: bool, evaluation_result: dict, error: str)
    """
    try:
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
        
        if not project_id:
            return False, None, "GOOGLE_CLOUD_PROJECT environment variable not set"
        
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel("gemini-2.0-flash-exp")
        
        with open(video_path, 'rb') as f:
            video_data = f.read()
        
        video_part = Part.from_data(data=video_data, mime_type="video/mp4")
        
        evaluation_prompt = """Evaluate this presentation video and provide a detailed assessment with scores.

SCORING RUBRIC (Total: 15 points):

1. CLARITY & COMMUNICATION (0-3 points)
   - Voice clarity and articulation
   - Pace and rhythm of speech
   - Audio quality
   - Language proficiency

2. STRUCTURE & ORGANIZATION (0-3 points)
   - Logical flow and structure
   - Introduction, body, conclusion
   - Time management
   - Smooth transitions

3. DELIVERY & PRESENTATION SKILLS (0-3 points)
   - Confidence and presence
   - Eye contact and body language
   - Enthusiasm and engagement
   - Professional appearance

4. CONTENT & SUBSTANCE (0-3 points)
   - Depth of content
   - Relevance and accuracy
   - Problem-solution clarity
   - Innovation and creativity

5. VISUAL AIDS & PRODUCTION (0-3 points)
   - Slide quality and design
   - Visual demonstrations
   - Video production quality
   - Use of supporting materials

EVALUATION FORMAT - Return ONLY valid JSON:

{
    "total_score": [0-15],
    "criteria_scores": {
        "clarity_communication": {
            "score": [0-3],
            "feedback": "Detailed feedback"
        },
        "structure_organization": {
            "score": [0-3],
            "feedback": "Detailed feedback"
        },
        "delivery_presentation": {
            "score": [0-3],
            "feedback": "Detailed feedback"
        },
        "content_substance": {
            "score": [0-3],
            "feedback": "Detailed feedback"
        },
        "visual_production": {
            "score": [0-3],
            "feedback": "Detailed feedback"
        }
    },
    "strengths": ["List 3-5 key strengths"],
    "areas_for_improvement": ["List 3-5 areas for improvement"],
    "overall_feedback": "Comprehensive summary",
    "recommendations": ["Specific actionable recommendations"]
}

Be objective and thorough. Provide specific examples from the video."""
        
        response = model.generate_content([video_part, evaluation_prompt])
        response_text = response.text
        
        evaluation_result = {
            "raw_evaluation": response_text,
            "model_used": "gemini-2.0-flash-exp"
        }
        
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                parsed_eval = json.loads(json_str)
                evaluation_result["structured_evaluation"] = parsed_eval
        except json.JSONDecodeError:
            pass
        
        return True, evaluation_result, None
        
    except Exception as e:
        return False, None, str(e)


def evaluate_video_presentation(video_url):
    """
    Evaluate a hackathon presentation video.
    Main function called by the orchestrator.
    
    Args:
        video_url: YouTube URL of the presentation video
        
    Returns:
        JSON string with category, score, and feedback
    """
    temp_video_path = None
    temp_dir = None
    
    try:
        print(f"\n🎬 Video Analysis Agent: Processing {video_url}")
        
        # Download video
        temp_dir = tempfile.mkdtemp()
        success, video_path, error = _download_video_internal(video_url, temp_dir)
        
        if not success:
            return json.dumps({
                "category": "Video Presentation Analysis",
                "score": 0,
                "feedback": f"Failed to download video: {error}"
            })
        
        temp_video_path = video_path
        video_size = os.path.getsize(temp_video_path)
        video_size_mb = video_size / (1024 * 1024)
        
        print(f"Analyzing video: {video_size_mb:.2f} MB")
        
        # Evaluate with Gemini
        success, evaluation, error = _evaluate_with_gemini(temp_video_path)
        
        if not success:
            return json.dumps({
                "category": "Video Presentation Analysis",
                "score": 0,
                "feedback": f"Video evaluation failed: {error}"
            })
        
        # Extract structured data
        structured_eval = evaluation.get("structured_evaluation", {})
        total_score = structured_eval.get("total_score", 0)
        
        # Build feedback
        feedback_parts = []
        
        overall = structured_eval.get("overall_feedback", "")
        if overall:
            feedback_parts.append(f"Overall: {overall}")
        
        criteria = structured_eval.get("criteria_scores", {})
        if criteria:
            feedback_parts.append("\n\nBreakdown:")
            for key, data in criteria.items():
                score = data.get("score", 0)
                criterion_name = key.replace("_", " ").title()
                feedback_parts.append(f"• {criterion_name}: {score}/3")
        
        strengths = structured_eval.get("strengths", [])
        if strengths:
            feedback_parts.append("\n\nStrengths:")
            for strength in strengths[:3]:
                feedback_parts.append(f"✓ {strength}")
        
        improvements = structured_eval.get("areas_for_improvement", [])
        if improvements:
            feedback_parts.append("\n\nAreas for Improvement:")
            for improvement in improvements[:3]:
                feedback_parts.append(f"→ {improvement}")
        
        response = {
            "category": "Video Presentation Analysis",
            "score": int(total_score),
            "feedback": " ".join(feedback_parts) if feedback_parts else "Evaluation completed."
        }
        
        return json.dumps(response)
        
    except Exception as e:
        return json.dumps({
            "category": "Video Presentation Analysis",
            "score": 0,
            "feedback": f"Error during evaluation: {str(e)}"
        })
    
    finally:
        # Cleanup
        if temp_video_path and os.path.exists(temp_video_path):
            try:
                os.remove(temp_video_path)
                if temp_dir and os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
            except Exception as e:
                print(f"Warning: Could not cleanup temp file: {e}")
