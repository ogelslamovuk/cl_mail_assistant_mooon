# Skeleton Architecture

## Goals of this stage
- Build only modular skeleton (no full business logic).
- Keep project case-aware and thread-aware from day one.
- Ensure inspectable artifacts + basic logs.

## Pipeline modules
- `mail_import`
- `pre_triage`
- `identity_context_enrichment`
- `case_thread_binding`
- `llm_understanding`
- `router`
- `knowledge_rag`
- `draft_builder`
- `telegram_operator_delivery`
- `operator_actions`
- `reply_sender`

## Shared contract
Every module uses one unified contract:
- Input: `PipelineContext`
- Output: `ModuleResult`, containing:
  - `context` (updated `PipelineContext`)
  - `status`
  - `notes`
  - `artifact_refs`

## Core entities
- `EmailHeaders` with required fields:
  - `message_id`
  - `in_reply_to`
  - `references`
  - `subject`
  - `sender`
  - `sent_at`
- `Message`, `Thread`, `Case`
- plus placeholders for routing/draft/operator data.

## Layers
- `src/layers/config`: Excel config placeholder.
- `src/layers/state`: Excel state placeholder.
- `src/layers/artifacts`: inspectable artifacts + logging.

## Isolated module run
Examples:
- `python -m src.runners.run_mail_import`
- `python -m src.runners.run_router`
- `python -m src.runners.run_reply_sender`

## Orchestrator run
- Full pipeline:
  - `python -m src.runners.run_pipeline`
- Partial pipeline:
  - `python -m src.runners.run_pipeline --from-step pre_triage --to-step router`
- Explicit subset:
  - `python -m src.runners.run_pipeline --steps mail_import,pre_triage,router`

## Artifacts
- Module outputs: `artifacts/modules/<module>/<run_id>/output.json`
- Run snapshot: `artifacts/runs/<run_id>/pipeline_context.json`
- Logs: `artifacts/logs/*.log`

## Out of scope for this stage
- Production triage/router/enrichment behavior.
- Real Telegram workflow.
- Final sending implementation details.
- Advanced audit/metrics subsystem.
