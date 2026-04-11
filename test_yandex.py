import imaplib
import time
from email import message_from_bytes
from email.header import decode_header
from email.utils import parseaddr


EMAIL_ADDRESS = "info@mooon.by"
IMAP_USERNAME = "info@mooon.by"
APP_PASSWORD = "lqlgohujyafberqi"

IMAP_HOST = "imap.yandex.com"
IMAP_PORT = 993
MAILBOX = "INBOX"
POLL_INTERVAL_SEC = 3


def decode_mime_header(value: str | None) -> str:
    if not value:
        return ""

    parts = decode_header(value)
    decoded_chunks = []

    for part, encoding in parts:
        if isinstance(part, bytes):
            decoded_chunks.append(part.decode(encoding or "utf-8", errors="replace"))
        else:
            decoded_chunks.append(part)

    return "".join(decoded_chunks).strip()


def connect_imap() -> imaplib.IMAP4_SSL:
    print("Подключаюсь к Yandex IMAP...")
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(IMAP_USERNAME, APP_PASSWORD)
    mail.select(MAILBOX, readonly=True)
    print(f"Успешно подключено. Папка: {MAILBOX}")
    return mail


def get_all_uids(mail: imaplib.IMAP4_SSL) -> set[str]:
    status, data = mail.uid("search", None, "ALL")
    if status != "OK":
        raise RuntimeError("Не удалось получить список UID из ящика.")

    raw = data[0].decode("utf-8").strip()
    if not raw:
        return set()

    return set(raw.split())


def fetch_sender_and_subject(mail: imaplib.IMAP4_SSL, uid: str) -> tuple[str, str]:
    status, data = mail.uid(
        "fetch",
        uid,
        "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])",
    )
    if status != "OK":
        raise RuntimeError(f"Не удалось получить заголовки письма UID={uid}")

    header_bytes = None
    for item in data:
        if isinstance(item, tuple) and len(item) >= 2 and isinstance(item[1], bytes):
            header_bytes = item[1]
            break

    if not header_bytes:
        raise RuntimeError(f"Пустые заголовки письма UID={uid}")

    msg = message_from_bytes(header_bytes)

    from_raw = msg.get("From", "")
    subject_raw = msg.get("Subject", "")

    _, from_email = parseaddr(from_raw)
    subject = decode_mime_header(subject_raw)

    return from_email or from_raw, subject


def main() -> None:
    mail = None
    known_uids: set[str] = set()

    try:
        mail = connect_imap()
        known_uids = get_all_uids(mail)
        print(f"Базовая инициализация завершена. Текущих писем в {MAILBOX}: {len(known_uids)}")
        print("Жду новые входящие...\n")

        while True:
            try:
                mail.noop()
                current_uids = get_all_uids(mail)
                new_uids = sorted(current_uids - known_uids, key=lambda x: int(x))

                for uid in new_uids:
                    sender_email, subject = fetch_sender_and_subject(mail, uid)
                    print(f"Получено входящее от {sender_email} | subject={subject}")

                known_uids = current_uids
                time.sleep(POLL_INTERVAL_SEC)

            except KeyboardInterrupt:
                print("\nОстановлено пользователем.")
                break

            except Exception as e:
                print(f"Ошибка в цикле опроса: {e}")
                print("Пробую переподключиться через 5 секунд...")
                time.sleep(5)
                mail = connect_imap()
                mail.noop()

    finally:
        if mail is not None:
            try:
                mail.logout()
            except Exception:
                pass


if __name__ == "__main__":
    main()