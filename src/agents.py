from crewai import Agent
from src.config import llm


def create_writer_agent() -> Agent:
    return Agent(
        role="Publication Writer",
        goal="Generate publication-ready text from a subject tip",
        backstory=(
            "You are a professional content writer for online publications. "
            "You write clear, engaging articles that directly address the subject. "
            "You produce publication-ready copy with no preamble or metadata."
        ),
        llm=llm,
        verbose=True,
    )
