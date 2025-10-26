from agents.base_agent import create_agent
from utils.github_utils import fetch_github_content
from utils.github_utils import estimate_gemini_tokens

def evaluate_feasibility(repo_url):
    repo_content = fetch_github_content(repo_url)
    rubric = """Assess if the project is functional, complete, and deployable.
                Content to look for:

                Working prototype: Does the code run without major errors?
                
                Scope coverage: Are all parts of the problem addressed?
                
                Data availability: Are datasets included or clearly referenced?
                
                Instructions: Clear setup instructions in README.
                Scoring Guidelines:
                | Score Range | Description                                                                                |
                | ----------- | ------------------------------------------------------------------------------------------ |
                | 16–20       | Solution is fully implementable, all features are complete, and constraints are addressed. |
                | 11–15       | Mostly feasible; minor gaps or missing features.                                           |
                | 6–10        | Partially feasible; multiple features incomplete or unrealistic.                           |
                | 0–5         | Not feasible; major features missing or impractical.                                       |
                """
    agent = create_agent("Feasibility & Completeness", 20, rubric)
    estimate_gemini_tokens(repo_content)
    output = agent.run({"repo_content": repo_content})
    return output
