# Mock Demo Flow

This demo flow is safe for customer email: Telegram cards are sent through the real Telegram Bot API when credentials are configured, while customer email is never sent.

## Main Demo Scenario

1. Put one or more raw `.eml` files into:

```powershell
fixtures/mock_mailbox/inbox/
```

2. Run the single demo runner:

```powershell
python -m src.runners.run_mock_mailbox_flow
```

3. Receive a real Telegram operator card.
4. Press an operator action in Telegram.
5. Inspect artifacts:

- `artifacts/operator_actions/`
- `artifacts/revision_requests/`
- `artifacts/mock_outbox/`
- `artifacts/modules/mail_import/`

The runner processes every `.eml` in `fixtures/mock_mailbox/inbox/`, moves successful files to `fixtures/mock_mailbox/processed/`, moves failed files to `fixtures/mock_mailbox/failed/`, and writes a readable error artifact under `artifacts/mock_mailbox_errors/`.

If the inbox is empty, it prints exactly:

```text
[mock_flow] no .eml files found in fixtures/mock_mailbox/inbox
```

The runner does not create synthetic mail by itself.

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

## Pipeline

`python -m src.runners.run_mock_mailbox_flow` executes:

- `MailImportModule`
- `AttachmentExtractionModule`
- `IdentityContextEnrichmentModule`
- `CaseThreadBindingModule`
- `LlmUnderstandingModule`
- `KnowledgeRetrievalModule`
- `DecisionLayerModule`
- `DraftBuilderModule`
- `TelegramOperatorDeliveryModule`

After cards are sent, it starts the same production Telegram callback/message handling path used by:

```powershell
python -m src.runners.run_operator_bot
```

Polling duration is read from:

```yaml
mock_flow:
  telegram_poll_seconds: 300
```

The CLI override is:

```powershell
python -m src.runners.run_mock_mailbox_flow --poll-seconds 60
```

## Advanced/debug runners

- `python -m src.runners.run_draft_builder --dossier-path <dossier-path>`
- `python -m src.runners.run_telegram_operator_delivery --delivery-mode real --dossier-path <dossier-path>`
- `python -m src.runners.run_operator_bot`
- `python -m src.runners.run_operator_actions --dossier-path <dossier-path> --action approve`

These are for debugging existing dossiers. They are not the primary demo path.

## Artifacts

- Card artifacts: `artifacts/telegram_operator_delivery/<case_id>/card_*.json`
- Operator actions: `artifacts/operator_actions/<case_id>/action_*.json`
- Revision requests: `artifacts/revision_requests/<case_id>/revision_request_*.json`
- Mock outbox: `artifacts/mock_outbox/<case_id>/reply_*.md` and `reply_*.json`
- Card index and mock Telegram offsets: `artifacts/state/operator_cards_index.json`, `artifacts/state/operator_bot_state.json`
- Mail import dossiers: `artifacts/modules/mail_import/<run_id>/message_*.md`
- Mock inbox errors: `artifacts/mock_mailbox_errors/*.json`

## Current Limitations

- Telegram delivery depends on Telegram Bot API availability and configured bot/chat credentials.
- Draft revision is deterministic and local; the revision path does not send real customer email.
- Real email sending is intentionally not implemented in this flow.
