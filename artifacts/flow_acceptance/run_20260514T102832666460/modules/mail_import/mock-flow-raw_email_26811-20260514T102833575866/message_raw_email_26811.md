# Message dossier raw_email_26811

- UID: raw_email_26811
- Message-ID: <CAH4Fh+j2fFagprqRhiK8_iEKJsi9YPkKdZ2rXss=_Fgk2StcFw@mail.gmail.com>
- Direction: inbound
- From: ninago558@gmail.com
- Subject: Re:
- Sent at: 2026-05-06 00:08:07+03:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T102832666460\modules\mail_import\mock-flow-raw_email_26811-20260514T102833575866\raw_email_raw_email_26811.eml

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
- Summary: Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка».
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: schedule/repertoire/movie-show question
- Suggested next step: Передать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: ninago558@gmail.com

## Body

```
Здравствуйте ещё раз, не могли бы вы сказать, ещё не договаривались со
студией Glitch? Всем Уручьем ждём показ сериала, интригующие ждём июня.

вс, 19 апр. 2026 г., 23:06 Общая mooon <info@mooon.by>:

> Доброго времени суток.
> Мы видим высокий интерес наших зрителей к этому проекту и  делаем всё
> возможное, чтобы оправдать ваши ожидания.. В случае успешных переговоров с
> правообладателем проекта «Удивительный цифровой цирк» на территории
> Республики Беларусь, мы непременно организуем его показы
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<CAH4Fh+j2fFagprqRhiK8_iEKJsi9YPkKdZ2rXss=_Fgk2StcFw@mail.gmail.com>",
  "direction": "inbound",
  "headers": {
    "message_id": "<CAH4Fh+j2fFagprqRhiK8_iEKJsi9YPkKdZ2rXss=_Fgk2StcFw@mail.gmail.com>",
    "in_reply_to": "<45621776629162@3d1cd0e9-1e27-45a4-b8ec-96a96b28957c>",
    "references": [
      "<CAH4Fh+iSvGcDSVZxQK30B4kR5kdH0BdCeiPY-C99JdoXRxU-oA@mail.gmail.com>",
      "<45621776629162@3d1cd0e9-1e27-45a4-b8ec-96a96b28957c>"
    ],
    "subject": "Re:",
    "sender": "ninago558@gmail.com",
    "sent_at": "2026-05-06 00:08:07+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Здравствуйте ещё раз, не могли бы вы сказать, ещё не договаривались со\r\nстудией Glitch? Всем Уручьем ждём показ сериала, интригующие ждём июня.\r\n\r\nвс, 19 апр. 2026 г., 23:06 Общая mooon <info@mooon.by>:\r\n\r\n> Доброго времени суток.\r\n> Мы видим высокий интерес наших зрителей к этому проекту и  делаем всё\r\n> возможное, чтобы оправдать ваши ожидания.. В случае успешных переговоров с\r\n> правообладателем проекта «Удивительный цифровой цирк» на территории\r\n> Республики Беларусь, мы непременно организуем его показы",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26811-20260514T102833575866\\raw_email_raw_email_26811.eml",
  "raw_headers": "Received: from postback11b.mail.yandex.net (postback11b.mail.yandex.net [2a02:6b8:c02:900:1:45:d181:da11])\r\n\tby qlbyrov2ssu7cgq2.sas.yp-c.yandex.net (notsolitesrv) with LMTPS id 3PHsSnMXTJqZ-gk80CzgK\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 00:08:21 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-60.iva.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-60.iva.yp-c.yandex.net [IPv6:2a02:6b8:c0c:bd06:0:640:8a5c:0])\r\n\tby postback11b.mail.yandex.net (Yandex) with ESMTPS id 6690FC00F2\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 00:08:21 +0300 (MSK)\nReceived: from mail-ed1-x530.google.com (mail-ed1-x530.google.com [2a00:1450:4864:20::530])\r\n\tby mail-nwsmtp-mxfront-production-main-60.iva.yp-c.yandex.net (mxfront) with ESMTPS id K8oX2u2LLuQ0-4Whs58wN;\r\n\tWed, 06 May 2026 00:08:21 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-60.iva.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-60.iva.yp-c.yandex.net: domain of gmail.com designates 2a00:1450:4864:20::530 as permitted sender, rule=[ip6:2a00:1450:4864::/56]) smtp.mail=ninago558@gmail.com; dkim=pass header.i=@gmail.com\nX-Yandex-Spam: 1\nReceived: by mail-ed1-x530.google.com with SMTP id 4fb4d7f45d1cf-67b7c71c165so7024657a12.0\r\n        for <info@mooon.by>; Tue, 05 May 2026 14:08:20 -0700 (PDT)\nARC-Seal: i=1; a=rsa-sha256; t=1778015300; cv=none;\r\n        d=google.com; s=arc-20240605;\r\n        b=ELCN0LxVZyEdE5vHywYDZjD2t0wDcDNBc9AsMhJeTdDYj+MFZmQq4LvMQqdmqGxKen\r\n         rZd/ByFZQqGswyc2Rcunxjj4efnBcue2d76trL1kcOjgXOE/iUx1OZqS3C5Sm9D95Iar\r\n         g+23ZRIao7rxAS/NFM19muJ5n3CImYRIPqDldw9OELhmxgbgyhSZ858sbmVwdGi3Yrs1\r\n         tHob6ayE1fAbblRP9QN5DZ4z3K3aKfcqXN1AyMQCtMFaP5sMVHmTuEfE01TEdHsQJ9Bt\r\n         Jr1TfA55Xr88DGVAOpKCXkPH6WfumQKTr9cgs27DgOFEjTd1piocuQpLZVRyZEdWNyDm\r\n         7mrQ==\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;\r\n        h=to:subject:message-id:date:from:in-reply-to:references:mime-version\r\n         :dkim-signature;\r\n        bh=PRR9JXPIq7ezKzvZw1cKABLcw0PMWoAKsb9LHyCGXiY=;\r\n        fh=GgBjxJOT51bynVg0d/XU6Oq7QuhXZWhL3eb7Lz78hbA=;\r\n        b=ciNnxkY2OVqkQwONC2OMvHH+65UnA0l7kg85SD0sF+9F0t59RurGAxM1VtTP0TP83f\r\n         DNkHA9HO/GGKrExJ7dfcEIXUp8Kas5NWC5UjedX8U+u2QqwSDnyr15JOYghMQwLNKTdM\r\n         Gz9udpm3IQhlsVZ7lrh1uD3V+umon/+rhMBvfS2FGTNDaDO5IIMC5zIh/UvSknXYjbaD\r\n         ZXOW8HiliOrtMjuVn9tndqEUUrJwPGtMdCftpl0OfmTfKQr/vt+NNhYHOrtDGYXwMPY0\r\n         FrDAelAGgTBDzMVnf5GdIGkS0AEH64wSqrqh9Y39WE/Azv91sX6Zqi9spjs6VWrvH0F6\r\n         YhUg==;\r\n        darn=mooon.by\nARC-Authentication-Results: i=1; mx.google.com; arc=none\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=gmail.com; s=20251104; t=1778015300; x=1778620100; darn=mooon.by;\r\n        h=to:subject:message-id:date:from:in-reply-to:references:mime-version\r\n         :from:to:cc:subject:date:message-id:reply-to;\r\n        bh=PRR9JXPIq7ezKzvZw1cKABLcw0PMWoAKsb9LHyCGXiY=;\r\n        b=MfhAG8NRDxM1z9+fcfFnPnpuvYZLg28/xeeRUB4MHhl8r/1b3TLI+WDL/UF7jzyf+S\r\n         CBsvNxkzaWxxy7rTYRpRSdhcfY7WSEelPmcmMN/vMCwuop4A/pwg5hzaDohBMiEIO0jD\r\n         UzE/YQULX9ILaMDHB5KBb04Z7GRyxcLCanZbVLcIx+cjYUnkx3y931KWDRuMpQ7p5DvE\r\n         3Ws14vO3nEPkdxaisHIQ//5VPuUCtOKotNEgYFFll8qrzn9eBUQNP0Qt7+45HrXAomir\r\n         zeopeA2SJZUXlj1iQa/S5IwZdYSurmwDz/ivOm3unj/KxaJfk2M++CbHZwc0xJS/XYj8\r\n         Oo6A==\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20251104; t=1778015300; x=1778620100;\r\n        h=to:subject:message-id:date:from:in-reply-to:references:mime-version\r\n         :x-gm-gg:x-gm-message-state:from:to:cc:subject:date:message-id\r\n         :reply-to;\r\n        bh=PRR9JXPIq7ezKzvZw1cKABLcw0PMWoAKsb9LHyCGXiY=;\r\n        b=agD7KIVyZSiIC8FBEmR6MATmqOULZuVXa3Oq63qIyHoc+iCeJ37DKcUuAsCNaSiA18\r\n         BiaXazWgnDiSAfP/zzRRgWheXNPsu93UVaXs1pziJXvrvd/5iPKb4rTHD7/M0wAUybb+\r\n         qEN15YbAPHoe0s3MAtbQ1j4gKbprm3jJiIzDB+5oZATSM9/NYQDIgbi4clrTqiwAH5Ev\r\n         jU5dCmwYBKdQErUY0X02z7P4TgJCBiNXaNEIY5/sfPKm1lTRvViwraW2E4HdmB6VuNxH\r\n         BAmYH2NhXfu1r+XDYFPgiCwUA7KCa/HQu73PEdUwwM8dukOBjX+N1gGUgGN1gbW1Jsii\r\n         tVcQ==\nX-Gm-Message-State: AOJu0YwBFEzhnaX0rtQYCCT2Em1Bw8bfFGgxBzwcEFO32PFpDZOVAA4S\r\n\tkz4ahaDpIIeBH+kq/YS1ne7iDs328rnS7nJkwjXKKUQnydliqEJzuQr6UEfceEO2ld/jOvgLBkP\r\n\txc3YZcDVXkDnEuq6LOv2hXMXQabFj5746/w==\nX-Gm-Gg: AeBDiettJ5ucGZ3YyRmXazqyzFg5Wwystraa8A0I0FdVibd4H5x2yem6i4QSzw2CJ1Q\r\n\tqCKDLHNiv8lB3B/tvD6BSTcDLOEIMuDwRsQ2dh3C5ETB8yEquG1b1j8fqnsk8es+3254NDNPMu7\r\n\tlVTsdHqKebhs9cY4fRYd4BDx42ijFYUKQFG8H1bjVV/mFUmEySnamtw2JeYkvDYNE6ycbWJl5Ys\r\n\tPqEOTittbjRfxyOLXwezWYwn7EeQK6KIcQcjC0aTLBubxG2HjjOThhXy/p1zsXag6r3OAAVFSgT\r\n\tT9Jj4gA9TKYPTm8csdKWQD+85/q2MKAsaxWjBCuun0cJh5kE5uw=\nX-Received: by 2002:aa7:d445:0:b0:67b:cd3f:ec8 with SMTP id\r\n 4fb4d7f45d1cf-67d63d89ac5mr84261a12.6.1778015299738; Tue, 05 May 2026\r\n 14:08:19 -0700 (PDT)\nMIME-Version: 1.0\nReferences: <CAH4Fh+iSvGcDSVZxQK30B4kR5kdH0BdCeiPY-C99JdoXRxU-oA@mail.gmail.com>\r\n <45621776629162@3d1cd0e9-1e27-45a4-b8ec-96a96b28957c>\nIn-Reply-To: <45621776629162@3d1cd0e9-1e27-45a4-b8ec-96a96b28957c>\nFrom: =?UTF-8?B?0J3QmNCd0JAg0JPQvg==?= <ninago558@gmail.com>\nDate: Wed, 6 May 2026 00:08:07 +0300\nX-Gm-Features: AVHnY4JOt5pqiPh9vBd1d4KYvAcUZONik5eVw4kl_UnWBy3IaTpNHHj-EoSWOY4\nMessage-ID: <CAH4Fh+j2fFagprqRhiK8_iEKJsi9YPkKdZ2rXss=_Fgk2StcFw@mail.gmail.com>\nSubject: Re:\nTo: =?UTF-8?B?0J7QsdGJ0LDRjyBtb29vbg==?= <info@mooon.by>\nContent-Type: multipart/alternative; boundary=\"00000000000058a25a0651187271\"\nReturn-Path: ninago558@gmail.com\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26811",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Здравствуйте ещё раз, не могли бы вы сказать, ещё не договаривались со\r\nстудией Glitch? Всем Уручьем ждём показ сериала, интригующие ждём июня.\r\n\r\nвс, 19 апр. 2026 г., 23:06 Общая mooon <info@mooon.by>:\r\n\r\n> Доброго времени суток.\r\n> Мы видим высокий интерес наших зрителей к этому проекту и  делаем всё\r\n> возможное, чтобы оправдать ваши ожидания.. В случае успешных переговоров с\r\n> правообладателем проекта «Удивительный цифровой цирк» на территории\r\n> Республики Беларусь, мы непременно организуем его показы",
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
      "size_bytes": 883,
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
      "size_bytes": 1145,
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
      "uid": "raw_email_26811",
      "message_id": "<CAH4Fh+j2fFagprqRhiK8_iEKJsi9YPkKdZ2rXss=_Fgk2StcFw@mail.gmail.com>",
      "subject": "Re:",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26811-20260514T102833575866\\raw_email_raw_email_26811.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26811-20260514T102833575866\\message_raw_email_26811.md",
      "items": []
    },
    "early_classification": {
      "uid": "raw_email_26811",
      "status": "ok",
      "classification": "schedule_or_repertoire_question",
      "operator_summary": "Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка».",
      "case_summary_short": "Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка».",
      "should_run_ticket_enrichment": false,
      "should_run_customer_kb": true,
      "should_build_customer_draft": false,
      "response_mode_hint": "handoff_to_operator",
      "proposed_action_type": "mark_manual_processing",
      "proposed_action_text": "Передать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён.",
      "action_stub_allowed": true,
      "classification_reason": "schedule/repertoire/movie-show question",
      "sender_email": "ninago558@gmail.com",
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
        "uid": "raw_email_26811",
        "message_id": "<CAH4Fh+j2fFagprqRhiK8_iEKJsi9YPkKdZ2rXss=_Fgk2StcFw@mail.gmail.com>",
        "subject": "Re:",
        "lookup_emails": [
          "ninago558@gmail.com"
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
        "uid": "raw_email_26811",
        "message_id": "<CAH4Fh+j2fFagprqRhiK8_iEKJsi9YPkKdZ2rXss=_Fgk2StcFw@mail.gmail.com>",
        "subject": "Re:",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26811-20260514T102833575866\\message_raw_email_26811.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26811-20260514T102833575866\\message_raw_email_26811.md"
        },
        "lookup_keys": {
          "sender_email_reference": "ninago558@gmail.com",
          "body_emails": [
            "info@mooon.by"
          ],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "ninago558@gmail.com"
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
          "body_emails_found": 1,
          "lookup_emails_total": 1,
          "confidence": "none",
          "skip_reason": "schedule/repertoire/movie-show question"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26811",
      "message_id": "<CAH4Fh+j2fFagprqRhiK8_iEKJsi9YPkKdZ2rXss=_Fgk2StcFw@mail.gmail.com>",
      "direction": "inbound",
      "sender": "ninago558@gmail.com",
      "subject": "Re:",
      "case_id": "case-000003",
      "thread_id": "thread-000003",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\state\\case_thread_registry.xlsx",
      "registry_row_number": 4,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "<45621776629162@3d1cd0e9-1e27-45a4-b8ec-96a96b28957c>",
        "references": [
          "<CAH4Fh+iSvGcDSVZxQK30B4kR5kdH0BdCeiPY-C99JdoXRxU-oA@mail.gmail.com>",
          "<45621776629162@3d1cd0e9-1e27-45a4-b8ec-96a96b28957c>"
        ]
      },
      "thread_history": [
        {
          "message_id": "<CAH4Fh+j2fFagprqRhiK8_iEKJsi9YPkKdZ2rXss=_Fgk2StcFw@mail.gmail.com>",
          "direction": "inbound",
          "sender": "ninago558@gmail.com",
          "subject": "Re:",
          "sent_at": "2026-05-06 00:08:07+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26811-20260514T102833575866\\message_raw_email_26811.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26811",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка».",
        "topic": "Вопрос по расписанию или репертуару",
        "customer_need": "Понять, возможен ли показ; без live schedule connector передать ответственным.",
        "entities": [
          {
            "type": "sender",
            "value": "ninago558@gmail.com"
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
      "uid": "raw_email_26811",
      "status": "found",
      "error": "",
      "knowledge_base_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\config\\knowledge_base\\knowledge_base.xlsx",
      "query": {
        "text": "Re: Здравствуйте ещё раз, не могли бы вы сказать, ещё не договаривались со\r\nстудией Glitch? Всем Уручьем ждём показ сериала, интригующие ждём июня.\r\n\r\nвс, 19 апр. 2026 г., 23:06 Общая mooon <info@mooon.by>:\r\n\r\n> Доброго времени суток.\r\n> Мы видим высокий интерес наших зрителей к этому проекту и  делаем всё\r\n> возможное, чтобы оправдать ваши ожидания.. В случае успешных переговоров с\r\n> правообладателем проекта «Удивительный цифровой цирк» на территории\r\n> Республики Беларусь, мы непременно организуем его показы Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка». Вопрос по расписанию или репертуару Понять, возможен ли показ; без live schedule connector передать ответственным. ninago558@gmail.com",
        "response_mode": "handoff_to_operator",
        "entities": [
          "ninago558@gmail.com"
        ]
      },
      "matched_items": [
        {
          "id": "kb_refunds_by_purchase_channel",
          "category": "refunds",
          "type": "rule",
          "title": "Возврат билетов зависит от канала покупки",
          "score": 6.0,
          "content": "Билеты, купленные в кассе, возвращаются в кассе кинотеатра не позднее чем за 10 минут до начала сеанса. Билеты Silver Screen Arena City возвращаются только в Arena City. Билеты, купленные на mooon.by, можно вернуть через личный кабинет не позднее чем за 60 минут до начала сеанса; денежный возврат — через кассу. Билеты go2.by возвращаются через go2.by/searchtickets или support@go2.by не позднее чем за 60 минут до начала сеанса. Специальные мероприятия возвращаются не менее чем за 24 часа через кассу.",
          "operator_instruction": "Сначала определить канал покупки. Если канал неизвестен — запросить номер заказа, e-mail, кинотеатр, дату/время сеанса и квитанцию.",
          "template_hint": "Порядок возврата зависит от того, где был приобретён билет: в кассе, на mooon.by или через go2.by.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'Скрипты ответов на звонки и пис'!B18:E18",
          "matched_keywords": [
            "mooon.by"
          ]
        },
        {
          "id": "kb_contacts_call_center_queue",
          "category": "general",
          "type": "operator_instruction",
          "title": "Если гость долго не может дозвониться в колл-центр",
          "score": 5.65,
          "content": "Звонки обрабатываются в порядке очередности; время ожидания может увеличиваться из-за длительности предыдущих разговоров и уточняющих вопросов.",
          "operator_instruction": "Если письмо уже пришло на info@mooon.by, не отправлять гостя снова звонить без необходимости. Решить вопрос по письму или запросить недостающие данные.",
          "template_hint": "Звонки обрабатываются в порядке очередности. Вы также можете описать вопрос в ответном письме.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'БАЗА ЗНАНИЙ'!B14:D14",
          "matched_keywords": [
            "info@mooon.by"
          ]
        },
        {
          "id": "kb_refunds_no_exchange_only_refund_and_new_purchase",
          "category": "refunds",
          "type": "rule",
          "title": "Обмен билета на другой сеанс не выполняется",
          "score": 4.0,
          "content": "Обмен или перенос билета на другой сеанс невозможен. Гостю нужно оформить возврат старого билета и приобрести новый билет на нужный сеанс.",
          "operator_instruction": "Не обещать ручной обмен. Объяснить схему: возврат по правилам канала покупки и новая покупка.",
          "template_hint": "Обмен билетов на другой сеанс невозможен. Можно оформить возврат старых билетов и приобрести новые.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'Скрипты ответов на звонки и пис'!B20:D20",
          "matched_keywords": [
            "mooon.by"
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
      "uid": "raw_email_26811",
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
        "kb_refunds_by_purchase_channel",
        "kb_contacts_call_center_queue",
        "kb_refunds_no_exchange_only_refund_and_new_purchase"
      ],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка».",
      "case_summary_short": "Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка».",
      "classification": "schedule_or_repertoire_question",
      "should_build_customer_draft": false,
      "proposed_action_type": "mark_manual_processing",
      "proposed_action_text": "Передать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён.",
      "action_stub_allowed": true,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26811",
      "status": "skipped",
      "error": "",
      "skip_reason": "Черновик не создавался: вопрос требует проверки расписания/репертуара ответственными.",
      "draft_type": "handoff_to_operator",
      "latest_revision": 0,
      "draft_text": "",
      "operator_note": "Черновик не создавался: вопрос требует проверки расписания/репертуара ответственными.",
      "source_response_mode": "handoff_to_operator",
      "created_at": "2026-05-14T10:28:33.826505+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26811-20260514T102833575866\\message_raw_email_26811.md",
      "revisions": [],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "found",
        "decision_layer_status": "ok",
        "knowledge_item_ids": []
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26811",
      "status": "mock_sent",
      "error": "",
      "created_at": "2026-05-14T10:28:33.856794+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26811-20260514T102833575866\\message_raw_email_26811.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26811-20260514T102833575866\\message_raw_email_26811.md",
      "case_id": "case-000003",
      "thread_id": "thread-000003",
      "telegram_message_id": 3,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "artifact_only",
      "telegram_operations": [],
      "callback_data": [
        "ma|approve|2a19c0b11738d8af",
        "ma|needs_edit|2a19c0b11738d8af",
        "ma|handoff|2a19c0b11738d8af",
        "ma|ignore|2a19c0b11738d8af",
        "ma|action_request|2a19c0b11738d8af"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|2a19c0b11738d8af"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|2a19c0b11738d8af"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|2a19c0b11738d8af"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|2a19c0b11738d8af"
        },
        {
          "action": "action_request",
          "label": "⚡ Выполнить действие",
          "callback_data": "ma|action_request|2a19c0b11738d8af"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: raw_email_26811\nПолучено: 06.05.2026 00:08\nОт: ninago558@gmail.com\nТема письма: Re:\nСуть обращения: Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка».\n\n<b>Кейс</b>\nCase ID: case-000003 · Thread ID: thread-000003\n\n<b>История переписки</b>\n- входящее · 2026-05-06 00:08 · без темы · Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка».\n\n<b>Вложения</b>\nнет\n\n<b>Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: вопрос по репертуару/расписанию\nЧто хочет отправитель: Понять, возможен ли показ; без live schedule connector передать ответственным.\nЧто предлагает система: Вопрос касается репертуара/расписания; live schedule connector пока не подключён.\n\n<b>Что предлагает система</b>\nРежим: передать оператору\nПричина: Вопрос касается репертуара/расписания; live schedule connector пока не подключён.\n\n<b>Предлагаемое действие</b>\nПередать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён.\nТип действия: mark_manual_processing\n\n<b>База знаний</b>\n- Возврат билетов зависит от канала покупки / kb_refunds_by_purchase_channel / балл 6.0\n- Если гость долго не может дозвониться в колл-центр / kb_contacts_call_center_queue / балл 5.65\n- Обмен билета на другой сеанс не выполняется / kb_refunds_no_exchange_only_refund_and_new_purchase / балл 4.0\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\n- Нельзя отвечать фактом о показах без проверки актуального расписания.\n\n<b>Черновик</b>\nЧерновик не создавался: вопрос требует проверки расписания/репертуара ответственными.",
      "action": "",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\telegram_operator_delivery\\case-000003\\card_20260514T102833856942.json"
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
