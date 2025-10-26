from agents.base_agent import create_agent
from utils.github_utils import fetch_github_content
from utils.github_utils import estimate_gemini_tokens

def evaluate_impact(repo_url):
    repo_content = fetch_github_content(repo_url)
    rubric = """Evaluate societal or business impact, target audience, and scalability.
                Content to look for:

                Practical applicability: Who benefits from this solution?
                
                Data/Model scalability: Can it handle larger datasets?
                
                Extendibility: Can others build upon it?
                
                Future potential: Does it open opportunities for improvement?
                Scoring Guidelines:
                | Score Range | Description                                                                             |
                | ----------- | --------------------------------------------------------------------------------------- |
                | 13–15       | Solution has high potential impact, can scale effectively, and can be deployed broadly. |
                | 9–12        | Moderate impact; some scalability limitations.                                          |
                | 5–8         | Limited impact or scalability.                                                          |
                | 0–4         | No clear impact or scalability.                                                         |
                """
    agent = create_agent("Impact & Scalability", 15, rubric)
    estimate_gemini_tokens(repo_content)
    output = agent.run({"repo_content": repo_content})
    return output
