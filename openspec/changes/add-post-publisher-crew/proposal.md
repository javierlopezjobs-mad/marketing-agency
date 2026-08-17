# Post Publisher Crew

## Overview

Introduce a CrewAI-based crew that, given a tip about a subject, generates publication-ready text. This is the first version: a single agent that takes a topic tip as input and produces the article body for a publication.

## Problem Statement

The project currently produces content through standalone scripts (`chatgpt_api.py`, `main_article.py`, etc.) with no agent orchestration. There is no way to turn a raw tip (a brief note about a subject) into publication-ready text in a structured, reproducible pipeline. A CrewAI crew provides a spec-driven, extensible foundation: agents, tasks, and tools can grow incrementally (research, images, SEO, publishing) without rewriting the pipeline.

## Proposed Implementation

- Add CrewAI as a dependency (and its CLI tooling) to the project.
- Implement a single crew `PostPublisherCrew` composed of one agent (a writer) and one task (generate the publication text).
- The crew input is a `tip` (subject description) provided by the user.
- The writer agent produces the full publication text, following a configurable style/language.
- Provide an entry-point script (`main_crew.py`) that accepts the tip as input and prints/saves the resulting text.
- Add tests covering crew configuration and the generated-text contract (non-empty, contains subject, expected format).

## Success Criteria

- [ ] A CrewAI crew runs end-to-end from a `tip` input to generated publication text.
- [ ] The generated text is non-empty, addresses the tip's subject, and is suitable as publication copy.
- [ ] The crew is defined in a dedicated module (e.g., `src/crew.py`) with agent and task specifications.
- [ ] An entry point exists to run the crew with a user-provided tip.
- [ ] Tests pass (`pytest`) and the crew can be executed locally with the configured LLM.
- [ ] OpenSpec spec deltas are created for the crew capability and validated.

## Constraints

- First version: single agent only. No research, image, or publishing tools yet.
- Uses the project's existing LLM configuration (OpenAI key from `.env`).
- Text output only; no automatic posting to Blogger/YouTube in this version.

## Out of Scope

- Multi-agent crews, research agents, image generation, video/audio, SEO optimization.
- Direct integration with Blogger or other publishing APIs.
