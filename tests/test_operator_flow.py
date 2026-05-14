from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.pipeline.draft_builder.module import DraftBuilderModule
from src.pipeline.operator_actions.module import OperatorActionsModule
from src.pipeline.operator_bot import OperatorBotHandler
from src.pipeline.telegram_operator_delivery.module import TelegramOperatorDeliveryModule
from src.runners.run_mock_mailbox_flow import discover_eml_files, ensure_mock_mailbox_dirs
from src.shared.common.message_dossier import load_message_record, write_message_dossier
from src.shared.models.pipeline_context import PipelineContext


class OperatorFlowTest(unittest.TestCase):
    def test_card_layout_and_callbacks_are_demo_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dossier_path = self._write_dossier(Path(tmp) / "message_demo.md")
            artifacts_dir = str(Path(tmp) / "artifacts")

            draft_result = DraftBuilderModule(dossier_path=str(dossier_path)).run(PipelineContext(run_id="test-draft"))
            self.assertEqual(draft_result.status, "ok")

            card_result = TelegramOperatorDeliveryModule(
                dossier_path=str(dossier_path),
                artifacts_dir=artifacts_dir,
                delivery_mode="artifact",
            ).run(PipelineContext(run_id="test-card"))
            self.assertEqual(card_result.status, "ok")

            card = self._read_json(Path(card_result.metrics["card_artifact_path"]))
            text = card["card_text"]
            self.assertIn("<b>📩 Новое письмо</b>", text)
            self.assertLess(text.index("<b>Проверка билетов</b>"), text.index("<b>Что понял ассистент</b>"))
            self.assertIn("Билет: не найден", text)
            self.assertIn("<b>История переписки</b>", text)
            self.assertIn("входящее", text)
            self.assertIn("✏️ На доработку (LLM)", json.dumps(card["keyboard"], ensure_ascii=False))


    def test_revision_callback_does_not_send_force_reply_and_updates_card(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dossier_path = self._write_dossier(Path(tmp) / "message_demo.md")
            artifacts_dir = str(Path(tmp) / "artifacts")
            DraftBuilderModule(dossier_path=str(dossier_path)).run(PipelineContext(run_id="test-draft"))

            card_result = TelegramOperatorDeliveryModule(
                dossier_path=str(dossier_path),
                artifacts_dir=artifacts_dir,
                delivery_mode="artifact",
            ).run(PipelineContext(run_id="test-card"))
            self.assertEqual(card_result.status, "ok")
            card = self._read_json(Path(card_result.metrics["card_artifact_path"]))
            callback_data = next(item["callback_data"] for item in card["keyboard"] if item["action"] == "needs_edit")

            client = _FakeTelegramClient()
            handler = OperatorBotHandler(artifacts_dir=artifacts_dir, client=client)
            callback_result = handler.handle_callback(
                callback_data=callback_data,
                chat_id=100,
                message_id=int(card["telegram_message_id"]),
                callback_query_id="callback-1",
            )
            self.assertEqual(callback_result["status"], "ok")
            self.assertNotIn("sendMessage", [op["operation"] for op in client.operations])

            comment_result = handler.handle_operator_message(
                chat_id=100,
                text="Добавь конкретную инструкцию по возврату.",
                message_id=555,
                reply_to_message_id=int(card["telegram_message_id"]),
            )
            self.assertEqual(comment_result["status"], "ok")
            updated_card = self._read_json(Path(comment_result["card_artifact_path"]))
            self.assertIn("<b>Комментарий оператора</b>", updated_card["card_text"])
            self.assertIn("Добавь конкретную инструкцию по возврату.", updated_card["card_text"])
            self.assertIn("<b>Черновик v2</b>", updated_card["card_text"])

    def test_mock_mailbox_dirs_and_empty_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "mock_mailbox"
            inbox = root / "inbox"
            processed = root / "processed"
            failed = root / "failed"
            processing = root / "processing"
            ensure_mock_mailbox_dirs(inbox_dir=inbox, processing_dir=processing, processed_dir=processed, failed_dir=failed)

            self.assertTrue(inbox.exists())
            self.assertTrue(processing.exists())
            self.assertTrue(processed.exists())
            self.assertTrue(failed.exists())
            self.assertEqual(discover_eml_files(inbox), [])

    def test_needs_edit_creates_revision_and_new_russian_card(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dossier_path = self._write_dossier(Path(tmp) / "message_demo.md")
            artifacts_dir = str(Path(tmp) / "artifacts")
            DraftBuilderModule(dossier_path=str(dossier_path)).run(PipelineContext(run_id="test-draft"))

            result = OperatorActionsModule(
                dossier_path=str(dossier_path),
                artifacts_dir=artifacts_dir,
                action="needs_edit",
                operator_comment="Добавь просьбу указать номер заказа.",
                operator_username="demo_operator",
            ).run(PipelineContext(run_id="test-needs-edit"))

            self.assertEqual(result.status, "ok")
            payload = load_message_record(dossier_path)
            draft = payload["modules"]["draft_builder"]
            self.assertEqual(draft["latest_revision"], 2)
            self.assertIn("Добавь просьбу указать номер заказа.", draft["draft_text"])
            self.assertEqual(draft["revisions"][-1]["operator_comment"], "Добавь просьбу указать номер заказа.")
            self.assertFalse(payload["modules"]["operator_actions"]["real_email_sent"])

            card = self._read_json(Path(result.metrics["updated_card_ref"]))
            self.assertIn("✏️ Черновик доработан LLM", card["card_text"])
            self.assertIn("<b>Черновик v2</b>", card["card_text"])

    def test_approve_uses_latest_draft_and_never_sends_real_email(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dossier_path = self._write_dossier(Path(tmp) / "message_demo.md")
            artifacts_dir = str(Path(tmp) / "artifacts")
            context = PipelineContext(run_id="test-flow")
            DraftBuilderModule(dossier_path=str(dossier_path)).run(context)
            OperatorActionsModule(
                dossier_path=str(dossier_path),
                artifacts_dir=artifacts_dir,
                action="needs_edit",
                operator_comment="Добавь просьбу указать номер заказа.",
            ).run(context)

            result = OperatorActionsModule(
                dossier_path=str(dossier_path),
                artifacts_dir=artifacts_dir,
                action="approve",
                operator_username="demo_operator",
            ).run(PipelineContext(run_id="test-approve"))

            self.assertEqual(result.status, "ok")
            self.assertFalse(result.metrics["real_email_sent"])
            self.assertTrue(result.metrics["mock_reply_refs"])
            reply_json = self._read_json(Path(result.metrics["mock_reply_refs"][1]))
            self.assertEqual(reply_json["status"], "approved_mock_not_sent")
            self.assertFalse(reply_json["real_email_sent"])
            self.assertEqual(reply_json["draft_revision"], 2)
            self.assertIn("Добавь просьбу указать номер заказа.", reply_json["final_draft_text"])

            card = self._read_json(Path(result.metrics["updated_card_ref"]))
            self.assertIn("✅ Статус: утверждено", card["card_text"])
            self.assertIn("Реальный email не отправлен", card["card_text"])

    def test_handoff_and_ignore_update_cards_in_russian(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dossier_path = self._write_dossier(Path(tmp) / "message_demo.md")
            artifacts_dir = str(Path(tmp) / "artifacts")
            DraftBuilderModule(dossier_path=str(dossier_path)).run(PipelineContext(run_id="test-draft"))

            for action, expected in [
                ("handoff", "Кейс помечен для ручной обработки"),
                ("ignore", "Ответ не требуется"),
            ]:
                result = OperatorActionsModule(
                    dossier_path=str(dossier_path),
                    artifacts_dir=artifacts_dir,
                    action=action,
                ).run(PipelineContext(run_id=f"test-{action}"))
                self.assertEqual(result.status, "ok")
                card = self._read_json(Path(result.metrics["updated_card_ref"]))
                self.assertIn(expected, card["card_text"])
                self.assertNotIn("передано оператору", card["card_text"])

    def _write_dossier(self, path: Path) -> Path:
        payload = {
            "message_id": "<demo@example.test>",
            "direction": "inbound",
            "headers": {
                "sender": "guest@example.test",
                "subject": "Ticket email not received",
                "sent_at": "2026-05-13T10:00:00+00:00",
                "to": ["info@mooon.by"],
                "cc": [],
            },
            "body_text": "I paid online but did not receive the tickets.",
            "metadata": {"uid": "demo"},
            "modules": {
                "identity_context_enrichment": {
                    "result": {
                        "selected_lookup_email": "guest@example.test",
                        "ticket_db_status": "rescue_candidates",
                        "confidence": "low",
                        "candidates_count": 2,
                        "resolved_match": None,
                    },
                    "debug": {
                        "providers": {
                            "ticket_db": {
                                "candidates": [
                                    {"ticket": 1001, "event": "Demo Movie", "dateShow": "2026-05-13"},
                                    {"ticket": 1002, "event": "Demo Movie 2", "dateShow": "2026-05-14"},
                                ]
                            }
                        }
                    },
                },
                "case_thread_binding": {
                    "case_id": "case-demo",
                    "thread_id": "thread-demo",
                    "binding_rule": "new_case_thread",
                    "thread_history": [
                        {
                            "message_id": "<old@example.test>",
                            "direction": "inbound",
                            "sender": "guest@example.test",
                            "subject": "Ticket email not received",
                            "sent_at": "2026-05-13T09:55:00+00:00",
                            "status": "new_case_thread",
                        },
                        {
                            "message_id": "<demo@example.test>",
                            "direction": "inbound",
                            "sender": "guest@example.test",
                            "subject": "Ticket email not received",
                            "sent_at": "2026-05-13T10:00:00+00:00",
                            "status": "bound_existing_thread",
                        },
                    ],
                },
                "llm_understanding": {
                    "status": "ok",
                    "structured_output": {
                        "summary": "Гость оплатил онлайн, но не получил билет.",
                        "topic": "Не пришел электронный билет",
                        "customer_need": "Получить электронный билет или инструкцию по восстановлению.",
                        "entities": [{"type": "email", "value": "guest@example.test"}],
                        "confidence": 0.91,
                        "response_mode": "answer",
                        "response_mode_reason": "Можно дать безопасные инструкции.",
                    },
                },
                "knowledge_retrieval": {
                    "status": "found",
                    "matched_items": [
                        {
                            "id": "kb_system_ticket_sender",
                            "title": "Адрес отправителя электронных билетов",
                            "score": 11,
                            "template_hint": "Письмо с билетами отправляется с адреса ticket@silverscreen.by.",
                        }
                    ],
                },
                "decision_layer": {
                    "status": "ok",
                    "response_mode_final": "ask_clarifying_question",
                    "decision_reason": "Не найден подтвержденный заказ.",
                    "missing_data": ["Не найден подтвержденный билет/заказ клиента."],
                    "risks": [],
                },
            },
        }
        write_message_dossier(path, payload)
        return path

    @staticmethod
    def _read_json(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))



class _FakeTelegramClient:
    def __init__(self) -> None:
        self.operations: list[dict] = []
        self._message_id = 900

    def edit_message_text(self, **kwargs) -> dict:
        result = {"operation": "editMessageText", "ok": True, "message_id": kwargs.get("message_id")}
        self.operations.append(result)
        return result

    def edit_message_reply_markup(self, **kwargs) -> dict:
        result = {"operation": "editMessageReplyMarkup", "ok": True, "message_id": kwargs.get("message_id")}
        self.operations.append(result)
        return result

    def send_message(self, **kwargs) -> dict:
        self._message_id += 1
        result = {"operation": "sendMessage", "ok": True, "message_id": self._message_id, "chat_id": kwargs.get("chat_id")}
        self.operations.append(result)
        return result

    def answer_callback_query(self, **kwargs) -> dict:
        result = {"operation": "answerCallbackQuery", "ok": True}
        self.operations.append(result)
        return result

    def delete_message(self, **kwargs) -> dict:
        result = {"operation": "deleteMessage", "ok": True, "message_id": kwargs.get("message_id")}
        self.operations.append(result)
        return result

if __name__ == "__main__":
    unittest.main()
