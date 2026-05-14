# Message dossier raw_email_26808

- UID: raw_email_26808
- Message-ID: <CAP5WF-W+uK0mcvSBkcZ1QOTqkbU1fJx9Cnf7nGLObL6=RZYz4Q@mail.gmail.com>
- Direction: inbound
- From: kk@cinemalab.io
- Subject: Как вернуть билет деньги за билет
- Sent at: 2026-05-05 20:39:50+03:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T104151820822\modules\mail_import\mock-flow-raw_email_26808-20260514T104151837619\raw_email_raw_email_26808.eml

## Case / Thread

- Case ID: case-000001
- Thread ID: thread-000001
- Binding rule: new_case_thread
- Binding status: new_case_thread

## Enrichment

- Ticket DB status: <empty>
- Selected lookup email: katerinka166@gmail.com
- Resolved ticket: <empty>

## Attachments

- Count: 0
- Text found in: 0

## LLM Understanding

- Status: ok
- Response mode: ask_clarifying_question
- Confidence: 0.62
- Topic: Клиентский вопрос по билету/оплате
- Customer need: Получить помощь по билету или оплате.
- Summary: Гость спрашивает, как вернуть деньги за билет; указана почта katerinka166@gmail.com.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: customer ticket/payment/refund/certificate wording
- Suggested next step: Проверить карточку и выбрать действие кнопками.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: kk@cinemalab.io

## Body

```
мы купили билет как нам вернуть билет покупали на почту
katerinka166@gmail.com
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<CAP5WF-W+uK0mcvSBkcZ1QOTqkbU1fJx9Cnf7nGLObL6=RZYz4Q@mail.gmail.com>",
  "direction": "inbound",
  "headers": {
    "message_id": "<CAP5WF-W+uK0mcvSBkcZ1QOTqkbU1fJx9Cnf7nGLObL6=RZYz4Q@mail.gmail.com>",
    "in_reply_to": "",
    "references": [],
    "subject": "Как вернуть билет деньги за билет",
    "sender": "kk@cinemalab.io",
    "sent_at": "2026-05-05 20:39:50+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "мы купили билет как нам вернуть билет покупали на почту\r\nkaterinka166@gmail.com",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26808-20260514T104151837619\\raw_email_raw_email_26808.eml",
  "raw_headers": "Received: from postback16b.mail.yandex.net (postback16b.mail.yandex.net [2a02:6b8:c02:900:1:45:d181:da16])\r\n\tby k6o5hfpbdoiwr2lr.sas.yp-c.yandex.net (notsolitesrv) with LMTPS id 5g30mYc06JQv-GfbeeNdW\r\n\tfor <info@mooon.by>; Tue, 05 May 2026 20:40:29 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-95.iva.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-95.iva.yp-c.yandex.net [IPv6:2a02:6b8:c0c:1e06:0:640:ef89:0])\r\n\tby postback16b.mail.yandex.net (Yandex) with ESMTPS id 2AE69C0156\r\n\tfor <info@mooon.by>; Tue, 05 May 2026 20:40:29 +0300 (MSK)\nReceived: from mail-ej1-x62e.google.com (mail-ej1-x62e.google.com [2a00:1450:4864:20::62e])\r\n\tby mail-nwsmtp-mxfront-production-main-95.iva.yp-c.yandex.net (mxfront) with ESMTPS id SekYBG2Lk0U0-3EOeo2kv;\r\n\tTue, 05 May 2026 20:40:28 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-95.iva.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-95.iva.yp-c.yandex.net: domain of cinemalab.io designates 2a00:1450:4864:20::62e as permitted sender, rule=[ip6:2a00:1450:4864::/56]) smtp.mail=kk@cinemalab.io; dkim=pass header.i=@cinemalab.io\nX-Yandex-Spam: 1\nReceived: by mail-ej1-x62e.google.com with SMTP id a640c23a62f3a-ba922426c5cso962474666b.3\r\n        for <info@mooon.by>; Tue, 05 May 2026 10:40:28 -0700 (PDT)\nARC-Seal: i=1; a=rsa-sha256; t=1778002828; cv=none;\r\n        d=google.com; s=arc-20240605;\r\n        b=dxZIyon62eqZTUtXMxEJYeW9qCHoCehbiqPc/se5ZfSPIn+tEmV4MqVYnhHFGF60pB\r\n         Mx6M0iAUn/NCH5cVLd1peiVesQZpnd8vxwlqC9sRquJHtNfMnomMqCAApHCrlQ6Cy2Nn\r\n         OWK1qbCw1ls9cuNcBT6W5y4hR9X8hCuJnwMPdSMQ/0c8VA1u4vX5Ze/h8Vr8+zu75zKD\r\n         EsBpalm9e4EkrS4rCZqyMuIdVdjwwpPl++3WbBaiECl8gVb6r1iZ3xgGo1UBUIoI136p\r\n         z22c4OkxaUna23z3/FJHepm+BUTlEbXJwIvGX6M9JMTApODfjkfckQSxuCWeiIdc5IAE\r\n         wgOQ==\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;\r\n        h=to:subject:message-id:date:from:mime-version:dkim-signature;\r\n        bh=xI8x1AO6wXsGzTeGMmFoEXXqiG58GOO5ncW+YhEgEDg=;\r\n        fh=GgBjxJOT51bynVg0d/XU6Oq7QuhXZWhL3eb7Lz78hbA=;\r\n        b=j6N1ogmAT88c++e3aivoSrtfUpo78rVcDmUi+R/i6K7+kHx5AN6IYhGqPCaQJWCYO/\r\n         7ZrEl9wh6KEVDLS0NBQZ1iYEL1Ar7vvQugPwzAmY32ZD+8wjxiVVWyRPiWK2FqxI0wTY\r\n         LG+KPPMT2NzaeVU5yh05PdRbn3yFOx2Fw0OK41DvFrp/h7h20vlqHuBEAZgivYkEDKse\r\n         BcIZ/9Eh+wHU2REddNS/964g1Ubrg2R/rp563DPPCWnyyVasVJrOusCWYNX5ccLo79Dx\r\n         c/r9FWeCGtcwMtqAULMIOd6xc2TkhhQaSBf63c1FmOlnFGtRUC4kZayqJTSLpVxCLO54\r\n         dSog==;\r\n        darn=mooon.by\nARC-Authentication-Results: i=1; mx.google.com; arc=none\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=cinemalab.io; s=google; t=1778002828; x=1778607628; darn=mooon.by;\r\n        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject\r\n         :date:message-id:reply-to;\r\n        bh=xI8x1AO6wXsGzTeGMmFoEXXqiG58GOO5ncW+YhEgEDg=;\r\n        b=HP1nj23Z/4GcCNlfAE+/GcMVCsZj0HRRITHzLVpZj2d4DbBU6zgzS6R6M4jRCq7Qr6\r\n         dkpKkvLhq70z1WUr2h40cSHDygsqgrRDnmshsMHUmfZgqGa7GYUC4SMpooEK6WS0AN9Z\r\n         /RTWUDZQP/nsPAHVxx+qE7Bzd/5ZTqV5njnxlkn6hLggml8+6o7CpIsIkG8DmBYeaekK\r\n         +TiqYPm0f7aXhLHxA8bjcQUTNK1FgZtqapNb4RnKjUrKRV8vUKNvU4msecTgQ/sWqcGL\r\n         /JaXB7G32HuI+ivNeCft4NTr5auOgZxRbXrsxcVXz1D3vgZAn4x52Bdx6BqRfxAxwaZy\r\n         RBUw==\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20251104; t=1778002828; x=1778607628;\r\n        h=to:subject:message-id:date:from:mime-version:x-gm-gg\r\n         :x-gm-message-state:from:to:cc:subject:date:message-id:reply-to;\r\n        bh=xI8x1AO6wXsGzTeGMmFoEXXqiG58GOO5ncW+YhEgEDg=;\r\n        b=GfncRnbTAYDskYqiWDrCykpyZAHAGuDOnKXvVe9sT/v+Uy6UUZTEpf5f3wPKDFYfrY\r\n         6EgePfz52AMJtd2llIofdqYqIpqSXEEJwCWbipnBkB6lxdoiAsSrU0A/YdQ+figadGti\r\n         J5Y/zvUBzGy1Ql+ElYYCS5QsbvU6ECiYXPZqiMQ47xQn9/4JfZGBnV7zU9UDKXu3/urS\r\n         DjXrhQiu7GOF7FsplgadliJK55k5bvVmrWbImZ2nvQRLlweIFvwGwuUOLivHzwuMxkSU\r\n         fZCU62LF5xvi7ZH/qlOH5LN6H5B2xgmnO7qyZrVk6dp5dNFeqj5U3Ww98WyTEA//n1KF\r\n         YszA==\nX-Gm-Message-State: AOJu0Yy5xvb190Hi1XlAtOZPUoy9DmX2LjXVHl/x4RgVETxztjD1Qsr1\r\n\tHIVSWwBQzSRyCJMnvCeaV/iChcBB7gw+vseA3FdtoVdCgmX62nskXql7GwquQ9kCrOLaCHkqAIJ\r\n\tnm/A3g5zHLHfKoUsv/oyGZ218E8XhLUrX40mb6QwZYra4H9Olj/7WIlSXlrSN\nX-Gm-Gg: AeBDievmdUqzI6kh0O4W9OyH2v6UGtobcBYXmnfzOwRrDUCpQ4ryCsVpDE2QRwsCg73\r\n\tgf6FoTu5JAsHsJWooqDih08Y7a2hOOgt0Ajmv0QCtTbXkESTkQwgK8DA6Z9a8G9bIJTN0rWJ977\r\n\tb4vs/RK4z2uNQMNkt+iglCbK7WJBOUQq8OgtMLOqwdzKgZ1o7rqNWx+C12LlZVnglG7BOJttP3q\r\n\tk062IM7Cr78C53j8NgJTrOVk3+DUNKUFdY1fKz8Ovg5LKMGHfWYb1teqr/ZTcFexgwkPHDqcstT\r\n\tdfOrNtBS8+hGWabCVvGGYd7NhCClQpFm+N4nxIf3iONMpdJpMpAZx6aF3h+kIjrLjuPqq5lXzcD\r\n\tqN2Xv6el4SlnRUkUg/oto3/iltDrpVFc=\nX-Received: by 2002:a17:907:1b1b:b0:bbe:7709:5a8a with SMTP id\r\n a640c23a62f3a-bc40f1430f8mr224166666b.7.1778002827600; Tue, 05 May 2026\r\n 10:40:27 -0700 (PDT)\nMIME-Version: 1.0\nFrom: \"Carol O.\" <kk@cinemalab.io>\nDate: Tue, 5 May 2026 20:39:50 +0300\nX-Gm-Features: AVHnY4KrMpASUWFaDIZ3lSQWaQjhUObMaoa9bcynOwIctKlNywkYjOhH-nByqLA\nMessage-ID: <CAP5WF-W+uK0mcvSBkcZ1QOTqkbU1fJx9Cnf7nGLObL6=RZYz4Q@mail.gmail.com>\nSubject: =?UTF-8?B?0JrQsNC6INCy0LXRgNC90YPRgtGMINCx0LjQu9C10YIg0LTQtdC90YzQs9C4INC30LAg?=\r\n\t=?UTF-8?B?0LHQuNC70LXRgg==?=\nTo: =?UTF-8?B?0J7QsdGJ0LDRjyBtb29vbg==?= <info@mooon.by>\nContent-Type: multipart/alternative; boundary=\"000000000000f2fa540651158a62\"\nReturn-Path: kk@cinemalab.io\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26808",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "мы купили билет как нам вернуть билет покупали на почту\r\nkaterinka166@gmail.com",
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
      "size_bytes": 127,
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
      "size_bytes": 198,
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
      "uid": "raw_email_26808",
      "message_id": "<CAP5WF-W+uK0mcvSBkcZ1QOTqkbU1fJx9Cnf7nGLObL6=RZYz4Q@mail.gmail.com>",
      "subject": "Как вернуть билет деньги за билет",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26808-20260514T104151837619\\raw_email_raw_email_26808.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26808-20260514T104151837619\\message_raw_email_26808.md",
      "items": []
    },
    "early_classification": {
      "uid": "raw_email_26808",
      "status": "ok",
      "classification": "customer_support",
      "operator_summary": "Гость спрашивает, как вернуть деньги за билет; указана почта katerinka166@gmail.com.",
      "case_summary_short": "Гость спрашивает, как вернуть деньги за билет; указана почта katerinka166@gmail.com.",
      "should_run_ticket_enrichment": true,
      "should_run_customer_kb": true,
      "should_build_customer_draft": true,
      "response_mode_hint": "ask_clarifying_question",
      "proposed_action_type": "",
      "proposed_action_text": "",
      "action_stub_allowed": false,
      "classification_reason": "customer ticket/payment/refund/certificate wording",
      "sender_email": "kk@cinemalab.io",
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
        "uid": "raw_email_26808",
        "message_id": "<CAP5WF-W+uK0mcvSBkcZ1QOTqkbU1fJx9Cnf7nGLObL6=RZYz4Q@mail.gmail.com>",
        "subject": "Как вернуть билет деньги за билет",
        "lookup_emails": [
          "katerinka166@gmail.com",
          "kk@cinemalab.io"
        ],
        "selected_lookup_email": "katerinka166@gmail.com",
        "ticket_db_status": "unavailable",
        "crm_users_status": "stub",
        "payment_refund_status": "stub",
        "confidence": "none",
        "candidates_count": 0,
        "resolved_match": null,
        "note": "ticket_db unavailable: pymysql is not installed"
      },
      "debug": {
        "uid": "raw_email_26808",
        "message_id": "<CAP5WF-W+uK0mcvSBkcZ1QOTqkbU1fJx9Cnf7nGLObL6=RZYz4Q@mail.gmail.com>",
        "subject": "Как вернуть билет деньги за билет",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26808-20260514T104151837619\\message_raw_email_26808.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26808-20260514T104151837619\\message_raw_email_26808.md"
        },
        "lookup_keys": {
          "sender_email_reference": "kk@cinemalab.io",
          "body_emails": [
            "katerinka166@gmail.com"
          ],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "katerinka166@gmail.com",
            "kk@cinemalab.io"
          ],
          "selected_lookup_email": "katerinka166@gmail.com",
          "selected_lookup_localpart": "katerinka166"
        },
        "providers": {
          "ticket_db": {
            "status": "unavailable",
            "settings_source": "config.local.yaml",
            "candidates": [],
            "rescue_confident": false,
            "rescue_reason": "",
            "rescue_top1": 0.0,
            "rescue_gap": 0.0,
            "notes": [
              "ticket_db unavailable: pymysql is not installed"
            ],
            "query_email": "kk@cinemalab.io",
            "query_localpart": "kk",
            "lookup_trace": [
              {
                "email": "katerinka166@gmail.com",
                "status": "unavailable",
                "rows": 0,
                "rescue_candidates": 0,
                "rescue_confident": false
              },
              {
                "email": "kk@cinemalab.io",
                "status": "unavailable",
                "rows": 0,
                "rescue_candidates": 0,
                "rescue_confident": false
              }
            ]
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
          "ticket_db_status": "unavailable",
          "crm_users_status": "stub",
          "payment_refund_status": "stub",
          "attachment_report_present": true,
          "body_emails_found": 1,
          "lookup_emails_total": 2,
          "confidence": "none"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26808",
      "message_id": "<CAP5WF-W+uK0mcvSBkcZ1QOTqkbU1fJx9Cnf7nGLObL6=RZYz4Q@mail.gmail.com>",
      "direction": "inbound",
      "sender": "kk@cinemalab.io",
      "subject": "Как вернуть билет деньги за билет",
      "case_id": "case-000001",
      "thread_id": "thread-000001",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\state\\case_thread_registry.xlsx",
      "registry_row_number": 2,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "",
        "references": []
      },
      "thread_history": [
        {
          "message_id": "<CAP5WF-W+uK0mcvSBkcZ1QOTqkbU1fJx9Cnf7nGLObL6=RZYz4Q@mail.gmail.com>",
          "direction": "inbound",
          "sender": "kk@cinemalab.io",
          "subject": "Как вернуть билет деньги за билет",
          "sent_at": "2026-05-05 20:39:50+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26808-20260514T104151837619\\message_raw_email_26808.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26808",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Гость спрашивает, как вернуть деньги за билет; указана почта katerinka166@gmail.com.",
        "topic": "Клиентский вопрос по билету/оплате",
        "customer_need": "Получить помощь по билету или оплате.",
        "entities": [
          {
            "type": "sender",
            "value": "kk@cinemalab.io"
          }
        ],
        "confidence": 0.62,
        "response_mode": "ask_clarifying_question",
        "understanding_note": "Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.",
        "response_mode_reason": "customer ticket/payment/refund/certificate wording",
        "suggested_next_step": "Проверить карточку и выбрать действие кнопками.",
        "risk_level": "medium",
        "needs_human": false
      }
    },
    "knowledge_retrieval": {
      "uid": "raw_email_26808",
      "status": "found",
      "error": "",
      "knowledge_base_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\config\\knowledge_base\\knowledge_base.xlsx",
      "query": {
        "text": "Как вернуть билет деньги за билет мы купили билет как нам вернуть билет покупали на почту\r\nkaterinka166@gmail.com Гость спрашивает, как вернуть деньги за билет; указана почта katerinka166@gmail.com. Клиентский вопрос по билету/оплате Получить помощь по билету или оплате. kk@cinemalab.io",
        "response_mode": "ask_clarifying_question",
        "entities": [
          "kk@cinemalab.io"
        ]
      },
      "matched_items": [
        {
          "id": "kb_refunds_by_purchase_channel",
          "category": "refunds",
          "type": "rule",
          "title": "Возврат билетов зависит от канала покупки",
          "score": 7.0,
          "content": "Билеты, купленные в кассе, возвращаются в кассе кинотеатра не позднее чем за 10 минут до начала сеанса. Билеты Silver Screen Arena City возвращаются только в Arena City. Билеты, купленные на mooon.by, можно вернуть через личный кабинет не позднее чем за 60 минут до начала сеанса; денежный возврат — через кассу. Билеты go2.by возвращаются через go2.by/searchtickets или support@go2.by не позднее чем за 60 минут до начала сеанса. Специальные мероприятия возвращаются не менее чем за 24 часа через кассу.",
          "operator_instruction": "Сначала определить канал покупки. Если канал неизвестен — запросить номер заказа, e-mail, кинотеатр, дату/время сеанса и квитанцию.",
          "template_hint": "Порядок возврата зависит от того, где был приобретён билет: в кассе, на mooon.by или через go2.by.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'Скрипты ответов на звонки и пис'!B18:E18",
          "matched_keywords": [
            "вернуть билет"
          ]
        },
        {
          "id": "kb_tickets_not_received_recovery",
          "category": "tickets",
          "type": "operator_instruction",
          "title": "Если гостю не пришёл электронный билет",
          "score": 7.0,
          "content": "Если письмо с билетами не найдено, гость может скачать билет по ссылке https://mooon.by/ticket/download, указав номер заказа из квитанции и e-mail покупки. Также можно обратиться в кассу перед сеансом с квитанцией или номером заказа.",
          "operator_instruction": "Если в enrichment найден заказ — использовать найденные данные и не просить всё повторно. Если данных нет — запросить e-mail покупки, номер заказа, кинотеатр, фильм, дату/время и квитанцию.",
          "template_hint": "Проверьте папки «Спам» и «Рассылки». Если письма нет, билет можно скачать по ссылке https://mooon.by/ticket/download.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'Скрипты ответов на звонки и пис'!B25:E25",
          "matched_keywords": [
            "получить билет"
          ]
        },
        {
          "id": "kb_tickets_lost_without_receipt",
          "category": "tickets",
          "type": "operator_instruction",
          "title": "Если гость потерял билет и нет чека",
          "score": 5.8,
          "content": "Если гость потерял или выбросил билеты и у него нет чека, кинотеатр может не идентифицировать билеты, потому что факт оплаты не подтверждён.",
          "operator_instruction": "Запросить любые возможные данные: e-mail, дату, фильм, время, ряд/место, способ оплаты. Не обещать восстановление без подтверждений.",
          "template_hint": "Без подтверждения оплаты мы можем не смочь идентифицировать покупку, но попробуем проверить по дополнительным данным.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'БАЗА ЗНАНИЙ'!B63:C63",
          "matched_keywords": [
            "билет"
          ]
        }
      ],
      "routing_matches": [],
      "settings": {
        "min_score": 2,
        "max_results": 3,
        "max_routing_results": 2,
        "enabled_types": [
          "rule",
          "faq",
          "operator_instruction",
          "response_template",
          "regulation"
        ],
        "no_result_behavior": "return_empty",
        "source_format": "xlsx",
        "dynamic_data_policy": "do_not_store",
        "time_validity_policy": "valid_from_valid_to",
        "language_policy": "ru_content",
        "retrieval_scope": "stable_knowledge_only",
        "date_created": "2026-05-04",
        "routing_source": "KB_ROUTING"
      }
    },
    "decision_layer": {
      "uid": "raw_email_26808",
      "status": "ok",
      "error": "",
      "response_mode_initial": "ask_clarifying_question",
      "response_mode_final": "ask_clarifying_question",
      "decision_reason": "Письмо связано с билетом/оплатой, но подтвержденный заказ не найден в enrichment.",
      "missing_data": [
        "Номер заказа или билета, если он есть у гостя."
      ],
      "risks": [],
      "knowledge_item_ids": [
        "kb_refunds_by_purchase_channel",
        "kb_tickets_not_received_recovery",
        "kb_tickets_lost_without_receipt"
      ],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Гость спрашивает, как вернуть деньги за билет; указана почта katerinka166@gmail.com.",
      "case_summary_short": "Гость спрашивает, как вернуть деньги за билет; указана почта katerinka166@gmail.com.",
      "classification": "customer_support",
      "should_build_customer_draft": true,
      "proposed_action_type": "",
      "proposed_action_text": "",
      "action_stub_allowed": false,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26808",
      "status": "ok",
      "error": "",
      "draft_type": "ask_clarifying_question",
      "latest_revision": 1,
      "draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить помощь по билету или оплате.), пожалуйста, уточните:\n- Номер заказа или билета, если он есть у гостя.\nПорядок возврата зависит от того, где был приобретён билет: в кассе, на mooon.by или через go2.by.\nПроверьте папки «Спам» и «Рассылки». Если письма нет, билет можно скачать по ссылке https://mooon.by/ticket/download.\nБез подтверждения оплаты мы можем не смочь идентифицировать покупку, но попробуем проверить по дополнительным данным.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon.",
      "operator_note": "Черновик создан в демо-режиме; реальная отправка отключена.",
      "source_response_mode": "ask_clarifying_question",
      "created_at": "2026-05-14T10:41:52.435678+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26808-20260514T104151837619\\message_raw_email_26808.md",
      "revisions": [
        {
          "revision": 1,
          "created_at": "2026-05-14T10:41:52.435678+00:00",
          "revision_reason": "initial",
          "operator_comment": "",
          "draft_type": "ask_clarifying_question",
          "draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить помощь по билету или оплате.), пожалуйста, уточните:\n- Номер заказа или билета, если он есть у гостя.\nПорядок возврата зависит от того, где был приобретён билет: в кассе, на mooon.by или через go2.by.\nПроверьте папки «Спам» и «Рассылки». Если письма нет, билет можно скачать по ссылке https://mooon.by/ticket/download.\nБез подтверждения оплаты мы можем не смочь идентифицировать покупку, но попробуем проверить по дополнительным данным.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon."
        }
      ],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "found",
        "decision_layer_status": "ok",
        "knowledge_item_ids": [
          "kb_refunds_by_purchase_channel",
          "kb_tickets_not_received_recovery",
          "kb_tickets_lost_without_receipt"
        ]
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26808",
      "status": "mock_sent",
      "error": "",
      "created_at": "2026-05-14T10:41:52.487187+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26808-20260514T104151837619\\message_raw_email_26808.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26808-20260514T104151837619\\message_raw_email_26808.md",
      "case_id": "case-000001",
      "thread_id": "thread-000001",
      "telegram_message_id": 1,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "artifact_only",
      "telegram_operations": [],
      "callback_data": [
        "ma|approve|37e47ae54884585c",
        "ma|needs_edit|37e47ae54884585c",
        "ma|handoff|37e47ae54884585c",
        "ma|ignore|37e47ae54884585c"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|37e47ae54884585c"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|37e47ae54884585c"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|37e47ae54884585c"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|37e47ae54884585c"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: raw_email_26808\nПолучено: 05.05.2026 20:40\nОт: kk@cinemalab.io\nТема письма: Как вернуть билет деньги за билет\nСуть обращения: Гость спрашивает, как вернуть деньги за билет; указана почта katerinka166@gmail.com.\n\n<b>Кейс</b>\nCase ID: case-000001 · Thread ID: thread-000001\n\n<b>История переписки</b>\n- входящее · 2026-05-05 20:39 · Как вернуть билет деньги за билет · Гость спрашивает, как вернуть деньги за билет; указана почта katerinka166@gmail.com.\n\n<b>Вложения</b>\nнет\n\n<b>Enrichment</b>\nПроверка билетов: временно недоступна — ticket_db unavailable: pymysql is not installed.\n\n<b>Что понял ассистент</b>\nТип обращения: клиентский вопрос\nЧто хочет отправитель: Получить помощь по билету или оплате.\nЧто предлагает система: Письмо связано с билетом/оплатой, но подтвержденный заказ не найден в enrichment.\n\n<b>Что предлагает система</b>\nРежим: уточнить данные\nПричина: Письмо связано с билетом/оплатой, но подтвержденный заказ не найден в enrichment.\n\n<b>База знаний</b>\n- Возврат билетов зависит от канала покупки / kb_refunds_by_purchase_channel / балл 7.0\n- Если гостю не пришёл электронный билет / kb_tickets_not_received_recovery / балл 7.0\n- Если гость потерял билет и нет чека / kb_tickets_lost_without_receipt / балл 5.8\n\n<b>Что не хватает</b>\n- Номер заказа или билета, если он есть у гостя.\n\n<b>Риски</b>\nнет\n\n<b>Черновик v1</b>\nЗдравствуйте.\nЧтобы корректно обработать обращение (Получить помощь по билету или оплате.), пожалуйста, уточните:\n- Номер заказа или билета, если он есть у гостя.\nПорядок возврата зависит от того, где был приобретён билет: в кассе, на mooon.by или через go2.by.\nПроверьте папки «Спам» и «Рассылки». Если письма нет, билет можно скачать по ссылке https://mooon.by/ticket/download.\nБез подтверждения оплаты мы можем не смочь идентифицировать покупку, но попробуем проверить по дополнительным данным.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon.",
      "action": "",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\telegram_operator_delivery\\case-000001\\card_20260514T104152487358.json"
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
