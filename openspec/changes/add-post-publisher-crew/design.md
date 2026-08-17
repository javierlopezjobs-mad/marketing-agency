# Design: Post Publisher Crew

## Architecture Overview

The crew lives in the `marketing-agency` root as a standalone Python package. It reuses patterns from `post-publisher/` (OpenAI config, logging, dotenv) but does not import from it directly — the two remain decoupled so the crew can evolve independently.

```
marketing-agency/
├── openspec/
│   └── changes/
│       └── add-post-publisher-crew/
│           ├── proposal.md
│           └── design.md          ← this file
├── src/
│   ├── __init__.py
│   ├── crew.py                   # CrewAI crew definition
│   ├── agents.py                 # Agent definitions
│   ├── tasks.py                  # Task definitions
│   └── config.py                 # LLM and crew configuration
├── main_crew.py                  # CLI entry point
├── tests/
│   ├── __init__.py
│   └── test_crew.py
├── pyproject.toml
├── requirements.txt
├── .env                          # OPENAI_API_KEY (gitignored)
└── .gitignore
```

## Technical Decisions

### 1. CrewAI as the orchestration layer

CrewAI provides `Agent`, `Task`, `Crew`, and `Process` abstractions. The first version uses a **sequential process** with one agent and one task — minimal overhead, easy to extend later to hierarchical or parallel crews.

### 2. Single agent: the writer

| Property | Value |
|---|---|
| Role | Publication Writer |
| Goal | Generate publication-ready text from a subject tip |
| Backstory | Professional content writer for online publications |
| Tools | None (v1) — the agent relies solely on the LLM |

The agent receives the tip as the task description and returns the full article text. No external tools (web search, file I/O) in v1.

### 3. LLM configuration

The crew uses the same OpenAI key from `.env` (`OPENAI_API_KEY`). CrewAI's `ChatOpenAI` wrapper handles the connection. Default model: `gpt-4o-mini` (matching `post-publisher/chatgpt_api.py:21`). Temperature: `0.7` (matching `main_article.py:51`).

```python
# src/config.py
import os
from dotenv import load_dotenv
from crewai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
)
```

### 4. Task definition

The single task takes a `tip` (string) as input and expects the agent to produce the full publication text. The task's `expected_output` specifies the contract: a complete article, no metadata, no preamble.

```python
# src/tasks.py
from crewai import Task

def create_writing_task(agent, tip: str) -> Task:
    return Task(
        description=f"Write a publication-ready article about: {tip}",
        expected_output=(
            "A complete article in HTML <p> tags. "
            "No title, no preamble, no metadata. "
            "The text must address the subject directly."
        ),
        agent=agent,
    )
```

### 5. Crew composition

```python
# src/crew.py
from crewai import Crew, Process
from src.agents import create_writer_agent
from src.tasks import create_writing_task

class PostPublisherCrew:
    def __init__(self, tip: str, language: str = "English"):
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
```

### 6. Entry point

`main_crew.py` accepts a tip via CLI argument or interactive prompt, instantiates `PostPublisherCrew`, runs it, and prints the result.

```python
# main_crew.py
import sys
from src.crew import PostPublisherCrew

def main():
    tip = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter tip: ")
    crew = PostPublisherCrew(tip=tip)
    result = crew.run()
    print(result)

if __name__ == "__main__":
    main()
```

### 7. Testing strategy

- **Unit test**: `PostPublisherCrew` instantiation, agent/task creation, config loads.
- **Integration test** (mocked LLM): crew.kickoff() returns non-empty string, output contains tip keywords.
- No live API calls in CI — use `unittest.mock` to patch `ChatOpenAI`.

### 8. Dependencies

New `requirements.txt` (root level):

```
crewai>=0.30.0
crewai-tools>=0.14.0
python-dotenv>=1.0.0
pytest>=7.0.0
```

Note: CrewAI bundles its own OpenAI client. The old `openai==0.28.0` in `post-publisher/` is irrelevant here — the new project uses CrewAI's managed dependency.

## Future Extensibility

- **Research agent**: add `SerperDevTool` or `ScrapeWebsiteTool` for web research before writing.
- **SEO agent**: analyze keywords, suggest headings, optimize meta descriptions.
- **Image agent**: generate featured images via DALL-E or Stable Diffusion.
- **Publisher agent**: push text to Blogger/WordPress/Medium via API.
- **Multi-language**: accept `language` parameter, pass to agent backstory.
- **Hierarchical process**: add a manager agent to coordinate writer + editor + publisher.

## Risks

| Risk | Mitigation |
|---|---|
| CrewAI API changes | Pin version in requirements.txt |
| OpenAI rate limits | CrewAI handles retries; add backoff in config if needed |
| Output quality variance | Tune temperature, add validation task in v2 |
| Windows path issues | CrewAI uses pathlib internally; no raw `C:/` paths |
