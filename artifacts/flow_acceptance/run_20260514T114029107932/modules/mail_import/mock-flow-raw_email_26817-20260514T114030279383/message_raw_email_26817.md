# Message dossier raw_email_26817

- UID: raw_email_26817
- Message-ID: <2015231778062716@931ec2c2-2c26-4c20-b293-0968012507f7>
- Direction: inbound
- From: danilenko.sash@yandex.ru
- Subject: Re: (Без темы)
- Sent at: 2026-05-06 13:18:36+03:00
- Preferred body source: text/html
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T114029107932\modules\mail_import\mock-flow-raw_email_26817-20260514T114030279383\raw_email_raw_email_26817.eml

## Case / Thread

- Case ID: case-000003
- Thread ID: thread-000003
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
- Response mode: no_reply
- Confidence: 0.62
- Topic: Благодарность / вопрос закрыт
- Customer need: Ответ клиенту не требуется; вопрос уже закрыт, отправитель благодарит.
- Summary: Вопрос с пригласительным решён, отправитель благодарит за реакцию.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: sender thanks and confirms the issue is resolved
- Suggested next step: Проверить карточку и выбрать действие кнопками.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: danilenko.sash@yandex.ru

## Body

```
Добрый день! Вопрос с пригласительным улажен, благодарю за ваш отклик на сложившуюся ситуацию 

--
Отправлено из мобильной Яндекс Почты

 Кому: Danilenko Alexand a <danilenko.sash@yandex. u>;
 Тема: (Без темы);
04.05.2026, 18:58, "Общая mooon" <in o@mooon.by>:
 отправили информацию специалисту, ожидайте обратную связь.   ---------------- Кому: in o@mooon.by ( in o@mooon.by ); Тема: (Без темы); 04.05.2026, 17:15, "Danilenko Alexand a" < danilenko.sash@yandex. u >: 

--
Отправлено из мобильной Яндекс Почты     --  C уважением, команда mooon и Sil e Sc een
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<2015231778062716@931ec2c2-2c26-4c20-b293-0968012507f7>",
  "direction": "inbound",
  "headers": {
    "message_id": "<2015231778062716@931ec2c2-2c26-4c20-b293-0968012507f7>",
    "in_reply_to": "<10101777910254@mail.yandex.by>",
    "references": [
      "<10101777910254@mail.yandex.by>",
      "<1693811777904112@c2a5d8fa-3df2-458e-978b-30e7657e33bd>"
    ],
    "subject": "Re: (Без темы)",
    "sender": "danilenko.sash@yandex.ru",
    "sent_at": "2026-05-06 13:18:36+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Добрый день! Вопрос с пригласительным улажен, благодарю за ваш отклик на сложившуюся ситуацию \n\n--\nОтправлено из мобильной Яндекс Почты\n\n Кому: Danilenko Alexand a <danilenko.sash@yandex. u>;\n Тема: (Без темы);\n04.05.2026, 18:58, \"Общая mooon\" <in o@mooon.by>:\n отправили информацию специалисту, ожидайте обратную связь.   ---------------- Кому: in o@mooon.by ( in o@mooon.by ); Тема: (Без темы); 04.05.2026, 17:15, \"Danilenko Alexand a\" < danilenko.sash@yandex. u >: \n\n--\nОтправлено из мобильной Яндекс Почты     --  C уважением, команда mooon и Sil e Sc een",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26817-20260514T114030279383\\raw_email_raw_email_26817.eml",
  "raw_headers": "Received: from postback18a.mail.yandex.net (postback18a.mail.yandex.net [2a02:6b8:c0e:500:1:45:d181:da18])\r\n\tby bjnhvphodofzj2t6.vla.yp-c.yandex.net (notsolitesrv) with LMTPS id k4DyPW2tXJOU-3eUyMBLl;\r\n\tWed, 06 May 2026 13:18:36 +0300\nReceived: from mail-nwsmtp-mxback-production-main-31.vla.yp-c.yandex.net (mail-nwsmtp-mxback-production-main-31.vla.yp-c.yandex.net [IPv6:2a02:6b8:c2d:33a2:0:640:d702:0])\r\n\tby postback18a.mail.yandex.net (Yandex) with ESMTPS id 2F83CC02EF;\r\n\tWed, 06 May 2026 13:18:36 +0300 (MSK)\nReceived: from mail.yandex.ru (2a02:6b8:c15:2b1b:0:640:ebdd:0 [2a02:6b8:c15:2b1b:0:640:ebdd:0])\r\n\tby mail-nwsmtp-mxback-production-main-31.vla.yp-c.yandex.net (mxback) with HTTPS id VIeuhv1vlW20-vXUwRX6G;\r\n\tWed, 06 May 2026 13:18:36 +0300\nX-Yandex-Fwd: 1\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=yandex.ru; s=mail;\r\n\tt=1778062716; bh=RrnGt4VLFFWzKDnZpkZHUOo562uEWKv9vPsrMV/Pu84=;\r\n\th=Message-Id:References:Date:Subject:To:In-Reply-To:From;\r\n\tb=Tj6xbVrom9mMObBtaI3cRqhKIH0WuJv4fX1up9gMpTEGwcopwVRE8AZWKo78OAcxA\r\n\t jQdlm2lczysQlz5JEQYN5TWSQNkssK4rE4I/U/WqNEjqFXu1bkbSo2VLD9CM3xxLpz\r\n\t YqkW0DMG9hHsP2R1d4ssR9ufpYSPI7IdlMhFixEE=\nAuthentication-Results: mail-nwsmtp-mxback-production-main-31.vla.yp-c.yandex.net; dkim=pass header.i=@yandex.ru\nX-Yandex-Spam: 1\nReceived: by tbolwgpj3odg7fdr.vla.yp-c.yandex.net (sendbernar) with HTTPS id 92ce06ae372b28c73e255caae8f51a9b;\r\n\tWed, 06 May 2026 13:18:36 +0300\nFrom: Danilenko Alexandra <danilenko.sash@yandex.ru>\nTo: =?utf-8?B?0J7QsdGJ0LDRjyBtb29vbg==?= <info@mooon.by>\nIn-Reply-To: <10101777910254@mail.yandex.by>\nReferences: <10101777910254@mail.yandex.by> <1693811777904112@c2a5d8fa-3df2-458e-978b-30e7657e33bd>\nSubject: =?utf-8?B?UmU6ICjQkdC10Lcg0YLQtdC80Ysp?=\nMIME-Version: 1.0\nX-Mailer: Yamail [ http://yandex.ru ] 5.0\nDate: Wed, 06 May 2026 13:18:36 +0300\nMessage-Id: <2015231778062716@931ec2c2-2c26-4c20-b293-0968012507f7>\nContent-Transfer-Encoding: base64\nContent-Type: text/html; charset=utf-8\nReturn-Path: danilenko.sash@yandex.ru\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26817",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Добрый день! Вопрос с пригласительным улажен, благодарю за ваш отклик на сложившуюся ситуацию \n\n--\nОтправлено из мобильной Яндекс Почты\n\n Кому: Danilenko Alexand a <danilenko.sash@yandex. u>;\n Тема: (Без темы);\n04.05.2026, 18:58, \"Общая mooon\" <in o@mooon.by>:\n отправили информацию специалисту, ожидайте обратную связь.   ---------------- Кому: in o@mooon.by ( in o@mooon.by ); Тема: (Без темы); 04.05.2026, 17:15, \"Danilenko Alexand a\" < danilenko.sash@yandex. u >: \n\n--\nОтправлено из мобильной Яндекс Почты     --  C уважением, команда mooon и Sil e Sc een",
  "has_text_plain": false,
  "has_text_html": true,
  "preferred_body_source": "text/html",
  "body_sources": [
    "text/html"
  ],
  "mime_parts": [
    {
      "part_index": 0,
      "content_type": "text/html",
      "content_disposition": "",
      "filename": "",
      "content_id": "",
      "charset": "utf-8",
      "is_multipart": false,
      "size_bytes": 1184,
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
      "uid": "raw_email_26817",
      "message_id": "<2015231778062716@931ec2c2-2c26-4c20-b293-0968012507f7>",
      "subject": "Re: (Без темы)",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26817-20260514T114030279383\\raw_email_raw_email_26817.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26817-20260514T114030279383\\message_raw_email_26817.md",
      "items": []
    },
    "early_classification": {
      "uid": "raw_email_26817",
      "status": "ok",
      "classification": "gratitude_or_case_closed",
      "operator_summary": "Вопрос с пригласительным решён, отправитель благодарит за реакцию.",
      "case_summary_short": "Вопрос с пригласительным решён, отправитель благодарит за реакцию.",
      "should_run_ticket_enrichment": false,
      "should_run_customer_kb": false,
      "should_build_customer_draft": false,
      "response_mode_hint": "no_reply",
      "proposed_action_type": "",
      "proposed_action_text": "",
      "action_stub_allowed": false,
      "classification_reason": "sender thanks and confirms the issue is resolved",
      "sender_email": "danilenko.sash@yandex.ru",
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
        "uid": "raw_email_26817",
        "message_id": "<2015231778062716@931ec2c2-2c26-4c20-b293-0968012507f7>",
        "subject": "Re: (Без темы)",
        "lookup_emails": [
          "o@mooon.by",
          "danilenko.sash@yandex.ru"
        ],
        "selected_lookup_email": "",
        "ticket_db_status": "skipped",
        "crm_users_status": "stub",
        "payment_refund_status": "stub",
        "confidence": "none",
        "candidates_count": 0,
        "resolved_match": null,
        "note": "ticket enrichment skipped: sender thanks and confirms the issue is resolved"
      },
      "debug": {
        "uid": "raw_email_26817",
        "message_id": "<2015231778062716@931ec2c2-2c26-4c20-b293-0968012507f7>",
        "subject": "Re: (Без темы)",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26817-20260514T114030279383\\message_raw_email_26817.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26817-20260514T114030279383\\message_raw_email_26817.md"
        },
        "lookup_keys": {
          "sender_email_reference": "danilenko.sash@yandex.ru",
          "body_emails": [
            "o@mooon.by"
          ],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "o@mooon.by",
            "danilenko.sash@yandex.ru"
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
              "sender thanks and confirms the issue is resolved"
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
          "lookup_emails_total": 2,
          "confidence": "none",
          "skip_reason": "sender thanks and confirms the issue is resolved"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26817",
      "message_id": "<2015231778062716@931ec2c2-2c26-4c20-b293-0968012507f7>",
      "direction": "inbound",
      "sender": "danilenko.sash@yandex.ru",
      "subject": "Re: (Без темы)",
      "case_id": "case-000003",
      "thread_id": "thread-000003",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\state\\case_thread_registry.xlsx",
      "registry_row_number": 4,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "<10101777910254@mail.yandex.by>",
        "references": [
          "<10101777910254@mail.yandex.by>",
          "<1693811777904112@c2a5d8fa-3df2-458e-978b-30e7657e33bd>"
        ]
      },
      "thread_history": [
        {
          "message_id": "<2015231778062716@931ec2c2-2c26-4c20-b293-0968012507f7>",
          "direction": "inbound",
          "sender": "danilenko.sash@yandex.ru",
          "subject": "Re: (Без темы)",
          "sent_at": "2026-05-06 13:18:36+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26817-20260514T114030279383\\message_raw_email_26817.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26817",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Вопрос с пригласительным решён, отправитель благодарит за реакцию.",
        "topic": "Благодарность / вопрос закрыт",
        "customer_need": "Ответ клиенту не требуется; вопрос уже закрыт, отправитель благодарит.",
        "entities": [
          {
            "type": "sender",
            "value": "danilenko.sash@yandex.ru"
          }
        ],
        "confidence": 0.62,
        "response_mode": "no_reply",
        "understanding_note": "Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.",
        "response_mode_reason": "sender thanks and confirms the issue is resolved",
        "suggested_next_step": "Проверить карточку и выбрать действие кнопками.",
        "risk_level": "medium",
        "needs_human": false
      }
    },
    "knowledge_retrieval": {
      "uid": "raw_email_26817",
      "status": "skipped",
      "error": "",
      "reason": "sender thanks and confirms the issue is resolved",
      "classification": "gratitude_or_case_closed",
      "query": {
        "text": "",
        "response_mode": "no_reply",
        "entities": []
      },
      "matched_items": [],
      "routing_matches": [],
      "settings": {}
    },
    "decision_layer": {
      "uid": "raw_email_26817",
      "status": "ok",
      "error": "",
      "response_mode_initial": "no_reply",
      "response_mode_final": "no_reply",
      "decision_reason": "Вопрос с пригласительным решён, отправитель благодарит за реакцию.",
      "missing_data": [],
      "risks": [],
      "knowledge_item_ids": [],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Вопрос с пригласительным решён, отправитель благодарит за реакцию.",
      "case_summary_short": "Вопрос с пригласительным решён, отправитель благодарит за реакцию.",
      "classification": "gratitude_or_case_closed",
      "should_build_customer_draft": false,
      "proposed_action_type": "",
      "proposed_action_text": "",
      "action_stub_allowed": false,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26817",
      "status": "skipped",
      "error": "",
      "skip_reason": "Черновик не создавался: ответ клиенту не требуется.",
      "draft_type": "no_reply",
      "latest_revision": 0,
      "draft_text": "",
      "operator_note": "Черновик не создавался: ответ клиенту не требуется.",
      "source_response_mode": "no_reply",
      "created_at": "2026-05-14T11:40:30.536513+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26817-20260514T114030279383\\message_raw_email_26817.md",
      "revisions": [],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "skipped",
        "decision_layer_status": "ok",
        "knowledge_item_ids": []
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26817",
      "status": "mock_sent",
      "error": "",
      "created_at": "2026-05-14T11:40:30.567005+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26817-20260514T114030279383\\message_raw_email_26817.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26817-20260514T114030279383\\message_raw_email_26817.md",
      "case_id": "case-000003",
      "thread_id": "thread-000003",
      "telegram_message_id": 3,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "artifact_only",
      "telegram_operations": [],
      "callback_data": [
        "ma|approve|9610b7388d4ab5b9",
        "ma|needs_edit|9610b7388d4ab5b9",
        "ma|handoff|9610b7388d4ab5b9",
        "ma|ignore|9610b7388d4ab5b9"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|9610b7388d4ab5b9"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|9610b7388d4ab5b9"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|9610b7388d4ab5b9"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|9610b7388d4ab5b9"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: raw_email_26817\nПолучено: 06.05.2026 13:18\nОт: danilenko.sash@yandex.ru\nТема письма: Re: (Без темы)\nСуть обращения: Вопрос с пригласительным решён, отправитель благодарит за реакцию.\n\n<b>Кейс</b>\nCase ID: case-000003 · Thread ID: thread-000003\n\n<b>История переписки</b>\n- входящее · 2026-05-06 13:18 · Re: (Без темы) · Вопрос с пригласительным решён, отправитель благодарит за реакцию.\n\n<b>Вложения</b>\nнет\n\n<b>Проверка билетов / Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: благодарность / вопрос закрыт\nЧто хочет отправитель: Ответ клиенту не требуется; вопрос уже закрыт, отправитель благодарит.\nСледующий шаг: Вопрос с пригласительным решён, отправитель благодарит за реакцию.\n\n<b>Предлагаемое решение</b>\nРежим: не отвечать\nПричина: Вопрос с пригласительным решён, отправитель благодарит за реакцию.\n\n<b>База знаний</b>\nне применялась — письмо не требует клиентской базы знаний по билетам.\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\nнет\n\n<b>Черновик</b>\nЧерновик не создавался: ответ клиенту не требуется.",
      "action": "",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\telegram_operator_delivery\\case-000003\\card_20260514T114030567123.json"
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
