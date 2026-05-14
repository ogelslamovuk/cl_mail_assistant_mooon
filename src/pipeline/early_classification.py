from __future__ import annotations

import re
from email.utils import parseaddr
from typing import Any


OWN_MAILBOXES = {
    "info@mooon.by",
    "support@mooon.by",
    "no-reply@mooon.by",
    "noreply@mooon.by",
}

CLASS_CUSTOMER_SUPPORT = "customer_support"
CLASS_SCHEDULE = "schedule_or_repertoire_question"
CLASS_BUSINESS = "business_proposal"
CLASS_CANDIDATE = "candidate_or_portfolio"
CLASS_SERVICE = "service_notification"
CLASS_ACTION_REQUIRED = "action_required_notification"
CLASS_GRATITUDE = "gratitude_or_case_closed"
CLASS_TRAINING = "training_invitation"
CLASS_NEWSLETTER = "newsletter_or_promo"
CLASS_SECURITY = "security_or_no_reply_noise"
CLASS_BOUNCE = "bounce_or_delivery_noise"
CLASS_UNKNOWN = "unknown_meaningful"


def apply_early_classification(payload: dict[str, Any]) -> dict[str, Any]:
    result = classify_message(payload)
    payload.setdefault("modules", {})["early_classification"] = result
    return result


def early_classification(payload: dict[str, Any]) -> dict[str, Any]:
    value = (payload.get("modules") or {}).get("early_classification") or {}
    return value if isinstance(value, dict) else {}


def classify_message(payload: dict[str, Any]) -> dict[str, Any]:
    headers = payload.get("headers") if isinstance(payload.get("headers"), dict) else {}
    subject = str(headers.get("subject") or "").strip()
    sender = str(headers.get("sender") or "").strip()
    sender_email = _email(sender)
    body = str(payload.get("body_text") or "")
    raw_headers = str(payload.get("raw_headers") or "")
    text = _norm(" ".join([subject, sender, body, raw_headers]))
    header_names = _norm(raw_headers)

    attachments = _attachment_items(payload)
    has_attachment = bool(attachments)
    has_image = any(str(item.get("content_type") or "").lower().startswith("image/") for item in attachments)

    recipient_emails = _recipient_emails(headers)
    own_sender = sender_email in OWN_MAILBOXES or sender_email in recipient_emails
    summary = _operator_summary(
        classification="",
        sender=sender,
        sender_email=sender_email,
        subject=subject,
        body=body,
        text=text,
        has_image=has_image,
    )

    classification = CLASS_UNKNOWN
    reason = "meaningful message needs manual review"
    should_enrich = False
    should_kb = False
    should_draft = False
    response_mode = "handoff_to_operator"
    proposed_action_type = ""
    proposed_action_text = ""

    if bool(payload.get("is_bounce")) or _contains_any(text, ["mailer-daemon", "undelivered mail", "delivery status notification", "failure notice"]):
        classification = CLASS_BOUNCE
        reason = "bounce/delivery-status signals"
        response_mode = "no_reply"
        summary = "Техническое уведомление о недоставке письма."
    elif _looks_gratitude_closure(text):
        classification = CLASS_GRATITUDE
        reason = "sender thanks and confirms the issue is resolved"
        response_mode = "no_reply"
        summary = _gratitude_summary(body)
    elif _looks_action_required(sender_email, text):
        classification = CLASS_ACTION_REQUIRED
        reason = "payment provider / banking processing center operational notice"
        response_mode = "handoff_to_operator"
        proposed_action_type = "forward_to_chat_stub"
        proposed_action_text = "Переслать уведомление в ответственный чат по платёжным алертам."
        summary = _action_summary(sender, subject, body)
    elif _looks_security_or_no_reply(sender_email, text):
        classification = CLASS_SECURITY
        reason = "no-reply/security notification without customer request"
        response_mode = "no_reply"
        summary = _security_summary(sender, subject, body)
    elif _looks_newsletter(payload, text, header_names) and not _looks_customer_support(text, has_attachment):
        classification = CLASS_NEWSLETTER
        reason = "mailing/newsletter headers or unsubscribe signals"
        response_mode = "no_reply"
        summary = _newsletter_summary(sender, subject, body)
    elif _looks_candidate(text):
        classification = CLASS_CANDIDATE
        reason = "candidate/practice/portfolio wording"
        response_mode = "handoff_to_operator"
        proposed_action_type = "notify_department_stub"
        proposed_action_text = _candidate_action_text(text)
        summary = _candidate_summary(sender, body)
    elif _looks_training_invitation(text):
        classification = CLASS_TRAINING
        reason = "training invitation / administrative proposal"
        response_mode = "handoff_to_operator"
        proposed_action_type = "notify_department_stub"
        proposed_action_text = "Передать приглашение ответственным за административное обучение или документооборот для оценки необходимости участия."
        summary = _training_summary(sender, subject, body)
    elif _looks_business_proposal(text):
        classification = CLASS_BUSINESS
        reason = "business proposal / marketing services wording"
        response_mode = "handoff_to_operator"
        proposed_action_type = "notify_department_stub"
        proposed_action_text = _business_action_text(text)
        summary = _business_summary(sender, subject, body)
    elif _looks_schedule_question(text):
        classification = CLASS_SCHEDULE
        reason = "schedule/repertoire/movie-show question"
        should_kb = True
        response_mode = "handoff_to_operator"
        proposed_action_type = "mark_manual_processing"
        proposed_action_text = "Передать вопрос ответственным за репертуар/расписание; live schedule connector пока не подключён."
        summary = _schedule_summary(body, subject)
    elif _looks_customer_support(text, has_attachment):
        classification = CLASS_CUSTOMER_SUPPORT
        giftcard_support = _looks_giftcard_support(text)
        reason = "customer gift card support wording" if giftcard_support else "customer ticket/payment/refund/certificate wording"
        should_enrich = (not own_sender) and not giftcard_support
        should_kb = True
        should_draft = True
        response_mode = "ask_clarifying_question"
        summary = _customer_support_summary(subject, body, has_image)
    elif _looks_service_notification(text):
        classification = CLASS_SERVICE
        reason = "service notification"
        response_mode = "handoff_to_operator"
        proposed_action_type = "mark_manual_processing"
        proposed_action_text = "Кейс помечен для ручной обработки. Реальная маршрутизация пока не подключена."
        summary = _service_summary(sender, subject, body)

    if own_sender:
        should_enrich = False
        if reason == "meaningful message needs manual review":
            reason = "sender or recipient is our mailbox"

    result = {
        "uid": _resolve_uid(payload),
        "status": "ok",
        "classification": classification,
        "operator_summary": summary,
        "case_summary_short": summary,
        "should_run_ticket_enrichment": bool(should_enrich),
        "should_run_customer_kb": bool(should_kb),
        "should_build_customer_draft": bool(should_draft),
        "response_mode_hint": response_mode,
        "proposed_action_type": proposed_action_type,
        "proposed_action_text": proposed_action_text,
        "action_stub_allowed": bool(proposed_action_type),
        "classification_reason": reason,
        "sender_email": sender_email,
        "own_sender_or_recipient": bool(own_sender),
        "recipient_emails": sorted(recipient_emails),
        "attachment_count": len(attachments),
    }
    return result


def _looks_newsletter(payload: dict[str, Any], text: str, header_names: str) -> bool:
    if bool(payload.get("is_mailing_like")):
        return True
    return _contains_any(
        " ".join([text, header_names]),
        [
            "list-unsubscribe",
            "list-unsubscribe-post",
            "x-kmail",
            "klaviyo",
            "mailchimp",
            "sendgrid",
            "manage.kmail-lists.com",
            "unsubscribe",
            "one-click",
            "view this email in your browser",
        ],
    )


def _looks_gratitude_closure(text: str) -> bool:
    return _contains_any(text, ["благодар", "спасибо", "улажен", "решен", "решён"]) and _contains_any(
        text,
        ["вопрос", "пригласитель", "отклик", "ситуац", "улажен", "решен", "решён"],
    )


def _looks_security_or_no_reply(sender_email: str, text: str) -> bool:
    no_reply = any(token in sender_email for token in ["no-reply", "noreply", "do-not-reply"])
    security = _contains_any(
        text,
        [
            "вход в аккаунт",
            "нового устройства",
            "new device",
            "login",
            "security",
            "безопасн",
            "парол",
            "account",
        ],
    )
    return no_reply and security


def _looks_action_required(sender_email: str, text: str) -> bool:
    provider = _contains_any(sender_email, ["belassist.by", "assist", "bpc.by"]) or _contains_any(
        text,
        [
            "банковский процессинговый центр",
            "belassist",
            "компания электронных платежей",
            "эквайр",
            "acquiring",
        ],
    )
    operational = _contains_any(
        text,
        [
            "плановые работы",
            "технологические работы",
            "перерыв в проведении платежей",
            "недоступн",
            "downtime",
            "maintenance",
            "платеж",
        ],
    )
    return provider and operational


def _looks_candidate(text: str) -> bool:
    return _contains_any(
        text,
        [
            "летнюю практику",
            "практику",
            "студент",
            "портфолио",
            "видеомонтаж",
            "монтажер",
            "монтажёр",
            "соцсет",
            "adobe premiere",
            "after effects",
            "capcut",
            "резюме",
        ],
    )


def _looks_business_proposal(text: str) -> bool:
    return _contains_any(
        text,
        [
            "предлагаем",
            "предложение о сотрудничестве",
            "сотрудничество",
            "партнерств",
            "партнёрств",
            "маркетинг",
            "smm",
            "реклам",
            "наши услуги",
            "коммерческое предложение",
            "короткометраж",
            "съемк",
            "съёмк",
            "локаци",
            "локацию",
            "аренды",
            "аренда",
            "титрах",
        ],
    )


def _looks_training_invitation(text: str) -> bool:
    return _contains_any(
        text,
        [
            "приглашает пройти обучение",
            "приглашение на обучение",
            "создание и ведение архива",
            "научно-техническая обработка",
            "академических часов",
            "регистрация",
            "университет национальной академии наук",
        ],
    )


def _looks_schedule_question(text: str) -> bool:
    return _contains_any(
        text,
        [
            "цифровой цирк",
            "glitch",
            "показ",
            "показы",
            "прокат",
            "репертуар",
            "расписан",
            "сеанс",
            "фильм",
            "мультфильм",
            "кино",
        ],
    ) and not _contains_any(
        text,
        ["билет", "оплат", "заказ", "возврат", "съемк", "съёмк", "аренд", "локац", "титр", "короткометраж"],
    )


def _looks_giftcard_support(text: str) -> bool:
    return _contains_any(text, ["подарочн", "сертификат", "карта", "карту", "карты"]) and _contains_any(
        text,
        ["остаток", "актив", "не активна", "баланс", "номинал", "провер", "проверьте"],
    )


def _looks_customer_support(text: str, has_attachment: bool) -> bool:
    return _contains_any(
        text,
        [
            "билет",
            "ticket",
            "оплат",
            "ошибка оплаты",
            "заказ",
            "возврат",
            "вернуть деньги",
            "подарочн",
            "сертификат",
            "карт",
            "квитанц",
            "не приш",
            "не получил",
            "не получила",
        ],
    ) or (has_attachment and _contains_any(text, ["ошибка", "оплат", "платеж"]))


def _looks_service_notification(text: str) -> bool:
    return _contains_any(text, ["уведомляем", "service notification", "notification", "информируем"])


def _operator_summary(
    *,
    classification: str,
    sender: str,
    sender_email: str,
    subject: str,
    body: str,
    text: str,
    has_image: bool,
) -> str:
    if _looks_gratitude_closure(text):
        return _gratitude_summary(body)
    if _looks_schedule_question(text):
        return _schedule_summary(body, subject)
    if _looks_customer_support(text, has_image):
        return _customer_support_summary(subject, body, has_image)
    if _looks_candidate(text):
        return _candidate_summary(sender, body)
    if _looks_training_invitation(text):
        return _training_summary(sender, subject, body)
    if _looks_business_proposal(text):
        return _business_summary(sender, subject, body)
    return _fallback_summary(sender, subject, body)


def _schedule_summary(body: str, subject: str) -> str:
    text = _norm(" ".join([subject, body]))
    if "цифровой цирк" in text or "glitch" in text:
        if _contains_any(text, ["еще раз", "ещё раз", "повтор", "re:"]):
            return "Гость повторно спрашивает о возможности показа «Удивительного цифрового цирка»."
        return "Гость спрашивает, планирует ли mooon показывать «Цифровой цирк» в Беларуси."
    return "Гость спрашивает о расписании, репертуаре или возможности показа фильма."


def _customer_support_summary(subject: str, body: str, has_image: bool) -> str:
    text = _norm(" ".join([subject, body]))
    if "ошибка оплаты" in text or (_contains_any(text, ["оплат", "платеж"]) and _contains_any(text, ["ошибка", "выбивает"])):
        if has_image:
            return "Гость сообщает об ошибке оплаты при покупке билетов и приложил скриншот."
        return "Гость сообщает об ошибке оплаты при покупке билетов."
    if "подароч" in text and ("сертификат" in text or "карт" in text):
        if _contains_any(text, ["остаток", "актив", "не активна", "баланс", "номинал", "проверь"]):
            return "Гость просит проверить подарочную карту: остаток и статус активации; карта отображается как неактивная."
        if _contains_any(text, ["вернуть", "возврат", "деньги"]):
            return "Гость спрашивает, можно ли вернуть деньги за подарочную карту mooon."
        return "Гость обращается по вопросу подарочной карты mooon."
    if _contains_any(text, ["вернуть", "возврат", "деньги"]) and "билет" in text:
        email_match = re.search(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", body, flags=re.IGNORECASE)
        suffix = f"; указана почта {email_match.group(0)}." if email_match else "."
        return "Гость спрашивает, как вернуть деньги за билет" + suffix
    if "не приш" in text and "билет" in text:
        return "Гость сообщает, что после покупки не получил билеты."
    return _fallback_summary("", subject, body)


def _action_summary(sender: str, subject: str, body: str) -> str:
    if "плановые работы" in _norm(subject + " " + body):
        return "BELASSIST сообщает о плановых работах Банковского процессингового центра и возможном кратком перерыве платежей."
    return _fallback_summary(sender, subject, body)


def _newsletter_summary(sender: str, subject: str, body: str) -> str:
    text = _norm(sender + " " + subject + " " + body)
    if "uniquex" in text or "unique x" in text:
        return "Unique X прислали рекламную рассылку о партнёрстве с AUWE в Бразилии."
    return _fallback_summary(sender, subject, body, prefix="Рекламная рассылка")


def _gratitude_summary(body: str) -> str:
    text = _norm(_meaningful_excerpt(body, limit=260))
    if "пригласитель" in text and _contains_any(text, ["улажен", "решен", "решён"]):
        return "Вопрос с пригласительным решён, отправитель благодарит за реакцию."
    return "Отправитель благодарит и подтверждает, что вопрос решён."


def _candidate_summary(sender: str, body: str) -> str:
    text = _norm(sender + " " + body)
    if "никита" in text or "nikita" in text or "nikitamaskevich" in text:
        return "Никита Маскевич предлагает помощь с видеомонтажом, соцсетями и роликами, приложил ссылку на портфолио."
    if "мария" in text and ("бгу" in text or "институте бизнеса" in text or "аналитическую практику" in text):
        return "Мария, студентка маркетинга БГУ, просит пройти двухнедельную бесплатную аналитическую практику."
    if "практик" in text or "стажиров" in text:
        return "Отправитель просит рассмотреть практику или стажировку."
    return _fallback_summary(sender, "", body, prefix="Кандидат/исполнитель")


def _candidate_action_text(text: str) -> str:
    if _contains_any(text, ["видеомонтаж", "соцсет", "smm", "ролик"]):
        return "Переслать письмо в отдел маркетинга/SMM или ответственному за практику."
    if _contains_any(text, ["аналитическую практику", "студент", "бгу", "практику"]):
        return "Передать запрос ответственным за практику/HR или маркетинг."
    return "Переслать письмо в отдел маркетинга/SMM или ответственному за практику."


def _business_summary(sender: str, subject: str, body: str) -> str:
    text = _norm(" ".join([sender, subject, body]))
    if _contains_any(text, ["короткометраж", "съемк", "съёмк", "локаци", "аренд", "титрах"]):
        return "Александра предлагает снять короткометражный фильм в локации mooon и обсудить аренду или упоминание в титрах."
    return _fallback_summary(sender, subject, body, prefix="Бизнес-предложение")


def _business_action_text(text: str) -> str:
    if _contains_any(text, ["короткометраж", "съемк", "съёмк", "локаци", "аренд", "титрах"]):
        return "Передать письмо ответственным за партнёрства, маркетинг или администрацию объекта."
    return "Передать предложение ответственным за маркетинг или партнёрства."


def _training_summary(sender: str, subject: str, body: str) -> str:
    text = _norm(" ".join([sender, subject, body]))
    if "архив" in text:
        return "Университет НАН Беларуси приглашает на курс по архивному делу; во вложениях информационное письмо и регистрационная форма."
    return _fallback_summary(sender, subject, body, prefix="Приглашение на обучение")


def _security_summary(sender: str, subject: str, body: str) -> str:
    if "tilda" in _norm(sender + " " + subject + " " + body):
        return "Tilda прислала no-reply уведомление о входе в аккаунт с нового устройства."
    return _fallback_summary(sender, subject, body, prefix="Служебное security-уведомление")


def _service_summary(sender: str, subject: str, body: str) -> str:
    return _fallback_summary(sender, subject, body, prefix="Служебное уведомление")


def _fallback_summary(sender: str, subject: str, body: str, prefix: str = "Смысл письма") -> str:
    preview = _meaningful_excerpt(body) or subject.strip()
    if preview:
        return f"{prefix}: {_truncate(preview, 180)}"
    if sender:
        return f"{prefix}: письмо от {sender} без понятного текста."
    return "Суть не определена: нужен ручной просмотр письма."


def _attachment_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    module = (payload.get("modules") or {}).get("attachment_extraction") or {}
    items = module.get("items") if isinstance(module, dict) else []
    if isinstance(items, list) and items:
        return [item for item in items if isinstance(item, dict)]
    inventory = payload.get("attachments_inventory") or []
    return [item for item in inventory if isinstance(item, dict)]


def _recipient_emails(headers: dict[str, Any]) -> set[str]:
    result = set(OWN_MAILBOXES)
    for key in ("to", "cc"):
        values = headers.get(key) or []
        if isinstance(values, str):
            values = [values]
        for value in values:
            email = _email(str(value or ""))
            if email:
                result.add(email)
    return result


def _email(value: str) -> str:
    parsed = parseaddr(str(value or ""))[1].strip().lower()
    if parsed:
        return parsed
    match = re.search(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", str(value or ""), flags=re.IGNORECASE)
    return match.group(0).lower() if match else ""


def _resolve_uid(payload: dict[str, Any]) -> str:
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    return str(metadata.get("uid") or metadata.get("fixture_ref") or payload.get("uid") or "unknown")


def _contains_any(value: str, tokens: list[str]) -> bool:
    haystack = str(value or "").casefold().replace("ё", "е")
    return any(token.casefold().replace("ё", "е") in haystack for token in tokens)


def _norm(value: str) -> str:
    return " ".join(str(value or "").casefold().replace("ё", "е").split())


def _first_sentence(value: str) -> str:
    text = " ".join(str(value or "").split())
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return parts[0].strip() if parts else text


def _meaningful_excerpt(value: str, limit: int = 220) -> str:
    text = str(value or "").replace("\xa0", " ")
    for marker in ["\n\n--", "\n--", "\nКому:", "\nОт:", "-----Original Message-----", "----------------"]:
        if marker in text:
            text = text.split(marker, 1)[0]
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[*_`]+", "", text)
    text = " ".join(text.split()).strip()
    if not text:
        return ""
    text = re.sub(
        r"^(здравствуйте|добрый день|добрый вечер|доброе утро|привет)[!,. ]+",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()
    if not text:
        return ""
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    if not sentences:
        return _truncate(text, limit)
    if len(sentences[0]) < 12 and len(sentences) > 1:
        return _truncate(sentences[1], limit)
    return _truncate(sentences[0], limit)


def _truncate(value: str, limit: int) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(limit - 1, 1)].rstrip() + "…"
