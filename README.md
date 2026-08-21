# marketing-agency

CrewAI-based content generation crew: turn a subject tip into publication-ready HTML text via a single writer agent (`PostPublisherCrew`).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit per the configuration table below
```

## LLM configuration

The model/provider is selected entirely through `.env` — no code changes needed.
CrewAI routes common providers natively (OpenAI, OpenRouter, Ollama, DeepSeek, vLLM, ...).

| Variable | Default | Purpose |
|---|---|---|
| `LLM_MODEL` | `openai/gpt-4o-mini` | Model string with provider prefix |
| `LLM_API_KEY` | falls back to `OPENAI_API_KEY` | Provider API key |
| `LLM_BASE_URL` | unset | Custom OpenAI-compatible endpoint |
| `LLM_TEMPERATURE` | `0.7` | Sampling temperature |

An API key is only required when the setup needs one: `ollama/*` models and custom `LLM_BASE_URL` endpoints work keyless.

**Free options:**

```bash
# OpenRouter free tier (key at openrouter.ai)
LLM_MODEL=openrouter/meta-llama/llama-3.3-70b-instruct:free
LLM_API_KEY=sk-or-...

# Fully local via Ollama (no key) — run `ollama pull qwen2.5` first
LLM_MODEL=ollama/qwen2.5
```

Groq (`groq/...`) and Gemini (`gemini/...`) require optional extras:
`pip install litellm` / `pip install "crewai[google-genai]"`.

Quick config smoke test (no API call):

```bash
python -c "from src.config import llm; print(llm.model, llm.temperature, llm.base_url)"
```

## Usage

```bash
python main_crew.py "The rise of AI agents"   # tip as argument
python main_crew.py                            # or interactive prompt
```

Output is the generated article body (HTML `<p>` paragraphs), printed to stdout.

## Tests

```bash
pytest
```

All tests run offline — no live LLM calls.

## Project structure

```
main_crew.py        # CLI entry point
src/config.py       # env-driven LLM configuration
src/agents.py       # writer agent definition
src/tasks.py        # writing task definition
src/crew.py         # PostPublisherCrew orchestration
openspec/           # OpenSpec specs and change proposals
```
