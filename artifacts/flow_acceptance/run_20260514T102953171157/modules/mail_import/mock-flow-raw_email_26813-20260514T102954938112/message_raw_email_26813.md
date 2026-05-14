# Message dossier raw_email_26813

- UID: raw_email_26813
- Message-ID: <2099806958.3267.1778050892115@dc2ac00.ps>
- Direction: inbound
- From: support@belassist.by
- Subject: Плановые работы - ОАО "Банковский процессинговый центр" 07.05.2026
- Sent at: 2026-05-06 07:01:32+00:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T102953171157\modules\mail_import\mock-flow-raw_email_26813-20260514T102954938112\raw_email_raw_email_26813.eml

## Case / Thread

- Case ID: case-000005
- Thread ID: thread-000005
- Binding rule: new_case_thread
- Binding status: new_case_thread

## Enrichment

- Ticket DB status: <empty>
- Selected lookup email: <empty>
- Resolved ticket: <empty>

## Attachments

- Count: 0
- Text found in: 0

## LLM Understanding

- Status: ok
- Response mode: handoff_to_operator
- Confidence: 0.62
- Topic: Служебное уведомление, требующее действия
- Customer need: Зафиксировать служебное уведомление и уведомить ответственных stub-действием.
- Summary: BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: payment provider / banking processing center operational notice
- Suggested next step: Переслать уведомление в ответственный чат по платёжным алертам.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: support@belassist.by

## Body

```
Уважаемые клиенты!

Уведомляем Вас о том, что 07.05.2026 в 06:00 и в 23:30 (МСК) ОАО "Банковский процессинговый центр" будет проводить плановые технологические работы. В указанное время возможен перерыв в проведении платежей по банковским картам до 1 минуты.

Просим Вас учесть данную информацию в работе.
--
С уважением,
ООО "Компания Электронных Платежей "АССИСТ"
support@belassist.by
www.belassist.by
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<2099806958.3267.1778050892115@dc2ac00.ps>",
  "direction": "inbound",
  "headers": {
    "message_id": "<2099806958.3267.1778050892115@dc2ac00.ps>",
    "in_reply_to": "",
    "references": [],
    "subject": "Плановые работы - ОАО \"Банковский процессинговый центр\" 07.05.2026",
    "sender": "support@belassist.by",
    "sent_at": "2026-05-06 07:01:32+00:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Уважаемые клиенты!\r\n\r\nУведомляем Вас о том, что 07.05.2026 в 06:00 и в 23:30 (МСК) ОАО \"Банковский процессинговый центр\" будет проводить плановые технологические работы. В указанное время возможен перерыв в проведении платежей по банковским картам до 1 минуты.\r\n\r\nПросим Вас учесть данную информацию в работе.\n--\r\nС уважением,\r\nООО \"Компания Электронных Платежей \"АССИСТ\"\r\nsupport@belassist.by\r\nwww.belassist.by",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\raw_email_raw_email_26813.eml",
  "raw_headers": "Received: from postback6d.mail.yandex.net (postback6d.mail.yandex.net [2a02:6b8:c41:1300:1:45:d181:da06])\r\n\tby mail-notsolitesrv-production-main-38.klg.yp-c.yandex.net (notsolitesrv) with LMTPS id djFBjKNhjwpG-5MtFNiPD\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 10:01:33 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-83.iva.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-83.iva.yp-c.yandex.net [IPv6:2a02:6b8:c0c:8911:0:640:81aa:0])\r\n\tby postback6d.mail.yandex.net (Yandex) with ESMTPS id 1915EC0014\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 10:01:33 +0300 (MSK)\nReceived: from relay07.paysecure.ru (relay07.paysecure.ru [195.50.5.76])\r\n\tby mail-nwsmtp-mxfront-production-main-83.iva.yp-c.yandex.net (mxfront) with ESMTPS id W1bRJN4LZuQ0-6P2YJRIg;\r\n\tWed, 06 May 2026 10:01:32 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-83.iva.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-83.iva.yp-c.yandex.net: domain of belassist.by designates 195.50.5.76 as permitted sender, rule=[ip4:195.50.5.64/28]) smtp.mail=crm-bounce-mailing@belassist.by\nX-Yandex-Spam: 1\nReceived: from localhost (127.0.0.1)\r\n\tby relay07.paysecure.ru with esmtp (Exim 4.96)\r\n\t(envelope-from <crm-bounce-mailing@belassist.by>)\r\n\tid 1wKWGC-00A1h4-0W\r\n\tfor info@mooon.by;\r\n\tWed, 06 May 2026 07:01:32 +0000\nReceived: from localhost ([127.0.0.1] helo=dc2ac00.ps)\r\n\tby dc2ac00.ps with esmtp (Exim 4.96)\r\n\t(envelope-from <crm-bounce-mailing@belassist.by>)\r\n\tid 1wKWGC-000nUQ-0P\r\n\tfor info@mooon.by;\r\n\tWed, 06 May 2026 07:01:32 +0000\nDate: Wed, 6 May 2026 07:01:32 +0000 (UTC)\nFrom: BELASSIST <support@belassist.by>\nTo: info@mooon.by\nMessage-ID: <2099806958.3267.1778050892115@dc2ac00.ps>\nSubject: =?utf-8?B?0J/Qu9Cw0L3QvtCy0YvQtSDRgNCw0LHQvtGC0Ysg?=\r\n =?utf-8?B?LSDQntCQ0J4gItCR0LDQvdC60L7QstGB0LrQuNC5?=\r\n =?utf-8?B?INC/0YDQvtGG0LXRgdGB0LjQvdCz0L7QstGL0Lkg?=\r\n =?utf-8?B?0YbQtdC90YLRgCIgMDcuMDUuMjAyNg==?=\nMIME-Version: 1.0\nContent-Type: multipart/mixed; \r\n\tboundary=\"----=_Part_3266_773052791.1778050892115\"\nX-Priority: 3\nX-MSMail-Priority: Normal\nX-Mailer: Assist mailer v2.4.1\nReturn-Path: crm-bounce-mailing@belassist.by\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26813",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Уважаемые клиенты!\r\n\r\nУведомляем Вас о том, что 07.05.2026 в 06:00 и в 23:30 (МСК) ОАО \"Банковский процессинговый центр\" будет проводить плановые технологические работы. В указанное время возможен перерыв в проведении платежей по банковским картам до 1 минуты.\r\n\r\nПросим Вас учесть данную информацию в работе.\n--\r\nС уважением,\r\nООО \"Компания Электронных Платежей \"АССИСТ\"\r\nsupport@belassist.by\r\nwww.belassist.by",
  "has_text_plain": true,
  "has_text_html": false,
  "preferred_body_source": "text/plain",
  "body_sources": [
    "text/plain"
  ],
  "mime_parts": [
    {
      "part_index": 0,
      "content_type": "multipart/mixed",
      "content_disposition": "",
      "filename": "",
      "content_id": "",
      "charset": "",
      "is_multipart": true,
      "size_bytes": 0,
      "is_inline": false,
      "is_attachment": false
    },
    {
      "part_index": 1,
      "content_type": "text/plain",
      "content_disposition": "",
      "filename": "",
      "content_id": "",
      "charset": "utf-8",
      "is_multipart": false,
      "size_bytes": 687,
      "is_inline": false,
      "is_attachment": false
    }
  ],
  "has_attachments": false,
  "has_inline_parts": false,
  "attachments_inventory": [],
  "is_bounce": false,
  "is_auto_reply": false,
  "is_mailing_like": false,
  "is_system_generated_likely": false,
  "bounce_reasons": [],
  "auto_reply_reasons": [],
  "mailing_like_reasons": [],
  "system_generated_reasons": [],
  "modules": {
    "mail_import": {
      "status": "ok",
      "note": "mail_import completed"
    },
    "attachment_extraction": {
      "uid": "raw_email_26813",
      "message_id": "<2099806958.3267.1778050892115@dc2ac00.ps>",
      "subject": "Плановые работы - ОАО \"Банковский процессинговый центр\" 07.05.2026",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\raw_email_raw_email_26813.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md",
      "items": []
    },
    "early_classification": {
      "uid": "raw_email_26813",
      "status": "ok",
      "classification": "action_required_notification",
      "operator_summary": "BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.",
      "case_summary_short": "BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.",
      "should_run_ticket_enrichment": false,
      "should_run_customer_kb": false,
      "should_build_customer_draft": false,
      "response_mode_hint": "handoff_to_operator",
      "proposed_action_type": "forward_to_chat_stub",
      "proposed_action_text": "Переслать уведомление в ответственный чат по платёжным алертам.",
      "action_stub_allowed": true,
      "classification_reason": "payment provider / banking processing center operational notice",
      "sender_email": "support@belassist.by",
      "own_sender_or_recipient": false,
      "recipient_emails": [
        "info@mooon.by",
        "no-reply@mooon.by",
        "noreply@mooon.by",
        "support@mooon.by"
      ],
      "attachment_count": 0
    },
    "identity_context_enrichment": {
      "result": {
        "uid": "raw_email_26813",
        "message_id": "<2099806958.3267.1778050892115@dc2ac00.ps>",
        "subject": "Плановые работы - ОАО \"Банковский процессинговый центр\" 07.05.2026",
        "lookup_emails": [
          "support@belassist.by"
        ],
        "selected_lookup_email": "",
        "ticket_db_status": "skipped",
        "crm_users_status": "stub",
        "payment_refund_status": "stub",
        "confidence": "none",
        "candidates_count": 0,
        "resolved_match": null,
        "note": "ticket enrichment skipped: payment provider / banking processing center operational notice"
      },
      "debug": {
        "uid": "raw_email_26813",
        "message_id": "<2099806958.3267.1778050892115@dc2ac00.ps>",
        "subject": "Плановые работы - ОАО \"Банковский процессинговый центр\" 07.05.2026",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md"
        },
        "lookup_keys": {
          "sender_email_reference": "support@belassist.by",
          "body_emails": [
            "support@belassist.by"
          ],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "support@belassist.by"
          ],
          "selected_lookup_email": "",
          "selected_lookup_localpart": ""
        },
        "providers": {
          "ticket_db": {
            "status": "skipped",
            "settings_source": "",
            "candidates": [],
            "notes": [
              "payment provider / banking processing center operational notice"
            ],
            "query_email": "",
            "query_localpart": "",
            "lookup_trace": []
          },
          "crm_users": {
            "provider": "crm_users",
            "status": "stub",
            "rows": [],
            "notes": [
              "not implemented yet"
            ]
          },
          "payment_refund": {
            "provider": "payment_refund",
            "status": "stub",
            "rows": [],
            "notes": [
              "not implemented yet"
            ]
          }
        },
        "resolved_match": null,
        "summary": {
          "ticket_found": false,
          "ticket_db_status": "skipped",
          "crm_users_status": "stub",
          "payment_refund_status": "stub",
          "attachment_report_present": true,
          "body_emails_found": 1,
          "lookup_emails_total": 1,
          "confidence": "none",
          "skip_reason": "payment provider / banking processing center operational notice"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26813",
      "message_id": "<2099806958.3267.1778050892115@dc2ac00.ps>",
      "direction": "inbound",
      "sender": "support@belassist.by",
      "subject": "Плановые работы - ОАО \"Банковский процессинговый центр\" 07.05.2026",
      "case_id": "case-000005",
      "thread_id": "thread-000005",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\state\\case_thread_registry.xlsx",
      "registry_row_number": 6,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "",
        "references": []
      },
      "thread_history": [
        {
          "message_id": "<2099806958.3267.1778050892115@dc2ac00.ps>",
          "direction": "inbound",
          "sender": "support@belassist.by",
          "subject": "Плановые работы - ОАО \"Банковский процессинговый центр\" 07.05.2026",
          "sent_at": "2026-05-06 07:01:32+00:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26813",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.",
        "topic": "Служебное уведомление, требующее действия",
        "customer_need": "Зафиксировать служебное уведомление и уведомить ответственных stub-действием.",
        "entities": [
          {
            "type": "sender",
            "value": "support@belassist.by"
          }
        ],
        "confidence": 0.62,
        "response_mode": "handoff_to_operator",
        "understanding_note": "Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.",
        "response_mode_reason": "payment provider / banking processing center operational notice",
        "suggested_next_step": "Переслать уведомление в ответственный чат по платёжным алертам.",
        "risk_level": "medium",
        "needs_human": true
      }
    },
    "knowledge_retrieval": {
      "uid": "raw_email_26813",
      "status": "skipped",
      "error": "",
      "reason": "payment provider / banking processing center operational notice",
      "classification": "action_required_notification",
      "query": {
        "text": "",
        "response_mode": "handoff_to_operator",
        "entities": []
      },
      "matched_items": [],
      "routing_matches": [],
      "settings": {}
    },
    "decision_layer": {
      "uid": "raw_email_26813",
      "status": "ok",
      "error": "",
      "response_mode_initial": "handoff_to_operator",
      "response_mode_final": "handoff_to_operator",
      "decision_reason": "BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.",
      "missing_data": [],
      "risks": [
        "Реальная маршрутизация пока не подключена; доступно только stub-действие."
      ],
      "knowledge_item_ids": [],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.",
      "case_summary_short": "BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.",
      "classification": "action_required_notification",
      "should_build_customer_draft": false,
      "proposed_action_type": "forward_to_chat_stub",
      "proposed_action_text": "Переслать уведомление в ответственный чат по платёжным алертам.",
      "action_stub_allowed": true,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26813",
      "status": "skipped",
      "error": "",
      "skip_reason": "Черновик не создавался: это служебное уведомление, нужен только внутренний action.",
      "draft_type": "handoff_to_operator",
      "latest_revision": 0,
      "draft_text": "",
      "operator_note": "Черновик не создавался: это служебное уведомление, нужен только внутренний action.",
      "source_response_mode": "handoff_to_operator",
      "created_at": "2026-05-14T10:29:55.099249+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md",
      "revisions": [],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "skipped",
        "decision_layer_status": "ok",
        "knowledge_item_ids": []
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26813",
      "status": "action_action_request",
      "error": "",
      "created_at": "2026-05-14T10:31:21.074859+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md",
      "case_id": "case-000005",
      "thread_id": "thread-000005",
      "telegram_message_id": 5,
      "telegram_chat_id": 12345,
      "telegram_delivery_mode": "telegram_bot_api",
      "telegram_operations": [
        {
          "operation": "editMessageText",
          "ok": true,
          "message_id": 5,
          "chat_id": 12345
        },
        {
          "operation": "editMessageReplyMarkup",
          "ok": true,
          "message_id": 5,
          "chat_id": 12345
        },
        {
          "operation": "answerCallbackQuery",
          "ok": true,
          "result": true,
          "text": "Действие зафиксировано. Реальная маршрутизация пока не подключена."
        }
      ],
      "callback_data": [
        "ma|approve|8efb7c94681901e8",
        "ma|needs_edit|8efb7c94681901e8",
        "ma|handoff|8efb7c94681901e8",
        "ma|ignore|8efb7c94681901e8",
        "ma|action_request|8efb7c94681901e8"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|8efb7c94681901e8"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|8efb7c94681901e8"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|8efb7c94681901e8"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|8efb7c94681901e8"
        },
        {
          "action": "action_request",
          "label": "⚡ Выполнить действие",
          "callback_data": "ma|action_request|8efb7c94681901e8"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n⚡ Действие зафиксировано. Реальная маршрутизация пока не подключена.\n\n<b>Письмо</b>\nUID: raw_email_26813\nПолучено: 06.05.2026 10:01\nОт: support@belassist.by\nТема письма: Плановые работы - ОАО \"Банковский процессинговый центр\" 07.05.2026\nСуть обращения: BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.\n\n<b>Кейс</b>\nCase ID: case-000005 · Thread ID: thread-000005\n\n<b>История переписки</b>\n- входящее · 2026-05-06 07:01 · Плановые работы - ОАО \"Банковский процесс… · BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратко…\n\n<b>Вложения</b>\nнет\n\n<b>Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: служебное уведомление, требуется действие\nЧто хочет отправитель: Зафиксировать служебное уведомление и уведомить ответственных stub-действием.\nЧто предлагает система: BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.\n\n<b>Что предлагает система</b>\nРежим: передать оператору\nПричина: BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей.\n\n<b>Предлагаемое действие</b>\nПереслать уведомление в ответственный чат по платёжным алертам.\nТип действия: forward_to_chat_stub\n\n<b>База знаний</b>\nне применялась — письмо не является клиентским обращением по билетам.\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\n- Реальная маршрутизация пока не подключена; доступно только stub-действие.\n\n<b>Черновик</b>\nЧерновик не создавался: это служебное уведомление, нужен только внутренний action.\n\n<b>Последнее действие</b>\nstub-действие зафиксировано",
      "action": "action_request",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\telegram_operator_delivery\\case-000005\\card_20260514T103121075021.json"
    },
    "operator_actions": {
      "status": "ok",
      "latest_action": {
        "uid": "raw_email_26813",
        "case_id": "case-000005",
        "thread_id": "thread-000005",
        "action": "action_requested",
        "operator_comment": "",
        "operator_telegram_id": "42",
        "operator_username": "tester",
        "created_at": "20260514T103121073144",
        "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md#modules.draft_builder",
        "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md",
        "callback_data": "ma|action_request|8efb7c94681901e8",
        "mock_reply_refs": [],
        "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\telegram_operator_delivery\\case-000005\\card_20260514T103121075021.json",
        "real_email_sent": false,
        "action_type": "forward_to_chat_stub",
        "status": "stub_recorded",
        "real_routing": false,
        "proposed_action_text": "Переслать уведомление в ответственный чат по платёжным алертам."
      },
      "actions": [
        {
          "uid": "raw_email_26813",
          "case_id": "case-000005",
          "thread_id": "thread-000005",
          "action": "action_requested",
          "operator_comment": "",
          "operator_telegram_id": "42",
          "operator_username": "tester",
          "created_at": "20260514T103121073144",
          "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md#modules.draft_builder",
          "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\modules\\mail_import\\mock-flow-raw_email_26813-20260514T102954938112\\message_raw_email_26813.md",
          "callback_data": "ma|action_request|8efb7c94681901e8",
          "mock_reply_refs": [],
          "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102953171157\\telegram_operator_delivery\\case-000005\\card_20260514T103121075021.json",
          "real_email_sent": false,
          "action_type": "forward_to_chat_stub",
          "status": "stub_recorded",
          "real_routing": false,
          "proposed_action_text": "Переслать уведомление в ответственный чат по платёжным алертам."
        }
      ],
      "real_email_sent": false
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
