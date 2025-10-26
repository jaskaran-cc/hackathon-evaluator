# Video Analysis Agent

## Overview

The **Video Analysis Agent** is a new evaluation agent that analyzes hackathon presentation videos using AI-powered multimodal analysis. It provides comprehensive scoring out of 15 points with detailed feedback.

## Features

- 🎬 **YouTube Video Analysis**: Automatically downloads and analyzes presentation videos
- 🤖 **AI-Powered Evaluation**: Uses Google Gemini 2.0 Flash for multimodal understanding
- 📊 **15-Point Scoring System**: Evaluates across 5 comprehensive criteria
- 💡 **Detailed Feedback**: Provides strengths, improvements, and recommendations
- 🔄 **Seamless Integration**: Works with existing multi-agent orchestrator

## Scoring Criteria

The agent evaluates presentations across 5 criteria (total 15 points):

1. **Clarity & Communication** (0-3 points)
   - Voice clarity and articulation
   - Pace and rhythm
   - Audio quality
   - Language proficiency

2. **Structure & Organization** (0-3 points)
   - Logical flow and structure
   - Introduction, body, conclusion
   - Time management
   - Smooth transitions

3. **Delivery & Presentation Skills** (0-3 points)
   - Confidence and presence
   - Eye contact and body language
   - Enthusiasm and engagement
   - Professional appearance

4. **Content & Substance** (0-3 points)
   - Depth of content
   - Relevance and accuracy
   - Problem-solution clarity
   - Innovation and creativity

5. **Visual Aids & Production** (0-3 points)
   - Slide quality and design
   - Visual demonstrations
   - Video production quality
   - Supporting materials

## Setup

### 1. Install Dependencies

The agent uses embedded logic from PitchIQ, no external dependencies needed:

```bash
pip install yt-dlp google-cloud-aiplatform python-dotenv
```

### 2. Configure Environment

Create or update `.env` file:

```bash
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
```

### 3. Authentication

Set up Google Cloud authentication:

```bash
# Option 1: Application Default Credentials
gcloud auth application-default login

# Option 2: Service Account JSON
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## Usage

### API Endpoint

The `/evaluate` endpoint now accepts an optional `video_url` parameter:

```python
import requests

response = requests.post("http://localhost:8000/evaluate", json={
    "repo_url": "https://github.com/team/project",
    "video_url": "https://youtube.com/watch?v=VIDEO_ID"  # Optional
})

result = response.json()
```

### Request Format

```json
{
  "repo_url": "https://github.com/team/hackathon-project",
  "video_url": "https://youtube.com/watch?v=fpZ5U_YrCDM"
}
```

### Response Format

```json
{
  "repository": "https://github.com/team/hackathon-project",
  "video": "https://youtube.com/watch?v=fpZ5U_YrCDM",
  "total_score": 78,
  "details": {
    "Innovation": {"score": 20, "feedback": "..."},
    "Technical": {"score": 18, "feedback": "..."},
    "Feasibility": {"score": 16, "feedback": "..."},
    "Impact": {"score": 12, "feedback": "..."},
    "Presentation": {"score": 10, "feedback": "..."},
    "Video Presentation": {
      "score": 12,
      "feedback": "Overall: Strong presentation...\n\nBreakdown:\n• Clarity Communication: 2.5/3\n• Structure Organization: 2.5/3\n• Delivery Presentation: 2.0/3\n• Content Substance: 3.0/3\n• Visual Production: 2.0/3\n\nStrengths:\n✓ Excellent content depth\n✓ Clear articulation\n✓ Well-structured flow\n\nAreas for Improvement:\n→ Improve eye contact\n→ Add more visual aids"
    }
  }
}
```

## Testing

### Standalone Test

Test the video analysis agent directly:

```bash
python test_video_agent.py
```

### Full Integration Test

Test with the complete API:

```bash
# Start the API server
python app.py

# In another terminal, test the endpoint
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/team/project",
    "video_url": "https://youtube.com/watch?v=VIDEO_ID"
  }'
```

## Architecture

### Core Components

1. **Video Downloader** (`_download_video_internal`)
   - Downloads YouTube videos using yt-dlp
   - Progress tracking and error handling
   - Embedded from PitchIQ's youtubeDownloader

2. **AI Evaluator** (`_evaluate_with_gemini`)
   - Multimodal analysis with Gemini 2.0 Flash
   - Structured JSON response parsing
   - Embedded from PitchIQ's presentationEvaluator

3. **Main Function** (`evaluate_video_presentation`)
   - Orchestrates download and evaluation
   - Formats feedback for hackathon-evaluator
   - Returns standardized JSON response

### Data Flow

```
YouTube URL
    ↓
Download Video (yt-dlp)
    ↓
Upload to Gemini 2.0 Flash
    ↓
AI Multimodal Analysis
    ↓
Structured JSON Response
    ↓
Format for Orchestrator
    ↓
Return Score & Feedback
```

## Technical Details

### Performance

- **Video Download**: 5-30 seconds (depends on video size)
- **AI Analysis**: 30-90 seconds (depends on video length)
- **Total Time**: ~60-120 seconds per video

### Supported Formats

- YouTube URLs (youtube.com/watch?v=...)
- YouTube Shorts (youtube.com/shorts/...)
- YouTube short URLs (youtu.be/...)

### Limitations

- Maximum video length: ~10 minutes (recommended)
- File size limit: Depends on Gemini API limits
- Requires valid Google Cloud credentials

## Error Handling

The agent gracefully handles errors:

- **Download Failures**: Returns score of 0 with error message
- **API Errors**: Catches and reports Gemini API issues
- **Invalid URLs**: Validates and reports URL problems
- **Missing Credentials**: Clear error messages for auth issues

## Benefits

### For Evaluators
- ✅ Objective, consistent video analysis
- ✅ Detailed feedback across multiple criteria
- ✅ Time-saving automation
- ✅ Standardized scoring

### For Participants
- ✅ Comprehensive presentation feedback
- ✅ Specific improvement recommendations
- ✅ Fair AI-powered evaluation
- ✅ Actionable insights

## Powered By

This agent embeds core logic from **[PitchIQ](https://github.com/Bavalpreet/PitchIQ)** - an AI-powered presentation evaluation platform.

- Repository: https://github.com/Bavalpreet/PitchIQ
- Technology: Google Gemini 2.0 Flash (Multimodal AI)
- License: Compatible with hackathon-evaluator

## Future Enhancements

Potential improvements:
- [ ] Support for direct video file uploads
- [ ] Batch video processing
- [ ] Custom evaluation rubrics
- [ ] Multi-language support
- [ ] Timestamp-based analysis
- [ ] Comparative scoring across submissions

## Troubleshooting

### Issue: "GOOGLE_CLOUD_PROJECT environment variable not set"

**Solution**: Set environment variables:
```bash
export GOOGLE_CLOUD_PROJECT=your_project_id
export GOOGLE_CLOUD_LOCATION=us-central1
```

### Issue: "Your default credentials were not found"

**Solution**: Authenticate with Google Cloud:
```bash
gcloud auth application-default login
```

### Issue: Video download fails

**Solution**: Install ffmpeg for best quality:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

## Contributing

The video analysis agent follows the same pattern as other agents in this repository. To contribute:

1. Fork the repository
2. Create a feature branch
3. Test your changes with `test_video_agent.py`
4. Submit a pull request

## License

This agent maintains compatibility with the hackathon-evaluator license and embeds logic from PitchIQ (MIT License compatible).
