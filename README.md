# cl_mail_assistant_mooon

Modular support-mail pipeline system.

## Current stage
- Modular mail pipeline with isolated runners.
- Mail import, attachment extraction, enrichment, case/thread binding and structured understanding are represented in dossiers.
- Mock operator demo flow is available for draft building, Telegram operator-card artifacts, operator actions and mock outbox.
- Orchestrator can run full or partial pipeline.

## Quick start
- Run one module:
  - `python -m src.runners.run_mail_import --mode fixture --fixture-path fixtures/emails/sample_email_01.eml`
- Run background IMAP poller:
  - `python -m src.runners.run_mail_import_poller`
- Run full pipeline:
  - `python -m src.runners.run_pipeline`

## Mock operator demo flow
- Build or revise a draft for a dossier:
  - `python -m src.runners.run_draft_builder --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md`
- Create a Telegram operator card artifact:
  - `python -m src.runners.run_telegram_operator_delivery --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md`
- Send to Draft Builder for revision with an operator comment:
  - `python -m src.runners.run_operator_actions --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md --action needs_edit --operator-comment "Добавь просьбу указать номер заказа."`
- Approve the latest draft into mock outbox:
  - `python -m src.runners.run_operator_actions --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md --action approve`
- Demo artifacts are written under `artifacts/telegram_operator_delivery/`, `artifacts/operator_actions/` and `artifacts/mock_outbox/`.
- Real customer email sending is disabled in this mock flow; approvals only create mock outbox files.

## Local config
- Create `config.local.yaml` in repo root based on `config.example.yaml`.
- `mail_import` runner reads section `mail_import`.
- CLI args override config values for the current run.
- `mail_import` poller reads `mail_import` section, supports only `mode: imap`, polls by `poll_interval_sec`, and writes to `artifacts/state/import_registry.xlsx`.

For full structure/details see `docs/skeleton.md`.
