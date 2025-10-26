# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import json
import time

# Import your evaluation agents
from agents.innovation_agent import evaluate_innovation
from agents.technical_agent import evaluate_technical
from agents.feasibility_agent import evaluate_feasibility
from agents.impact_agent import evaluate_impact
from agents.presentation_agent import evaluate_presentation
from agents.video_analysis_agent import evaluate_video_presentation
# top of your script (before any ChatGoogleGenerativeAI() calls)
app = FastAPI(title="Hackathon Repo Evaluation API")

# Input model
class RepoRequest(BaseModel):
    repo_url: str
    video_url: str | None = None  # Optional YouTube video URL for presentation analysis

# Multi-agent orchestrator
def orchestrate_evaluation(repo_url: str, video_url: str | None = None):
    print(f">Starting multi-agent evaluation for: {repo_url}\n")
    if video_url:
        print(f" Video URL provided: {video_url}\n")
    
    results = {}
    total_score = 0

    agents = {
        "Innovation": evaluate_innovation,
        "Technical": evaluate_technical,
        "Feasibility": evaluate_feasibility,
        "Impact": evaluate_impact,
        "Presentation": evaluate_presentation,
    }
    
    # Add video analysis agent if video URL is provided
    if video_url:
        agents["Video Presentation"] = lambda url: evaluate_video_presentation(video_url)

    for name, func in agents.items():
        print(f"🤖 Evaluating {name}...")
        try:
            res = func(repo_url)
            clean_str = res.strip().lstrip("```json").rstrip("```").strip()
            data = json.loads(clean_str)
            time.sleep(5)  # optional: adjust delay to prevent rate limiting
        except Exception as e:
            data = {"category": name, "score": 0, "feedback": str(e)}

        results[name] = data
        total_score += data.get("score", 0)

    report = {"repository": repo_url, "total_score": total_score, "details": results}
    print("\n✅ Evaluation complete!\n")
    return report

# API endpoint
@app.post("/evaluate")
def evaluate_repo(request: RepoRequest):
    try:
        report = orchestrate_evaluation(request.repo_url, request.video_url)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For direct testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
