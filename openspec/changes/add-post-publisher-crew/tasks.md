# Implementation Tasks

1. Create project root structure: `src/`, `tests/`, `main_crew.py`, `pyproject.toml`, `requirements.txt`
2. Write `src/__init__.py` and `src/config.py` — load dotenv, configure `ChatOpenAI` with `gpt-4o-mini` and temperature 0.7
3. Write `src/agents.py` — define `create_writer_agent()` returning a CrewAI `Agent` with role/goal/backstory
4. Write `src/tasks.py` — define `create_writing_task(agent, tip)` returning a CrewAI `Task` with description and expected output contract
5. Write `src/crew.py` — implement `PostPublisherCrew` class with `__init__(tip, language)` and `run()` method using sequential process
6. Write `main_crew.py` — CLI entry point accepting tip as arg or interactive input, calls `PostPublisherCrew.run()`, prints result
7. Write `requirements.txt` — crewai>=0.30.0, crewai-tools>=0.14.0, python-dotenv>=1.0.0, pytest>=7.0.0
8. Write `tests/__init__.py` and `tests/test_crew.py` — unit tests for config load, agent creation, task creation, crew instantiation
9. Write `tests/test_crew.py` integration test — mock LLM, verify `crew.kickoff()` returns non-empty string containing tip keyword
10. Run `pytest` — all tests pass, no live API calls
11. Manual smoke test — run `python main_crew.py "The rise of AI agents"` with live API key, verify output is publication-ready text
