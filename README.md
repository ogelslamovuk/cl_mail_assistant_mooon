# cl_mail_assistant_mooon

Modular support-mail pipeline system.

## Current stage
- Modular mail pipeline with isolated runners.
- Mail import, attachment extraction, enrichment, case/thread binding and structured understanding are represented in dossiers.
- Mock `.eml` inbox demo flow runs the full local pipeline and sends real Telegram Bot API operator cards.
- Orchestrator can run full or partial pipeline.

## Quick start: demo from .eml inbox
1. Put raw `.eml` files here:
   - `fixtures/mock_mailbox/inbox/`
2. Run:
   - `python -m src.runners.run_mock_mailbox_flow`
3. Receive the Telegram operator card.
4. Press an operator action:
   - `✅ Утвердить`
   - `✏️ На доработку (LLM)`
   - `👤 Оператору`
   - `🚫 Игнорировать`
5. Check results:
   - `artifacts/operator_actions/`
   - `artifacts/revision_requests/`
   - `artifacts/mock_outbox/`
   - `artifacts/modules/mail_import/`

If the inbox is empty, the runner prints:

```text
[mock_flow] no .eml files found in fixtures/mock_mailbox/inbox
```

It does not create fake mail unless you explicitly put `.eml` files into the inbox.

## Telegram operator demo flow
- Main runner:
  - `python -m src.runners.run_mock_mailbox_flow`
- It processes all `.eml` files in `fixtures/mock_mailbox/inbox/`, moves successful files to `fixtures/mock_mailbox/processed/`, moves failed files to `fixtures/mock_mailbox/failed/`, sends Telegram cards, then keeps Telegram polling alive for `mock_flow.telegram_poll_seconds`.
- Override polling time:
  - `python -m src.runners.run_mock_mailbox_flow --poll-seconds 60`
- Advanced/debug: build or revise a draft for an existing dossier:
  - `python -m src.runners.run_draft_builder --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md`
- Advanced/debug: create a real Telegram operator card when `telegram_operator_delivery.bot_token` and `operator_chat_id` are configured:
  - `python -m src.runners.run_telegram_operator_delivery --delivery-mode real --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md`
- Advanced/debug: send to Draft Builder for revision with an operator comment:
  - `python -m src.runners.run_operator_actions --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md --action needs_edit --operator-comment "Добавь просьбу указать номер заказа."`
- Advanced/debug: approve the latest draft into mock outbox:
  - `python -m src.runners.run_operator_actions --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md --action approve`
- Bot callback/message handling uses `python -m src.runners.run_operator_bot`.
- Demo artifacts are written under `artifacts/telegram_operator_delivery/`, `artifacts/operator_actions/`, `artifacts/revision_requests/` and `artifacts/mock_outbox/`.
- Real customer email sending is disabled in this mock flow; approvals only create mock outbox files.

## Local config
- Create `config.local.yaml` in repo root based on `config.example.yaml`.
- `mail_import` runner reads section `mail_import`.
- `run_mock_mailbox_flow` reads `mock_flow.telegram_poll_seconds` and accepts `--poll-seconds` as an override.
- CLI args override config values for the current run.
- `mail_import` poller reads `mail_import` section, supports only `mode: imap`, polls by `poll_interval_sec`, and writes to `artifacts/state/import_registry.xlsx`.

For full structure/details see `docs/skeleton.md`.
