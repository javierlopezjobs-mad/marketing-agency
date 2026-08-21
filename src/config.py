import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

model = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")
api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
base_url = os.getenv("LLM_BASE_URL")
temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))

if not api_key and not base_url and not model.startswith("ollama/"):
    raise ValueError("LLM_API_KEY not set")

llm = LLM(
    model=model,
    temperature=temperature,
    api_key=api_key,
    base_url=base_url,
)
