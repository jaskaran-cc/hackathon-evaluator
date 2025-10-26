from agents.base_agent import create_agent
from utils.github_utils import fetch_github_content
from utils.github_utils import estimate_gemini_tokens

def evaluate_innovation(repo_url):
    repo_content = fetch_github_content(repo_url)
    rubric = """How novel, creative, and well-understood the problem statement is.
                Content to look for:
                README clarity: Does it describe the problem clearly?
                
                Problem statement: Is the problem real-world, challenging, and relevant?
                
                Approach novelty: Are they using creative methods or standard solutions?
                
                Differentiation: How is this solution different from existing solutions?
                
                Scoring Guidelines:
                | Score Range | Description                                                                                                                    |
                | ----------- | ------------------------------------------------------------------------------------------------------------------------------ |
                | 21–25       | Submission demonstrates a **novel solution**, deep understanding of the problem, and clearly identifies the need it addresses. |
                | 16–20       | Solution shows some originality, understands the problem, but novelty is limited.                                              |
                | 11–15       | Basic understanding of the problem, limited or incremental innovation.                                                         |
                | 6–10        | Minimal understanding; solution is mostly generic or obvious.                                                                  |
                | 0–5         | No clear understanding or innovation present.                                                                                  |

                """
    agent = create_agent("Innovation & Problem Understanding", 25, rubric)
    estimate_gemini_tokens(repo_content)
    output = agent.run({"repo_content": repo_content})
    return output
