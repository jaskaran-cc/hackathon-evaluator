import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import Callbacks
from langchain_google_genai import ChatGoogleGenerativeAI

# Create a tiny dummy BaseCache class so Pydantic finds it.
# This is harmless — you are not enabling any cache behavior.
class _DummyBaseCache:
    pass

# Attach it and rebuild the model
ChatGoogleGenerativeAI.BaseCache = _DummyBaseCache
ChatGoogleGenerativeAI.model_rebuild()
def get_llm():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GOOGLE_API_KEY environment variable.")
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.0)


def create_agent(category_name, weight, rubric_desc):
    prompt = ChatPromptTemplate.from_template("""
        You are an expert hackathon evaluator responsible for the category: **{category_name}**
        
        Evaluate ONLY this category for the provided GitHub repository content.
        
        Criteria Description:
        {rubric_desc}
        
        Return ONLY valid JSON, nothing else, like this:
        
            {{
              "category": "<category_name>",
              "score": <integer between 0 and max_weight>,
              "feedback": "<your brief feedback with code citations>"
            }}
            
            Must follow Notes: 
            1. Do NOT include any extra text, explanation
            2. Don't return in markdown format
            3. Valid json so that json.loads work
        
        Repository content:
        {repo_content}
        """.replace('{category_name}',category_name).replace('{rubric_desc}',rubric_desc).replace('{weight}',str(weight)))

    return LLMChain(llm=get_llm(), prompt=prompt)
