# Message dossier callback_approve

- UID: callback_approve
- Message-ID: <callback-approve@example.test>
- Direction: inbound
- From: guest@example.test
- Subject: Не пришёл билет
- Sent at: 2026-05-13T10:00:00+03:00
- Preferred body source: <empty>
- Raw email: <empty>

## Case / Thread

- Case ID: case-callback-approve
- Thread ID: thread-callback-approve
- Binding rule: <empty>
- Binding status: <empty>

## Enrichment

- Ticket DB status: <empty>
- Selected lookup email: <empty>
- Resolved ticket: <empty>

## Attachments

- Count: 0
- Text found in: 0

## LLM Understanding

- Status: ok
- Response mode: ask_clarifying_question
- Confidence: <empty>
- Topic: Не пришёл электронный билет
- Customer need: Получить билет или инструкцию по восстановлению.
- Summary: Гость оплатил билет, но не получил письмо.
- Response mode reason: Нужно уточнить номер заказа или контакт.

Entities:
- email: guest@example.test

## Body

```
Оплатил билет онлайн, но письмо с билетом не пришло.
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<callback-approve@example.test>",
  "direction": "inbound",
  "headers": {
    "sender": "guest@example.test",
    "subject": "Не пришёл билет",
    "sent_at": "2026-05-13T10:00:00+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Оплатил билет онлайн, но письмо с билетом не пришло.",
  "metadata": {
    "uid": "callback_approve"
  },
  "modules": {
    "case_thread_binding": {
      "case_id": "case-callback-approve",
      "thread_id": "thread-callback-approve",
      "thread_history": []
    },
    "llm_understanding": {
      "status": "ok",
      "structured_output": {
        "summary": "Гость оплатил билет, но не получил письмо.",
        "topic": "Не пришёл электронный билет",
        "customer_need": "Получить билет или инструкцию по восстановлению.",
        "entities": [
          {
            "type": "email",
            "value": "guest@example.test"
          }
        ],
        "response_mode": "ask_clarifying_question",
        "response_mode_reason": "Нужно уточнить номер заказа или контакт."
      }
    },
    "knowledge_retrieval": {
      "status": "found",
      "matched_items": [
        {
          "id": "kb_system_ticket_sender",
          "title": "Адрес отправителя электронных билетов",
          "score": 10,
          "template_hint": "Письмо с билетами отправляется с адреса ticket@silverscreen.by."
        }
      ]
    },
    "decision_layer": {
      "status": "ok",
      "response_mode_final": "ask_clarifying_question",
      "decision_reason": "Не хватает номера заказа или контактных данных для проверки.",
      "missing_data": [
        "Номер заказа или email/телефон, указанный при покупке."
      ],
      "risks": []
    },
    "draft_builder": {
      "uid": "callback_approve",
      "status": "ok",
      "error": "",
      "draft_type": "ask_clarifying_question",
      "latest_revision": 1,
      "draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить билет или инструкцию по восстановлению.), пожалуйста, уточните:\n- Номер заказа или email/телефон, указанный при покупке.\nПисьмо с билетами отправляется с адреса ticket@silverscreen.by.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon.",
      "operator_note": "Черновик создан в демо-режиме; реальная отправка отключена.",
      "source_response_mode": "ask_clarifying_question",
      "created_at": "2026-05-14T12:44:09.022646+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124404092050\\callback_fixtures\\message_callback_approve.md",
      "revisions": [
        {
          "revision": 1,
          "created_at": "2026-05-14T12:44:09.022646+00:00",
          "revision_reason": "initial",
          "operator_comment": "",
          "draft_type": "ask_clarifying_question",
          "draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить билет или инструкцию по восстановлению.), пожалуйста, уточните:\n- Номер заказа или email/телефон, указанный при покупке.\nПисьмо с билетами отправляется с адреса ticket@silverscreen.by.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon."
        }
      ],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "found",
        "decision_layer_status": "ok",
        "knowledge_item_ids": [
          "kb_system_ticket_sender"
        ]
      }
    },
    "telegram_operator_delivery": {
      "uid": "callback_approve",
      "status": "mock_sent",
      "error": "",
      "created_at": "2026-05-14T12:44:09.089791+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124404092050\\callback_fixtures\\message_callback_approve.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124404092050\\callback_fixtures\\message_callback_approve.md",
      "case_id": "case-callback-approve",
      "thread_id": "thread-callback-approve",
      "telegram_message_id": 7,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "artifact_only",
      "telegram_operations": [],
      "callback_data": [
        "ma|approve|cc429fd324543ca4",
        "ma|needs_edit|cc429fd324543ca4",
        "ma|handoff|cc429fd324543ca4",
        "ma|ignore|cc429fd324543ca4"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|cc429fd324543ca4"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|cc429fd324543ca4"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|cc429fd324543ca4"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|cc429fd324543ca4"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: callback_approve\nПолучено: 13.05.2026 10:00\nОт: guest@example.test\nТема письма: Не пришёл билет\nСуть обращения: Гость оплатил билет, но не получил письмо.\n\n<b>Кейс</b>\nCase ID: case-callback-approve · Thread ID: thread-callback-approve\n\n<b>История переписки</b>\nотсутствует\n\n<b>Вложения</b>\nнет\n\n<b>Проверка билетов / Enrichment</b>\nБилет: не найден\n\n<b>Что понял ассистент</b>\nТип обращения: Не пришёл электронный билет\nЧто хочет отправитель: Получить билет или инструкцию по восстановлению.\nСледующий шаг: отправить гостю запрос недостающих данных.\n\n<b>Что предлагает система</b>\nЧто сделать: отправить гостю запрос недостающих данных.\nПочему: Не хватает номера заказа или контактных данных для проверки.\n\n<b>База знаний</b>\n- Адрес отправителя электронных билетов\n\n<b>Что не хватает</b>\n- Номер заказа или email/телефон, указанный при покупке.\n\n<b>Риски</b>\nнет\n\n<b>Черновик v1</b>\nЗдравствуйте.\nЧтобы корректно обработать обращение (Получить билет или инструкцию по восстановлению.), пожалуйста, уточните:\n- Номер заказа или email/телефон, указанный при покупке.\nПисьмо с билетами отправляется с адреса ticket@silverscreen.by.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon.",
      "action": "",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124404092050",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124404092050\\telegram_operator_delivery\\case-callback-approve\\card_20260514T124409089927.json"
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
