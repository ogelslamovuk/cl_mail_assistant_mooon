# Mock Demo Flow

This demo flow is safe for customer email: Telegram cards are sent through the real Telegram Bot API when credentials are configured, while customer email is never sent.

## Scope

- Telegram operator card title is `📩 Новое письмо`.
- The card shows `Enrichment` before `Понимание`.
- The card includes `Письмо`, `История переписки`, `Enrichment`, `Понимание`, `Решение системы`, `База знаний` and `Черновик`.
- Ticket enrichment is one compact block with lookup email, ticket DB status, confidence, resolved ticket or candidate count.
- Thread history is compact and limited to recent messages.
- Operator actions update the card text in Russian.
- `✏️ На доработку (LLM)` switches the real Telegram message to comment-waiting state; the next operator message creates a revision request and a new Draft Builder revision.
- `approve` writes `artifacts/mock_outbox/<case_id>/reply_*.md` and `reply_*.json` from the latest draft revision.
- `real_email_sent` remains `false`.

## Runners

Build the first draft:

```powershell
python -m src.runners.run_draft_builder --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md
```

Create the operator card through the real Bot API:

```powershell
python -m src.runners.run_telegram_operator_delivery --delivery-mode real --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md
```

Run the production bot handler for callbacks and operator comments:

```powershell
python -m src.runners.run_operator_bot
```

Approve the latest revision into mock outbox:

```powershell
python -m src.runners.run_operator_actions --dossier-path artifacts/modules/mail_import/fixture-1_approve/message_1_approve.md --action approve
```

## Artifacts

- Card artifacts: `artifacts/telegram_operator_delivery/<case_id>/card_*.json`
- Operator actions: `artifacts/operator_actions/<case_id>/action_*.json`
- Revision requests: `artifacts/revision_requests/<case_id>/revision_request_*.json`
- Mock outbox: `artifacts/mock_outbox/<case_id>/reply_*.md` and `reply_*.json`
- Card index and mock Telegram offsets: `artifacts/state/operator_cards_index.json`, `artifacts/state/operator_bot_state.json`

## Current Limitations

- Telegram delivery depends on Telegram Bot API availability and configured bot/chat credentials.
- Draft revision is deterministic and local; no external LLM call is required for tests.
- Real email sending is intentionally not implemented in this flow.
