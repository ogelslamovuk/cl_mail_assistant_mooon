# cl_mail_assistant_mooon

Skeleton of a modular support-mail pipeline system.

## Current stage
- Architecture + project skeleton only.
- Modules are isolated and runnable separately.
- Orchestrator can run full or partial pipeline.

## Quick start
- Run one module:
  - `python -m src.runners.run_mail_import --mode fixture --fixture-path fixtures/emails/sample_email_01.eml`
- Run background IMAP poller:
  - `python -m src.runners.run_mail_import_poller`
- Run full pipeline:
  - `python -m src.runners.run_pipeline`

## Local config
- Create `config.local.yaml` in repo root based on `config.example.yaml`.
- `mail_import` runner reads section `mail_import`.
- CLI args override config values for the current run.
- `mail_import` poller reads `mail_import` section, supports only `mode: imap`, polls by `poll_interval_sec`, and writes to `artifacts/state/import_registry.xlsx`.

For full structure/details see `docs/skeleton.md`.
