# Message dossier raw_email_26812

- UID: raw_email_26812
- Message-ID: <79C61931-7F3B-4721-92F2-437B995A737E@gmail.com>
- Direction: inbound
- From: olga.evs2010@gmail.com
- Subject: Ошибка оплаты
- Sent at: 2026-05-06 08:17:14+03:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T104151820822\modules\mail_import\mock-flow-raw_email_26812-20260514T104154177182\raw_email_raw_email_26812.eml

## Case / Thread

- Case ID: case-000005
- Thread ID: thread-000005
- Binding rule: new_case_thread
- Binding status: new_case_thread

## Enrichment

- Ticket DB status: <empty>
- Selected lookup email: olga.evs2010@gmail.com
- Resolved ticket: <empty>

## Attachments

- Count: 1
- Text found in: 0

- attachment_extraction_raw_email_26812__image0.png
  - content_type: image/png
  - text_found: no

## LLM Understanding

- Status: ok
- Response mode: ask_clarifying_question
- Confidence: 0.62
- Topic: Клиентский вопрос по билету/оплате
- Customer need: Получить помощь по билету или оплате.
- Summary: Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: customer ticket/payment/refund/certificate wording
- Suggested next step: Проверить карточку и выбрать действие кнопками.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: olga.evs2010@gmail.com

## Body

```
Добрый день, пытаюсь купить билеты и вчера вечером, и утром

И выбивает с ошибкой оплаты 

Что делать? Как купить билеты?

Благодарю!

С Уважением, Ольга
+375291807055
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<79C61931-7F3B-4721-92F2-437B995A737E@gmail.com>",
  "direction": "inbound",
  "headers": {
    "message_id": "<79C61931-7F3B-4721-92F2-437B995A737E@gmail.com>",
    "in_reply_to": "",
    "references": [],
    "subject": "Ошибка оплаты",
    "sender": "olga.evs2010@gmail.com",
    "sent_at": "2026-05-06 08:17:14+03:00",
    "to": [
      "info@mooon.by"
    ],
    "cc": []
  },
  "body_text": "Добрый день, пытаюсь купить билеты и вчера вечером, и утром\r\n\r\nИ выбивает с ошибкой оплаты \r\n\r\nЧто делать? Как купить билеты?\r\n\r\nБлагодарю!\r\n\r\nС Уважением, Ольга\r\n+375291807055",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\raw_email_raw_email_26812.eml",
  "raw_headers": "Received: from postback1a.mail.yandex.net (postback1a.mail.yandex.net [2a02:6b8:c0e:500:1:45:d181:da01])\r\n\tby mail-notsolitesrv-production-main-25.vla.yp-c.yandex.net (notsolitesrv) with LMTPS id KqxkfzltabX8-Z1Bu9pAf\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 08:17:28 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-80.iva.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-80.iva.yp-c.yandex.net [IPv6:2a02:6b8:c0c:d10c:0:640:b29a:0])\r\n\tby postback1a.mail.yandex.net (Yandex) with ESMTPS id 36CF1C02F5\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 08:17:28 +0300 (MSK)\nReceived: from mail-wm1-x32b.google.com (mail-wm1-x32b.google.com [2a00:1450:4864:20::32b])\r\n\tby mail-nwsmtp-mxfront-production-main-80.iva.yp-c.yandex.net (mxfront) with ESMTPS id RHZvDt3LE8c0-p1YeqryX;\r\n\tWed, 06 May 2026 08:17:27 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-80.iva.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-80.iva.yp-c.yandex.net: domain of gmail.com designates 2a00:1450:4864:20::32b as permitted sender, rule=[ip6:2a00:1450:4864::/56]) smtp.mail=olga.evs2010@gmail.com; dkim=pass header.i=@gmail.com\nX-Yandex-Spam: 1\nReceived: by mail-wm1-x32b.google.com with SMTP id 5b1f17b1804b1-48896199cbaso52156655e9.1\r\n        for <info@mooon.by>; Tue, 05 May 2026 22:17:27 -0700 (PDT)\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=gmail.com; s=20251104; t=1778044646; x=1778649446; darn=mooon.by;\r\n        h=to:message-id:subject:date:mime-version:from\r\n         :content-transfer-encoding:from:to:cc:subject:date:message-id\r\n         :reply-to;\r\n        bh=iVTWTtCmHydj+yvvKszurSbfvCaBIzybeFCYptPFKow=;\r\n        b=b117VL6wi2s33hUeFJw6CXkBo7y90TT47AZZRe61uXQLaVt7zvGxXEQW8uBQ2/O/r8\r\n         ojhrjrzO9kILZptwVztW2+IKXwMzTRvssNiHsBJA1M669/fpq6Jxnu13Ic3ExCwpwAq4\r\n         ZhOst+rVvA3UQ55dXj29AOmUASRGoRGKxDLBF7LcqSkN+NvRKC7tvKqa6+R4d0fWfkbN\r\n         15KPQdhCfcgUxLerROE7UpU0NE0DxnmnIWvUPUMWK2PjWHPbLUldPuukmX8LhYvYayb8\r\n         it+AhQyNySTl8XOu3mmD6RSIRU1wcV1SOTpFOMtABJAWT0ftvIu1jWsr4xxuXwfc5TFN\r\n         Kaow==\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20251104; t=1778044646; x=1778649446;\r\n        h=to:message-id:subject:date:mime-version:from\r\n         :content-transfer-encoding:x-gm-gg:x-gm-message-state:from:to:cc\r\n         :subject:date:message-id:reply-to;\r\n        bh=iVTWTtCmHydj+yvvKszurSbfvCaBIzybeFCYptPFKow=;\r\n        b=i2AMtV3gjc2aFCFAG0VFdvNYnAKytiaF0khKLQIF4y13fGw/CJX9nHXk0FCjXfphul\r\n         hUuDx0aw+WqX4JiRtKozGVmggPZOj2jMVi9QciwaH2v0C6AIDFPb1sR+jLOLk4Xyf2lk\r\n         Hcuu4q4pD1uT1eC6z/jM6JzugeREkZ/woyyVx/HtlegEqRw0IaShtA3VmANUGU1ncG/8\r\n         Ok03yEwYRJTpSIPH020QbHpLj/D5u84WssyEuncwzKUZTqVLw54F2iIy8DWbpI8H8srV\r\n         8RudW0HYxtUo/IMwfXfBnFET/iuvhK2wcIgduoRkQq5OcwtWsLG2BLko/RrtZWXB4FAv\r\n         LYKg==\nX-Gm-Message-State: AOJu0YyRfYA6X50T3WjDbqgyZvpV/Krlz0RHjugqyolhd1T1hhJnJR2H\r\n\t21LeyV8Y6FpWj61TU2AIKHsuICjK39Oc35x9LrofROv6XAH2XpLPqPTQto/aSA==\nX-Gm-Gg: AeBDievlxWKnOPqZfHeazSRmDKEBMbsmDASwNyCfPjiYER6MUIu12R5dl5L7Ui9av2f\r\n\tNKC8D6jxQZAgDAxtP6EEvudzdto8GpEph4bWmgKpzBUSqPYVOs1tZyoDT5ed5CLISOucbIxRe4A\r\n\t+fhuIt1Nc63efNMiMgMwftO0ORz3/fLiqQ5+Yeyz1Rs6IUMEmX8c1EFqtsWHi8Chr9GAY6gTtcM\r\n\tGtreJiRgCvoQLpvlUwoHseABfAFZVfuJftpLT9UYK64O9Tl2NFeuTXn9Uct3aJ5Bec1iNr+krz7\r\n\tG3DvPfuY1tOXtd3zW6m5/e3nkIoEL5qCfAmrjmMRpZJZNDMA6LKzJN4o/4FdS4UeyInpMrM37Kr\r\n\tlR9yBkubVUJoke3khRj/N60Qy9hqjWZwayIs9KBRx4ZfulAEh0EQpSzlx+VvfAiu5d0ZqjfYi3v\r\n\t36IYpvjdzezJMCFwK/I2AZnNvJzvhcEaVAt2l7Hs7DvTw2TTX8c1zaMAlE5Q==\nX-Received: by 2002:a05:600c:a10d:b0:48a:53ea:13df with SMTP id 5b1f17b1804b1-48e51f21f39mr20817285e9.2.1778044646350;\r\n        Tue, 05 May 2026 22:17:26 -0700 (PDT)\nReceived: from smtpclient.apple ([46.53.247.255])\r\n        by smtp.gmail.com with ESMTPSA id 5b1f17b1804b1-48e52f5d299sm11098215e9.0.2026.05.05.22.17.25\r\n        for <info@mooon.by>\r\n        (version=TLS1_3 cipher=TLS_AES_256_GCM_SHA384 bits=256/256);\r\n        Tue, 05 May 2026 22:17:25 -0700 (PDT)\nContent-Type: multipart/mixed; boundary=Apple-Mail-409C938B-8DCA-439F-9E81-B94A91803C2C\nContent-Transfer-Encoding: 7bit\nFrom: Olga Evseichik <olga.evs2010@gmail.com>\nMime-Version: 1.0 (1.0)\nDate: Wed, 6 May 2026 08:17:14 +0300\nSubject: =?utf-8?B?0J7RiNC40LHQutCwINC+0L/Qu9Cw0YLRiw==?=\nMessage-Id: <79C61931-7F3B-4721-92F2-437B995A737E@gmail.com>\nTo: info@mooon.by\nX-Mailer: iPhone Mail (23D8133)\nReturn-Path: olga.evs2010@gmail.com\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26812",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Добрый день, пытаюсь купить билеты и вчера вечером, и утром\r\n\r\nИ выбивает с ошибкой оплаты \r\n\r\nЧто делать? Как купить билеты?\r\n\r\nБлагодарю!\r\n\r\nС Уважением, Ольга\r\n+375291807055",
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
      "size_bytes": 299,
      "is_inline": false,
      "is_attachment": false
    },
    {
      "part_index": 2,
      "content_type": "image/png",
      "content_disposition": "inline",
      "filename": "image0.png",
      "content_id": "",
      "charset": "",
      "is_multipart": false,
      "size_bytes": 891229,
      "is_inline": true,
      "is_attachment": false
    },
    {
      "part_index": 3,
      "content_type": "text/plain",
      "content_disposition": "",
      "filename": "",
      "content_id": "",
      "charset": "utf-8",
      "is_multipart": false,
      "size_bytes": 32,
      "is_inline": false,
      "is_attachment": false
    }
  ],
  "has_attachments": false,
  "has_inline_parts": true,
  "attachments_inventory": [
    {
      "part_index": 2,
      "filename": "image0.png",
      "content_type": "image/png",
      "content_disposition": "inline",
      "content_id": "",
      "is_inline": true,
      "is_attachment": false,
      "size_bytes": 891229
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
      "uid": "raw_email_26812",
      "message_id": "<79C61931-7F3B-4721-92F2-437B995A737E@gmail.com>",
      "subject": "Ошибка оплаты",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\raw_email_raw_email_26812.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\message_raw_email_26812.md",
      "items": [
        {
          "part_index": 2,
          "filename_original": "image0.png",
          "filename_saved": "attachment_extraction_raw_email_26812__image0.png",
          "content_type": "image/png",
          "content_disposition": "inline",
          "is_inline": true,
          "is_attachment": false,
          "saved_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\attachment_extraction_raw_email_26812__image0.png",
          "text_found": false,
          "text_path": "",
          "text_preview": "",
          "extraction_method": "ocr_unavailable",
          "error": "",
          "skip_reason": ""
        }
      ]
    },
    "early_classification": {
      "uid": "raw_email_26812",
      "status": "ok",
      "classification": "customer_support",
      "operator_summary": "Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот.",
      "case_summary_short": "Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот.",
      "should_run_ticket_enrichment": true,
      "should_run_customer_kb": true,
      "should_build_customer_draft": true,
      "response_mode_hint": "ask_clarifying_question",
      "proposed_action_type": "",
      "proposed_action_text": "",
      "action_stub_allowed": false,
      "classification_reason": "customer ticket/payment/refund/certificate wording",
      "sender_email": "olga.evs2010@gmail.com",
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
        "uid": "raw_email_26812",
        "message_id": "<79C61931-7F3B-4721-92F2-437B995A737E@gmail.com>",
        "subject": "Ошибка оплаты",
        "lookup_emails": [
          "olga.evs2010@gmail.com"
        ],
        "selected_lookup_email": "olga.evs2010@gmail.com",
        "ticket_db_status": "unavailable",
        "crm_users_status": "stub",
        "payment_refund_status": "stub",
        "confidence": "none",
        "candidates_count": 0,
        "resolved_match": null,
        "note": "ticket_db unavailable: pymysql is not installed"
      },
      "debug": {
        "uid": "raw_email_26812",
        "message_id": "<79C61931-7F3B-4721-92F2-437B995A737E@gmail.com>",
        "subject": "Ошибка оплаты",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\message_raw_email_26812.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\message_raw_email_26812.md"
        },
        "lookup_keys": {
          "sender_email_reference": "olga.evs2010@gmail.com",
          "body_emails": [],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "olga.evs2010@gmail.com"
          ],
          "selected_lookup_email": "olga.evs2010@gmail.com",
          "selected_lookup_localpart": "olga.evs2010"
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
            "query_email": "olga.evs2010@gmail.com",
            "query_localpart": "olga.evs2010",
            "lookup_trace": [
              {
                "email": "olga.evs2010@gmail.com",
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
          "body_emails_found": 0,
          "lookup_emails_total": 1,
          "confidence": "none"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26812",
      "message_id": "<79C61931-7F3B-4721-92F2-437B995A737E@gmail.com>",
      "direction": "inbound",
      "sender": "olga.evs2010@gmail.com",
      "subject": "Ошибка оплаты",
      "case_id": "case-000005",
      "thread_id": "thread-000005",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\state\\case_thread_registry.xlsx",
      "registry_row_number": 6,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "",
        "references": []
      },
      "thread_history": [
        {
          "message_id": "<79C61931-7F3B-4721-92F2-437B995A737E@gmail.com>",
          "direction": "inbound",
          "sender": "olga.evs2010@gmail.com",
          "subject": "Ошибка оплаты",
          "sent_at": "2026-05-06 08:17:14+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\message_raw_email_26812.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26812",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот.",
        "topic": "Клиентский вопрос по билету/оплате",
        "customer_need": "Получить помощь по билету или оплате.",
        "entities": [
          {
            "type": "sender",
            "value": "olga.evs2010@gmail.com"
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
      "uid": "raw_email_26812",
      "status": "found",
      "error": "",
      "knowledge_base_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\config\\knowledge_base\\knowledge_base.xlsx",
      "query": {
        "text": "Ошибка оплаты Добрый день, пытаюсь купить билеты и вчера вечером, и утром\r\n\r\nИ выбивает с ошибкой оплаты \r\n\r\nЧто делать? Как купить билеты?\r\n\r\nБлагодарю!\r\n\r\nС Уважением, Ольга\r\n+375291807055 Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот. Клиентский вопрос по билету/оплате Получить помощь по билету или оплате. olga.evs2010@gmail.com",
        "response_mode": "ask_clarifying_question",
        "entities": [
          "olga.evs2010@gmail.com"
        ]
      },
      "matched_items": [
        {
          "id": "kb_payment_general_failed_payment",
          "category": "payment",
          "type": "operator_instruction",
          "title": "Если не проходит оплата или невозможно купить билет",
          "score": 11.9,
          "content": "При проблеме оплаты можно предложить повторить оплату, использовать другой браузер или устройство, проверить данные карты и при необходимости обратиться в банк/платёжную поддержку.",
          "operator_instruction": "Если гость описывает конкретную ошибку или прикладывает скриншот — использовать её. Если данных мало — запросить скриншот ошибки, банк/тип карты, способ оплаты, время попытки и e-mail заказа.",
          "template_hint": "Попробуйте, пожалуйста, повторить оплату в другом браузере или на другом устройстве. Если ошибка сохранится, пришлите скриншот.",
          "source": "Скрипты ответов на популярные вопросы, работа с info@mooon.by.xlsx",
          "source_ref": "'Скрипты ответов на звонки и пис'!B27:C27",
          "matched_keywords": [
            "ошибка оплаты",
            "купить билет"
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
      "uid": "raw_email_26812",
      "status": "ok",
      "error": "",
      "response_mode_initial": "ask_clarifying_question",
      "response_mode_final": "ask_clarifying_question",
      "decision_reason": "Письмо связано с билетом/оплатой, но подтвержденный заказ не найден в enrichment.",
      "missing_data": [
        "Время попытки оплаты и последние 4 цифры карты/банк, если это потребуется для проверки."
      ],
      "risks": [],
      "knowledge_item_ids": [
        "kb_payment_general_failed_payment",
        "kb_tickets_lost_without_receipt",
        "kb_refunds_no_exchange_only_refund_and_new_purchase"
      ],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот.",
      "case_summary_short": "Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот.",
      "classification": "customer_support",
      "should_build_customer_draft": true,
      "proposed_action_type": "",
      "proposed_action_text": "",
      "action_stub_allowed": false,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26812",
      "status": "ok",
      "error": "",
      "draft_type": "ask_clarifying_question",
      "latest_revision": 1,
      "draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить помощь по билету или оплате.), пожалуйста, уточните:\n- Время попытки оплаты и последние 4 цифры карты/банк, если это потребуется для проверки.\nПопробуйте, пожалуйста, повторить оплату в другом браузере или на другом устройстве. Если ошибка сохранится, пришлите скриншот.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon.",
      "operator_note": "Черновик создан в демо-режиме; реальная отправка отключена.",
      "source_response_mode": "ask_clarifying_question",
      "created_at": "2026-05-14T10:41:54.895101+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\message_raw_email_26812.md",
      "revisions": [
        {
          "revision": 1,
          "created_at": "2026-05-14T10:41:54.895101+00:00",
          "revision_reason": "initial",
          "operator_comment": "",
          "draft_type": "ask_clarifying_question",
          "draft_text": "Здравствуйте.\nЧтобы корректно обработать обращение (Получить помощь по билету или оплате.), пожалуйста, уточните:\n- Время попытки оплаты и последние 4 цифры карты/банк, если это потребуется для проверки.\nПопробуйте, пожалуйста, повторить оплату в другом браузере или на другом устройстве. Если ошибка сохранится, пришлите скриншот.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon."
        }
      ],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "found",
        "decision_layer_status": "ok",
        "knowledge_item_ids": [
          "kb_payment_general_failed_payment",
          "kb_tickets_lost_without_receipt",
          "kb_refunds_no_exchange_only_refund_and_new_purchase"
        ]
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26812",
      "status": "mock_sent",
      "error": "",
      "created_at": "2026-05-14T10:41:54.928177+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\message_raw_email_26812.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\modules\\mail_import\\mock-flow-raw_email_26812-20260514T104154177182\\message_raw_email_26812.md",
      "case_id": "case-000005",
      "thread_id": "thread-000005",
      "telegram_message_id": 5,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "artifact_only",
      "telegram_operations": [],
      "callback_data": [
        "ma|approve|9c3af27f628c3637",
        "ma|needs_edit|9c3af27f628c3637",
        "ma|handoff|9c3af27f628c3637",
        "ma|ignore|9c3af27f628c3637"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|9c3af27f628c3637"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|9c3af27f628c3637"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|9c3af27f628c3637"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|9c3af27f628c3637"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n<b>Письмо</b>\nUID: raw_email_26812\nПолучено: 06.05.2026 08:17\nОт: olga.evs2010@gmail.com\nТема письма: Ошибка оплаты\nСуть обращения: Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот.\n\n<b>Кейс</b>\nCase ID: case-000005 · Thread ID: thread-000005\n\n<b>История переписки</b>\n- входящее · 2026-05-06 08:17 · Ошибка оплаты · Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот.\n\n<b>Вложения</b>\nФайлов: 1\n- image0.png · изображение PNG · скриншот ошибки оплаты / отклонённого платежа\n\n<b>Enrichment</b>\nПроверка билетов: временно недоступна — ticket_db unavailable: pymysql is not installed.\n\n<b>Что понял ассистент</b>\nТип обращения: клиентский вопрос\nЧто хочет отправитель: Получить помощь по билету или оплате.\nЧто предлагает система: Письмо связано с билетом/оплатой, но подтвержденный заказ не найден в enrichment.\n\n<b>Что предлагает система</b>\nРежим: уточнить данные\nПричина: Письмо связано с билетом/оплатой, но подтвержденный заказ не найден в enrichment.\n\n<b>База знаний</b>\n- Если не проходит оплата или невозможно купить билет / kb_payment_general_failed_payment / балл 11.9\n\n<b>Что не хватает</b>\n- Время попытки оплаты и последние 4 цифры карты/банк, если это потребуется для проверки.\n\n<b>Риски</b>\nнет\n\n<b>Черновик v1</b>\nЗдравствуйте.\nЧтобы корректно обработать обращение (Получить помощь по билету или оплате.), пожалуйста, уточните:\n- Время попытки оплаты и последние 4 цифры карты/банк, если это потребуется для проверки.\nПопробуйте, пожалуйста, повторить оплату в другом браузере или на другом устройстве. Если ошибка сохранится, пришлите скриншот.\nПосле этого мы сможем продолжить проверку.\nС уважением, команда mooon.",
      "action": "",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T104151820822\\telegram_operator_delivery\\case-000005\\card_20260514T104154928297.json"
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
