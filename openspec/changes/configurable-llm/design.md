# Design: Configurable LLM

## Context

`src/config.py` builds a module-level CrewAI `LLM` singleton at import time with a hardcoded `openai/gpt-4o-mini` model and a mandatory `OPENAI_API_KEY`. `src/agents.py` imports this singleton; nothing else touches LLM construction. CrewAI's `LLM` routes models through built-in native providers (openai, openrouter, ollama, deepseek, hosted_vllm, cerebras, …) plus optional `base_url`; other providers require opt-in extras (`litellm` for e.g. Groq, `crewai[google-genai]` for Gemini) — verified against the installed version. No new dependencies are required for the scenarios in scope.

Constraint: tests reload `src.config` under patched env vars, so import-time configuration must stay cheap and deterministic.

## Goals / Non-Goals

**Goals:**
- Switch models/providers by editing `.env` only.
- Support keyless providers (local Ollama) and free-tier providers.
- Keep existing `OPENAI_API_KEY`-only setups working unchanged.

**Non-Goals:**
- Per-agent or per-task model overrides (single shared LLM is enough today).
- Provider-specific config validation (LiteLLM owns provider semantics).
- Runtime/model hot-swapping mid-process.

## Decisions

### 1. Generic env vars with legacy fallback
`LLM_MODEL`, `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_TEMPERATURE`; key resolution order: `LLM_API_KEY` → `OPENAI_API_KEY`.

*Why not provider-specific vars (`OPENROUTER_API_KEY`, etc.)?* A single generic pair keeps our surface minimal; provider-native env vars still work where the underlying client supports them.

### 2. Conditional key validation instead of unconditional raise
Raise `ValueError` only when: no key is resolvable AND the setup needs one — i.e. model is not `ollama/*` and `LLM_BASE_URL` is unset. Message names the missing variable (`LLM_API_KEY not set`).

*Why not always warn?* Silent misconfiguration surfaces as a confusing LiteLLM auth error deep in a crew run. Failing fast at import with a clear message preserves today's ergonomics.

*Why not a hardcoded per-provider "needs key" table?* Maintenance burden and it would drift from LiteLLM's actual behavior; the two keyless cases we care about (Ollama, custom base_url) cover the realistic local/free setups.

### 3. Keep the module-level singleton
Config stays read-at-import; agents keep importing `llm`.

*Why not a `get_llm()` factory?* Cleaner for testing, but it touches every consumer and the existing test style already handles reloads via `importlib.reload`. Minimal diff wins; a factory can come later if per-run configuration is ever needed.

### 4. Default model unchanged
No `LLM_MODEL` → `openai/gpt-4o-mini`. Guarantees backward compatibility for current `.env` files.

## Risks / Trade-offs

- [Free-tier rate limits break long crew runs] → Document limits in `.env.example`; retry/queueing is out of scope.
- [Some providers need optional extras (Groq via `litellm`, Gemini via `crewai[google-genai]`)] → Documented in `.env.example`; installing an extra is a one-line change, not a code change.
- [Typo in `LLM_MODEL` fails late with an obscure LiteLLM error] → Acceptable; document common prefixes in `.env.example`.
- [Import-time validation makes some tests env-sensitive] → Follow existing `patch.dict(os.environ)` + `reload` test pattern.
- [Delta modifies a requirement from an unarchived change] → Delta text is self-contained; archive `add-post-publisher-crew` first when syncing specs.

## Migration Plan

1. Land config change + updated `.env.example` + tests together.
2. Existing users: no action required (defaults reproduce current behavior).
3. Rollback: revert commit; `.env` additions are inert for old code.

## Open Questions

- Should `main_crew.py` print the active model at startup for easier debugging? (lean yes, trivial)
