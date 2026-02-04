# Agent Instructions (Cursor / AI assistant)

You are helping implement a production-minded GenAI service.

## Non-negotiables
1) Small diffs: propose a plan, then implement in small patches.
2) Typed & validated: Pydantic for API I/O; LLM outputs must be validated server-side.
3) Reliability: timeouts, bounded retries, and graceful error handling for external calls.
4) Security: never log secrets or raw PII; no credentials in code.
5) Observability: structured logs with request_id + latency + status.
6) Tests: each new feature gets at least 1 happy-path and 1 failure-path test.
7) Docs: update README when adding endpoints/env vars.

## Architecture constraints
- API layer (`app/api`) is thin: validate → call service → return.
- Service layer (`app/services`) holds GenAI logic + integrations.
- Core (`app/core`) holds config, logging, error types.
