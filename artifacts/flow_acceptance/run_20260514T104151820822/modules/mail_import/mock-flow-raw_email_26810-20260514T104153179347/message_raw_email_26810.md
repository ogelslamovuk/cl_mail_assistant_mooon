# Message dossier raw_email_26810

- UID: raw_email_26810
- Message-ID: <CAHMrrW75sbOF+Jp8JGc1kK=7=tH04x4qeuHAcpwzRdo3wuz58w@mail.gmail.com>
- Direction: inbound
- From: kykruniksi765@gmail.com
- Subject: <empty>
- Sent at: 2026-05-05 23:18:37+03:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T104151820822\modules\mail_import\mock-flow-raw_email_26810-20260514T104153179347\raw_email_raw_email_26810.eml

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
- Response mode: handoff_to_operator
- Confidence: 0.62
- Topic: Вопрос по расписанию или репертуару
- Customer need: Понять, возможен ли показ; без live schedule connector передать ответственным.
- Summary: Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: schedule/repertoire/movie-show question
- Suggested next step: Передать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: kykruniksi765@gmail.com

## Body

```
Скажите честно пожалуйста. Вы хотя бы пытаетесь договориться с Glitch
насчёт показа Цифрового цирка на территории Беларуси?
Может вам сразу отворот поворот дали из-за санкций? Потому что вы сами
надеюсь понимаете, что фан база офигительно большая,и с этим нужно что то
делать.
Говорю же, хотя бы честный ответ что кина не будет)
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<CAHMrrW75sbOF+Jp8JGc1kK=7=tH04x4qeuHAcpwzRdo3wuz58w@mail.gmail.com>",
  "direction": "inbound",
  "headers": {
    "message_id": "<CAHMrrW75sbOF+Jp8JGc1kK=7=tH04x4qeuHAcpwzRdo3wuz58w@mail.gmail.com>",
    "in_reply_to": "",
    "references": [],
    "subject": "",
    "sender": "kykruniksi765@gmail.com",
    "sent_at": "2026-05-05 23:18:37+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Скажите честно пожалуйста. Вы хотя бы пытаетесь договориться с Glitch\r\nнасчёт показа Цифрового цирка на территории Беларуси?\r\nМожет вам сразу отворот поворот дали из-за санкций? Потому что вы сами\r\nнадеюсь понимаете, что фан база офигительно большая,и с этим нужно что то\r\nделать.\r\nГоворю же, хотя бы честный ответ что кина не будет)",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26810-20260514T104153179347\\raw_email_raw_email_26810.eml",
  "raw_headers": "Received: from postback27b.mail.yandex.net (postback27b.mail.yandex.net [2a02:6b8:c02:900:1:45:d181:da27])\r\n\tby wqztmwmfffvcpf7z.sas.yp-c.yandex.net (notsolitesrv) with LMTPS id dY5owiP2i4HA-0d8IuKsV\r\n\tfor <info@mooon.by>; Tue, 05 May 2026 23:18:50 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-92.iva.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-92.iva.yp-c.yandex.net [IPv6:2a02:6b8:c0c:2a2b:0:640:4e83:0])\r\n\tby postback27b.mail.yandex.net (Yandex) with ESMTPS id 4D9C2C000A\r\n\tfor <info@mooon.by>; Tue, 05 May 2026 23:18:50 +0300 (MSK)\nReceived: from mail-ej1-x636.google.com (mail-ej1-x636.google.com [2a00:1450:4864:20::636])\r\n\tby mail-nwsmtp-mxfront-production-main-92.iva.yp-c.yandex.net (mxfront) with ESMTPS id nInRxh2LO4Y0-aJ6fwiHY;\r\n\tTue, 05 May 2026 23:18:50 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-92.iva.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-92.iva.yp-c.yandex.net: domain of gmail.com designates 2a00:1450:4864:20::636 as permitted sender, rule=[ip6:2a00:1450:4864::/56]) smtp.mail=kykruniksi765@gmail.com; dkim=pass header.i=@gmail.com\nX-Yandex-Spam: 1\nReceived: by mail-ej1-x636.google.com with SMTP id a640c23a62f3a-baa8c78ac7fso788374866b.0\r\n        for <info@mooon.by>; Tue, 05 May 2026 13:18:49 -0700 (PDT)\nARC-Seal: i=1; a=rsa-sha256; t=1778012329; cv=none;\r\n        d=google.com; s=arc-20240605;\r\n        b=IZQkHEy95IEcJhVF1/r8/Y4+IBpOEvZkMRzzOyhiUAfmJa//HC45MC0afHnYTB1CEG\r\n         +cTHZUz//Zis/nsL3RYF8w0WvoqDEWyO7sbKQ6MjCu55oTUNIOV3MaSL82T2j/2bhTei\r\n         szrJIuClFBo8dBoeKBbCN3AyBYGVDA+3DGHy2vS1TGxjVhzREODps/JbFc1g1ide0vhV\r\n         ++i32AllLVUop+WvFckg1MMWk/rilvArwi1hVOcI3IF3uwGGOkpqDm/9Jmf16F9JQHMN\r\n         cYWjybclIYseCUAVGqlpU01tCsOKYAz96h7od1aPlvNjtHqBmMzQ0KwPKArN9682pOVX\r\n         JSXw==\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;\r\n        h=to:subject:message-id:date:from:mime-version:dkim-signature;\r\n        bh=UvQyjUrHf6Lxpl8wbDEfDaVXIfteW1GagGhd54sa37k=;\r\n        fh=GgBjxJOT51bynVg0d/XU6Oq7QuhXZWhL3eb7Lz78hbA=;\r\n        b=aVbsCHM4GRUT/ksRanptYldlrDm0F5KyjmbaHru4ltTd41ZLeo3VbMIKY7sN0oLN80\r\n         1n3c1DLji0EKDeI340BdiMtPxu6CdUd0DAvE08+ubGpxox4T8ess59Aqh7Uq7C+cfobx\r\n         b+h0q2EXnmY8F5aDZBKMcGbn4rSc0BPsDsuQmPwyxKKt69LG735AolTIbXoXA9ux5OQk\r\n         FcNKWQRqON9c1haLCwzVaaiMy/qv1g+dm26LigmMsLpDXSqTPUf6b+dpT4yumNR8K0uU\r\n         AV8XTPGm1vdj4LhDKb9IrLSaruKdFOJq3nFsi76UDyNW2FI+ciq4KEHvVYmW/lQ5cKaf\r\n         wliw==;\r\n        darn=mooon.by\nARC-Authentication-Results: i=1; mx.google.com; arc=none\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=gmail.com; s=20251104; t=1778012329; x=1778617129; darn=mooon.by;\r\n        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject\r\n         :date:message-id:reply-to;\r\n        bh=UvQyjUrHf6Lxpl8wbDEfDaVXIfteW1GagGhd54sa37k=;\r\n        b=BhPjbRFpJbTDE7NBCJfbyrRN+OtrfZdxt4nsUDhX4TzMvaZY+Xgx4O5i6MToRbFerI\r\n         pGE0xlpOY/V+ZUWYNPxVFsjn5Ls0c9K80yls1K2H61pg3xirbnWhvVKd9R56+w5v4kBx\r\n         vVVXZpMWk957meWKK7EbG5iiY/lxb94GAsRNrtASVzHa1fCtc09w91mnfyCoK7hVOtrh\r\n         xOnigEGHk4acoIRo7ee0DKQFyW0JmSIiPH6AfjPsN1rw5TUlsGJ/k1utlRYZDN0D6M8N\r\n         YQQWKtQE29zbQxAUTjxbVQInqopaNWdQE7DBfZrxVCzcsbbB3MR99zB8dQAxzgNxAxJp\r\n         nVLw==\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20251104; t=1778012329; x=1778617129;\r\n        h=to:subject:message-id:date:from:mime-version:x-gm-gg\r\n         :x-gm-message-state:from:to:cc:subject:date:message-id:reply-to;\r\n        bh=UvQyjUrHf6Lxpl8wbDEfDaVXIfteW1GagGhd54sa37k=;\r\n        b=GVxADC2ZuhHOC+NmCW8MtvYoDCOQuJdEzPVQgQ+I7mYeIVxLZ5pZpGlZDilSS9RfdX\r\n         K4o+yAKhXLt9U+cKahAxwVczeF+jVdfqlYj/OlHMpNWhPLOnMsG5geGFS30iwTYzzlP7\r\n         B3QhMQ7hwrIybLe9hsaVFr4eeqN1ZkveygAXROBQmBTxGekqFZoRa6+CpDZD780QsFv7\r\n         Enz1UWuj4B4+KeS7WbH/4/kTSVdeVurWKfXgLFilZfmtL92VMW4kTn2QVvckIwwBtknT\r\n         ADlsTJdIhn26qEoE+REpEezYdCNob6prVz7tSXMJL80jFS5HZEqnoDqML0EObkB3NJzY\r\n         ykpg==\nX-Gm-Message-State: AOJu0Yz5t8XIPk1fpIMfSLWsTDuPlWyncH7JefuJEaGJv2qtXWMxpQum\r\n\tZogKyL7NdpXwQcGeRKJiwmmwkuiJttl1SC6s4Djn4IE1bfu8Co4fI5hOa1txPrBjFsJaBU2r8+Z\r\n\tPlxEGSjA9NdTdH+pFfmX0sVpqrlHlyafKEg==\nX-Gm-Gg: AeBDietgZ0PXiQTy/HKM2o+A1pZcfjHkshWOD4N5pTad6fPQqg8NLBHyNHo0R7mdzYX\r\n\tI8Ih+ujDkjERCLBWX5pHZYxkyP9K8wCO/34JfuFPqIXcrbSEO3CWnGJLPaE3LTq7cYNa+KFIykP\r\n\toXszhLF7LizbBE+gi8XUTcRYTriyuKG+a/ea0AWdE3eT5msnZHAGPoKaRC4c+ojTk/l3gm5Tf78\r\n\te/PVzBdn4CQWp1PXsopuePNbKC0E2oe5STlyIIMRtRv29isBZROClqO9Krq5jxyBcBCln3hwwFR\r\n\t1NQ4zf55uG/ZCmHnOXTt\nX-Received: by 2002:a17:906:fd87:b0:bad:f5dd:6740 with SMTP id\r\n a640c23a62f3a-bc56aa411e4mr2235966b.3.1778012328734; Tue, 05 May 2026\r\n 13:18:48 -0700 (PDT)\nMIME-Version: 1.0\nFrom: =?UTF-8?B?0JDQuyDQlNC+?= <kykruniksi765@gmail.com>\nDate: Tue, 5 May 2026 23:18:37 +0300\nX-Gm-Features: AVHnY4LyMALf4Lm6ZyJ80YENdsnHvCRuYl72rwKrHAiqSTkuO8YdzYmt5zS-i3I\nMessage-ID: <CAHMrrW75sbOF+Jp8JGc1kK=7=tH04x4qeuHAcpwzRdo3wuz58w@mail.gmail.com>\nSubject: \nTo: =?UTF-8?B?0J7QsdGJ0LDRjyBtb29vbg==?= <info@mooon.by>\nContent-Type: multipart/alternative; boundary=\"00000000000042b15d065117c186\"\nReturn-Path: kykruniksi765@gmail.com\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26810",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Скажите честно пожалуйста. Вы хотя бы пытаетесь договориться с Glitch\r\nнасчёт показа Цифрового цирка на территории Беларуси?\r\nМожет вам сразу отворот поворот дали из-за санкций? Потому что вы сами\r\nнадеюсь понимаете, что фан база офигительно большая,и с этим нужно что то\r\nделать.\r\nГоворю же, хотя бы честный ответ что кина не будет)",
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
      "size_bytes": 597,
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
      "size_bytes": 658,
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
      "uid": "raw_email_26810",
      "message_id": "<CAHMrrW75sbOF+Jp8JGc1kK=7=tH04x4qeuHAcpwzRdo3wuz58w@mail.gmail.com>",
      "subject": "",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26810-20260514T104153179347\\raw_email_raw_email_26810.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26810-20260514T104153179347\\message_raw_email_26810.md",
      "items": []
    },
    "early_classification": {
      "uid": "raw_email_26810",
      "status": "ok",
      "classification": "schedule_or_repertoire_question",
      "operator_summary": "Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси.",
      "case_summary_short": "Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси.",
      "should_run_ticket_enrichment": false,
      "should_run_customer_kb": true,
      "should_build_customer_draft": false,
      "response_mode_hint": "handoff_to_operator",
      "proposed_action_type": "mark_manual_processing",
      "proposed_action_text": "Передать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён.",
      "action_stub_allowed": true,
      "classification_reason": "schedule/repertoire/movie-show question",
      "sender_email": "kykruniksi765@gmail.com",
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
        "uid": "raw_email_26810",
        "message_id": "<CAHMrrW75sbOF+Jp8JGc1kK=7=tH04x4qeuHAcpwzRdo3wuz58w@mail.gmail.com>",
        "subject": "",
        "lookup_emails": [
          "kykruniksi765@gmail.com"
        ],
        "selected_lookup_email": "",
        "ticket_db_status": "skipped",
        "crm_users_status": "stub",
        "payment_refund_status": "stub",
        "confidence": "none",
        "candidates_count": 0,
        "resolved_match": null,
        "note": "ticket enrichment skipped: schedule/repertoire/movie-show question"
      },
      "debug": {
        "uid": "raw_email_26810",
        "message_id": "<CAHMrrW75sbOF+Jp8JGc1kK=7=tH04x4qeuHAcpwzRdo3wuz58w@mail.gmail.com>",
        "subject": "",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26810-20260514T104153179347\\message_raw_email_26810.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26810-20260514T104153179347\\message_raw_email_26810.md"
        },
        "lookup_keys": {
          "sender_email_reference": "kykruniksi765@gmail.com",
          "body_emails": [],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "kykruniksi765@gmail.com"
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
              "schedule/repertoire/movie-show question"
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
          "skip_reason": "schedule/repertoire/movie-show question"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26810",
      "message_id": "<CAHMrrW75sbOF+Jp8JGc1kK=7=tH04x4qeuHAcpwzRdo3wuz58w@mail.gmail.com>",
      "direction": "inbound",
      "sender": "kykruniksi765@gmail.com",
      "subject": "",
      "case_id": "case-000003",
      "thread_id": "thread-000003",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\state\\case_thread_registry.xlsx",
      "registry_row_number": 4,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "",
        "references": []
      },
      "thread_history": [
        {
          "message_id": "<CAHMrrW75sbOF+Jp8JGc1kK=7=tH04x4qeuHAcpwzRdo3wuz58w@mail.gmail.com>",
          "direction": "inbound",
          "sender": "kykruniksi765@gmail.com",
          "subject": "",
          "sent_at": "2026-05-05 23:18:37+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26810-20260514T104153179347\\message_raw_email_26810.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26810",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси.",
        "topic": "Вопрос по расписанию или репертуару",
        "customer_need": "Понять, возможен ли показ; без live schedule connector передать ответственным.",
        "entities": [
          {
            "type": "sender",
            "value": "kykruniksi765@gmail.com"
          }
        ],
        "confidence": 0.62,
        "response_mode": "handoff_to_operator",
        "understanding_note": "Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.",
        "response_mode_reason": "schedule/repertoire/movie-show question",
        "suggested_next_step": "Передать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён.",
        "risk_level": "medium",
        "needs_human": true
      }
    },
    "knowledge_retrieval": {
      "uid": "raw_email_26810",
      "status": "found",
      "error": "",
      "knowledge_base_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\config\\knowledge_base\\knowledge_base.xlsx",
      "query": {
        "text": " Скажите честно пожалуйста. Вы хотя бы пытаетесь договориться с Glitch\r\nнасчёт показа Цифрового цирка на территории Беларуси?\r\nМожет вам сразу отворот поворот дали из-за санкций? Потому что вы сами\r\nнадеюсь понимаете, что фан база офигительно большая,и с этим нужно что то\r\nделать.\r\nГоворю же, хотя бы честный ответ что кина не будет) Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси. Вопрос по расписанию или репертуару Понять, возможен ли показ; без live schedule connector передать ответственным. kykruniksi765@gmail.com",
        "response_mode": "handoff_to_operator",
        "entities": [
          "kykruniksi765@gmail.com"
        ]
      },
      "matched_items": [
        {
          "id": "kb_channel_no_messengers_for_guests",
          "category": "general",
          "type": "rule",
          "title": "Билеты не отправляются гостям в Viber или Telegram",
          "score": 3.85,
          "content": "Сеть mooon и Silver Screen не использует мессенджеры для коммуникации с гостями. Билеты и служебные письма направляются по e-mail.",
          "operator_instruction": "Не обещать отправку билета в мессенджер. Направлять гостя к e-mail, скачиванию билета или кассе.",
          "template_hint": "В настоящий момент мы не используем мессенджеры для коммуникации с гостями.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'БАЗА ЗНАНИЙ'!B16:C16",
          "matched_keywords": [
            "mooon"
          ]
        },
        {
          "id": "kb_repertoire_rights_available_only",
          "category": "legal",
          "type": "faq",
          "title": "Показываются фильмы с доступными лицензионными правами",
          "score": 3.8,
          "content": "В сети показываются фильмы, лицензионные права на которые доступны для территории Республики Беларусь. В прокате могут быть перевыпуски и ретроспективы, но конкретные показы зависят от доступности прав и репертуарного планирования.",
          "operator_instruction": "Не обещать показ конкретного фильма. Предложить следить за обновлениями на сайте.",
          "template_hint": "В прокате находятся фильмы, лицензионные права на которые доступны для территории Республики Беларусь.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'БАЗА ЗНАНИЙ'!B41:C41",
          "matched_keywords": [
            "репертуар"
          ]
        },
        {
          "id": "kb_repertoire_grodno_differs_by_demand",
          "category": "repertoire",
          "type": "faq",
          "title": "Почему афиша в Гродно может отличаться",
          "score": 3.75,
          "content": "Расписание сеансов может формироваться с учётом реального спроса зрителей: посещаемости, предварительных продаж и запросов на разные фильмы. Пожелания зрителя можно зафиксировать и передать в отдел репертуарного планирования.",
          "operator_instruction": "Если гость просит конкретный фильм — зафиксировать пожелание, но не обещать показ.",
          "template_hint": "Расписание сеансов формируется на основе реального спроса зрителей.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'БАЗА ЗНАНИЙ'!B32:C32",
          "matched_keywords": [
            "репертуар"
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
      "uid": "raw_email_26810",
      "status": "ok",
      "error": "",
      "response_mode_initial": "handoff_to_operator",
      "response_mode_final": "handoff_to_operator",
      "decision_reason": "Вопрос касается репертуара/расписания; live schedule connector пока не подключён.",
      "missing_data": [],
      "risks": [
        "Нельзя отвечать фактом о показах без проверки актуального расписания."
      ],
      "knowledge_item_ids": [
        "kb_channel_no_messengers_for_guests",
        "kb_repertoire_rights_available_only",
        "kb_repertoire_grodno_differs_by_demand"
      ],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси.",
      "case_summary_short": "Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси.",
      "classification": "schedule_or_repertoire_question",
      "should_build_customer_draft": false,
      "proposed_action_type": "mark_manual_processing",
      "proposed_action_text": "Передать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён.",
      "action_stub_allowed": true,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26810",
      "status": "skipped",
      "error": "",
      "skip_reason": "Черновик не создавался: вопрос требует проверки расписания/репертуара ответственными.",
      "draft_type": "handoff_to_operator",
      "latest_revision": 0,
      "draft_text": "",
      "operator_note": "Черновик не создавался: вопрос требует проверки расписания/репертуара ответственными.",
      "source_response_mode": "handoff_to_operator",
      "created_at": "2026-05-14T10:41:53.591976+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26810-20260514T104153179347\\message_raw_email_26810.md",
      "revisions": [],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "found",
        "decision_layer_status": "ok",
        "knowledge_item_ids": []
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26810",
      "status": "mock_sent",
      "error": "",
      "created_at": "2026-05-14T10:41:53.618700+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26810-20260514T104153179347\\message_raw_email_26810.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26810-20260514T104153179347\\message_raw_email_26810.md",
      "case_id": "case-000003",
      "thread_id": "thread-000003",
      "telegram_message_id": 3,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "artifact_only",
      "telegram_operations": [],
      "callback_data": [
        "ma|approve|f5457b9352e473a2",
        "ma|needs_edit|f5457b9352e473a2",
        "ma|handoff|f5457b9352e473a2",
        "ma|ignore|f5457b9352e473a2",
        "ma|action_request|f5457b9352e473a2"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|f5457b9352e473a2"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|f5457b9352e473a2"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|f5457b9352e473a2"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|f5457b9352e473a2"
        },
        {
          "action": "action_request",
          "label": "⚡ Выполнить действие",
          "callback_data": "ma|action_request|f5457b9352e473a2"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: raw_email_26810\nПолучено: 05.05.2026 23:18\nОт: kykruniksi765@gmail.com\nТема письма: без темы\nСуть обращения: Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси.\n\n<b>Кейс</b>\nCase ID: case-000003 · Thread ID: thread-000003\n\n<b>История переписки</b>\n- входящее · 2026-05-05 23:18 · без темы · Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси.\n\n<b>Вложения</b>\nнет\n\n<b>Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: вопрос по репертуару/расписанию\nЧто хочет отправитель: Понять, возможен ли показ; без live schedule connector передать ответственным.\nЧто предлагает система: Вопрос касается репертуара/расписания; live schedule connector пока не подключён.\n\n<b>Что предлагает система</b>\nРежим: передать оператору\nПричина: Вопрос касается репертуара/расписания; live schedule connector пока не подключён.\n\n<b>Предлагаемое действие</b>\nПередать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён.\nТип действия: mark_manual_processing\n\n<b>База знаний</b>\n- Билеты не отправляются гостям в Viber или Telegram / kb_channel_no_messengers_for_guests / балл 3.85\n- Показываются фильмы с доступными лицензионными правами / kb_repertoire_rights_available_only / балл 3.8\n- Почему афиша в Гродно может отличаться / kb_repertoire_grodno_differs_by_demand / балл 3.75\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\n- Нельзя отвечать фактом о показах без проверки актуального расписания.\n\n<b>Черновик</b>\nЧерновик не создавался: вопрос требует проверки расписания/репертуара ответственными.",
      "action": "",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\telegram_operator_delivery\\case-000003\\card_20260514T104153618808.json"
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
