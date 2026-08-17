import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set")

llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.7,
    api_key=api_key,
)
