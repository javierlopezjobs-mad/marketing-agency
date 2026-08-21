# Spec Delta: Configurable LLM

> Note: modifies the `post-publisher-crew` capability defined by the in-flight
> `add-post-publisher-crew` change (`openspec/changes/add-post-publisher-crew/specs/post-publisher-crew/spec-delta.md`).
> Archive that change before syncing this delta.

## MODIFIED Requirements

### Requirement: LLM Configuration

WHEN `src/config.py` is imported,
the system SHALL construct the shared CrewAI `LLM` object from environment variables loaded from the `.env` file in the project root:
`LLM_MODEL` (model string with provider prefix), `LLM_API_KEY`, optional `LLM_BASE_URL`, and optional `LLM_TEMPERATURE`.
The system SHALL resolve the API key as `LLM_API_KEY`, falling back to `OPENAI_API_KEY`.
The default model SHALL be `openai/gpt-4o-mini` and the default temperature `0.7`.

#### Scenario: Custom free-provider model selected via environment

GIVEN a `.env` file containing `LLM_MODEL=openrouter/meta-llama/llama-3.3-70b-instruct:free` and `LLM_API_KEY=<openrouter-key>`
WHEN `src/config.py` is imported
THEN the constructed `LLM` object SHALL use the OpenRouter model string
AND the LLM's api key SHALL be the resolved `LLM_API_KEY` value

#### Scenario: Defaults reproduce legacy behavior

GIVEN a `.env` file containing only `OPENAI_API_KEY=sk-...`
WHEN `src/config.py` is imported
THEN the constructed `LLM` object SHALL use model `openai/gpt-4o-mini`
AND the api key SHALL be the `OPENAI_API_KEY` value
AND the temperature SHALL be 0.7

#### Scenario: Keyless local model allowed

GIVEN `LLM_MODEL=ollama/qwen2.5` is set and no API key variable is defined
WHEN `src/config.py` is imported
THEN the system SHALL NOT raise an error
AND the constructed `LLM` object SHALL use the Ollama model string

#### Scenario: Custom base URL allowed without key

GIVEN `LLM_BASE_URL=http://localhost:8080/v1` is set and no API key variable is defined
WHEN `src/config.py` is imported
THEN the system SHALL NOT raise an error
AND the constructed `LLM` object SHALL use the configured base URL

#### Scenario: Missing API key when required

GIVEN no `LLM_MODEL`, `LLM_BASE_URL`, or resolvable API key is set
WHEN `src/config.py` is imported
THEN the system SHALL raise a `ValueError` with message "LLM_API_KEY not set"

#### Scenario: Temperature override

GIVEN `LLM_TEMPERATURE=0.2` is set
WHEN `src/config.py` is imported
THEN the constructed `LLM` object SHALL use temperature 0.2
