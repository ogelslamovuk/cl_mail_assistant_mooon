# Message dossier raw_email_26815

- UID: raw_email_26815
- Message-ID: <CAB8YdmqP_C_Y_Z4wik6bqf=6Kt2T0GVRJaBg3nQ7uVw3cXyQ_A@mail.gmail.com>
- Direction: inbound
- From: nikitamaskevich@gmail.com
- Subject: <empty>
- Sent at: 2026-05-06 11:00:28+03:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T102832666460\modules\mail_import\mock-flow-raw_email_26815-20260514T102835202984\raw_email_raw_email_26815.eml

## Case / Thread

- Case ID: case-000007
- Thread ID: thread-000007
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
- Summary: Никита Маскевич предлагает помощь с видеомонтажом, соцсетями и роликами, приложил ссылку на портфолио.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: candidate/practice/portfolio wording
- Suggested next step: Передать обращение ответственным за маркетинг/SMM или практику.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: nikitamaskevich@gmail.com

## Body

```
Здравствуйте!

Меня зовут Никита, я студент 4 курса Белорусского государственного
университета, факультета социокультурных коммуникаций, направления
«Коммуникативный дизайн».

Подскажите, пожалуйста, есть ли  возможность пройти у вас летнюю практику в
качестве видеомонтажёра? Я хотел бы развиваться в этой сфере, поэтому мне
важно к вам попасть

Я владею средними навыками видеомонтажа, работаю в программах  Adobe
Premiere Pro, After Effects, CapCut, а также имею опыт создания  роликов
для соцсетей / учебных проектов / личных проектов.

Буду рад возможности присоединиться к вашей команде, получить практический
опыт и внести свой вклад в проекты.

При необходимости готов  предоставить портфолио и выполнить тестовое
задание.

Практика является не оплачиваемой. Для её оформления нужно просто подписать
 заявление от университета, которое я смогу вам предоставить — без
необходимости оформления через бухгалтерию.

Спасибо за внимание!

С уважением,
Маскевич Никита Дмитриевич

https://drive.google.com/drive/u/0/folders/1eDteVaAMnfc-MLUekXxPlYE3tfWZyloF
— Ссылка на портфолио
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<CAB8YdmqP_C_Y_Z4wik6bqf=6Kt2T0GVRJaBg3nQ7uVw3cXyQ_A@mail.gmail.com>",
  "direction": "inbound",
  "headers": {
    "message_id": "<CAB8YdmqP_C_Y_Z4wik6bqf=6Kt2T0GVRJaBg3nQ7uVw3cXyQ_A@mail.gmail.com>",
    "in_reply_to": "",
    "references": [],
    "subject": "",
    "sender": "nikitamaskevich@gmail.com",
    "sent_at": "2026-05-06 11:00:28+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Здравствуйте!\r\n\r\nМеня зовут Никита, я студент 4 курса Белорусского государственного\r\nуниверситета, факультета социокультурных коммуникаций, направления\r\n«Коммуникативный дизайн».\r\n\r\nПодскажите, пожалуйста, есть ли  возможность пройти у вас летнюю практику в\r\nкачестве видеомонтажёра? Я хотел бы развиваться в этой сфере, поэтому мне\r\nважно к вам попасть\r\n\r\nЯ владею средними навыками видеомонтажа, работаю в программах  Adobe\r\nPremiere Pro, After Effects, CapCut, а также имею опыт создания  роликов\r\nдля соцсетей / учебных проектов / личных проектов.\r\n\r\nБуду рад возможности присоединиться к вашей команде, получить практический\r\nопыт и внести свой вклад в проекты.\r\n\r\nПри необходимости готов  предоставить портфолио и выполнить тестовое\r\nзадание.\r\n\r\nПрактика является не оплачиваемой. Для её оформления нужно просто подписать\r\n заявление от университета, которое я смогу вам предоставить — без\r\nнеобходимости оформления через бухгалтерию.\r\n\r\nСпасибо за внимание!\r\n\r\nС уважением,\r\nМаскевич Никита Дмитриевич\r\n\r\nhttps://drive.google.com/drive/u/0/folders/1eDteVaAMnfc-MLUekXxPlYE3tfWZyloF\r\n— Ссылка на портфолио",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26815-20260514T102835202984\\raw_email_raw_email_26815.eml",
  "raw_headers": "Received: from postback25a.mail.yandex.net (postback25a.mail.yandex.net [2a02:6b8:c0e:500:1:45:d181:da25])\r\n\tby 7oxtwft5tfxdka7d.vla.yp-c.yandex.net (notsolitesrv) with LMTPS id KSJgVKWXhefb-Fawj3fMD\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 11:00:42 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-59.iva.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-59.iva.yp-c.yandex.net [IPv6:2a02:6b8:c0c:a1a4:0:640:1e5b:0])\r\n\tby postback25a.mail.yandex.net (Yandex) with ESMTPS id 8D9C1C01CB\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 11:00:42 +0300 (MSK)\nReceived: from mail-ua1-x92a.google.com (mail-ua1-x92a.google.com [2607:f8b0:4864:20::92a])\r\n\tby mail-nwsmtp-mxfront-production-main-59.iva.yp-c.yandex.net (mxfront) with ESMTPS id f0cV2i4LieA0-30GKrKoD;\r\n\tWed, 06 May 2026 11:00:42 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-59.iva.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-59.iva.yp-c.yandex.net: domain of gmail.com designates 2607:f8b0:4864:20::92a as permitted sender, rule=[ip6:2607:f8b0:4864::/56]) smtp.mail=nikitamaskevich@gmail.com; dkim=pass header.i=@gmail.com\nX-Yandex-Spam: 1\nReceived: by mail-ua1-x92a.google.com with SMTP id a1e0cc1a2514c-956948531a1so1706122241.2\r\n        for <info@mooon.by>; Wed, 06 May 2026 01:00:42 -0700 (PDT)\nARC-Seal: i=1; a=rsa-sha256; t=1778054440; cv=none;\r\n        d=google.com; s=arc-20240605;\r\n        b=hhRbJu0GEnuUCu+rftxp0jFNiC0cAwD9zoEehGwpYewXEMs3LN0wn8kKdtjFXYKTjQ\r\n         ykBcgF6fOYCyAGmTuU/Mi/xE8haMsxMUQOGLxAJTPBUd7fwAjq3DJLIDRe5Ich9zENY5\r\n         mOnCQLyD04HjeZ8dZIfW05CPqqRi2Ecmo98G0QCCnHTjuE/DG1doYVYe523HJsDO6b+2\r\n         zSBbsQnV6ansAZwVMrVj+FvUwLZvJzxVRP+GkMtj3uxI6iVmHmcxX3i/Dmb2DzwsCd7C\r\n         5bdFVGkRjp1cVyKRnyH56jiN5bCtsXkfbHz5xUz1SOhXLl8OK7QwssFtPb/urayAoeH2\r\n         deOA==\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;\r\n        h=to:subject:message-id:date:from:mime-version:dkim-signature;\r\n        bh=TcdOi8BFy7+AVEW7Ny2AI2K8YPVIc+pFrLtdKaduvpI=;\r\n        fh=DFpNV6sNijizt1AwqqxcY2JMLszXwwNyEEKoHuk5Kmw=;\r\n        b=hIm+LpZBIYBp9nenEKF9IzgMDqZGK+G4rxx+nxB41afAggmp49sNPfgzshFO14qNkt\r\n         ZFO9NJU9Ls+Amy+UPhfIhigizUgnypxPfDiOFGv+jrfjv2aiC8vgeWYobsYh/bTHNsGF\r\n         00whfhrnB0+J3SwUcYxWlt4/Y9laDhY6u/x0PzpuJWYVa16XYdITN2bU54xMmGi7qr+d\r\n         +A+DnwYnYr+UsC82bQtgo8NWmKc7cRSWbBDtq6Mka+O+MC6PGn4j/wynClRoUN4ODru7\r\n         ky7nlFezYJ/kpPOeye8dvprtZxBxuqk9TLjhHF+OreYgPsWCM72vXJ8/Cebk95M7VHPT\r\n         XMxQ==;\r\n        darn=mooon.by\nARC-Authentication-Results: i=1; mx.google.com; arc=none\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=gmail.com; s=20251104; t=1778054440; x=1778659240; darn=mooon.by;\r\n        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject\r\n         :date:message-id:reply-to;\r\n        bh=TcdOi8BFy7+AVEW7Ny2AI2K8YPVIc+pFrLtdKaduvpI=;\r\n        b=N5RoSl2tmtN/JG1VxTJslS02LWfosZorLSpMWfaI3n9jH+C0dqL+V8/fu4LUYnBo34\r\n         g9XXFINIak+hugP52yKAFPkSdeItKloDMRLMLdbbPRFZNmwxwbv2bKYl3gaPbbX4VlTZ\r\n         tPQTRpAjOXpA2EN8ea8an5ubkAbQX26BcJQC/rhxW4/uxiLq6RhPugvpfoY/OyZLRWOf\r\n         y3uHoAAO+DdiO24WApLqxkUzDC502pdkzKUVmRhTRzcAAvi0o4a8fA2hk3eHvQPFLQTq\r\n         Q06F8/ls0wtfF+wODu/1yYzQGDK9mHUQE8IMA2UavMF3YiJurwIc9t9vnFRd+ctekovH\r\n         YTXQ==\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20251104; t=1778054440; x=1778659240;\r\n        h=to:subject:message-id:date:from:mime-version:x-gm-gg\r\n         :x-gm-message-state:from:to:cc:subject:date:message-id:reply-to;\r\n        bh=TcdOi8BFy7+AVEW7Ny2AI2K8YPVIc+pFrLtdKaduvpI=;\r\n        b=gG9JJysrHMYsOUnHq1ZK+B0x5poj9cZsEMYqNn1464672HdqPZlfJ9blALjTTUf4RR\r\n         /rZPAHaEk+CaVUqNElVhXkFLarzDGHBju/BelHDnPdP3ziWzGDYLi+DrhxIOL8S4r+bU\r\n         DyLVbo+dQS+iqnaatdiANARkq6efgZ8mqAwtARr3zQQGU9LUk6lHZXCya9FgORDSNvVH\r\n         b+ES+hnXnDgNBM8Ql/nB1NBuDWMFtsc8FJLiAvcqUVaiTARdoB8TitSomPIwJMR4RlKN\r\n         vb8cf8Ef0ag2UybvaBGuZhGptpeutuUQgwMBQ83zfVYTN2Nl0HjGFcJYRU/oXNg8Mr0l\r\n         I+oA==\nX-Gm-Message-State: AOJu0YxOhPRSVHLouJy/TatrrU8J7mmTXtk/3+9x56+YY/7bLhy6MA2a\r\n\tZ+0GCLFGrbCW++8G2peeRZ1a5Jcj5oXIBxk4lOZ4ZfbKkH9QBOP5Or/GFKGuTM35nxbVKx67a5C\r\n\ttH6IXlKbCcZj6v8YKcuA1rL+YzdSc9F7sRfT19jMwag==\nX-Gm-Gg: AeBDiesLOzA8yMse+wVnmJ8KkHh8RkcMIJjhBgWeET7v/x1v3Vbpmn5rAPsZFYKP73H\r\n\tEjWL8xHUsUS6+i3X3TIJaEDVggUhmib+V+nSEoQC6jOEj7XbN4wQ3mTwHSLSYQnUntOXrxZo+12\r\n\t86TyMAwefeKdAdNyoWx2+etsZI/hREbWgjrx7Pdj/5s9PLIlfjBpHXROApMF3vStwDhz1+kAjCU\r\n\tC1fopFHCxTjtaw3pcHAv9SWHCRRjJMWlFNTiWttcR6rH/JUrGb//ZMzVCMJwAE0Rlz6vbvxjV0o\r\n\t0rBR9iapfuClQnpZWVAV\nX-Received: by 2002:a05:6102:2921:b0:62f:3c55:d419 with SMTP id\r\n ada2fe7eead31-630f8c17667mr760563137.0.1778054440231; Wed, 06 May 2026\r\n 01:00:40 -0700 (PDT)\nMIME-Version: 1.0\nFrom: LeGostaeV <nikitamaskevich@gmail.com>\nDate: Wed, 6 May 2026 11:00:28 +0300\nX-Gm-Features: AVHnY4KEB_xhZlTh4QEAySy2DReIj4ZcsW-15TDjo2yulPr0DWPghGg11eQ0dQY\nMessage-ID: <CAB8YdmqP_C_Y_Z4wik6bqf=6Kt2T0GVRJaBg3nQ7uVw3cXyQ_A@mail.gmail.com>\nSubject: \nTo: info@mooon.by\nContent-Type: multipart/alternative; boundary=\"0000000000004d25d70651218fd8\"\nReturn-Path: nikitamaskevich@gmail.com\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26815",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Здравствуйте!\r\n\r\nМеня зовут Никита, я студент 4 курса Белорусского государственного\r\nуниверситета, факультета социокультурных коммуникаций, направления\r\n«Коммуникативный дизайн».\r\n\r\nПодскажите, пожалуйста, есть ли  возможность пройти у вас летнюю практику в\r\nкачестве видеомонтажёра? Я хотел бы развиваться в этой сфере, поэтому мне\r\nважно к вам попасть\r\n\r\nЯ владею средними навыками видеомонтажа, работаю в программах  Adobe\r\nPremiere Pro, After Effects, CapCut, а также имею опыт создания  роликов\r\nдля соцсетей / учебных проектов / личных проектов.\r\n\r\nБуду рад возможности присоединиться к вашей команде, получить практический\r\nопыт и внести свой вклад в проекты.\r\n\r\nПри необходимости готов  предоставить портфолио и выполнить тестовое\r\nзадание.\r\n\r\nПрактика является не оплачиваемой. Для её оформления нужно просто подписать\r\n заявление от университета, которое я смогу вам предоставить — без\r\nнеобходимости оформления через бухгалтерию.\r\n\r\nСпасибо за внимание!\r\n\r\nС уважением,\r\nМаскевич Никита Дмитриевич\r\n\r\nhttps://drive.google.com/drive/u/0/folders/1eDteVaAMnfc-MLUekXxPlYE3tfWZyloF\r\n— Ссылка на портфолио",
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
      "size_bytes": 1915,
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
      "size_bytes": 2059,
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
      "uid": "raw_email_26815",
      "message_id": "<CAB8YdmqP_C_Y_Z4wik6bqf=6Kt2T0GVRJaBg3nQ7uVw3cXyQ_A@mail.gmail.com>",
      "subject": "",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26815-20260514T102835202984\\raw_email_raw_email_26815.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26815-20260514T102835202984\\message_raw_email_26815.md",
      "items": []
    },
    "early_classification": {
      "uid": "raw_email_26815",
      "status": "ok",
      "classification": "candidate_or_portfolio",
      "operator_summary": "Никита Маскевич предлагает помощь с видеомонтажом, соцсетями и роликами, приложил ссылку на портфолио.",
      "case_summary_short": "Никита Маскевич предлагает помощь с видеомонтажом, соцсетями и роликами, приложил ссылку на портфолио.",
      "should_run_ticket_enrichment": false,
      "should_run_customer_kb": false,
      "should_build_customer_draft": false,
      "response_mode_hint": "handoff_to_operator",
      "proposed_action_type": "notify_department_stub",
      "proposed_action_text": "Передать обращение ответственным за маркетинг/SMM или практику.",
      "action_stub_allowed": true,
      "classification_reason": "candidate/practice/portfolio wording",
      "sender_email": "nikitamaskevich@gmail.com",
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
        "uid": "raw_email_26815",
        "message_id": "<CAB8YdmqP_C_Y_Z4wik6bqf=6Kt2T0GVRJaBg3nQ7uVw3cXyQ_A@mail.gmail.com>",
        "subject": "",
        "lookup_emails": [
          "nikitamaskevich@gmail.com"
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
        "uid": "raw_email_26815",
        "message_id": "<CAB8YdmqP_C_Y_Z4wik6bqf=6Kt2T0GVRJaBg3nQ7uVw3cXyQ_A@mail.gmail.com>",
        "subject": "",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26815-20260514T102835202984\\message_raw_email_26815.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26815-20260514T102835202984\\message_raw_email_26815.md"
        },
        "lookup_keys": {
          "sender_email_reference": "nikitamaskevich@gmail.com",
          "body_emails": [],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "nikitamaskevich@gmail.com"
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
      "uid": "raw_email_26815",
      "message_id": "<CAB8YdmqP_C_Y_Z4wik6bqf=6Kt2T0GVRJaBg3nQ7uVw3cXyQ_A@mail.gmail.com>",
      "direction": "inbound",
      "sender": "nikitamaskevich@gmail.com",
      "subject": "",
      "case_id": "case-000007",
      "thread_id": "thread-000007",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\state\\case_thread_registry.xlsx",
      "registry_row_number": 8,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "",
        "references": []
      },
      "thread_history": [
        {
          "message_id": "<CAB8YdmqP_C_Y_Z4wik6bqf=6Kt2T0GVRJaBg3nQ7uVw3cXyQ_A@mail.gmail.com>",
          "direction": "inbound",
          "sender": "nikitamaskevich@gmail.com",
          "subject": "",
          "sent_at": "2026-05-06 11:00:28+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26815-20260514T102835202984\\message_raw_email_26815.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26815",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Никита Маскевич предлагает помощь с видеомонтажом, соцсетями и роликами, приложил ссылку на портфолио.",
        "topic": "Кандидат или портфолио",
        "customer_need": "Передать предложение/портфолио ответственным на ручную обработку.",
        "entities": [
          {
            "type": "sender",
            "value": "nikitamaskevich@gmail.com"
          }
        ],
        "confidence": 0.62,
        "response_mode": "handoff_to_operator",
        "understanding_note": "Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.",
        "response_mode_reason": "candidate/practice/portfolio wording",
        "suggested_next_step": "Передать обращение ответственным за маркетинг/SMM или практику.",
        "risk_level": "medium",
        "needs_human": true
      }
    },
    "knowledge_retrieval": {
      "uid": "raw_email_26815",
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
      "uid": "raw_email_26815",
      "status": "ok",
      "error": "",
      "response_mode_initial": "handoff_to_operator",
      "response_mode_final": "handoff_to_operator",
      "decision_reason": "Передать обращение ответственным за маркетинг/SMM или практику.",
      "missing_data": [],
      "risks": [],
      "knowledge_item_ids": [],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Никита Маскевич предлагает помощь с видеомонтажом, соцсетями и роликами, приложил ссылку на портфолио.",
      "case_summary_short": "Никита Маскевич предлагает помощь с видеомонтажом, соцсетями и роликами, приложил ссылку на портфолио.",
      "classification": "candidate_or_portfolio",
      "should_build_customer_draft": false,
      "proposed_action_type": "notify_department_stub",
      "proposed_action_text": "Передать обращение ответственным за маркетинг/SMM или практику.",
      "action_stub_allowed": true,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26815",
      "status": "skipped",
      "error": "",
      "skip_reason": "Черновик не создавался: обращение помечено для ручной обработки ответственными.",
      "draft_type": "handoff_to_operator",
      "latest_revision": 0,
      "draft_text": "",
      "operator_note": "Черновик не создавался: обращение помечено для ручной обработки ответственными.",
      "source_response_mode": "handoff_to_operator",
      "created_at": "2026-05-14T10:28:35.423922+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26815-20260514T102835202984\\message_raw_email_26815.md",
      "revisions": [],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "skipped",
        "decision_layer_status": "ok",
        "knowledge_item_ids": []
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26815",
      "status": "mock_sent",
      "error": "",
      "created_at": "2026-05-14T10:28:35.456941+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26815-20260514T102835202984\\message_raw_email_26815.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\modules\\mail_import\\mock-flow-raw_email_26815-20260514T102835202984\\message_raw_email_26815.md",
      "case_id": "case-000007",
      "thread_id": "thread-000007",
      "telegram_message_id": 7,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "artifact_only",
      "telegram_operations": [],
      "callback_data": [
        "ma|approve|b602a438a12fe730",
        "ma|needs_edit|b602a438a12fe730",
        "ma|handoff|b602a438a12fe730",
        "ma|ignore|b602a438a12fe730",
        "ma|action_request|b602a438a12fe730"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|b602a438a12fe730"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|b602a438a12fe730"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|b602a438a12fe730"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|b602a438a12fe730"
        },
        {
          "action": "action_request",
          "label": "⚡ Выполнить действие",
          "callback_data": "ma|action_request|b602a438a12fe730"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: raw_email_26815\nПолучено: 06.05.2026 11:00\nОт: nikitamaskevich@gmail.com\nТема письма: без темы\nСуть обращения: Никита Маскевич предлагает помощь с видеомонтажом, соцсетями и роликами, приложил ссылку на портфолио.\n\n<b>Кейс</b>\nCase ID: case-000007 · Thread ID: thread-000007\n\n<b>История переписки</b>\n- входящее · 2026-05-06 11:00 · без темы · Никита Маскевич предлагает помощь с видеомонтажом, соцсетями и роликами, приложил ссылку на…\n\n<b>Вложения</b>\nнет\n\n<b>Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: кандидат/портфолио\nЧто хочет отправитель: Передать предложение/портфолио ответственным на ручную обработку.\nЧто предлагает система: Передать обращение ответственным за маркетинг/SMM или практику.\n\n<b>Что предлагает система</b>\nРежим: передать оператору\nПричина: Передать обращение ответственным за маркетинг/SMM или практику.\n\n<b>Предлагаемое действие</b>\nПередать обращение ответственным за маркетинг/SMM или практику.\nТип действия: notify_department_stub\n\n<b>База знаний</b>\nне применялась — письмо не является клиентским обращением по билетам.\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\nнет\n\n<b>Черновик</b>\nЧерновик не создавался: обращение помечено для ручной обработки ответственными.",
      "action": "",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T102832666460\\telegram_operator_delivery\\case-000007\\card_20260514T102835457032.json"
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
