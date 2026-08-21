# Tasks: Configurable LLM

## 1. Configuration

- [ ] 1.1 Rewrite `src/config.py` to build the `LLM` from `LLM_MODEL`, `LLM_API_KEY` (fallback `OPENAI_API_KEY`), optional `LLM_BASE_URL`, and `LLM_TEMPERATURE`; default model `openai/gpt-4o-mini`, default temperature `0.7`
- [ ] 1.2 Implement conditional key validation: raise `ValueError("LLM_API_KEY not set")` only when no key is resolvable and the model is not `ollama/*` and `LLM_BASE_URL` is unset
- [ ] 1.3 Update `.env.example` with the new variables and commented free-provider examples (OpenRouter, Groq, Gemini, Ollama, custom base URL)

## 2. Tests

- [ ] 2.1 Update existing config tests (`test_config_loads_api_key`, `test_config_missing_api_key`) for the new resolution order and error message
- [ ] 2.2 Add tests: custom model via `LLM_MODEL`, keyless `ollama/*` allowed, keyless custom `LLM_BASE_URL` allowed, temperature override, defaults reproduce legacy behavior
- [ ] 2.3 Run full suite (`.venv/bin/python -m pytest`) — all tests pass without live API calls

## 3. Validation

- [ ] 3.1 Verify legacy setup: `.env` with only `OPENAI_API_KEY` still runs `python main_crew.py "<tip>"` end-to-end
- [ ] 3.2 Validate change artifacts (`openspec validate --change configurable-llm`) and mark tasks complete
