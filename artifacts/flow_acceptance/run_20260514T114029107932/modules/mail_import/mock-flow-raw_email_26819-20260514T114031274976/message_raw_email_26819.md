# Message dossier raw_email_26819

- UID: raw_email_26819
- Message-ID: <CADcvMHdYg4ofatkfRVMH=OxJPawT6dH=e6hFJr0eQqUgHPH0UA@mail.gmail.com>
- Direction: inbound
- From: akademkurs.uni@gmail.com
- Subject: Создание и ведение архива организации. Научно-техническая обработка документов. Приглашение на обучение
- Sent at: 2026-05-06 15:33:50+03:00
- Preferred body source: text/plain
- Raw email: D:\JetBrains\cl_mail_assistant_mooon\artifacts\flow_acceptance\run_20260514T114029107932\modules\mail_import\mock-flow-raw_email_26819-20260514T114031274976\raw_email_raw_email_26819.eml

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

- Count: 2
- Text found in: 1

- attachment_extraction_raw_email_26819__Регистрационная форма_шаблон.docx
  - content_type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
  - text_found: yes
  - preview: РЕГИСТРАЦИОННАЯ ФОРМА УЧАСТНИКА Организация Название курса Создание и ведение архива организации. Научно-техническая обработка документов ФИО участника на русском языке на белорусском языке Должность участника E-mail уча
- attachment_extraction_raw_email_26819__ИНФ_ПИСЬМО_Архив.pdf
  - content_type: application/pdf
  - text_found: no

## LLM Understanding

- Status: ok
- Response mode: handoff_to_operator
- Confidence: 0.62
- Topic: Приглашение на обучение
- Customer need: Передать приглашение на обучение ответственным на ручную обработку.
- Summary: Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное письмо и регистрационная форма.
- Understanding note: Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.
- Response mode reason: training invitation / administrative proposal
- Suggested next step: Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.
- Backend/model: deterministic_fallback/local-rule-fallback
- Prompt/context version: fallback/fallback
- Duration ms: 0
- Error: forced fallback for flow acceptance smoke

Entities:
- sender: akademkurs.uni@gmail.com

## Body

```
Здравствуйте!
Государственное учреждение образования
«Университет Национальной академии наук Беларуси»
приглашает пройти обучение по теме
*«Создание и ведение архива организации. Научно-техническая обработка
документов»*.

⏰ Дата: *5** июня 2026 г.*

📚 Объем: *6 академических часов*

📍 Формат: *ОНЛАЙН* или* ОЧНО* (по выбору участника).

👉 Регистрация *ЗДЕСЬ
<https://docs.google.com/forms/d/e/1FAIpQLSf49WzYJ6PJ-iy2ue9BCOGXvt51qw6YsocXLcmGMVCEezDJcQ/viewform?usp=sharing&ouid=106457711131715822435>*
 или по форме в приложении.
Подробная информация – в письме во вложении

-- 
*С уважением,*

*Центр дополнительного образования *

*Университета НАН Беларуси*
*+375 29 363 86 92 *

*Сайт: www.academkurs.by <http://www.academkurs.by/>*
*E-mail: **akademkurs.uni@gmail.com <akademkurs.bel@gmail.com> *
*E-mail: akademkurs.bel@gmail.com <akademkurs.bel@gmail.com> *
```

<!-- MESSAGE_DOSSIER_PAYLOAD_START -->
{
  "message_id": "<CADcvMHdYg4ofatkfRVMH=OxJPawT6dH=e6hFJr0eQqUgHPH0UA@mail.gmail.com>",
  "direction": "inbound",
  "headers": {
    "message_id": "<CADcvMHdYg4ofatkfRVMH=OxJPawT6dH=e6hFJr0eQqUgHPH0UA@mail.gmail.com>",
    "in_reply_to": "",
    "references": [],
    "subject": "Создание и ведение архива организации. Научно-техническая обработка документов. Приглашение на обучение",
    "sender": "akademkurs.uni@gmail.com",
    "sent_at": "2026-05-06 15:33:50+03:00",
    "to": [],
    "cc": []
  },
  "body_text": "Здравствуйте!\r\nГосударственное учреждение образования\r\n«Университет Национальной академии наук Беларуси»\r\nприглашает пройти обучение по теме\r\n*«Создание и ведение архива организации. Научно-техническая обработка\r\nдокументов»*.\r\n\r\n⏰ Дата: *5** июня 2026 г.*\r\n\r\n📚 Объем: *6 академических часов*\r\n\r\n📍 Формат: *ОНЛАЙН* или* ОЧНО* (по выбору участника).\r\n\r\n👉 Регистрация *ЗДЕСЬ\r\n<https://docs.google.com/forms/d/e/1FAIpQLSf49WzYJ6PJ-iy2ue9BCOGXvt51qw6YsocXLcmGMVCEezDJcQ/viewform?usp=sharing&ouid=106457711131715822435>*\r\n или по форме в приложении.\r\nПодробная информация – в письме во вложении\r\n\r\n-- \r\n*С уважением,*\r\n\r\n*Центр дополнительного образования *\r\n\r\n*Университета НАН Беларуси*\r\n*+375 29 363 86 92 *\r\n\r\n*Сайт: www.academkurs.by <http://www.academkurs.by/>*\r\n*E-mail: **akademkurs.uni@gmail.com <akademkurs.bel@gmail.com> *\r\n*E-mail: akademkurs.bel@gmail.com <akademkurs.bel@gmail.com> *",
  "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\raw_email_raw_email_26819.eml",
  "raw_headers": "Received: from postback18d.mail.yandex.net (postback18d.mail.yandex.net [2a02:6b8:c41:1300:1:45:d181:da18])\r\n\tby mail-notsolitesrv-production-main-76.klg.yp-c.yandex.net (notsolitesrv) with LMTPS id wQtRGssUtWZq-5cRrEQoM\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 15:34:12 +0300\nReceived: from mail-nwsmtp-mxfront-production-main-697.klg.yp-c.yandex.net (mail-nwsmtp-mxfront-production-main-697.klg.yp-c.yandex.net [IPv6:2a02:6b8:c42:e1ad:0:640:5656:0])\r\n\tby postback18d.mail.yandex.net (Yandex) with ESMTPS id 58463C0159\r\n\tfor <info@mooon.by>; Wed, 06 May 2026 15:34:12 +0300 (MSK)\nReceived: from mail-wr1-x42b.google.com (mail-wr1-x42b.google.com [2a00:1450:4864:20::42b])\r\n\tby mail-nwsmtp-mxfront-production-main-697.klg.yp-c.yandex.net (mxfront) with ESMTPS id BYgRtw7LJiE0-AcTSpxqu;\r\n\tWed, 06 May 2026 15:34:11 +0300\nX-Yandex-Fwd: 1\nAuthentication-Results: mail-nwsmtp-mxfront-production-main-697.klg.yp-c.yandex.net; spf=pass (mail-nwsmtp-mxfront-production-main-697.klg.yp-c.yandex.net: domain of gmail.com designates 2a00:1450:4864:20::42b as permitted sender, rule=[ip6:2a00:1450:4864::/56]) smtp.mail=akademkurs.uni@gmail.com; dkim=pass header.i=@gmail.com\nX-Yandex-Spam: 1\nReceived: by mail-wr1-x42b.google.com with SMTP id ffacd0b85a97d-44e1860558fso2289099f8f.0\r\n        for <info@mooon.by>; Wed, 06 May 2026 05:34:11 -0700 (PDT)\nARC-Seal: i=1; a=rsa-sha256; t=1778070850; cv=none;\r\n        d=google.com; s=arc-20240605;\r\n        b=jUzAVDv6K6in8LD5llNO+MfNgTa4mE2GkU71YD/ejiqFOiKNLla1++NKim+wsCs1bx\r\n         rIoEc1AL/wTfeJOe7FDjgBR3CMki/gLD1yOfdXSa/sLTbb/L4SXYvTxQUkYTicigobVp\r\n         7B3jLQlWgqxvU68mqzqGLjAUKIVapFP+ennsBnaOF9+0kTb5nk6BKrtoZemrYj/egk7e\r\n         FUYxbRaNoBWyaDnktFPLmCcaBwm4xB5fqQ9ZFPNSrlafC26dWn69kJ1VI3Uc1OsnmiWJ\r\n         GiI1YOk2UQxbfx65jhJCuqUphSJegjLpzmWW/rOmeeVJAJLRjAqiHq2XkhAVwKNkV1Fv\r\n         3pqQ==\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;\r\n        h=to:subject:message-id:date:from:mime-version:dkim-signature;\r\n        bh=KTlVQt/0+hbZtk60HepctbEl1G/5Asfb62Pc8MoYMMc=;\r\n        fh=ZF15EAaGCR2FP6pwjBDG9acIW8RK1R8/h2VL0qA7IYw=;\r\n        b=R8wOn2lyNDirlKAvEWWiCGokz1OIIN9goitpvuzTXkcaQmIQ8L0TfENAYzu6MSEOwB\r\n         1SHSxUnBEwpYEiok/Qzp9v8rulkLRkSR3L5x0OUDALV7yZl1M0/GI11aNVWfHc2Wzviv\r\n         eBHXbMCtExOq2YXyorNtvymvC+2X/blY3fhG8h3AnUmm0IJU30M1VyXEq3gCa+lyBrES\r\n         RDZ17BTbDeeg/YVJali1g6FZ7hBKH2QJ6ac/xjaWNJiMwKwET+D+9fuFHq2yhiBDb6d+\r\n         d3SNkM17t8Sca6UmXnwDKD5EN50Lan2fcmISU7W4xyx4XzuHA4MgixyGpzhYoVKNSKWW\r\n         Nk+Q==;\r\n        darn=mooon.by\nARC-Authentication-Results: i=1; mx.google.com; arc=none\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=gmail.com; s=20251104; t=1778070850; x=1778675650; darn=mooon.by;\r\n        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject\r\n         :date:message-id:reply-to;\r\n        bh=KTlVQt/0+hbZtk60HepctbEl1G/5Asfb62Pc8MoYMMc=;\r\n        b=AISoK5I3T+4G8jHeLbOeLibK8Sp7q8N9CnR4Wrk/f9lrN5f9G7Cz+ZBs/+xCB8a48g\r\n         YE34L6kYq5UY+e+rm51f1J2dyiUTF1VahKQjAlTqBl5xNFV799O5iZ/jCNT6YZ+He2UU\r\n         3mCnyYGc+3LpKBrnnUk6hi0u4pWv3J9FEHW1gTmUBqYebvfwHJLoV7u4UU/v3of6a4lG\r\n         NMygawXBzbuqASOgKF07+xsjUNL4rY7c0QdAqWJoxASG7ul0egPze1AvBSIMF3p6CREt\r\n         5BeGg5FWrkdFIuEt6N7muyjFIMtjUEbyZdwY4qPkl0hR5JrkeowWeGAGqIDW43MLql0A\r\n         3OYQ==\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20251104; t=1778070850; x=1778675650;\r\n        h=to:subject:message-id:date:from:mime-version:x-gm-gg\r\n         :x-gm-message-state:from:to:cc:subject:date:message-id:reply-to;\r\n        bh=KTlVQt/0+hbZtk60HepctbEl1G/5Asfb62Pc8MoYMMc=;\r\n        b=NwCpOtz4JgJEP7FJDUHiFtlWQhY6DOWY+J/IUudyPsmnuX24G94e8TJPzkfD7ChV39\r\n         w2iCOIEYoRjJ6xKpvTKiO9hcl9uolRPZTK+K+NaKMiMDipc1SkNrhyskA1qWZ35Ht15K\r\n         JLqpCgVF/JgyzRq5R60ztiif+d2y7BcGafR56pH45yuFrfyu4a4XQvbRFQjbrR74JGX8\r\n         6+5XtHKlYrAbPdHCFZF3Xwb1Z3bTyqubVHp03x6ErL1T385zldfWOx67KH8fcYZwCtrM\r\n         2OfYw4vXa5HouHsg+ZHVEAQh5NYCUrP6cjzZl6BdC6A6HDRsyN6+jC9+4qZGsZdMvReX\r\n         ZMRg==\nX-Forwarded-Encrypted: i=1; AFNElJ8GNUGPnaN7784yjAG/5b6frxI+f2H6LnN3k/kkm5I//CEv6Iw8jqx+tXs0A3iPmkWdCI4u@mooon.by\nX-Gm-Message-State: AOJu0Yzkc87k5WO31OLNPhjHWLXd/OjOCO5oFkUQea59+UqTxe778I8V\r\n\tPvZ5/qS221blDgOX+Hlk9nbz0G58Xr3mWrQoobi+Bjt65krnq4HUAp7T49w4mWwhmpLkYLiVQxA\r\n\tTlse5lDD6r66oPObEHfR2KHX7T8wqrRM=\nX-Gm-Gg: AeBDiesxNc77On4lzCeRvy5e7tpqu4jX+EDZHRhIAsd4/qUiHPBkNVa8qPcb86doi3M\r\n\t00bKgy/s0it5poyGhq6TD7/3/gjP3kUaEYxOVuUfun2H4tuiMwZobd3jjz76PJNu6CzX+jlppQe\r\n\t9ntZpiGq6CHwZ62UVRNfGqqIwhbOFnwHazLVxhNcOAP3AGudxR89NPIlBeWeRHVW8mFUZOFXd1k\r\n\t/tqW1KRajqKvTx95MUfQSv2M+ti2TZOsHAY7/EgA5650OpB0ucjOWNN0CwRy3bxrqHXb67RpOkv\r\n\tsCJUUqEVLFbz6f3Jv3K/v4yZN+YfGRuyvehO\nX-Received: by 2002:a05:6000:1a8b:b0:449:d189:e79f with SMTP id\r\n ffacd0b85a97d-4515d5c56b4mr5610911f8f.32.1778070848437; Wed, 06 May 2026\r\n 05:34:08 -0700 (PDT)\nMIME-Version: 1.0\nFrom: =?UTF-8?B?0KPQvdC40LLQtdGA0YHQuNGC0LXRgiDQndCQ0J0g0JHQtdC70LDRgNGD0YHQuA==?= <akademkurs.uni@gmail.com>\nDate: Wed, 6 May 2026 15:33:50 +0300\nX-Gm-Features: AVHnY4JVXplJj7B-HTNvXUhedm7E6WT8NlqgdoTUnMLLc2oXIf3hgqJckl2ZfwA\nMessage-ID: <CADcvMHdYg4ofatkfRVMH=OxJPawT6dH=e6hFJr0eQqUgHPH0UA@mail.gmail.com>\nSubject: =?UTF-8?B?0KHQvtC30LTQsNC90LjQtSDQuCDQstC10LTQtdC90LjQtSDQsNGA0YXQuNCy0LAg0L7RgA==?=\r\n\t=?UTF-8?B?0LPQsNC90LjQt9Cw0YbQuNC4LiDQndCw0YPRh9C90L4t0YLQtdGF0L3QuNGH0LXRgdC60LDRjyDQvtCx?=\r\n\t=?UTF-8?B?0YDQsNCx0L7RgtC60LAg0LTQvtC60YPQvNC10L3RgtC+0LIuINCf0YDQuNCz0LvQsNGI0LXQvdC40LUg?=\r\n\t=?UTF-8?B?0L3QsCDQvtCx0YPRh9C10L3QuNC1?=\nTo: undisclosed-recipients:;\nContent-Type: multipart/mixed; boundary=\"000000000000503930065125612b\"\nReturn-Path: akademkurs.uni@gmail.com\nX-Yandex-Forward: 0857c52d081fdf2e3183d7ccdf48b137\n",
  "metadata": {
    "uid": "",
    "fixture_ref": "raw_email_26819",
    "mailbox": "mock_mailbox",
    "source_mode": "fixture"
  },
  "body_text_preview": "Здравствуйте!\r\nГосударственное учреждение образования\r\n«Университет Национальной академии наук Беларуси»\r\nприглашает пройти обучение по теме\r\n*«Создание и ведение архива организации. Научно-техническая обработка\r\nдокументов»*.\r\n\r\n⏰ Дата: *5** июня 2026 г.*\r\n\r\n📚 Объем: *6 академических часов*\r\n\r\n📍 Формат: *ОНЛАЙН* или* ОЧНО* (по выбору участника).\r\n\r\n👉 Регистрация *ЗДЕСЬ\r\n<https://docs.google.com/forms/d/e/1FAIpQLSf49WzYJ6PJ-iy2ue9BCOGXvt51qw6YsocXLcmGMVCEezDJcQ/viewform?usp=sharing&ouid=106457711131715822435>*\r\n или по форме в приложении.\r\nПодробная информация – в письме во вложении\r\n\r\n-- \r\n*С уважением,*\r\n\r\n*Центр дополнительного образования *\r\n\r\n*Университета НАН Беларуси*\r\n*+375 29 363 86 92 *\r\n\r\n*Сайт: www.academkurs.by <http://www.academkurs.by/>*\r\n*E-mail: **akademkurs.uni@gmail.com <akademkurs.bel@gmail.com> *\r\n*E-mail: akademkurs.bel@gmail.com <akademkurs.bel@gmail.com> *",
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
      "size_bytes": 1310,
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
      "size_bytes": 5751,
      "is_inline": false,
      "is_attachment": false
    },
    {
      "part_index": 4,
      "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "content_disposition": "attachment",
      "filename": "Регистрационная форма_шаблон.docx",
      "content_id": "f_mou178gt1",
      "charset": "",
      "is_multipart": false,
      "size_bytes": 18068,
      "is_inline": false,
      "is_attachment": true
    },
    {
      "part_index": 5,
      "content_type": "application/pdf",
      "content_disposition": "attachment",
      "filename": "ИНФ_ПИСЬМО_Архив.pdf",
      "content_id": "f_mou1752l0",
      "charset": "",
      "is_multipart": false,
      "size_bytes": 2329295,
      "is_inline": false,
      "is_attachment": true
    }
  ],
  "has_attachments": true,
  "has_inline_parts": false,
  "attachments_inventory": [
    {
      "part_index": 4,
      "filename": "Регистрационная форма_шаблон.docx",
      "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "content_disposition": "attachment",
      "content_id": "f_mou178gt1",
      "is_inline": false,
      "is_attachment": true,
      "size_bytes": 18068
    },
    {
      "part_index": 5,
      "filename": "ИНФ_ПИСЬМО_Архив.pdf",
      "content_type": "application/pdf",
      "content_disposition": "attachment",
      "content_id": "f_mou1752l0",
      "is_inline": false,
      "is_attachment": true,
      "size_bytes": 2329295
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
      "uid": "raw_email_26819",
      "message_id": "<CADcvMHdYg4ofatkfRVMH=OxJPawT6dH=e6hFJr0eQqUgHPH0UA@mail.gmail.com>",
      "subject": "Создание и ведение архива организации. Научно-техническая обработка документов. Приглашение на обучение",
      "raw_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\raw_email_raw_email_26819.eml",
      "message_file_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md",
      "items": [
        {
          "part_index": 4,
          "filename_original": "Регистрационная форма_шаблон.docx",
          "filename_saved": "attachment_extraction_raw_email_26819__Регистрационная форма_шаблон.docx",
          "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
          "content_disposition": "attachment",
          "is_inline": false,
          "is_attachment": true,
          "saved_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\attachment_extraction_raw_email_26819__Регистрационная форма_шаблон.docx",
          "text_found": true,
          "text_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\attachment_extraction_raw_email_26819__Регистрационная форма_шаблон.txt",
          "text_preview": "РЕГИСТРАЦИОННАЯ ФОРМА УЧАСТНИКА Организация Название курса Создание и ведение архива организации. Научно-техническая обработка документов ФИО участника на русском языке на белорусском языке Должность участника E-mail уча",
          "extraction_method": "docx_text",
          "error": "",
          "skip_reason": ""
        },
        {
          "part_index": 5,
          "filename_original": "ИНФ_ПИСЬМО_Архив.pdf",
          "filename_saved": "attachment_extraction_raw_email_26819__ИНФ_ПИСЬМО_Архив.pdf",
          "content_type": "application/pdf",
          "content_disposition": "attachment",
          "is_inline": false,
          "is_attachment": true,
          "saved_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\attachment_extraction_raw_email_26819__ИНФ_ПИСЬМО_Архив.pdf",
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
      "uid": "raw_email_26819",
      "status": "ok",
      "classification": "training_invitation",
      "operator_summary": "Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное письмо и регистрационная форма.",
      "case_summary_short": "Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное письмо и регистрационная форма.",
      "should_run_ticket_enrichment": false,
      "should_run_customer_kb": false,
      "should_build_customer_draft": false,
      "response_mode_hint": "handoff_to_operator",
      "proposed_action_type": "notify_department_stub",
      "proposed_action_text": "Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.",
      "action_stub_allowed": true,
      "classification_reason": "training invitation / administrative proposal",
      "sender_email": "akademkurs.uni@gmail.com",
      "own_sender_or_recipient": false,
      "recipient_emails": [
        "info@mooon.by",
        "no-reply@mooon.by",
        "noreply@mooon.by",
        "support@mooon.by"
      ],
      "attachment_count": 2
    },
    "identity_context_enrichment": {
      "result": {
        "uid": "raw_email_26819",
        "message_id": "<CADcvMHdYg4ofatkfRVMH=OxJPawT6dH=e6hFJr0eQqUgHPH0UA@mail.gmail.com>",
        "subject": "Создание и ведение архива организации. Научно-техническая обработка документов. Приглашение на обучение",
        "lookup_emails": [
          "akademkurs.uni@gmail.com",
          "akademkurs.bel@gmail.com"
        ],
        "selected_lookup_email": "",
        "ticket_db_status": "skipped",
        "crm_users_status": "stub",
        "payment_refund_status": "stub",
        "confidence": "none",
        "candidates_count": 0,
        "resolved_match": null,
        "note": "ticket enrichment skipped: training invitation / administrative proposal"
      },
      "debug": {
        "uid": "raw_email_26819",
        "message_id": "<CADcvMHdYg4ofatkfRVMH=OxJPawT6dH=e6hFJr0eQqUgHPH0UA@mail.gmail.com>",
        "subject": "Создание и ведение архива организации. Научно-техническая обработка документов. Приглашение на обучение",
        "paths": {
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md",
          "attachment_report_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md"
        },
        "lookup_keys": {
          "sender_email_reference": "akademkurs.uni@gmail.com",
          "body_emails": [
            "akademkurs.uni@gmail.com",
            "akademkurs.bel@gmail.com"
          ],
          "excluded_emails": [
            "info@mooon.by",
            "no-reply@mooon.by",
            "noreply@mooon.by",
            "support@mooon.by"
          ],
          "lookup_emails": [
            "akademkurs.uni@gmail.com",
            "akademkurs.bel@gmail.com"
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
              "training invitation / administrative proposal"
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
          "body_emails_found": 2,
          "lookup_emails_total": 2,
          "confidence": "none",
          "skip_reason": "training invitation / administrative proposal"
        }
      }
    },
    "case_thread_binding": {
      "uid": "raw_email_26819",
      "message_id": "<CADcvMHdYg4ofatkfRVMH=OxJPawT6dH=e6hFJr0eQqUgHPH0UA@mail.gmail.com>",
      "direction": "inbound",
      "sender": "akademkurs.uni@gmail.com",
      "subject": "Создание и ведение архива организации. Научно-техническая обработка документов. Приглашение на обучение",
      "case_id": "case-000005",
      "thread_id": "thread-000005",
      "binding_rule": "new_case_thread",
      "matched_message_id": "",
      "status": "new_case_thread",
      "registry_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\state\\case_thread_registry.xlsx",
      "registry_row_number": 6,
      "created": true,
      "message_chain_headers": {
        "in_reply_to": "",
        "references": []
      },
      "thread_history": [
        {
          "message_id": "<CADcvMHdYg4ofatkfRVMH=OxJPawT6dH=e6hFJr0eQqUgHPH0UA@mail.gmail.com>",
          "direction": "inbound",
          "sender": "akademkurs.uni@gmail.com",
          "subject": "Создание и ведение архива организации. Научно-техническая обработка документов. Приглашение на обучение",
          "sent_at": "2026-05-06 15:33:50+03:00",
          "binding_rule": "new_case_thread",
          "status": "new_case_thread",
          "parsed_email_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md"
        }
      ]
    },
    "llm_understanding": {
      "uid": "raw_email_26819",
      "status": "ok",
      "backend": "deterministic_fallback",
      "model": "local-rule-fallback",
      "prompt_version": "fallback",
      "context_version": "fallback",
      "duration_ms": 0,
      "error": "forced fallback for flow acceptance smoke",
      "structured_output": {
        "summary": "Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное письмо и регистрационная форма.",
        "topic": "Приглашение на обучение",
        "customer_need": "Передать приглашение на обучение ответственным на ручную обработку.",
        "entities": [
          {
            "type": "sender",
            "value": "akademkurs.uni@gmail.com"
          }
        ],
        "confidence": 0.62,
        "response_mode": "handoff_to_operator",
        "understanding_note": "Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.",
        "response_mode_reason": "training invitation / administrative proposal",
        "suggested_next_step": "Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.",
        "risk_level": "medium",
        "needs_human": true
      }
    },
    "knowledge_retrieval": {
      "uid": "raw_email_26819",
      "status": "skipped",
      "error": "",
      "reason": "training invitation / administrative proposal",
      "classification": "training_invitation",
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
      "uid": "raw_email_26819",
      "status": "ok",
      "error": "",
      "response_mode_initial": "handoff_to_operator",
      "response_mode_final": "handoff_to_operator",
      "decision_reason": "Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.",
      "missing_data": [],
      "risks": [],
      "knowledge_item_ids": [],
      "routing_item_ids": [],
      "recommended_route": {},
      "operator_summary": "Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное письмо и регистрационная форма.",
      "case_summary_short": "Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное письмо и регистрационная форма.",
      "classification": "training_invitation",
      "should_build_customer_draft": false,
      "proposed_action_type": "notify_department_stub",
      "proposed_action_text": "Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.",
      "action_stub_allowed": true,
      "real_email_sent": false
    },
    "draft_builder": {
      "uid": "raw_email_26819",
      "status": "skipped",
      "error": "",
      "skip_reason": "Черновик не создавался: обращение помечено для ручной обработки ответственными.",
      "draft_type": "handoff_to_operator",
      "latest_revision": 0,
      "draft_text": "",
      "operator_note": "Черновик не создавался: обращение помечено для ручной обработки ответственными.",
      "source_response_mode": "handoff_to_operator",
      "created_at": "2026-05-14T11:40:33.433833+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md",
      "revisions": [],
      "inputs": {
        "llm_understanding_status": "ok",
        "knowledge_retrieval_status": "skipped",
        "decision_layer_status": "ok",
        "knowledge_item_ids": []
      }
    },
    "telegram_operator_delivery": {
      "uid": "raw_email_26819",
      "status": "action_handoff",
      "error": "",
      "created_at": "2026-05-14T11:40:35.498453+00:00",
      "dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md",
      "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md",
      "case_id": "case-000005",
      "thread_id": "thread-000005",
      "telegram_message_id": 5,
      "telegram_chat_id": "mock-operator-chat",
      "telegram_delivery_mode": "telegram_bot_api",
      "telegram_operations": [
        {
          "operation": "editMessageText",
          "ok": true,
          "chat_id": "mock-operator-chat",
          "message_id": 5,
          "text": "<b>📩 Новое письмо</b>\n\n👤 Кейс помечен для ручной обработки. Реальная маршрутизация пока не подключена.\n\n<b>Письмо</b>\nUID: raw_email_26819\nПолучено: 06.05.2026 15:34\nОт: akademkurs.uni@gmail.com\nТема письма: Создание и ведение архива организации. Научно-техническая обработка документов. Приглашение на обучение\nСуть обращения: Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное письмо и регистрационная форма.\n\n<b>Кейс</b>\nCase ID: case-000005 · Thread ID: thread-000005\n\n<b>История переписки</b>\n- входящее · 2026-05-06 15:33 · Создание и ведение архива организации. На… · Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное…\n\n<b>Вложения</b>\nФайлов: 2\n- Регистрационная форма_шаблон.docx · DOCX · регистрационная форма участника курса\n- ИНФ_ПИСЬМО_Архив.pdf · PDF · информационное письмо о курсе по архивному делу\n\n<b>Проверка билетов / Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: приглашение на обучение / административное предложение\nЧто хочет отправитель: Передать приглашение на обучение ответственным на ручную обработку.\nСледующий шаг: Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.\n\n<b>Предлагаемое решение</b>\nРежим: передать оператору\nПричина: Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.\n\n<b>Предлагаемое действие</b>\nПередать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.\nТип действия: уведомить отдел\n\n<b>База знаний</b>\nне применялась — письмо не требует клиентской базы знаний по билетам.\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\nнет\n\n<b>Черновик</b>\nЧерновик не создавался: обращение помечено для ручной обработки ответственными.\n\n<b>Последнее действие</b>\nручная обработка",
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
          "message_id": 5,
          "reply_markup": {
            "inline_keyboard": []
          }
        },
        {
          "operation": "answerCallbackQuery",
          "ok": true,
          "callback_query_id": "cb_handoff",
          "text": "Кейс помечен для ручной обработки."
        }
      ],
      "callback_data": [
        "ma|approve|6b95e342de88db13",
        "ma|needs_edit|6b95e342de88db13",
        "ma|handoff|6b95e342de88db13",
        "ma|ignore|6b95e342de88db13",
        "ma|action_request|6b95e342de88db13"
      ],
      "keyboard": [
        {
          "action": "approve",
          "label": "✅ Утвердить",
          "callback_data": "ma|approve|6b95e342de88db13"
        },
        {
          "action": "needs_edit",
          "label": "✏️ На доработку (LLM)",
          "callback_data": "ma|needs_edit|6b95e342de88db13"
        },
        {
          "action": "handoff",
          "label": "👤 Оператору",
          "callback_data": "ma|handoff|6b95e342de88db13"
        },
        {
          "action": "ignore",
          "label": "🚫 Игнорировать",
          "callback_data": "ma|ignore|6b95e342de88db13"
        },
        {
          "action": "action_request",
          "label": "⚡ Выполнить действие",
          "callback_data": "ma|action_request|6b95e342de88db13"
        }
      ],
      "card_text": "<b>📩 Новое письмо</b>\n\n👤 Кейс помечен для ручной обработки. Реальная маршрутизация пока не подключена.\n\n<b>Письмо</b>\nUID: raw_email_26819\nПолучено: 06.05.2026 15:34\nОт: akademkurs.uni@gmail.com\nТема письма: Создание и ведение архива организации. Научно-техническая обработка документов. Приглашение на обучение\nСуть обращения: Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное письмо и регистрационная форма.\n\n<b>Кейс</b>\nCase ID: case-000005 · Thread ID: thread-000005\n\n<b>История переписки</b>\n- входящее · 2026-05-06 15:33 · Создание и ведение архива организации. На… · Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное…\n\n<b>Вложения</b>\nФайлов: 2\n- Регистрационная форма_шаблон.docx · DOCX · регистрационная форма участника курса\n- ИНФ_ПИСЬМО_Архив.pdf · PDF · информационное письмо о курсе по архивному делу\n\n<b>Проверка билетов / Enrichment</b>\nПроверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос.\n\n<b>Что понял ассистент</b>\nТип обращения: приглашение на обучение / административное предложение\nЧто хочет отправитель: Передать приглашение на обучение ответственным на ручную обработку.\nСледующий шаг: Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.\n\n<b>Предлагаемое решение</b>\nРежим: передать оператору\nПричина: Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.\n\n<b>Предлагаемое действие</b>\nПередать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия.\nТип действия: уведомить отдел\n\n<b>База знаний</b>\nне применялась — письмо не требует клиентской базы знаний по билетам.\n\n<b>Что не хватает</b>\nнет\n\n<b>Риски</b>\nнет\n\n<b>Черновик</b>\nЧерновик не создавался: обращение помечено для ручной обработки ответственными.\n\n<b>Последнее действие</b>\nручная обработка",
      "action": "handoff",
      "artifacts_dir": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932",
      "card_artifact_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\telegram_operator_delivery\\case-000005\\card_20260514T114035498753.json"
    },
    "operator_actions": {
      "status": "ok",
      "latest_action": {
        "uid": "raw_email_26819",
        "case_id": "case-000005",
        "thread_id": "thread-000005",
        "action": "handoff",
        "operator_comment": "",
        "operator_telegram_id": "101",
        "operator_username": "demo_operator",
        "created_at": "20260514T114035494210",
        "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md#modules.draft_builder",
        "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md",
        "callback_data": "ma|handoff|6b95e342de88db13",
        "mock_reply_refs": [],
        "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\telegram_operator_delivery\\case-000005\\card_20260514T114035498753.json",
        "real_email_sent": false,
        "status": "manual_processing_marked",
        "real_routing": false
      },
      "actions": [
        {
          "uid": "raw_email_26819",
          "case_id": "case-000005",
          "thread_id": "thread-000005",
          "action": "handoff",
          "operator_comment": "",
          "operator_telegram_id": "101",
          "operator_username": "demo_operator",
          "created_at": "20260514T114035494210",
          "draft_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md#modules.draft_builder",
          "source_dossier_path": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\modules\\mail_import\\mock-flow-raw_email_26819-20260514T114031274976\\message_raw_email_26819.md",
          "callback_data": "ma|handoff|6b95e342de88db13",
          "mock_reply_refs": [],
          "updated_card_ref": "D:\\JetBrains\\cl_mail_assistant_mooon\\artifacts\\flow_acceptance\\run_20260514T114029107932\\telegram_operator_delivery\\case-000005\\card_20260514T114035498753.json",
          "real_email_sent": false,
          "status": "manual_processing_marked",
          "real_routing": false
        }
      ],
      "real_email_sent": false
    }
  }
}
<!-- MESSAGE_DOSSIER_PAYLOAD_END -->
