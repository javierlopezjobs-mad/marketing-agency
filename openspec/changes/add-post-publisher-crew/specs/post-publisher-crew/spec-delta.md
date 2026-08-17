# Spec Delta: Post Publisher Crew

## ADDED Requirements

### Requirement: Crew Initialization

WHEN a user provides a tip string and optional language parameter,
the system SHALL instantiate a `PostPublisherCrew` object with those parameters.

#### Scenario: Valid tip provided

GIVEN the user provides the tip "The rise of AI agents"
WHEN `PostPublisherCrew` is instantiated with this tip
THEN the crew object SHALL be created with the tip stored as an attribute
AND the default language SHALL be "English"

#### Scenario: Empty tip provided

GIVEN the user provides an empty string as tip
WHEN `PostPublisherCrew` is instantiated with this tip
Then the system SHALL raise a `ValueError` with message "Tip cannot be empty"

### Requirement: Writer Agent Creation

WHEN `create_writer_agent()` is called,
the system SHALL return a CrewAI `Agent` object with role "Publication Writer".

#### Scenario: Agent has correct properties

GIVEN `create_writer_agent()` is called
WHEN the agent is returned
THEN the agent's role SHALL be "Publication Writer"
AND the agent's goal SHALL contain "generate publication-ready text"
AND the agent's backstory SHALL describe a professional content writer

### Requirement: Writing Task Creation

WHEN `create_writing_task(agent, tip)` is called with a valid agent and tip,
the system SHALL return a CrewAI `Task` object bound to that agent.

#### Scenario: Task description contains the tip

GIVEN a tip "Climate change solutions"
WHEN `create_writing_task(agent, tip)` is called
Then the task's description SHALL contain the string "Climate change solutions"
AND the task's expected_output SHALL specify HTML `<p>` tags

#### Scenario: Task is bound to the correct agent

GIVEN an agent instance and a tip
WHEN `create_writing_task(agent, tip)` is called
Then the task's agent attribute SHALL reference the provided agent

### Requirement: Crew Execution

WHEN `PostPublisherCrew.run()` is called,
the system SHALL execute the crew using a sequential process and return the result as a string.

#### Scenario: Crew produces non-empty output

GIVEN a `PostPublisherCrew` initialized with a valid tip
WHEN `run()` is called
THEN the return value SHALL be a non-empty string
AND the output SHALL contain a reference to the tip subject

#### Scenario: Crew uses sequential process

GIVEN a `PostPublisherCrew` is initialized
WHEN `run()` is called
Then the crew SHALL be created with `Process.sequential`

### Requirement: CLI Entry Point

WHEN `main_crew.py` is executed with a tip as a command-line argument,
the system SHALL run the crew with that tip and print the result to stdout.

#### Scenario: Tip provided as CLI argument

GIVEN the user runs `python main_crew.py "The future of work"`
WHEN the script executes
Then `PostPublisherCrew` SHALL be instantiated with tip "The future of work"
AND the result SHALL be printed to stdout

#### Scenario: No argument — interactive prompt

GIVEN the user runs `python main_crew.py` with no arguments
WHEN the script executes
Then the user SHALL be prompted to enter a tip
AND the entered tip SHALL be used for crew execution

### Requirement: LLM Configuration

WHEN the crew is initialized,
the system SHALL load the OpenAI API key from the `.env` file in the project root.

#### Scenario: API key loaded from .env

GIVEN a `.env` file containing `OPENAI_API_KEY=sk-...`
WHEN `src/config.py` is imported
Then `os.getenv("OPENAI_API_KEY")` SHALL return the key value

#### Scenario: Missing API key

GIVEN no `.env` file or missing `OPENAI_API_KEY` variable
WHEN `src/config.py` is imported
Then the system SHALL raise a `ValueError` with message "OPENAI_API_KEY not set"

### Requirement: Tests Pass Without Live API

WHEN `pytest` is run from the project root,
all tests SHALL pass without making live OpenAI API calls.

#### Scenario: Unit tests use mocked LLM

GIVEN `tests/test_crew.py` contains integration tests
WHEN `pytest` is executed
Then no real HTTP requests to `api.openai.com` SHALL be made
AND all tests SHALL complete within 10 seconds
