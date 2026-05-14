# Message dossier raw_email_26818

- UID: raw_email_26818
- Message-ID: <CAB0_ufNWx4xPwTeVp7mgZ1KAztCx4UTyCL5c=1E8owwqFo9MEg@mail.gmail.com>
- Direction: inbound
- From: therambertbelea007@gmail.com
- Subject: Предложение о сотрудничестве
- Sent at: 2026-05-06 14:52:16+03:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T124727595245\modules\mail_import\mock-flow-raw_email_26818-20260514T124732384548\raw_email_raw_email_26818.eml

## Case / Thread

- Case ID: case-000004
- Thread ID: thread-000004
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
- Topic: Бизнес-предложение
- Customer need: Определить ответственного и обработать вручную.
- Summary: Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: business proposal / marketing services wording
- Suggested next step: Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: therambertbelea007@gmail.com

## Body

```
Добрый день! Меня зовут Александра, я режиссёр короткометражного фильма. Мы
ищем локацию для съёмки одной сцены в уборной. Ваше пространство очень
подходит нам по стилистике. Нам потребуется максимум 2 часа для съёмок. Мы
гарантируем полную сохранность имущества, чистоту после съёмок и
минимальное присутствие (группа из 5 человек). Готовы обсудить условия
аренды или рассмотреть возможность съёмки на основе упоминания вашего
заведения в титрах. Будем рады обсудить все детали!
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<CAB0_ufNWx4xPwTeVp7mgZ1KAztCx4UTyCL5c=1E8owwqFo9MEg@mail.gmail.com>",
  "direction": "inbound",
  "headers": {
    "message_id": "<CAB0_ufNWx4xPwTeVp7mgZ1KAztCx4UTyCL5c=1E8owwqFo9MEg@mail.gmail.com>",
    "in_reply_to": "",
    "references": [],
    "subject": "Предложение о сотрудничестве",
    "sender": "therambertbelea007@gmail.com",
    "sent_at": "2026-05-06 14:52:16+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Добрый день! Меня зовут Александра, я режиссёр короткометражного фильма. Мы\r\nищем локацию для съёмки одной сцены в уборной. Ваше пространство очень\r\nподходит нам по стилистике. Нам потребуется максимум 2 часа для съёмок. Мы\r\nгарантируем полную сохранность имущества, чистоту после съёмок и\r\nминимальное присутствие (группа из 5 человек). Готовы обсудить условия\r\nаренды или рассмотреть возможность съёмки на основе упоминания вашего\r\nзаведения в титрах. Будем рады обсудить все детали!",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\raw_email_raw_email_26818.eml",
  "raw_headers": "Received: from postback4d.mail.yandex.net (postback4d.mail.yandex.net [2a02:6b8:c41:1300:1:45:d181:da04])\r\n\tby mail-notsolitesrv-production-main-71.klg.yp-c.yandex.net (notsolitesrv) with LMTPS id I5FIJzTNyDps-wsEQalXb\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 14:52:31 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-71.klg.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-71.klg.yp-c.yandex.net [IPv6:2a02:6b8:c43:4691:0:640:ca01:0])\r\n\tby postback4d.mail.yandex.net (Yandex) with ESMTPS id 03A57C0166\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 14:52:31 +0300 (MSK)\nReceived: from mail-lj1-x22f.google.com (mail-lj1-x22f.google.com [2a00:1450:4864:20::22f])\r\n\tby mail-nwsmtp-mxfront-production-main-71.klg.yp-c.yandex.net (mxfront) with ESMTPS id UqfXLh7JpuQ0-zY5cFpwS;\r\n\tWed, 06 May 2026 14:52:30 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-71.klg.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-71.klg.yp-c.yandex.net: domain of gmail.com designates 2a00:1450:4864:20::22f as permitted sender, rule=[ip6:2a00:1450:4864::/56]) smtp.mail=therambertbelea007@gmail.com; dkim=pass header.i=@gmail.com\nX-Yandex-Spam: 1\nReceived: by mail-lj1-x22f.google.com with SMTP id 38308e7fff4ca-39393c1b5aaso33824121fa.3\r\n        for <info@mooon.by>; Wed, 06 May 2026 04:52:30 -0700 (PDT)\nARC-Seal: i=1; a=rsa-sha256; t=1778068350; cv=none;\r\n        d=google.com; s=arc-20240605;\r\n        b=UM3iLY4chT5yIfR1wFVEifcAR441V4ZM4eyiq3FZWw7J/TR3gNzPQ6/kK7SDRNVzT3\r\n         LTj5VW+5rZ6o9lXWYjocG5WJNSLwwtca4r1CIMfSCvN55NSk9e/uRtaXbP8sKLQaW+Os\r\n         fgM/BH2UTzTp6uvAwRIKzttwlynm0e8aKfCBebGVq6fkcTcREiM/bg2/6DkDBKEGoGUp\r\n         LN4J/YoX+tUVydencIWly2Ut5aZQlN8d1Hy73fMskAyNRWuVkdHygyyIiS8/3d7rUnBK\r\n         TXR/POSmQ2d+z3ZAh8kYSY+xU+z4JLDU8g4dl94Wp5rsST3WB/faO/9/EQBfag63VYzG\r\n         qbJg==\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;\r\n        h=to:subject:message-id:date:from:mime-version:dkim-signature;\r\n        bh=Q/JuowVigmw9kCri+gICWKe93uP1BIuEi3AZuRSihFs=;\r\n        fh=DFpNV6sNijizt1AwqqxcY2JMLszXwwNyEEKoHuk5Kmw=;\r\n        b=bQXyQs8SJ2+nG3AWr6BhBeRGU2qoUaSl64Qkr/4ZXA+Pj2uepIE0djaxPCvwtgkcZq\r\n         Hf2tIrfC82fC2doJJ6rH27/+FCxaJVe8VDSkWCmmNQk0xlAdwBeFMdzuOEgNn32PxjXr\r\n         LKalTGBtXl/U/Fw6Eaq0ffSff/Tp6ATpk4/exawAVwRMQRDZ8rYy/9ENCQnSYo7ZD6Hg\r\n         lI47gy9S68g47DIR0uGefzIcjWhp8PhLGNG8sXsGhv2bCzsWPJuV5cpxMdPDmzBEpL6O\r\n         WdE46emqvQ+y2CbU9mQfC8T5SjHqGm4VA7hrTgtWMYSr4S6MpkME3Q1LzEszVNq5XHgE\r\n         Y7Zw==;\r\n        darn=mooon.by\nARC-Authentication-Results: i=1; mx.google.com; arc=none\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=gmail.com; s=20251104; t=1778068350; x=1778673150; darn=mooon.by;\r\n        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject\r\n         :date:message-id:reply-to;\r\n        bh=Q/JuowVigmw9kCri+gICWKe93uP1BIuEi3AZuRSihFs=;\r\n        b=LPKqht7+xgofFcd6Sdy7L1H/5QHqA0ev39rJdPN2oe5X6i0d/LVy9Mftv3U06E4pPI\r\n         o7oI3/XzxEAFeUqLyCJMc0erWbihzWeBVRT2zBPfDfV2k6jhkYuGpQF7a+J8GOrKcG1F\r\n         fBWVpkMp8YA8yTZlO710onQgl5CY4WD36I61hlZwWsgswBxYti8eQ+gxkfu30K9AYopt\r\n         T8Z2DA2lJoEHnRIubTIOjLgNYRx3jE1ST5mdEa6/478Yp0gD/xsBkAx4tVsjKMr024Ff\r\n         cu8LZ9epi9rUhhwJXqIlz+59K/XExm3u8r10pgYGzZ4V5e3uuJlO3eib33bS2uNwLHGu\r\n         6MGQ==\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20251104; t=1778068350; x=1778673150;\r\n        h=to:subject:message-id:date:from:mime-version:x-gm-gg\r\n         :x-gm-message-state:from:to:cc:subject:date:message-id:reply-to;\r\n        bh=Q/JuowVigmw9kCri+gICWKe93uP1BIuEi3AZuRSihFs=;\r\n        b=RBdde4agCd91Ym0bcbqnw3lAsQG5O9lwGuCYYxJmpUGOMDhyASJBM39eNJHOm+jCUF\r\n         2U8ldrKE7U/VxRva0vwKc8VYww1Wh8Ebf32yj44vcUAATkj9aX+6a4Eav1CHZUIkuQwp\r\n         SCuz9LdVdmMqZQZIPG+mNLes8X+oO/SZbtBV/e4qv9aNe+OHnc7tmTKtDW0nNJjPOkm2\r\n         M60nbxVzcqwfFJfHPgUbBzYDxcYvz/FTFRgd5C8eMY0Vshjq5ipNi2I6YW2W+2YF4gpd\r\n         ySlUicUjniBy9s1SURma/6b+/kGoHtAKaMD3JNrC4pQVY+U3LLs9+ckD4pMw5P6EVvkN\r\n         zzCw==\nX-Gm-Message-State: AOJu0YyDwl7tSzGdIC8HsA4HNxm97I03Qo26sEpu1ib031/2X1Ou2P8/\r\n\t3czhu+Wldy1bz1ggn2ln7yGIRJrygrP9KjbXWNiwDhfsDTxcoteaZ8ntiocCZlqIrIANF1Jo03g\r\n\tklvM7U76GksYsaQoK4GAuxECHCSQ/ung6aw==\nX-Gm-Gg: AeBDietpEm/oSPHd1mAlHYRFXpfYLc3hUyH1cXK/nExaJQ7nLYMHje1mR6Pt9US3fLV\r\n\t0MEx6AOdlOnFsxRoQmzOoc5RExjIPov4rxDqHCfs7pcqRDk4JaZ0aTbzbcWIJlUiL6UTM1vG6/g\r\n\tH3hakFCbQ2xipYUJB5Il96wgBJTwoQxJe9x39WOQCWsqv3lIeQOwoCQPsm5dB54IdjSoe4Bl8md\r\n\tX3MRBHJPGkPCbiCI5/vSaIseYKUeAv6PYl6P9WXCKOsn+gaSWWYsXD27WEjoDGRJS+wnNQ6Z1j8\r\n\tPkX7ffC5qeTYG25d\nX-Received: by 2002:a05:651c:4103:b0:393:903c:2259 with SMTP id\r\n 38308e7fff4ca-393c410b4c7mr9222791fa.10.1778068349667; Wed, 06 May 2026\r\n 04:52:29 -0700 (PDT)\nMIME-Version: 1.0\nFrom: Alexandra <therambertbelea007@gmail.com>\nDate: Wed, 6 May 2026 14:52:16 +0300\nX-Gm-Features: AVHnY4L1Hz-Zx0dhaN95rVHal_8rleb2A3qO4iZI0spqgB40fun7h8OMl7KmwxU\nMessage-ID: <CAB0_ufNWx4xPwTeVp7mgZ1KAztCx4UTyCL5c=1E8owwqFo9MEg@mail.gmail.com>\nSubject: =?UTF-8?B?0J/RgNC10LTQu9C+0LbQtdC90LjQtSDQviDRgdC+0YLRgNGD0LTQvdC40YfQtdGB0YLQsg==?=\r\n\t=?UTF-8?B?0LU=?=\nTo: info@mooon.by\nContent-Type: multipart/alternative; boundary=\"0000000000005e4e80065124cc15\"\nReturn-Path: therambertbelea007@gmail.com\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26818",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Добрый день! Меня зовут Александра, я режиссёр короткометражного фильма. Мы\r\nищем локацию для съёмки одной сцены в уборной. Ваше пространство очень\r\nподходит нам по стилистике. Нам потребуется максимум 2 часа для съёмок. Мы\r\nгарантируем полную сохранность имущества, чистоту после съёмок и\r\nминимальное присутствие (группа из 5 человек). Готовы обсудить условия\r\nаренды или рассмотреть возможность съёмки на основе упоминания вашего\r\nзаведения в титрах. Будем рады обсудить все детали!",
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
      "size_bytes": 886,
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
      "size_bytes": 928,
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
      "uid": "raw_email_26818",
      "message_id": "<CAB0_ufNWx4xPwTeVp7mgZ1KAztCx4UTyCL5c=1E8owwqFo9MEg@mail.gmail.com>",
      "subject": "Предложение о сотрудничестве",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\raw_email_raw_email_26818.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
      "items": []
    },
    "early_classification": {
      "uid": "raw_email_26818",
      "status": "ok",
      "classification": "business_proposal",
      "operator_summary": "Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.",
      "case_summary_short": "Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.",
      "should_run_ticket_enrichment": false,
      "should_run_customer_kb": false,
      "should_build_customer_draft": false,
      "response_mode_hint": "handoff_to_operator",
      "proposed_action_type": "notify_department_stub",
      "proposed_action_text": "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.",
      "action_stub_allowed": true,
      "classification_reason": "business proposal / marketing services wording",
      "sender_email": "therambertbelea007@gmail.com",
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
        "uid": "raw_email_26818",
        "message_id": "<CAB0_ufNWx4xPwTeVp7mgZ1KAztCx4UTyCL5c=1E8owwqFo9MEg@mail.gmail.com>",
        "subject": "Предложение о сотрудничестве",
        "lookup_emails": [
          "therambertbelea007@gmail.com"
        ],
        "selected_lookup_email": "",
        "ticket_db_status": "skipped",
        "crm_users_status": "stub",
        "payment_refund_status": "stub",
        "confidence": "none",
        "candidates_count": 0,
        "resolved_match": null,
        "note": "ticket enrichment skipped: business proposal / marketing services wording"
      },
      "debug": {
        "uid": "raw_email_26818",
        "message_id": "<CAB0_ufNWx4xPwTeVp7mgZ1KAztCx4UTyCL5c=1E8owwqFo9MEg@mail.gmail.com>",
        "subject": "Предложение о сотрудничестве",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md"
        },
        "lookup_keys": {
          "sender_email_reference": "therambertbelea007@gmail.com",
          "body_emails": [],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "therambertbelea007@gmail.com"
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
              "business proposal / marketing services wording"
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
          "skip_reason": "business proposal / marketing services wording"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26818",
      "message_id": "<CAB0_ufNWx4xPwTeVp7mgZ1KAztCx4UTyCL5c=1E8owwqFo9MEg@mail.gmail.com>",
      "direction": "inbound",
      "sender": "therambertbelea007@gmail.com",
      "subject": "Предложение о сотрудничестве",
      "case_id": "case-000004",
      "thread_id": "thread-000004",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\state\\case_thread_registry.xlsx",
      "registry_row_number": 5,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "",
        "references": []
      },
      "thread_history": [
        {
          "message_id": "<CAB0_ufNWx4xPwTeVp7mgZ1KAztCx4UTyCL5c=1E8owwqFo9MEg@mail.gmail.com>",
          "direction": "inbound",
          "sender": "therambertbelea007@gmail.com",
          "subject": "Предложение о сотрудничестве",
          "sent_at": "2026-05-06 14:52:16+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26818",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.",
        "topic": "Бизнес-предложение",
        "customer_need": "Определить ответственного и обработать вручную.",
        "entities": [
          {
            "type": "sender",
            "value": "therambertbelea007@gmail.com"
          }
        ],
        "confidence": 0.62,
        "response_mode": "handoff_to_operator",
        "understanding_note": "Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.",
        "response_mode_reason": "business proposal / marketing services wording",
        "suggested_next_step": "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.",
        "risk_level": "medium",
        "needs_human": true
      }
    },
    "knowledge_retrieval": {
      "uid": "raw_email_26818",
      "status": "skipped",
      "error": "",
      "reason": "business proposal / marketing services wording",
      "classification": "business_proposal",
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
      "uid": "raw_email_26818",
      "status": "ok",
      "error": "",
      "response_mode_initial": "handoff_to_operator",
      "response_mode_final": "handoff_to_operator",
      "decision_reason": "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.",
      "missing_data": [],
      "risks": [],
      "knowledge_item_ids": [],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.",
      "case_summary_short": "Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.",
      "classification": "business_proposal",
      "should_build_customer_draft": false,
      "proposed_action_type": "notify_department_stub",
      "proposed_action_text": "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.",
      "action_stub_allowed": true,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26818",
      "status": "skipped",
      "error": "",
      "skip_reason": "Черновик не создавался: обращение помечено для ручной обработки ответственными.",
      "draft_type": "handoff_to_operator",
      "latest_revision": 0,
      "draft_text": "",
      "operator_note": "Черновик не создавался: обращение помечено для ручной обработки ответственными.",
      "source_response_mode": "handoff_to_operator",
      "created_at": "2026-05-14T12:47:43.519450+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
      "revisions": [],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "skipped",
        "decision_layer_status": "ok",
        "knowledge_item_ids": []
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26818",
      "status": "action_action_request",
      "error": "",
      "created_at": "2026-05-14T12:47:43.665305+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
      "case_id": "case-000004",
      "thread_id": "thread-000004",
      "telegram_message_id": 4,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "telegram_bot_api",
      "telegram_operations": [
        {
          "operation": "editMessageText",
          "ok": true,
          "chat_id": "mock-operator-chat",
          "message_id": 4,
          "text": "<b>📩 Новое письмо</b>\n\n⚡ Действие зафиксировано: письмо передано в отдел партнёрств/маркетинга или администрацию объекта в mock-режиме. Реальная маршрутизация пока не подключена.\n\n<b>Письмо</b>\nUID: raw_email_26818\nПолучено: 06.05.2026 14:52\nОт: therambertbelea007@gmail.com\nТема письма: Предложение о сотрудничестве\nСуть обращения: Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.\n\n<b>Кейс</b>\nCase ID: case-000004 · Thread ID: thread-000004\n\n<b>История переписки</b>\nотсутствует\n\n<b>Вложения</b>\nнет\n\n<b>Проверка билетов / Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: бизнес-предложение\nЧто хочет отправитель: Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.\nСледующий шаг: Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта. Уточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания.\n\n<b>Что предлагает система</b>\nЧто сделать: Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта. Уточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания.\nПочему: Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.\n\n<b>Обновлённое действие v2</b>\nВерсия предложения: v2\nПередать письмо ответственным за партнёрства, маркетинг или администрацию объекта.\nУточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания.\nТип действия: уведомить отдел\n\n<b>База знаний</b>\nне применялась — письмо не требует клиентской базы знаний по билетам.\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\nнет\n\n<b>Комментарий оператора</b>\nУточни, что это съёмка фильма, а не вопрос расписания.\n\n<b>Черновик</b>\nЧерновик не создавался: обращение помечено для ручной обработки ответственными.\n\n<b>Последнее действие</b>\nдействие зафиксировано в mock-режиме",
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
          "message_id": 4,
          "reply_markup": {
            "inline_keyboard": []
          }
        },
        {
          "operation": "answerCallbackQuery",
          "ok": true,
          "callback_query_id": "cb_action_after_revision",
          "text": "Действие зафиксировано. Реальная маршрутизация пока не подключена."
        }
      ],
      "callback_data": [
        "ma|approve|48dbb608fd5e841b",
        "ma|needs_edit|48dbb608fd5e841b",
        "ma|handoff|48dbb608fd5e841b",
        "ma|ignore|48dbb608fd5e841b",
        "ma|action_request|48dbb608fd5e841b"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|48dbb608fd5e841b"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|48dbb608fd5e841b"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|48dbb608fd5e841b"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|48dbb608fd5e841b"
        },
        {
          "action": "action_request",
          "label": "⚡ Выполнить действие",
          "callback_data": "ma|action_request|48dbb608fd5e841b"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n⚡ Действие зафиксировано: письмо передано в отдел партнёрств/маркетинга или администрацию объекта в mock-режиме. Реальная маршрутизация пока не подключена.\n\n<b>Письмо</b>\nUID: raw_email_26818\nПолучено: 06.05.2026 14:52\nОт: therambertbelea007@gmail.com\nТема письма: Предложение о сотрудничестве\nСуть обращения: Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.\n\n<b>Кейс</b>\nCase ID: case-000004 · Thread ID: thread-000004\n\n<b>История переписки</b>\nотсутствует\n\n<b>Вложения</b>\nнет\n\n<b>Проверка билетов / Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: бизнес-предложение\nЧто хочет отправитель: Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах.\nСледующий шаг: Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта. Уточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания.\n\n<b>Что предлагает система</b>\nЧто сделать: Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта. Уточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания.\nПочему: Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.\n\n<b>Обновлённое действие v2</b>\nВерсия предложения: v2\nПередать письмо ответственным за партнёрства, маркетинг или администрацию объекта.\nУточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания.\nТип действия: уведомить отдел\n\n<b>База знаний</b>\nне применялась — письмо не требует клиентской базы знаний по билетам.\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\nнет\n\n<b>Комментарий оператора</b>\nУточни, что это съёмка фильма, а не вопрос расписания.\n\n<b>Черновик</b>\nЧерновик не создавался: обращение помечено для ручной обработки ответственными.\n\n<b>Последнее действие</b>\nдействие зафиксировано в mock-режиме",
      "action": "action_request",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\telegram_operator_delivery\\case-000004\\card_20260514T124743665392.json"
    },
    "operator_actions": {
      "status": "ok",
      "latest_action": {
        "uid": "raw_email_26818",
        "case_id": "case-000004",
        "thread_id": "thread-000004",
        "action": "action_requested",
        "operator_comment": "",
        "operator_telegram_id": "101",
        "operator_username": "demo_operator",
        "created_at": "20260514T124743664249",
        "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md#modules.draft_builder",
        "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
        "callback_data": "ma|action_request|48dbb608fd5e841b",
        "mock_reply_refs": [],
        "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\telegram_operator_delivery\\case-000004\\card_20260514T124743665392.json",
        "real_email_sent": false,
        "action_type": "notify_department_stub",
        "status": "stub_recorded",
        "real_routing": false,
        "proposed_action_text": "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.\nУточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания."
      },
      "actions": [
        {
          "uid": "raw_email_26818",
          "case_id": "case-000004",
          "thread_id": "thread-000004",
          "action": "needs_edit",
          "operator_comment": "",
          "operator_telegram_id": "101",
          "operator_username": "demo_operator",
          "created_at": "20260514T124743381363",
          "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md#modules.draft_builder",
          "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
          "callback_data": "ma|needs_edit|48dbb608fd5e841b",
          "mock_reply_refs": [],
          "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\telegram_operator_delivery\\case-000004\\card_20260514T124743432074.json",
          "real_email_sent": false,
          "status": "waiting_operator_comment"
        },
        {
          "uid": "raw_email_26818",
          "case_id": "case-000004",
          "thread_id": "thread-000004",
          "action": "action_requested",
          "operator_comment": "",
          "operator_telegram_id": "101",
          "operator_username": "demo_operator",
          "created_at": "20260514T124743664249",
          "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md#modules.draft_builder",
          "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
          "callback_data": "ma|action_request|48dbb608fd5e841b",
          "mock_reply_refs": [],
          "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\telegram_operator_delivery\\case-000004\\card_20260514T124743665392.json",
          "real_email_sent": false,
          "action_type": "notify_department_stub",
          "status": "stub_recorded",
          "real_routing": false,
          "proposed_action_text": "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.\nУточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания."
        }
      ],
      "real_email_sent": false
    },
    "revision_requests": {
      "status": "ok",
      "latest_request": {
        "uid": "raw_email_26818",
        "case_id": "case-000004",
        "thread_id": "thread-000004",
        "latest_revision": 0,
        "operator_comment": "Уточни, что это съёмка фильма, а не вопрос расписания.",
        "operator_telegram_id": "101",
        "operator_username": "demo_operator",
        "source_callback_data": "ma|needs_edit|48dbb608fd5e841b",
        "source_chat_id": "mock-operator-chat",
        "source_message_id": 4,
        "created_at": "20260514T124743491150",
        "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
        "status": "created",
        "artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\revision_requests\\case-000004\\revision_request_20260514T124743491150.json"
      },
      "requests": [
        {
          "uid": "raw_email_26818",
          "case_id": "case-000004",
          "thread_id": "thread-000004",
          "latest_revision": 0,
          "operator_comment": "Уточни, что это съёмка фильма, а не вопрос расписания.",
          "operator_telegram_id": "101",
          "operator_username": "demo_operator",
          "source_callback_data": "ma|needs_edit|48dbb608fd5e841b",
          "source_chat_id": "mock-operator-chat",
          "source_message_id": 4,
          "created_at": "20260514T124743491150",
          "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
          "status": "created",
          "artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\revision_requests\\case-000004\\revision_request_20260514T124743491150.json"
        }
      ]
    },
    "action_suggestion_builder": {
      "uid": "raw_email_26818",
      "status": "ok",
      "error": "",
      "latest_revision": 2,
      "action_type": "notify_department_stub",
      "action_text": "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.\nУточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания.",
      "operator_comment": "Уточни, что это съёмка фильма, а не вопрос расписания.",
      "created_at": "2026-05-14T12:47:43.547426+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T124727595245\\modules\\mail_import\\mock-flow-raw_email_26818-20260514T124732384548\\message_raw_email_26818.md",
      "revisions": [
        {
          "revision": 1,
          "created_at": "2026-05-14T12:47:43.547385+00:00",
          "revision_reason": "initial",
          "operator_comment": "",
          "action_type": "notify_department_stub",
          "action_text": "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта."
        },
        {
          "revision": 2,
          "created_at": "2026-05-14T12:47:43.547426+00:00",
          "revision_reason": "operator_needs_edit_comment",
          "operator_comment": "Уточни, что это съёмка фильма, а не вопрос расписания.",
          "action_type": "notify_department_stub",
          "action_text": "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта.\nУточнение оператора: Уточни, что это съёмка фильма, а не вопрос расписания."
        }
      ]
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
