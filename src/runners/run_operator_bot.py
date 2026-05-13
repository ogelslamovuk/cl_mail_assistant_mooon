from __future__ import annotations

import argparse

from src.pipeline.operator_bot import OperatorBotHandler
from src.pipeline.telegram_bot_api import TelegramBotApiClient
from src.pipeline.operator_flow import read_json, write_json
from src.shared.common.paths import resolve_project_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Telegram operator bot polling loop")
    parser.add_argument("--artifacts-dir", default="artifacts")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--poll-timeout", type=int, default=30)
    args = parser.parse_args()

    client = TelegramBotApiClient.from_config()
    if client is None:
        raise RuntimeError("Telegram bot token is not configured")

    handler = OperatorBotHandler(artifacts_dir=args.artifacts_dir, client=client)
    state_path = resolve_project_path(args.artifacts_dir) / "state" / "operator_bot_updates.json"

    while True:
        state = read_json(state_path, {"offset": None})
        offset = state.get("offset") if isinstance(state, dict) else None
        updates = client.get_updates(offset=offset, timeout=args.poll_timeout)
        if not updates.get("ok"):
            raise RuntimeError(f"Telegram getUpdates failed: {updates.get('error')}")

        for update in updates.get("result") or []:
            update_id = int(update.get("update_id"))
            state = {"offset": update_id + 1}
            callback_query = update.get("callback_query")
            if callback_query:
                message = callback_query.get("message") or {}
                chat = message.get("chat") or {}
                from_user = callback_query.get("from") or {}
                handler.handle_callback(
                    callback_data=str(callback_query.get("data") or ""),
                    chat_id=chat.get("id"),
                    message_id=int(message.get("message_id")),
                    operator_telegram_id=str(from_user.get("id") or ""),
                    operator_username=str(from_user.get("username") or ""),
                    callback_query_id=str(callback_query.get("id") or ""),
                )

            message = update.get("message")
            if message and message.get("text"):
                chat = message.get("chat") or {}
                from_user = message.get("from") or {}
                handler.handle_operator_message(
                    chat_id=chat.get("id"),
                    text=str(message.get("text") or ""),
                    operator_telegram_id=str(from_user.get("id") or ""),
                    operator_username=str(from_user.get("username") or ""),
                )
            write_json(state_path, state)

        if args.once:
            break


if __name__ == "__main__":
    main()
