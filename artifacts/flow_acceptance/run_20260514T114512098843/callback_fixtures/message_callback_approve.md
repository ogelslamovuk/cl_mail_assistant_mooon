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
      "latest_revision": 2,
      "draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить билет или инструкцию по восстановлению.), пожалуйста, уточните:\n- Номер заказа или email/телефон, указанный при покупке.\nПисьмо с билетами отправляется с адреса ticket@silverscreen.by.\nПосле этого мы сможем продолжить проверку.\nДополнительно: Добавь просьбу указать номер заказа.\nС уважением, команда mooon.",
      "operator_note": "Черновик создан в демо-режиме; реальная отправка отключена.",
      "source_response_mode": "ask_clarifying_question",
      "created_at": "2026-05-14T11:45:17.403315+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
      "revisions": [
        {
          "revision": 1,
          "created_at": "2026-05-14T11:45:17.109244+00:00",
          "revision_reason": "initial",
          "operator_comment": "",
          "draft_type": "ask_clarifying_question",
          "draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить билет или инструкцию по восстановлению.), пожалуйста, уточните:\n- Номер заказа или email/телефон, указанный при покупке.\nПисьмо с билетами отправляется с адреса ticket@silverscreen.by.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon."
        },
        {
          "revision": 2,
          "created_at": "2026-05-14T11:45:17.403315+00:00",
          "revision_reason": "operator_needs_edit_comment",
          "operator_comment": "Добавь просьбу указать номер заказа.",
          "draft_type": "ask_clarifying_question",
          "draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить билет или инструкцию по восстановлению.), пожалуйста, уточните:\n- Номер заказа или email/телефон, указанный при покупке.\nПисьмо с билетами отправляется с адреса ticket@silverscreen.by.\nПосле этого мы сможем продолжить проверку.\nДополнительно: Добавь просьбу указать номер заказа.\nС уважением, команда mooon."
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
      "status": "action_approve",
      "error": "",
      "created_at": "2026-05-14T11:45:17.607419+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
      "case_id": "case-callback-approve",
      "thread_id": "thread-callback-approve",
      "telegram_message_id": 9001,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "telegram_bot_api",
      "telegram_operations": [
        {
          "operation": "editMessageText",
          "ok": true,
          "chat_id": "mock-operator-chat",
          "message_id": 9001,
          "text": "<b>📩 Новое письмо</b>\n\n✅ Статус: утверждено\nMock-ответ создан.\nРеальный email не отправлен.\n\n<b>Письмо</b>\nUID: callback_approve\nПолучено: 13.05.2026 10:00\nОт: guest@example.test\nТема письма: Не пришёл билет\nСуть обращения: Гость оплатил билет, но не получил письмо.\n\n<b>Кейс</b>\nCase ID: case-callback-approve · Thread ID: thread-callback-approve\n\n<b>История переписки</b>\nнет\n\n<b>Вложения</b>\nнет\n\n<b>Проверка билетов / Enrichment</b>\nБилет: не найден\n\n<b>Что понял ассистент</b>\nТип обращения: Не пришёл электронный билет\nЧто хочет отправитель: Получить билет или инструкцию по восстановлению.\nСледующий шаг: Не хватает номера заказа или контактных данных для проверки.\n\n<b>Предлагаемое решение</b>\nРежим: уточнить данные\nПричина: Не хватает номера заказа или контактных данных для проверки.\n\n<b>База знаний</b>\n- Адрес отправителя электронных билетов / kb_system_ticket_sender / балл 10\n\n<b>Что не хватает</b>\n- Номер заказа или email/телефон, указанный при покупке.\n\n<b>Риски</b>\nнет\n\n<b>Черновик v2</b>\nЗдравствуйте.\nЧтобы корректно обработать обращение (Получить билет или инструкцию по восстановлению.), пожалуйста, уточните:\n- Номер заказа или email/телефон, указанный при покупке.\nПисьмо с билетами отправляется с адреса ticket@silverscreen.by.\nПосле этого мы сможем продолжить проверку.\nДополнительно: Добавь просьбу указать номер заказа.\nС уважением, команда mooon.\n\n<b>Последнее действие</b>\nутверждено",
          "reply_markup": {
            "inline_keyboard": [
              [
                {
                  "text": "Обработано",
                  "callback_data": "ma|noop|done"
                }
              ]
            ]
          }
        },
        {
          "operation": "editMessageReplyMarkup",
          "ok": true,
          "chat_id": "mock-operator-chat",
          "message_id": 9001,
          "reply_markup": {
            "inline_keyboard": []
          }
        },
        {
          "operation": "answerCallbackQuery",
          "ok": true,
          "callback_query_id": "cb_draft_approve",
          "text": "Mock-ответ создан."
        }
      ],
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
      "card_text": "<b>📩 Новое письмо</b>\n\n✅ Статус: утверждено\nMock-ответ создан.\nРеальный email не отправлен.\n\n<b>Письмо</b>\nUID: callback_approve\nПолучено: 13.05.2026 10:00\nОт: guest@example.test\nТема письма: Не пришёл билет\nСуть обращения: Гость оплатил билет, но не получил письмо.\n\n<b>Кейс</b>\nCase ID: case-callback-approve · Thread ID: thread-callback-approve\n\n<b>История переписки</b>\nнет\n\n<b>Вложения</b>\nнет\n\n<b>Проверка билетов / Enrichment</b>\nБилет: не найден\n\n<b>Что понял ассистент</b>\nТип обращения: Не пришёл электронный билет\nЧто хочет отправитель: Получить билет или инструкцию по восстановлению.\nСледующий шаг: Не хватает номера заказа или контактных данных для проверки.\n\n<b>Предлагаемое решение</b>\nРежим: уточнить данные\nПричина: Не хватает номера заказа или контактных данных для проверки.\n\n<b>База знаний</b>\n- Адрес отправителя электронных билетов / kb_system_ticket_sender / балл 10\n\n<b>Что не хватает</b>\n- Номер заказа или email/телефон, указанный при покупке.\n\n<b>Риски</b>\nнет\n\n<b>Черновик v2</b>\nЗдравствуйте.\nЧтобы корректно обработать обращение (Получить билет или инструкцию по восстановлению.), пожалуйста, уточните:\n- Номер заказа или email/телефон, указанный при покупке.\nПисьмо с билетами отправляется с адреса ticket@silverscreen.by.\nПосле этого мы сможем продолжить проверку.\nДополнительно: Добавь просьбу указать номер заказа.\nС уважением, команда mooon.\n\n<b>Последнее действие</b>\nутверждено",
      "action": "approve",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\telegram_operator_delivery\\case-callback-approve\\card_20260514T114517607621.json"
    },
    "operator_actions": {
      "status": "ok",
      "latest_action": {
        "uid": "callback_approve",
        "case_id": "case-callback-approve",
        "thread_id": "thread-callback-approve",
        "action": "approve",
        "operator_comment": "",
        "operator_telegram_id": "101",
        "operator_username": "demo_operator",
        "created_at": "20260514T114517567050",
        "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md#modules.draft_builder",
        "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
        "callback_data": "ma|approve|cc429fd324543ca4",
        "mock_reply_refs": [
          "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\mock_outbox\\case-callback-approve\\reply_20260514T114517569270.md",
          "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\mock_outbox\\case-callback-approve\\reply_20260514T114517569270.json"
        ],
        "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\telegram_operator_delivery\\case-callback-approve\\card_20260514T114517607621.json",
        "real_email_sent": false
      },
      "actions": [
        {
          "uid": "callback_approve",
          "case_id": "case-callback-approve",
          "thread_id": "thread-callback-approve",
          "action": "needs_edit",
          "operator_comment": "",
          "operator_telegram_id": "101",
          "operator_username": "demo_operator",
          "created_at": "20260514T114517309773",
          "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md#modules.draft_builder",
          "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
          "callback_data": "ma|needs_edit|cc429fd324543ca4",
          "mock_reply_refs": [],
          "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\telegram_operator_delivery\\case-callback-approve\\card_20260514T114517314527.json",
          "real_email_sent": false,
          "status": "waiting_operator_comment"
        },
        {
          "uid": "callback_approve",
          "case_id": "case-callback-approve",
          "thread_id": "thread-callback-approve",
          "action": "approve",
          "operator_comment": "",
          "operator_telegram_id": "101",
          "operator_username": "demo_operator",
          "created_at": "20260514T114517567050",
          "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md#modules.draft_builder",
          "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
          "callback_data": "ma|approve|cc429fd324543ca4",
          "mock_reply_refs": [
            "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\mock_outbox\\case-callback-approve\\reply_20260514T114517569270.md",
            "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\mock_outbox\\case-callback-approve\\reply_20260514T114517569270.json"
          ],
          "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\telegram_operator_delivery\\case-callback-approve\\card_20260514T114517607621.json",
          "real_email_sent": false
        }
      ],
      "real_email_sent": false
    },
    "revision_requests": {
      "status": "ok",
      "latest_request": {
        "uid": "callback_approve",
        "case_id": "case-callback-approve",
        "thread_id": "thread-callback-approve",
        "latest_revision": 1,
        "operator_comment": "Добавь просьбу указать номер заказа.",
        "operator_telegram_id": "101",
        "operator_username": "demo_operator",
        "source_callback_data": "ma|needs_edit|cc429fd324543ca4",
        "source_chat_id": "mock-operator-chat",
        "source_message_id": 7,
        "created_at": "20260514T114517375078",
        "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
        "status": "created",
        "artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\revision_requests\\case-callback-approve\\revision_request_20260514T114517375078.json"
      },
      "requests": [
        {
          "uid": "callback_approve",
          "case_id": "case-callback-approve",
          "thread_id": "thread-callback-approve",
          "latest_revision": 1,
          "operator_comment": "Добавь просьбу указать номер заказа.",
          "operator_telegram_id": "101",
          "operator_username": "demo_operator",
          "source_callback_data": "ma|needs_edit|cc429fd324543ca4",
          "source_chat_id": "mock-operator-chat",
          "source_message_id": 7,
          "created_at": "20260514T114517375078",
          "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
          "status": "created",
          "artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\revision_requests\\case-callback-approve\\revision_request_20260514T114517375078.json"
        }
      ]
    },
    "reply_sender": {
      "status": "approved_mock_not_sent",
      "to": "guest@example.test",
      "subject": "Re: Не пришёл билет",
      "uid": "callback_approve",
      "case_id": "case-callback-approve",
      "thread_id": "thread-callback-approve",
      "operator_action": {
        "uid": "callback_approve",
        "case_id": "case-callback-approve",
        "thread_id": "thread-callback-approve",
        "action": "approve",
        "operator_comment": "",
        "operator_telegram_id": "101",
        "operator_username": "demo_operator",
        "created_at": "20260514T114517567050",
        "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md#modules.draft_builder",
        "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
        "callback_data": "ma|approve|cc429fd324543ca4",
        "mock_reply_refs": [],
        "updated_card_ref": "",
        "real_email_sent": false
      },
      "final_draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить билет или инструкцию по восстановлению.), пожалуйста, уточните:\n- Номер заказа или email/телефон, указанный при покупке.\nПисьмо с билетами отправляется с адреса ticket@silverscreen.by.\nПосле этого мы сможем продолжить проверку.\nДополнительно: Добавь просьбу указать номер заказа.\nС уважением, команда mooon.",
      "draft_revision": 2,
      "timestamp": "20260514T114517569270",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\callback_fixtures\\message_callback_approve.md",
      "real_email_sent": false,
      "mock_reply_refs": [
        "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\mock_outbox\\case-callback-approve\\reply_20260514T114517569270.md",
        "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114512098843\\mock_outbox\\case-callback-approve\\reply_20260514T114517569270.json"
      ]
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
