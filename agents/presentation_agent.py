"""Presentation Agent - Powered by PitchIQ

Evaluates hackathon presentation videos using PitchIQ's AI-powered
presentation evaluation platform.
"""

import sys
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add PitchIQ to path
PITCHIQ_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../PitchIQ'))
if PITCHIQ_PATH not in sys.path:
    sys.path.insert(0, PITCHIQ_PATH)

from PitchIQ.tools.presentationEvaluator import evaluate_presentation_quick

def evaluate_presentation(video_url):
    """
    Evaluate a hackathon presentation video using PitchIQ.
    
    Args:
        video_url: YouTube URL of the presentation video
        
    Returns:
        JSON string with category, score, and feedback
    """
    try:
        # Use PitchIQ's presentation evaluator
        result = evaluate_presentation_quick(video_url)
        
        if not result.get("success"):
            return json.dumps({
                "category": "Presentation & Communication",
                "score": 0,
                "feedback": f"Failed to evaluate video: {result.get('error', 'Unknown error')}"
            })
        
        # Extract evaluation data
        evaluation = result.get("evaluation", {})
        structured_eval = evaluation.get("structured_evaluation", {})
        
        # Get total score (PitchIQ uses 0-15 scale, which matches!)
        total_score = structured_eval.get("total_score", 0)
        
        # Build comprehensive feedback
        feedback_parts = []
        
        # Add overall feedback
        overall = structured_eval.get("overall_feedback", "")
        if overall:
            feedback_parts.append(f"Overall: {overall}")
        
        # Add criteria breakdown
        criteria = structured_eval.get("criteria_scores", {})
        if criteria:
            feedback_parts.append("\nBreakdown:")
            for key, data in criteria.items():
                score = data.get("score", 0)
                criterion_name = key.replace("_", " ").title()
                feedback_parts.append(f"- {criterion_name}: {score}/3")
        
        # Add strengths
        strengths = structured_eval.get("strengths", [])
        if strengths:
            feedback_parts.append("\nStrengths:")
            for strength in strengths[:3]:  # Top 3
                feedback_parts.append(f"✓ {strength}")
        
        # Add improvement areas
        improvements = structured_eval.get("areas_for_improvement", [])
        if improvements:
            feedback_parts.append("\nAreas for Improvement:")
            for improvement in improvements[:3]:  # Top 3
                feedback_parts.append(f"→ {improvement}")
        
        # Format response
        response = {
            "category": "Presentation & Communication",
            "score": int(total_score),
            "feedback": " ".join(feedback_parts) if feedback_parts else "Evaluation completed."
        }
        
        return json.dumps(response)
        
    except Exception as e:
        return json.dumps({
            "category": "Presentation & Communication",
            "score": 0,
            "feedback": f"Error during evaluation: {str(e)}"
        })
