from crewai import Task, Agent


def create_writing_task(agent: Agent, tip: str) -> Task:
    return Task(
        description=(
            f"Write a publication-ready article about: {tip}\n\n"
            "The article must:\n"
            "- Be written in HTML with <p> tags for each paragraph\n"
            "- Directly address the subject from the tip\n"
            "- Be suitable as publication copy (no title, no preamble, no metadata)\n"
            "- Be informative and engaging"
        ),
        expected_output=(
            "A complete article in HTML <p> tags. "
            "No title, no preamble, no metadata. "
            "The text must address the subject directly."
        ),
        agent=agent,
    )
