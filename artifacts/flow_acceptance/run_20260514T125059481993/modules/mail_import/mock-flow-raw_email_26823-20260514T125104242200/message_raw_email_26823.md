# Message dossier raw_email_26823

- UID: raw_email_26823
- Message-ID: <CAAMdjv+mp=WuTosUy8CTud__EoQ-a1RTRF6F=Z6werLOhuT+5A@mail.gmail.com>
- Direction: inbound
- From: kozlova22anna@gmail.com
- Subject: <empty>
- Sent at: 2026-05-06 20:45:22+03:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T125059481993\modules\mail_import\mock-flow-raw_email_26823-20260514T125104242200\raw_email_raw_email_26823.eml

## Case / Thread

- Case ID: case-000007
- Thread ID: thread-000007
- Binding rule: new_case_thread
- Binding status: new_case_thread

## Enrichment

- Ticket DB status: <empty>
- Selected lookup email: kozlova22anna@gmail.com
- Resolved ticket: 43174015

## Attachments

- Count: 1
- Text found in: 0

- attachment_extraction_raw_email_26823__ticket.pdf
  - content_type: application/pdf
  - text_found: no

## LLM Understanding

- Status: ok
- Response mode: ask_clarifying_question
- Confidence: 0.62
- Topic: Клиентский вопрос по билету/оплате
- Customer need: Получить помощь по билету или оплате.
- Summary: Гость спрашивает, как вернуть деньги за билет.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: customer ticket/payment/refund/certificate wording
- Suggested next step: Проверить карточку и выбрать действие кнопками.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: kozlova22anna@gmail.com

## Body

```
Добрый вечер. Купила билеты не в тот кинотеатр . Можно сделать возврат ?
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<CAAMdjv+mp=WuTosUy8CTud__EoQ-a1RTRF6F=Z6werLOhuT+5A@mail.gmail.com>",
  "direction": "inbound",
  "headers": {
    "message_id": "<CAAMdjv+mp=WuTosUy8CTud__EoQ-a1RTRF6F=Z6werLOhuT+5A@mail.gmail.com>",
    "in_reply_to": "",
    "references": [],
    "subject": "",
    "sender": "kozlova22anna@gmail.com",
    "sent_at": "2026-05-06 20:45:22+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Добрый вечер. Купила билеты не в тот кинотеатр . Можно сделать возврат ?",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\raw_email_raw_email_26823.eml",
  "raw_headers": "Received: from postback2b.mail.yandex.net (postback2b.mail.yandex.net [2a02:6b8:c02:900:1:45:d181:da02])\r\n\tby eutejgsdnfcfz3to.sas.yp-c.yandex.net (notsolitesrv) with LMTPS id WLNh1olNAk5L-SxtXE1iP\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 20:45:38 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-898.sas.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-898.sas.yp-c.yandex.net [IPv6:2a02:6b8:c23:2243:0:640:d698:0])\r\n\tby postback2b.mail.yandex.net (Yandex) with ESMTPS id A22CBC00B0\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 20:45:38 +0300 (MSK)\nReceived: from mail-pj1-x1035.google.com (mail-pj1-x1035.google.com [2607:f8b0:4864:20::1035])\r\n\tby mail-nwsmtp-mxfront-production-main-898.sas.yp-c.yandex.net (mxfront) with ESMTPS id ajl4AQ0KSW20-fkGntScw;\r\n\tWed, 06 May 2026 20:45:37 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-898.sas.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-898.sas.yp-c.yandex.net: domain of gmail.com designates 2607:f8b0:4864:20::1035 as permitted sender, rule=[ip6:2607:f8b0:4864::/56]) smtp.mail=kozlova22anna@gmail.com; dkim=pass header.i=@gmail.com\nX-Yandex-Spam: 1\nReceived: by mail-pj1-x1035.google.com with SMTP id 98e67ed59e1d1-364e5d895e3so4808521a91.2\r\n        for <info@mooon.by>; Wed, 06 May 2026 10:45:37 -0700 (PDT)\nARC-Seal: i=1; a=rsa-sha256; t=1778089535; cv=none;\r\n        d=google.com; s=arc-20240605;\r\n        b=cibC/VjYvDKNq4rfJmpOVR9mp2RUSZyVCI7xm7OP7uoynkcnLF++SsH/wH6Lsfn7fz\r\n         z6mP5yNti5zXtLv52sSi2pZLwpClJera4oeUsO+lPmYTWebxTqwQBVO+eO4OM13C8oXS\r\n         hLvNPkb3cEDshcnXpb9fWXKPvUMXvM7yqqTdJ/7A8iPAK5QV4kuxcJyedPG6sZXEnrUT\r\n         aNI/InuCfGedJf9zcOtjynya/QB/XzuKFg9w+eCeOPvltRVOyFytLO7VGbGSCoSamt0M\r\n         4JLMOVtWXcfWtfGIAOB9ny5DaIcRlUFl7Qsw+BmgO+bjCkmpU+4mQCvd5oLva577KSh/\r\n         tong==\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;\r\n        h=to:subject:message-id:date:from:mime-version:dkim-signature;\r\n        bh=j/9C3sqcyRU802rhcXvIAb1echYbdHx9dfBpOwz+Oq8=;\r\n        fh=DFpNV6sNijizt1AwqqxcY2JMLszXwwNyEEKoHuk5Kmw=;\r\n        b=i9NHz/2W0XbY0p3JIQqHhj8y1wUu3+MQmXx15ebh0udT71T2YxxTiuWXNINuFt92Kp\r\n         lsXRLXNrmNUW+wi/GlRVy9JTFxBKrMhk1MGw0ETOV9CINfXjWG0bHzTKtUrTfU3ABn2J\r\n         ZUPDyJyVvaJEnIFZO/gsSxU1t54OT1bAFmLN64xPGXRTB0jOXnnL2visRoGXHrojJwdZ\r\n         gdvR9u5uVT4mtLqpGpnjDMQjUanbbC+CHRzw30bIfFcCMBkt+pwxjWxHu/rfRPWuz200\r\n         U8GDflY3KMNLyMaCRYkk896KOF9ySldA4cpYqtc2TdBa5vztctKyYtACSlCFIUmtbFTy\r\n         AmGQ==;\r\n        darn=mooon.by\nARC-Authentication-Results: i=1; mx.google.com; arc=none\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=gmail.com; s=20251104; t=1778089535; x=1778694335; darn=mooon.by;\r\n        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject\r\n         :date:message-id:reply-to;\r\n        bh=j/9C3sqcyRU802rhcXvIAb1echYbdHx9dfBpOwz+Oq8=;\r\n        b=Se/ucB/utK1kPGwGLJVu9Y4TH2dR1zX/idd9pYV5WBxS4g9FWu/KK/d0/zG4rEwyqp\r\n         0KXap/4R9X52s94nqMwlMw6wzRbIjGhvPZLZ+2uxHSQtap8MBWXGPxoYh9feJ3QEiHEk\r\n         ZSnK7HdTMaTisfRF2InrzUOG/iA3iJkSzQ9nMBMIwpY5FDssoO8oD3bifSSOFnn1/4VF\r\n         p9oEwuGyYeGTD//E9VSOmTDddjEca2te1Lmw8bNlC1CWNGPDIM4j6tIW0lM3y86Wc5yG\r\n         DtvP5uyrnvFqVDzH2y2fWz+3DO1NRMBK/NQApbm3ouP4S06z38XZ1BwNoRzeekhPygy7\r\n         dTCg==\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20251104; t=1778089535; x=1778694335;\r\n        h=to:subject:message-id:date:from:mime-version:x-gm-gg\r\n         :x-gm-message-state:from:to:cc:subject:date:message-id:reply-to;\r\n        bh=j/9C3sqcyRU802rhcXvIAb1echYbdHx9dfBpOwz+Oq8=;\r\n        b=C3dKr25CJ/dfMnSZQNFnsoyHn1e1EnOi1mpwvQWzmsbs7JeXP+M6SD6m9buhh/47hK\r\n         55aufp2Yd28AU9p7x8bbsPawMaX6elxkrIGgw125BqvEfExB2KP71LWNM3r2tZsm6ZPw\r\n         +TesEczlUaBxlfnOmTTeCaAHILMSuhR96sBZRR5Y3iK5q2OObluuBkqDPUktabl/sU36\r\n         jvx+xXa3UOeIhdLiSjMaWxiNM57/g8yZ47UbSXoEkBlKCZ+Lve9lTD97C/NAB2471CyO\r\n         LkQHrpheZDxhugCquKYi89RhzW+JfR98vNV1revqKGr7HfJ97NG1Rz6/8AIdbdJUsWvE\r\n         gZfg==\nX-Gm-Message-State: AOJu0YzGrLqyroDuyfWr+fYPOLggCPqBtxs3mRKy55x3kNjZ7ZvAf1G7\r\n\tsZKoxzXgpBgn2bKTg3+Wa1oem3QgCJqKb5V/AwHYSgD8C6suUSkjSgsRFJPMOP9j0F/Uy8Z3SGj\r\n\turffm5FTNFMttZX1SsPdZNjVdfMBGsFSyMQ==\nX-Gm-Gg: AeBDievcIv9I2sgzQ05J3Rt9iz9hEWi7ITQYM/8qOMWzf78/ocfHZdy7rPpuflw3fvm\r\n\tNMi6Jrqclrva8qXDLqEwT2jeOmZ4d8dudPFdSzFxtiLcOoBq+AAQ5UBA+kZSmNHxUaCFnwSSbN3\r\n\tGH5bN6dbDZ/NV84MZQAdYYTVLnr7pFo9xN66CqNwmqDK8Y1U6TePXahp49ctDQ76uqrCshBzqT0\r\n\t/sjFKRhn5NEagQx0rstOzYUmdWNygFxZIaHHnlOqQd/aMJYBRtvrFC9i3Y3k8gjpZYLC6Kxsc+2\r\n\t0MREF3sp1U/3CrFjOs7r\nX-Received: by 2002:a17:90b:4d04:b0:35a:189b:43db with SMTP id\r\n 98e67ed59e1d1-365ab9b8bd7mr4006640a91.4.1778089535028; Wed, 06 May 2026\r\n 10:45:35 -0700 (PDT)\nMIME-Version: 1.0\nFrom: Anna Kozlova <kozlova22anna@gmail.com>\nDate: Wed, 6 May 2026 20:45:22 +0300\nX-Gm-Features: AVHnY4LgRJwNVGm2i8LhNYLIkvfb1SxnQfrmrR5NKu0SBdbHIPW9UDy3kB6538I\nMessage-ID: <CAAMdjv+mp=WuTosUy8CTud__EoQ-a1RTRF6F=Z6werLOhuT+5A@mail.gmail.com>\nSubject: \nTo: info@mooon.by\nContent-Type: multipart/mixed; boundary=\"0000000000001d5b57065129bb8a\"\nReturn-Path: kozlova22anna@gmail.com\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26823",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Добрый вечер. Купила билеты не в тот кинотеатр . Можно сделать возврат ?",
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
      "part_index": 2,
      "content_type": "text/plain",
      "content_disposition": "",
      "filename": "",
      "content_id": "",
      "charset": "utf-8",
      "is_multipart": false,
      "size_bytes": 131,
      "is_inline": false,
      "is_attachment": false
    },
    {
      "part_index": 3,
      "content_type": "text/html",
      "content_disposition": "",
      "filename": "",
      "content_id": "",
      "charset": "utf-8",
      "is_multipart": false,
      "size_bytes": 133,
      "is_inline": false,
      "is_attachment": false
    },
    {
      "part_index": 4,
      "content_type": "application/pdf",
      "content_disposition": "attachment",
      "filename": "ticket.pdf",
      "content_id": "19dfe64ed7262f069f61",
      "charset": "",
      "is_multipart": false,
      "size_bytes": 103107,
      "is_inline": false,
      "is_attachment": true
    }
  ],
  "has_attachments": true,
  "has_inline_parts": false,
  "attachments_inventory": [
    {
      "part_index": 4,
      "filename": "ticket.pdf",
      "content_type": "application/pdf",
      "content_disposition": "attachment",
      "content_id": "19dfe64ed7262f069f61",
      "is_inline": false,
      "is_attachment": true,
      "size_bytes": 103107
    }
  ],
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
      "uid": "raw_email_26823",
      "message_id": "<CAAMdjv+mp=WuTosUy8CTud__EoQ-a1RTRF6F=Z6werLOhuT+5A@mail.gmail.com>",
      "subject": "",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\raw_email_raw_email_26823.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\message_raw_email_26823.md",
      "items": [
        {
          "part_index": 4,
          "filename_original": "ticket.pdf",
          "filename_saved": "attachment_extraction_raw_email_26823__ticket.pdf",
          "content_type": "application/pdf",
          "content_disposition": "attachment",
          "is_inline": false,
          "is_attachment": true,
          "saved_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\attachment_extraction_raw_email_26823__ticket.pdf",
          "text_found": false,
          "text_path": "",
          "text_preview": "",
          "extraction_method": "pdf_native_unavailable",
          "error": "",
          "skip_reason": ""
        }
      ]
    },
    "early_classification": {
      "uid": "raw_email_26823",
      "status": "ok",
      "classification": "customer_support",
      "operator_summary": "Гость спрашивает, как вернуть деньги за билет.",
      "case_summary_short": "Гость спрашивает, как вернуть деньги за билет.",
      "should_run_ticket_enrichment": true,
      "should_run_customer_kb": true,
      "should_build_customer_draft": true,
      "response_mode_hint": "ask_clarifying_question",
      "proposed_action_type": "",
      "proposed_action_text": "",
      "action_stub_allowed": false,
      "classification_reason": "customer ticket/payment/refund/certificate wording",
      "sender_email": "kozlova22anna@gmail.com",
      "own_sender_or_recipient": false,
      "recipient_emails": [
        "info@mooon.by",
        "no-reply@mooon.by",
        "noreply@mooon.by",
        "support@mooon.by"
      ],
      "attachment_count": 1
    },
    "identity_context_enrichment": {
      "result": {
        "uid": "raw_email_26823",
        "message_id": "<CAAMdjv+mp=WuTosUy8CTud__EoQ-a1RTRF6F=Z6werLOhuT+5A@mail.gmail.com>",
        "subject": "",
        "lookup_emails": [
          "kozlova22anna@gmail.com"
        ],
        "selected_lookup_email": "kozlova22anna@gmail.com",
        "ticket_db_status": "found_strict",
        "crm_users_status": "stub",
        "payment_refund_status": "stub",
        "confidence": "high",
        "candidates_count": 1,
        "resolved_match": {
          "ticket": 43174015,
          "idTrading": 7056395,
          "dateShow": "2026-05-09",
          "timeShow": "18:40:00",
          "theater": "mooon в ТРК Minsk City Mall",
          "event": "Дьявол носит Prada 2",
          "auditorium": "Зал 1 Premiere",
          "line": 2,
          "seat": 8,
          "match_type": "local_mock_fixture",
          "emailClient": "kozlova22anna@gmail.com",
          "resolved_via": "ticket_db_strict"
        },
        "note": "TECHNICAL WARNING: ticket_db unavailable; local mock ticket fixture used for demo acceptance."
      },
      "debug": {
        "uid": "raw_email_26823",
        "message_id": "<CAAMdjv+mp=WuTosUy8CTud__EoQ-a1RTRF6F=Z6werLOhuT+5A@mail.gmail.com>",
        "subject": "",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\message_raw_email_26823.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\message_raw_email_26823.md"
        },
        "lookup_keys": {
          "sender_email_reference": "kozlova22anna@gmail.com",
          "body_emails": [],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "kozlova22anna@gmail.com"
          ],
          "selected_lookup_email": "kozlova22anna@gmail.com",
          "selected_lookup_localpart": "kozlova22anna"
        },
        "providers": {
          "ticket_db": {
            "status": "found_strict",
            "settings_source": "config.local.yaml",
            "candidates": [
              {
                "ticket": 43174015,
                "idTrading": 7056395,
                "dateShow": "2026-05-09",
                "timeShow": "18:40:00",
                "theater": "mooon в ТРК Minsk City Mall",
                "event": "Дьявол носит Prada 2",
                "auditorium": "Зал 1 Premiere",
                "line": 2,
                "seat": 8,
                "match_type": "local_mock_fixture",
                "emailClient": "kozlova22anna@gmail.com",
                "candidate_source": "strict"
              }
            ],
            "rescue_confident": false,
            "rescue_reason": "",
            "rescue_top1": 0.0,
            "rescue_gap": 0.0,
            "notes": [
              "TECHNICAL WARNING: ticket_db unavailable; local mock ticket fixture used for demo acceptance."
            ],
            "query_email": "kozlova22anna@gmail.com",
            "query_localpart": "kozlova22anna",
            "lookup_trace": [
              {
                "email": "kozlova22anna@gmail.com",
                "status": "found_strict",
                "rows": 1,
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
        "resolved_match": {
          "ticket": 43174015,
          "idTrading": 7056395,
          "dateShow": "2026-05-09",
          "timeShow": "18:40:00",
          "theater": "mooon в ТРК Minsk City Mall",
          "event": "Дьявол носит Prada 2",
          "auditorium": "Зал 1 Premiere",
          "line": 2,
          "seat": 8,
          "match_type": "local_mock_fixture",
          "emailClient": "kozlova22anna@gmail.com",
          "resolved_via": "ticket_db_strict"
        },
        "summary": {
          "ticket_found": true,
          "ticket_db_status": "found_strict",
          "crm_users_status": "stub",
          "payment_refund_status": "stub",
          "attachment_report_present": true,
          "body_emails_found": 0,
          "lookup_emails_total": 1,
          "confidence": "high"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26823",
      "message_id": "<CAAMdjv+mp=WuTosUy8CTud__EoQ-a1RTRF6F=Z6werLOhuT+5A@mail.gmail.com>",
      "direction": "inbound",
      "sender": "kozlova22anna@gmail.com",
      "subject": "",
      "case_id": "case-000007",
      "thread_id": "thread-000007",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\state\\case_thread_registry.xlsx",
      "registry_row_number": 8,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "",
        "references": []
      },
      "thread_history": [
        {
          "message_id": "<CAAMdjv+mp=WuTosUy8CTud__EoQ-a1RTRF6F=Z6werLOhuT+5A@mail.gmail.com>",
          "direction": "inbound",
          "sender": "kozlova22anna@gmail.com",
          "subject": "",
          "sent_at": "2026-05-06 20:45:22+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\message_raw_email_26823.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26823",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Гость спрашивает, как вернуть деньги за билет.",
        "topic": "Клиентский вопрос по билету/оплате",
        "customer_need": "Получить помощь по билету или оплате.",
        "entities": [
          {
            "type": "sender",
            "value": "kozlova22anna@gmail.com"
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
      "uid": "raw_email_26823",
      "status": "found",
      "error": "",
      "knowledge_base_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\config\\knowledge_base\\knowledge_base.xlsx",
      "query": {
        "text": " Добрый вечер. Купила билеты не в тот кинотеатр . Можно сделать возврат ? Гость спрашивает, как вернуть деньги за билет. Клиентский вопрос по билету/оплате Получить помощь по билету или оплате. kozlova22anna@gmail.com",
        "response_mode": "ask_clarifying_question",
        "entities": [
          "kozlova22anna@gmail.com"
        ]
      },
      "matched_items": [
        {
          "id": "kb_giftcards_no_cash_refund",
          "category": "certificates",
          "type": "regulation",
          "title": "Деньги по подарочной карте или сертификату не возвращаются",
          "score": 6.9,
          "content": "Подарочная карта или сертификат предназначены для оплаты услуг/товаров. Денежный возврат по подарочной карте или сертификату не выполняется, если иное не установлено отдельным решением.",
          "operator_instruction": "При претензии с юридическими требованиями передать оператору/юристам.",
          "template_hint": "Подарочная карта предназначена для оплаты услуг кинопространства.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'Скрипты ответов на звонки и пис'!B90:C90",
          "matched_keywords": [
            "деньги",
            "возврат"
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
        },
        {
          "id": "kb_reviews_request_details_for_nonstandard_case",
          "category": "complaints",
          "type": "response_template",
          "title": "Запрос деталей по нестандартной жалобе",
          "score": 5.75,
          "content": "Для нестандартных ситуаций нужно запросить дополнительные детали, чтобы разобраться: кинотеатр, дата, время, сеанс, зал/места, описание ситуации и контактные данные.",
          "operator_instruction": "Использовать как шаблон уточнения, если исходное письмо эмоциональное, но без фактов.",
          "template_hint": "Уточните, пожалуйста, дату, время посещения, кинотеатр, зал и детали ситуации.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'Скрипты ответов на отзывы'!B20:C20",
          "matched_keywords": [
            "кинотеатр"
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
      "uid": "raw_email_26823",
      "status": "ok",
      "error": "",
      "response_mode_initial": "ask_clarifying_question",
      "response_mode_final": "answer",
      "decision_reason": "Билет/заказ найден в проверке билетов; уточнять email, телефон или номер заказа не нужно.",
      "missing_data": [],
      "risks": [],
      "knowledge_item_ids": [
        "kb_giftcards_no_cash_refund",
        "kb_tickets_lost_without_receipt",
        "kb_reviews_request_details_for_nonstandard_case"
      ],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Гость спрашивает, как вернуть деньги за билет.",
      "case_summary_short": "Гость спрашивает, как вернуть деньги за билет.",
      "classification": "customer_support",
      "should_build_customer_draft": true,
      "proposed_action_type": "",
      "proposed_action_text": "",
      "action_stub_allowed": false,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26823",
      "status": "ok",
      "error": "",
      "draft_type": "answer",
      "latest_revision": 1,
      "draft_text": "Здравствуйте.\nМы нашли ваш заказ: заказ 7056395 · Дьявол носит Prada 2 · 2026-05-09 18:40:00 · mooon в ТРК Minsk City Mall.\nЕсли нужно оформить возврат, подтвердите это в ответном письме; оператор продолжит обработку по найденному заказу.\nС уважением, команда mooon.",
      "operator_note": "Черновик создан в демо-режиме; реальная отправка отключена.",
      "source_response_mode": "answer",
      "created_at": "2026-05-14T12:51:05.044184+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\message_raw_email_26823.md",
      "revisions": [
        {
          "revision": 1,
          "created_at": "2026-05-14T12:51:05.044184+00:00",
          "revision_reason": "initial",
          "operator_comment": "",
          "draft_type": "answer",
          "draft_text": "Здравствуйте.\nМы нашли ваш заказ: заказ 7056395 · Дьявол носит Prada 2 · 2026-05-09 18:40:00 · mooon в ТРК Minsk City Mall.\nЕсли нужно оформить возврат, подтвердите это в ответном письме; оператор продолжит обработку по найденному заказу.\nС уважением, команда mooon."
        }
      ],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "found",
        "decision_layer_status": "ok",
        "knowledge_item_ids": [
          "kb_giftcards_no_cash_refund",
          "kb_tickets_lost_without_receipt",
          "kb_reviews_request_details_for_nonstandard_case"
        ]
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26823",
      "status": "mock_sent",
      "error": "",
      "created_at": "2026-05-14T12:51:06.460023+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\message_raw_email_26823.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\message_raw_email_26823.md",
      "case_id": "case-000007",
      "thread_id": "thread-000007",
      "telegram_message_id": 9003,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "telegram_bot_api",
      "telegram_operations": [
        {
          "operation": "sendMessage",
          "ok": true,
          "chat_id": "mock-operator-chat",
          "message_id": 9003,
          "text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: raw_email_26823\nПолучено: 06.05.2026 20:45\nОт: kozlova22anna@gmail.com\nТема письма: без темы\nСуть обращения: Гость спрашивает, как вернуть деньги за билет.\n\n<b>Кейс</b>\nCase ID: case-000007 · Thread ID: thread-000007\n\n<b>История переписки</b>\nотсутствует\n\n<b>Вложения</b>\nФайлов: 1\n- ticket.pdf · PDF · электронный билет / билетный документ\n\n<b>Проверка билетов</b>\nБилет найден: заказ 7056395 · Дьявол носит Prada 2 · 2026-05-09 18:40:00 · mooon в ТРК Minsk City Mall\n\n<b>Что понял ассистент</b>\nТип обращения: клиентский вопрос\nЧто хочет отправитель: Гость спрашивает, как вернуть деньги за билет.\nСледующий шаг: отправить гостю инструкцию по возврату по найденному заказу.\n\n<b>Что предлагает система</b>\nЧто сделать: отправить гостю инструкцию по возврату по найденному заказу.\nПочему: Билет/заказ найден в проверке билетов; уточнять email, телефон или номер заказа не нужно.\n\n<b>База знаний</b>\nнет\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\nнет\n\n<b>Черновик v1</b>\nЗдравствуйте.\nМы нашли ваш заказ: заказ 7056395 · Дьявол носит Prada 2 · 2026-05-09 18:40:00 · mooon в ТРК Minsk City Mall.\nЕсли нужно оформить возврат, подтвердите это в ответном письме; оператор продолжит обработку по найденному заказу.\nС уважением, команда mooon.",
          "reply_markup": {
            "inline_keyboard": [
              [
                {
                  "text": "✅ Утвердить",
                  "callback_data": "ma|approve|811dd8355a9b1ddd"
                },
                {
                  "text": "✏️ На доработку (LLM)",
                  "callback_data": "ma|needs_edit|811dd8355a9b1ddd"
                }
              ],
              [
                {
                  "text": "👤 Оператору",
                  "callback_data": "ma|handoff|811dd8355a9b1ddd"
                },
                {
                  "text": "🚫 Игнорировать",
                  "callback_data": "ma|ignore|811dd8355a9b1ddd"
                }
              ]
            ]
          },
          "reply_to_message_id": null
        },
        {
          "operation": "sendDocument",
          "ok": true,
          "chat_id": "mock-operator-chat",
          "message_id": 9004,
          "file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\modules\\mail_import\\mock-flow-raw_email_26823-20260514T125104242200\\attachment_extraction_raw_email_26823__ticket.pdf",
          "caption": "Вложение к raw_email_26823: электронный билет / билетный документ"
        }
      ],
      "callback_data": [
        "ma|approve|811dd8355a9b1ddd",
        "ma|needs_edit|811dd8355a9b1ddd",
        "ma|handoff|811dd8355a9b1ddd",
        "ma|ignore|811dd8355a9b1ddd"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|811dd8355a9b1ddd"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|811dd8355a9b1ddd"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|811dd8355a9b1ddd"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|811dd8355a9b1ddd"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: raw_email_26823\nПолучено: 06.05.2026 20:45\nОт: kozlova22anna@gmail.com\nТема письма: без темы\nСуть обращения: Гость спрашивает, как вернуть деньги за билет.\n\n<b>Кейс</b>\nCase ID: case-000007 · Thread ID: thread-000007\n\n<b>История переписки</b>\nотсутствует\n\n<b>Вложения</b>\nФайлов: 1\n- ticket.pdf · PDF · электронный билет / билетный документ\n\n<b>Проверка билетов</b>\nБилет найден: заказ 7056395 · Дьявол носит Prada 2 · 2026-05-09 18:40:00 · mooon в ТРК Minsk City Mall\n\n<b>Что понял ассистент</b>\nТип обращения: клиентский вопрос\nЧто хочет отправитель: Гость спрашивает, как вернуть деньги за билет.\nСледующий шаг: отправить гостю инструкцию по возврату по найденному заказу.\n\n<b>Что предлагает система</b>\nЧто сделать: отправить гостю инструкцию по возврату по найденному заказу.\nПочему: Билет/заказ найден в проверке билетов; уточнять email, телефон или номер заказа не нужно.\n\n<b>База знаний</b>\nнет\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\nнет\n\n<b>Черновик v1</b>\nЗдравствуйте.\nМы нашли ваш заказ: заказ 7056395 · Дьявол носит Prada 2 · 2026-05-09 18:40:00 · mooon в ТРК Minsk City Mall.\nЕсли нужно оформить возврат, подтвердите это в ответном письме; оператор продолжит обработку по найденному заказу.\nС уважением, команда mooon.",
      "action": "",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T125059481993\\telegram_operator_delivery\\case-000007\\card_20260514T125106460127.json"
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
