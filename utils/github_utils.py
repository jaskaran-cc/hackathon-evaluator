import requests
import tiktoken
import requests


def estimate_gemini_tokens(text: str) -> int:
    """
    Estimate token count for Gemini model (approximation using tiktoken).
    """
    # Gemini uses BPE tokenizer similar to OpenAI
    encoding = tiktoken.get_encoding("cl100k_base")  # Recommended default for Gemini
    tokens = encoding.encode(text)
    print(f"Token count for prompt: {len(tokens)}")

# Example

def fetch_github_content(repo_url):
    """
    Fetch README + top Python files content from a public GitHub repo.

    Args:
        repo_url (str): GitHub repo URL (https://github.com/<owner>/<repo>)
        max_files (int): Max number of Python files to fetch
        max_chars (int): Max characters per file to include
    Returns:
        str: Combined string of README + code snippets
    """
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        GITHUB_TOKEN = os.getenv("PAT")
        headers = {
            "Accept": "application/vnd.github.v3.raw",
            "Authorization": f"token {GITHUB_TOKEN}"
        }
        parts = repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]
        base_api = f"https://api.github.com/repos/{owner}/{repo}"

        # Fetch README
        readme_resp = requests.get(f"{base_api}/readme", headers=headers)
        readme_text = readme_resp.text if readme_resp.status_code == 200 else "README not found"

        # Fetch file tree
        tree_resp = requests.get(f"{base_api}/git/trees/main?recursive=1", headers=headers)
        tree_json = tree_resp.json() if tree_resp.status_code == 200 else {}

        # Define allowed file types for evaluation
        allowed_extensions = (".py", ".ipynb", ".md", ".json", ".yaml", ".yml", ".txt")

        # Filter relevant files
        eval_files = [
            item["path"]
            for item in tree_json.get("tree", [])
            if item["type"] == "blob" and item["path"].endswith(allowed_extensions)
        ]

        # Fetch content of Python files
        code_snippets = []
        for path in eval_files:
            file_resp = requests.get(f"{base_api}/contents/{path}", headers=headers)
            if file_resp.status_code == 200:
                code_content = file_resp.text  # truncate large files
                code_snippets.append(f"# File: {path}\n{code_content}\n")
            else:
                code_snippets.append(f"# File: {path} could not be fetched\n")

        combined_content = f"README:\n{readme_text}\n\nPython Code Snippets:\n" + "\n".join(code_snippets)
        return combined_content

    except Exception as e:
        return f"Error fetching repo: {str(e)}"
