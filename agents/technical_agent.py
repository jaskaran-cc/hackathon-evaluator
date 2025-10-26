from agents.base_agent import create_agent
from utils.github_utils import fetch_github_content
from utils.github_utils import estimate_gemini_tokens

def evaluate_technical(repo_url):
    repo_content = fetch_github_content(repo_url)
    rubric = """Assess algorithmic depth, documentation, architecture, and coding best practices.
                Content to look for:

                Python code quality: PEP8 compliance, readable variable names, modularity.
                
                Implementation correctness: Does code logically follow the proposed approach?
                
                Dependencies: Appropriate libraries and clean setup (requirements.txt, environment.yml).
                
                Error handling & testing: Are there tests or exception handling?
                
                Scoring Guidelines:
                
                | Score Range | Description                                                                                                          |
                | ----------- | -------------------------------------------------------------------------------------------------------------------- |
                | 21–25       | Code is **well-structured, efficient, readable**, follows best practices, includes documentation and error handling. |
                | 16–20       | Code works correctly, readable, minor issues with structure or efficiency.                                           |
                | 11–15       | Code functions but has **noticeable readability, style, or structural issues**.                                      |
                | 6–10        | Code has major issues; partially works or is hard to read.                                                           |
                | 0–5         | Code does not work or is unstructured and unreadable.                                                                |

                """
    agent = create_agent("Technical Depth & Code Quality", 25, rubric)
    estimate_gemini_tokens(repo_content)
    output = agent.run({"repo_content": repo_content})
    return output
