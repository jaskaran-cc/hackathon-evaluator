from agents.base_agent import create_agent
from utils.github_utils import fetch_github_content
from utils.github_utils import estimate_gemini_tokens

def evaluate_presentation(repo_url):
    repo_content = fetch_github_content(repo_url)
    rubric = """Evaluate clarity of README, visuals, and ease of understanding for end-users.
                Content to look for:

                README structure: Clear sections (Overview, Installation, Usage, Results).
                
                Visuals: Diagrams, screenshots, or charts explaining workflow.
                
                Code comments: Explanations of tricky logic or algorithms.
                
                Writing quality: Grammar, conciseness, clarity.
                Scoring Guidelines:
                | Score Range | Description                                                                                  |
                | ----------- | -------------------------------------------------------------------------------------------- |
                | 13–15       | Very clear, organized, concise presentation; visuals and explanations enhance understanding. |
                | 9–12        | Mostly clear; minor lapses in organization or clarity.                                       |
                | 5–8         | Somewhat unclear; difficult to follow in places.                                             |
                | 0–4         | Poorly communicated; confusing or incomplete.                                                |
                """
    agent = create_agent("Presentation & Communication", 15, rubric)
    estimate_gemini_tokens(repo_content)
    output = agent.run({"repo_content": repo_content})
    return output
