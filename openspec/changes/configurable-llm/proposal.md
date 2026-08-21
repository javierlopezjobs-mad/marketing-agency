# Configurable LLM

## Why

The model is hardcoded (`openai/gpt-4o-mini` in `src/config.py`) and the pipeline refuses to start without an `OPENAI_API_KEY`. Switching models — e.g. to free-tier or local providers — currently requires editing source code. Making the LLM selection configuration-driven unlocks free models (OpenRouter free tier, Groq, Gemini, local Ollama) and any OpenAI-compatible endpoint without code changes.

## What Changes

- Replace the hardcoded model/key in `src/config.py` with environment-driven configuration:
  - `LLM_MODEL` — provider-prefixed model string (e.g. `openrouter/meta-llama/llama-3.3-70b-instruct:free`, `groq/llama-3.3-70b-versatile`, `ollama/qwen2.5`); defaults to `openai/gpt-4o-mini`.
  - `LLM_API_KEY` — generic key, falling back to legacy `OPENAI_API_KEY`.
  - `LLM_BASE_URL` — optional override for any OpenAI-compatible endpoint.
  - `LLM_TEMPERATURE` — optional, defaults to `0.7`.
- Relax API-key validation: raise only when the configured setup requires a key (not needed for `ollama/*` models or when `LLM_BASE_URL` is set).
- Update `.env.example` documenting the new variables and free-provider examples.
- No changes to agents, tasks, crew, or CLI — they keep consuming the shared `llm` object.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `post-publisher-crew`: The "LLM Configuration" requirement changes from mandating `OPENAI_API_KEY` to environment-driven model/provider selection with conditional key validation.

## Impact

- **Code**: `src/config.py` (rewritten config loading); `.env.example`; tests in `tests/test_crew.py` covering config behavior.
- **Dependencies**: none added — CrewAI routes common providers natively (OpenRouter, Ollama, DeepSeek, vLLM, …); niche providers need optional extras (`litellm` for Groq, `crewai[google-genai]` for Gemini), documented in `.env.example`.
- **Compatibility**: existing `.env` files with only `OPENAI_API_KEY` keep working unchanged.
- **Specs**: modifies the `post-publisher-crew` capability (builds on the in-flight `add-post-publisher-crew` change).
