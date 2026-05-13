# Mock Demo Flow

This demo flow is local and safe: it creates Telegram-card artifacts and mock outbox files only. It never sends real customer email.

## Scope

- Telegram operator card title is `📩 Новое письмо`.
- The card shows `Обогащение` before `Понимание`.
- Ticket enrichment is one compact block with lookup email, ticket DB status, confidence, resolved ticket or candidate count.
- Thread history is compact and limited to recent messages.
- Operator actions update the card text in Russian.
- `✏️ На доработку (LLM)` accepts an operator comment and creates a new Draft Builder revision.
- `approve` writes `artifacts/mock_outbox/<case_id>/reply_*.md` and `reply_*.json` from the latest draft revision.
- `real_email_sent` remains `false`.

## Runners

Build the first draft:

```powershell
python -m src.runners.run_draft_builder --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md
```

Create the operator card:

```powershell
python -m src.runners.run_telegram_operator_delivery --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md
```

Request a revision with an operator comment:

```powershell
python -m src.runners.run_operator_actions --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md --action needs_edit --operator-comment "Добавь просьбу указать номер заказа."
```

Approve the latest revision into mock outbox:

```powershell
python -m src.runners.run_operator_actions --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md --action approve
```

## Artifacts

- Card artifacts: `artifacts/telegram_operator_delivery/<case_id>/card_*.json`
- Operator actions: `artifacts/operator_actions/<case_id>/action_*.json`
- Mock outbox: `artifacts/mock_outbox/<case_id>/reply_*.md` and `reply_*.json`
- Card index and mock Telegram offsets: `artifacts/state/operator_cards_index.json`, `artifacts/state/operator_bot_state.json`

## Current Limitations

- Telegram delivery is represented by local artifacts in demo mode.
- Draft revision is deterministic and local; no external LLM call is required for tests.
- Real email sending is intentionally not implemented in this flow.
