# PitchIQ Integration for Hackathon Evaluator

## Overview

The **Presentation Agent** has been enhanced with [**PitchIQ**](https://github.com/Bavalpreet/PitchIQ) - an AI-powered video presentation evaluation platform powered by Google Gemini 2.0.

## What's New

### Before
The presentation agent evaluated **GitHub repositories** (README, documentation, code structure).

### After
The presentation agent now evaluates **video presentations** using PitchIQ's advanced AI capabilities:

- 🎯 **15-Point Scoring System** across 5 criteria
- 🎤 **Multimodal Analysis** of audio and visual content
- 📊 **Detailed Feedback** on delivery, clarity, structure, and content
- 🤖 **Powered by Gemini 2.0 Flash** for accurate video understanding

## Setup

### 1. Clone PitchIQ

The presentation agent expects PitchIQ to be in the parent directory:

```bash
cd /path/to/hackathon
git clone https://github.com/Bavalpreet/PitchIQ.git
```

Your directory structure should look like:
```
hackathon/
├── hackathon-evaluator/
└── PitchIQ/
```

### 2. Install Dependencies

```bash
# Install PitchIQ dependencies
cd PitchIQ
pip install -r requirements.txt

# Install hackathon-evaluator dependencies
cd ../hackathon-evaluator
pip install -r requirements.txt
```

### 3. Configure Environment

Set up your Google Cloud credentials in a `.env` file:

```bash
# In hackathon-evaluator/.env
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
```

## Usage

### API Endpoint

The `/evaluate` endpoint now accepts a **video URL** for the presentation evaluation:

```python
import requests

response = requests.post("http://localhost:8000/evaluate", json={
    "repo_url": "https://github.com/username/hackathon-project",
    "video_url": "https://youtube.com/watch?v=YOUR_VIDEO_ID"
})

results = response.json()
```

### Updated Input Model

```python
class RepoRequest(BaseModel):
    repo_url: str           # GitHub repository URL
    video_url: str | None   # YouTube video URL for presentation evaluation
```

### Response Format

The presentation evaluation returns:

```json
{
  "category": "Presentation & Communication",
  "score": 12,
  "feedback": "Overall: Strong presentation with clear communication...\n\nBreakdown:\n- Clarity Communication: 2.5/3\n- Structure Organization: 2.5/3\n- Delivery Presentation: 2.0/3\n- Content Substance: 3.0/3\n- Visual Production: 2.0/3\n\nStrengths:\n✓ Excellent content depth\n✓ Clear articulation\n✓ Well-structured flow\n\nAreas for Improvement:\n→ Improve eye contact\n→ Add more visual aids\n→ Work on body language"
}
```

## How It Works

### 1. Video Analysis

When a video URL is provided, the presentation agent:
1. Downloads the video from YouTube
2. Sends it to Google Gemini 2.0 for multimodal analysis
3. Evaluates across 5 comprehensive criteria:
   - **Clarity & Communication** (0-3)
   - **Structure & Organization** (0-3)
   - **Delivery & Presentation Skills** (0-3)
   - **Content & Substance** (0-3)
   - **Visual Aids & Production** (0-3)

### 2. Scoring

- **Total Score**: 0-15 points (matches hackathon-evaluator scale)
- **Criteria Breakdown**: Individual scores for each criterion
- **Detailed Feedback**: Strengths, improvements, and recommendations

### 3. Integration

The presentation agent seamlessly integrates with the existing multi-agent system:

```python
agents = {
    "Innovation": evaluate_innovation,        # GitHub repo
    "Technical": evaluate_technical,          # GitHub repo
    "Feasibility": evaluate_feasibility,      # GitHub repo
    "Impact": evaluate_impact,                # GitHub repo
    "Presentation": evaluate_presentation,    # Video URL (PitchIQ)
}
```

## Benefits

### For Evaluators
- ✅ Objective video analysis
- ✅ Consistent scoring across submissions
- ✅ Detailed, actionable feedback
- ✅ Time-saving automation

### For Participants
- ✅ Comprehensive feedback on presentation skills
- ✅ Clear breakdown by criteria
- ✅ Specific improvement recommendations
- ✅ Fair, AI-powered evaluation

## Example Usage

### Complete Hackathon Evaluation

```python
# Evaluate a hackathon submission
result = orchestrate_evaluation(
    repo_url="https://github.com/team/awesome-project",
    video_url="https://youtube.com/watch?v=demo123"
)

print(f"Total Score: {result['total_score']}/75")
print(f"Presentation Score: {result['details']['Presentation']['score']}/15")
```

### Response

```json
{
  "repository": "https://github.com/team/awesome-project",
  "video": "https://youtube.com/watch?v=demo123",
  "total_score": 65,
  "details": {
    "Innovation": {"score": 12, "feedback": "..."},
    "Technical": {"score": 13, "feedback": "..."},
    "Feasibility": {"score": 11, "feedback": "..."},
    "Impact": {"score": 14, "feedback": "..."},
    "Presentation": {"score": 15, "feedback": "..."}
  }
}
```

## Technical Details

### Architecture

```
Hackathon Evaluator
    ↓
Presentation Agent
    ↓
PitchIQ Integration Layer
    ↓
PitchIQ.tools.presentationEvaluator
    ↓
YouTube Downloader (yt-dlp)
    ↓
Google Gemini 2.0 Flash (Multimodal)
    ↓
Structured JSON Response
```

### Error Handling

The agent gracefully handles errors:
- Invalid video URLs
- Download failures
- API errors
- Returns score of 0 with error message

### Performance

- **Video Processing**: 30-90 seconds (depends on video length)
- **Recommended Video Length**: 2-10 minutes
- **Supported Formats**: YouTube URLs, YouTube shorts

## Troubleshooting

### Issue: Module not found

**Solution**: Ensure PitchIQ is in the correct directory relative to hackathon-evaluator:

```bash
ls -la ../PitchIQ  # Should show the PitchIQ directory
```

### Issue: Google Cloud credentials

**Solution**: Set environment variables:

```bash
export GOOGLE_CLOUD_PROJECT=your_project_id
export GOOGLE_CLOUD_LOCATION=us-central1
```

### Issue: Video download fails

**Solution**: Install ffmpeg:

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg
```

## Future Enhancements

Potential improvements:
- [ ] Support for direct video file uploads
- [ ] Batch video evaluation
- [ ] Real-time streaming analysis
- [ ] Custom rubric support
- [ ] Multi-language support

## Credits

**PitchIQ** - AI-Powered Presentation Evaluation Platform
- Repository: https://github.com/Bavalpreet/PitchIQ
- Powered by: Google Gemini 2.0 Flash

## License

This integration maintains the licenses of both:
- hackathon-evaluator (original license)
- PitchIQ (original license)
