from crewai import Crew, Process
from src.agents import create_writer_agent
from src.tasks import create_writing_task


class PostPublisherCrew:
    def __init__(self, tip: str, language: str = "English"):
        if not tip or not tip.strip():
            raise ValueError("Tip cannot be empty")
        self.tip = tip
        self.language = language

    def run(self) -> str:
        agent = create_writer_agent()
        task = create_writing_task(agent, self.tip)
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        return str(result)
