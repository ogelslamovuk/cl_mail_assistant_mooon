# Message dossier raw_email_26820

- UID: raw_email_26820
- Message-ID: <CAAT5JNyYBBUkqE_v8LLqXzKuSF_h=jt+c=NC8z0HdCBbvAbQiw@mail.gmail.com>
- Direction: inbound
- From: cukarevamasa1@gmail.com
- Subject: <empty>
- Sent at: 2026-05-06 16:36:07+03:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T124727595245\modules\mail_import\mock-flow-raw_email_26820-20260514T124740264087\raw_email_raw_email_26820.eml

## Case / Thread

- Case ID: case-000006
- Thread ID: thread-000006
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
- Topic: Кандидат или портфолио
- Customer need: Передать предложение/портфолио ответственным на ручную обработку.
- Summary: Мария, студентка маркетинга БГУ, просит пройти двухнедельную бесплатную аналитическую практику.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: candidate/practice/portfolio wording
- Suggested next step: Передать запрос ответственным за практику/HR или маркетинг.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: cukarevamasa1@gmail.com

## Body

```
Здравствуйте! Меня зовут Мария, я учусь на маркетинге в институте бизнеса
БГУ, ищу себе аналитическую практику. Очень хотела бы попасть к вам в
компанию на две недели на бесплатной основе. Куда можно обратиться по этому
вопросу?
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<CAAT5JNyYBBUkqE_v8LLqXzKuSF_h=jt+c=NC8z0HdCBbvAbQiw@mail.gmail.com>",
  "direction": "inbound",
  "headers": {
    "message_id": "<CAAT5JNyYBBUkqE_v8LLqXzKuSF_h=jt+c=NC8z0HdCBbvAbQiw@mail.gmail.com>",
    "in_reply_to": "",
    "references": [],
    "subject": "",
    "sender": "cukarevamasa1@gmail.com",
    "sent_at": "2026-05-06 16:36:07+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Здравствуйте! Меня зовут Мария, я учусь на маркетинге в институте бизнеса\r\nБГУ, ищу себе аналитическую практику. Очень хотела бы попасть к вам в\r\nкомпанию на две недели на бесплатной основе. Куда можно обратиться по этому\r\nвопросу?",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26820-20260514T124740264087\\raw_email_raw_email_26820.eml",
  "raw_headers": "Received: from postback17b.mail.yandex.net (postback17b.mail.yandex.net [2a02:6b8:c02:900:1:45:d181:da17])\r\n\tby tzjn5bhp3dymwlvf.sas.yp-c.yandex.net (notsolitesrv) with LMTPS id KS5vxVjZ9mCj-xlYXjvUd\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 16:37:10 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-90.sas.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-90.sas.yp-c.yandex.net [IPv6:2a02:6b8:c23:294a:0:640:6196:0])\r\n\tby postback17b.mail.yandex.net (Yandex) with ESMTPS id 488C8C00DF\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 16:37:10 +0300 (MSK)\nReceived: from mail-pj1-x102f.google.com (mail-pj1-x102f.google.com [2607:f8b0:4864:20::102f])\r\n\tby mail-nwsmtp-mxfront-production-main-90.sas.yp-c.yandex.net (mxfront) with ESMTPS id 8bhJm38KCOs0-AEbiCRF6;\r\n\tWed, 06 May 2026 16:37:09 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-90.sas.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-90.sas.yp-c.yandex.net: domain of gmail.com designates 2607:f8b0:4864:20::102f as permitted sender, rule=[ip6:2607:f8b0:4864::/56]) smtp.mail=cukarevamasa1@gmail.com; dkim=pass header.i=@gmail.com\nX-Yandex-Spam: 1\nReceived: by mail-pj1-x102f.google.com with SMTP id 98e67ed59e1d1-362e30526f8so2744475a91.3\r\n        for <info@mooon.by>; Wed, 06 May 2026 06:37:09 -0700 (PDT)\nARC-Seal: i=1; a=rsa-sha256; t=1778074627; cv=none;\r\n        d=google.com; s=arc-20240605;\r\n        b=W2zcFkQ+tvIlZGmvQDz7Ko2EdVoB7xbZpZYQX4u2VOZwFFR3gRZtbM83oWMhxu91n8\r\n         3Xehs9sZOdD5MTaaEtkBnC3vAAvkmCwvmdKrFC6Z9e5D8AT0saT73aBIPOHQSFwq+F+c\r\n         +/GvlSWY4Lw75AnaYuOlcEP0BzZ8IrineebIHa2vE8ypASwPsbprwmw/sVqTTX9PHHzo\r\n         2/DM8dmmJyR/NxqiA5oEUDtOaUAobK/DNd6PSf2nvNkOfSrQMa9mS5nza6zFAFbr8Ter\r\n         DPf73+3T/n93jDE4K2Z9MuMT2yNayKALu1B/PkozqQxjy9eeSOXlw+g/JhwXDK+T0nga\r\n         pe9g==\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;\r\n        h=to:subject:message-id:date:from:mime-version:dkim-signature;\r\n        bh=5dMNn+z4/HUts0KDTm0kjonc63/8xb5NrsqxVNcnd58=;\r\n        fh=DFpNV6sNijizt1AwqqxcY2JMLszXwwNyEEKoHuk5Kmw=;\r\n        b=iegtXG84ZYz9GUmc9GfIzIiFO/RxSLjo/oe6mM6AEa51R21f9d1XGBGx/DL6LZ8XD2\r\n         gaWkQOK1wBcxJZPUzEFiHkl1Z1xw+btmjSS4ngwMX+sp1UGf5EsqZSuK6b8bl8uH6VaU\r\n         isT7EKdip028erBBYiGfnkqBTg4RhNEoTa966AxKa3WdEDiacm7/224kK85RCzuqhi8a\r\n         cOXXghG0xPgU/bfEQT0slVrQlMdVTCT/h8nF/LjgdBBfP63rihhovWHy2Mq1ySunpqQq\r\n         p9yGk2p3sDxZGscy+JCl3WATiSipHqzposL4hhf/aiB534zykZUzy4NxCWRneQAdZiM/\r\n         ONiA==;\r\n        darn=mooon.by\nARC-Authentication-Results: i=1; mx.google.com; arc=none\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=gmail.com; s=20251104; t=1778074627; x=1778679427; darn=mooon.by;\r\n        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject\r\n         :date:message-id:reply-to;\r\n        bh=5dMNn+z4/HUts0KDTm0kjonc63/8xb5NrsqxVNcnd58=;\r\n        b=BuRM0q0Vl9myQVISwZMbfJk7XUDhGBDbCLLdioGoKMO8mDnlBcGCK7TYpemYqckp0W\r\n         iS+Xd3L3+oz1CObe+1Flubiw//vLK6agVN3iLKbMB8Np8cpSxGphGmlWcV8ixLYRJ82k\r\n         ZlI5OmuwaiqRxWeZdIcXObSgFz751nAa25vx7SyERuoFj2cVn81LpKwJZ9BpTfCvegBL\r\n         GrwAOKcbCMZv/qg/zHZVZXsA/zTiJGHgGb4wxOomgzNZYmYNE9n6U90JxVN1t1yo/ysj\r\n         24M51GSpBKL33Ws39gswk+9t/p+Kqnq80WT6IsEVMlVoFVPQHIDKiQJbsUne9OQSEuSC\r\n         TxGg==\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20251104; t=1778074627; x=1778679427;\r\n        h=to:subject:message-id:date:from:mime-version:x-gm-gg\r\n         :x-gm-message-state:from:to:cc:subject:date:message-id:reply-to;\r\n        bh=5dMNn+z4/HUts0KDTm0kjonc63/8xb5NrsqxVNcnd58=;\r\n        b=rUrYjTC3Hm8C/MjI02btpFmOFL4IbbWiyPceKMgfUoPNoQyIJSFNZ009Vvzhz1PkbX\r\n         P3E0dj8dgbY3a1IWIScZ7XChvVw8/gFc+AlG6qlHMNwtV4jXkBXVVNQ/GV+vw4ba5nf/\r\n         VF+M/eKjj+neBqN9MbOqT7ILgDOEReMnUZAp0z9VfOA/Xq5aWZhs+HGJLsJpWgmsP4YO\r\n         8xavPiR5VRWBumaRbHiyDxV7ej8hQXCxhZRwRfJsGPALgsR3GnAFw5G7KuM93Jh7JSFd\r\n         RlwUVmbm17VI56zA/fdhIgmLCOtsesatPBCcHm+3N/405lspmUOz+PMU6hPdk81RoYaM\r\n         Q7Sw==\nX-Gm-Message-State: AOJu0Yx0OvA1gHvl3JtLhkg2kXkeXPRV4a+gzJFAnAWdjJ2xV+tP6aTy\r\n\t1dCd/NSE8ZrrKn5xSajuA/8hWGRuwjtwtL06sA50InPyzMilooelZAvgq+8t/8dZ6gxJW9JQMZa\r\n\t9pwB93kfJUysKuVmgFFdAAE1l+YXCeflYFHyq4UDzqw==\nX-Gm-Gg: AeBDieu/a9cClubdbSBqAeBUcxpF3mfok2n8qJ/6re5y/cGF+E0TVRAx9Po4d8cob/v\r\n\tOk/igOS52R8Ao5+sEgBoSA1TO6oPztDXbzO8XFBV+ZH8ved8XDYFGwj5Nl4kRkPBcgOp9W7EA7i\r\n\tzBdIR2JX4fXCRttymgPbBeIme9yxynRSL+GypvlMwigwRRnVO51HmwS0xYUeuWkfklv98l8w5B2\r\n\tYgTp+3y46EItO0e98G35tdH78VU363bRlQdQk70PmYOydRPSNhFmS+pbN9DpQBAe1xLZ/qZw0FL\r\n\tM01K9a3PHp0wPui8vQ==\nX-Received: by 2002:a17:90b:1646:b0:35f:b50e:defc with SMTP id\r\n 98e67ed59e1d1-365ac080794mr3563830a91.16.1778074627373; Wed, 06 May 2026\r\n 06:37:07 -0700 (PDT)\nMIME-Version: 1.0\nFrom: =?UTF-8?B?0JHQvtC70L7RgtC+0LLQsCDQnNCw0YDQuNGP?= <cukarevamasa1@gmail.com>\nDate: Wed, 6 May 2026 16:36:07 +0300\nX-Gm-Features: AVHnY4KckOOA2mcM1rK0ZHO3LQs-X73SUybYAGFK46S6QnNrDpC0nJg3OVrJm_4\nMessage-ID: <CAAT5JNyYBBUkqE_v8LLqXzKuSF_h=jt+c=NC8z0HdCBbvAbQiw@mail.gmail.com>\nSubject: \nTo: info@mooon.by\nContent-Type: multipart/alternative; boundary=\"0000000000008c7f3f06512642ea\"\nReturn-Path: cukarevamasa1@gmail.com\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26820",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Здравствуйте! Меня зовут Мария, я учусь на маркетинге в институте бизнеса\r\nБГУ, ищу себе аналитическую практику. Очень хотела бы попасть к вам в\r\nкомпанию на две недели на бесплатной основе. Куда можно обратиться по этому\r\nвопросу?",
  "has_text_plain": true,
  "has_text_html": true,
  "preferred_body_source": "text/plain",
  "body_sources": [
    "text/plain",
    "text/html"
  ],
  "mime_parts": [
    {
      "part_index": 0,
      "content_type": "multipart/alternative",
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
      "size_bytes": 420,
      "is_inline": false,
      "is_attachment": false
    },
    {
      "part_index": 2,
      "content_type": "text/html",
      "content_disposition": "",
      "filename": "",
      "content_id": "",
      "charset": "utf-8",
      "is_multipart": false,
      "size_bytes": 439,
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
      "uid": "raw_email_26820",
      "message_id": "<CAAT5JNyYBBUkqE_v8LLqXzKuSF_h=jt+c=NC8z0HdCBbvAbQiw@mail.gmail.com>",
      "subject": "",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26820-20260514T124740264087\\raw_email_raw_email_26820.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26820-20260514T124740264087\\message_raw_email_26820.md",
      "items": []
    },
    "early_classification": {
      "uid": "raw_email_26820",
      "status": "ok",
      "classification": "candidate_or_portfolio",
      "operator_summary": "Мария, студентка маркетинга БГУ, просит пройти двухнедельную бесплатную аналитическую практику.",
      "case_summary_short": "Мария, студентка маркетинга БГУ, просит пройти двухнедельную бесплатную аналитическую практику.",
      "should_run_ticket_enrichment": false,
      "should_run_customer_kb": false,
      "should_build_customer_draft": false,
      "response_mode_hint": "handoff_to_operator",
      "proposed_action_type": "notify_department_stub",
      "proposed_action_text": "Передать запрос ответственным за практику/HR или маркетинг.",
      "action_stub_allowed": true,
      "classification_reason": "candidate/practice/portfolio wording",
      "sender_email": "cukarevamasa1@gmail.com",
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
        "uid": "raw_email_26820",
        "message_id": "<CAAT5JNyYBBUkqE_v8LLqXzKuSF_h=jt+c=NC8z0HdCBbvAbQiw@mail.gmail.com>",
        "subject": "",
        "lookup_emails": [
          "cukarevamasa1@gmail.com"
        ],
        "selected_lookup_email": "",
        "ticket_db_status": "skipped",
        "crm_users_status": "stub",
        "payment_refund_status": "stub",
        "confidence": "none",
        "candidates_count": 0,
        "resolved_match": null,
        "note": "ticket enrichment skipped: candidate/practice/portfolio wording"
      },
      "debug": {
        "uid": "raw_email_26820",
        "message_id": "<CAAT5JNyYBBUkqE_v8LLqXzKuSF_h=jt+c=NC8z0HdCBbvAbQiw@mail.gmail.com>",
        "subject": "",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26820-20260514T124740264087\\message_raw_email_26820.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26820-20260514T124740264087\\message_raw_email_26820.md"
        },
        "lookup_keys": {
          "sender_email_reference": "cukarevamasa1@gmail.com",
          "body_emails": [],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "cukarevamasa1@gmail.com"
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
              "candidate/practice/portfolio wording"
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
          "body_emails_found": 0,
          "lookup_emails_total": 1,
          "confidence": "none",
          "skip_reason": "candidate/practice/portfolio wording"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26820",
      "message_id": "<CAAT5JNyYBBUkqE_v8LLqXzKuSF_h=jt+c=NC8z0HdCBbvAbQiw@mail.gmail.com>",
      "direction": "inbound",
      "sender": "cukarevamasa1@gmail.com",
      "subject": "",
      "case_id": "case-000006",
      "thread_id": "thread-000006",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\state\\case_thread_registry.xlsx",
      "registry_row_number": 7,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "",
        "references": []
      },
      "thread_history": [
        {
          "message_id": "<CAAT5JNyYBBUkqE_v8LLqXzKuSF_h=jt+c=NC8z0HdCBbvAbQiw@mail.gmail.com>",
          "direction": "inbound",
          "sender": "cukarevamasa1@gmail.com",
          "subject": "",
          "sent_at": "2026-05-06 16:36:07+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26820-20260514T124740264087\\message_raw_email_26820.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26820",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Мария, студентка маркетинга БГУ, просит пройти двухнедельную бесплатную аналитическую практику.",
        "topic": "Кандидат или портфолио",
        "customer_need": "Передать предложение/портфолио ответственным на ручную обработку.",
        "entities": [
          {
            "type": "sender",
            "value": "cukarevamasa1@gmail.com"
          }
        ],
        "confidence": 0.62,
        "response_mode": "handoff_to_operator",
        "understanding_note": "Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.",
        "response_mode_reason": "candidate/practice/portfolio wording",
        "suggested_next_step": "Передать запрос ответственным за практику/HR или маркетинг.",
        "risk_level": "medium",
        "needs_human": true
      }
    },
    "knowledge_retrieval": {
      "uid": "raw_email_26820",
      "status": "skipped",
      "error": "",
      "reason": "candidate/practice/portfolio wording",
      "classification": "candidate_or_portfolio",
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
      "uid": "raw_email_26820",
      "status": "ok",
      "error": "",
      "response_mode_initial": "handoff_to_operator",
      "response_mode_final": "handoff_to_operator",
      "decision_reason": "Передать запрос ответственным за практику/HR или маркетинг.",
      "missing_data": [],
      "risks": [],
      "knowledge_item_ids": [],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Мария, студентка маркетинга БГУ, просит пройти двухнедельную бесплатную аналитическую практику.",
      "case_summary_short": "Мария, студентка маркетинга БГУ, просит пройти двухнедельную бесплатную аналитическую практику.",
      "classification": "candidate_or_portfolio",
      "should_build_customer_draft": false,
      "proposed_action_type": "notify_department_stub",
      "proposed_action_text": "Передать запрос ответственным за практику/HR или маркетинг.",
      "action_stub_allowed": true,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26820",
      "status": "skipped",
      "error": "",
      "skip_reason": "Черновик не создавался: обращение помечено для ручной обработки ответственными.",
      "draft_type": "handoff_to_operator",
      "latest_revision": 0,
      "draft_text": "",
      "operator_note": "Черновик не создавался: обращение помечено для ручной обработки ответственными.",
      "source_response_mode": "handoff_to_operator",
      "created_at": "2026-05-14T12:47:40.864115+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26820-20260514T124740264087\\message_raw_email_26820.md",
      "revisions": [],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "skipped",
        "decision_layer_status": "ok",
        "knowledge_item_ids": []
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26820",
      "status": "mock_sent",
      "error": "",
      "created_at": "2026-05-14T12:47:40.944916+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26820-20260514T124740264087\\message_raw_email_26820.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26820-20260514T124740264087\\message_raw_email_26820.md",
      "case_id": "case-000006",
      "thread_id": "thread-000006",
      "telegram_message_id": 6,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "artifact_only",
      "telegram_operations": [],
      "callback_data": [
        "ma|approve|c24a6dd59cfd8510",
        "ma|needs_edit|c24a6dd59cfd8510",
        "ma|handoff|c24a6dd59cfd8510",
        "ma|ignore|c24a6dd59cfd8510",
        "ma|action_request|c24a6dd59cfd8510"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|c24a6dd59cfd8510"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|c24a6dd59cfd8510"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|c24a6dd59cfd8510"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|c24a6dd59cfd8510"
        },
        {
          "action": "action_request",
          "label": "⚡ Выполнить действие",
          "callback_data": "ma|action_request|c24a6dd59cfd8510"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: raw_email_26820\nПолучено: 06.05.2026 16:37\nОт: cukarevamasa1@gmail.com\nТема письма: без темы\nСуть обращения: Мария, студентка маркетинга БГУ, просит пройти двухнедельную бесплатную аналитическую практику.\n\n<b>Кейс</b>\nCase ID: case-000006 · Thread ID: thread-000006\n\n<b>История переписки</b>\nотсутствует\n\n<b>Вложения</b>\nнет\n\n<b>Проверка билетов / Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: кандидат/портфолио\nЧто хочет отправитель: Мария, студентка маркетинга БГУ, просит пройти двухнедельную бесплатную аналитическую практику.\nСледующий шаг: Передать запрос ответственным за практику/HR или маркетинг.\n\n<b>Что предлагает система</b>\nЧто сделать: Передать запрос ответственным за практику/HR или маркетинг.\n\n<b>Предлагаемое действие</b>\nВерсия предложения: v1\nПередать запрос ответственным за практику/HR или маркетинг.\nТип действия: уведомить отдел\n\n<b>База знаний</b>\nне применялась — письмо не требует клиентской базы знаний по билетам.\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\nнет\n\n<b>Черновик</b>\nЧерновик не создавался: обращение помечено для ручной обработки ответственными.",
      "action": "",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\telegram_operator_delivery\\case-000006\\card_20260514T124740945061.json"
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
