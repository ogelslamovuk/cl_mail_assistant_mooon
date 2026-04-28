from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from src.layers.config.excel_config_store import ExcelConfigStore
from src.shared.common.message_dossier import load_message_record, write_message_dossier
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.pipeline_context import PipelineContext


CANONICAL_RESPONSE_MODES = {
    "answer",
    "ask_clarifying_question",
    "handoff_to_operator",
    "no_reply",
    "ignore",
}
VALID_RISK_LEVELS = {"low", "medium", "high"}

REQUIRED_OUTPUT_FIELDS = [
    "summary",
    "topic",
    "customer_need",
    "entities",
    "confidence",
    "response_mode",
    "understanding_note",
    "response_mode_reason",
    "suggested_next_step",
]


@dataclass
class AttemptResult:
    status: str
    error: str
    raw_response_text: str
    parsed_output: dict[str, Any] | None
    duration_ms: int


class LlmUnderstandingModule:
    name = "llm_understanding"

    def __init__(self, dossier_path: str, config_path: str) -> None:
        self.dossier_path = str(dossier_path)
        self.config_path = str(config_path)

    def run(self, context: PipelineContext) -> ModuleResult:
        started_at = time.perf_counter()
        dossier_file = Path(self.dossier_path)
        if not dossier_file.exists():
            return ModuleResult(context=context, status="error", notes=[f"dossier missing: {dossier_file}"])

        try:
            dossier_payload = load_message_record(dossier_file)
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"dossier unreadable: {exc}"])

        try:
            config = ExcelConfigStore(self.config_path).load()
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"config unreadable: {exc}"])

        uid = self._resolve_uid(dossier_payload)
        structured_input = self._build_structured_input(dossier_payload, config.get('flags') or {})
        prompt_package = self._build_prompt_package(config=config, structured_input=structured_input)
        max_attempts = max(int(config["settings"].get("llm_retry_max_attempts", 2) or 2), 1)

        final_attempt: AttemptResult | None = None
        for attempt_index in range(1, max_attempts + 1):
            retry_hint = "" if attempt_index == 1 else self._retry_hint()
            try:
                raw_response_text = self._call_backend(config=config, prompt_package=prompt_package, retry_hint=retry_hint)
                parsed_output = self._parse_and_validate_output(
                    raw_response_text=raw_response_text,
                    allowed_response_modes=config["allowed_response_modes"],
                )
                duration_ms = int((time.perf_counter() - started_at) * 1000)
                final_attempt = AttemptResult(
                    status="ok",
                    error="",
                    raw_response_text=raw_response_text,
                    parsed_output=parsed_output,
                    duration_ms=duration_ms,
                )
                break
            except Exception as exc:
                duration_ms = int((time.perf_counter() - started_at) * 1000)
                final_attempt = AttemptResult(
                    status="error",
                    error=str(exc),
                    raw_response_text=locals().get("raw_response_text", ""),
                    parsed_output=None,
                    duration_ms=duration_ms,
                )

        assert final_attempt is not None

        metrics = {
            "uid": uid,
            "dossier_path": str(dossier_file),
            "config_path": self.config_path,
            "backend": config["backend"],
            "model": self._resolve_model(config),
            "prompt_version": config["prompt_version"],
            "context_version": config["context_version"],
            "status": final_attempt.status,
            "error": final_attempt.error,
            "duration_ms": final_attempt.duration_ms,
            "raw_response_text": final_attempt.raw_response_text,
            "structured_output": final_attempt.parsed_output,
            "prompt_package": {
                "system_prompt": prompt_package["system_prompt"],
                "user_prompt": prompt_package["user_prompt"],
                "allowed_response_modes": config["allowed_response_modes"],
                "flags": config.get("flags") or {},
            },
        }

        if final_attempt.status == "ok" and final_attempt.parsed_output is not None:
            self._write_understanding_to_dossier(
                dossier_file=dossier_file,
                dossier_payload=dossier_payload,
                uid=uid,
                config=config,
                attempt=final_attempt,
            )
            context.understanding[self.name] = final_attempt.parsed_output
            context.artifacts.setdefault(self.name, []).append(str(dossier_file))
            notes = [
                f"llm_understanding processed uid={uid}",
                f"response_mode={final_attempt.parsed_output['response_mode']}",
                f"confidence={final_attempt.parsed_output['confidence']}",
            ]
            return ModuleResult(
                context=context,
                status="ok",
                notes=notes,
                artifact_refs=[str(dossier_file)],
                metrics=metrics,
            )

        return ModuleResult(
            context=context,
            status="error",
            notes=[f"llm_understanding failed uid={uid}: {final_attempt.error}"],
            artifact_refs=[],
            metrics=metrics,
        )

    def _write_understanding_to_dossier(
        self,
        *,
        dossier_file: Path,
        dossier_payload: dict[str, Any],
        uid: str,
        config: dict[str, Any],
        attempt: AttemptResult,
    ) -> None:
        modules = dossier_payload.setdefault("modules", {})
        if not isinstance(modules, dict):
            modules = {}
            dossier_payload["modules"] = modules

        modules[self.name] = {
            "uid": uid,
            "status": attempt.status,
            "backend": config["backend"],
            "model": self._resolve_model(config),
            "prompt_version": config["prompt_version"],
            "context_version": config["context_version"],
            "duration_ms": attempt.duration_ms,
            "error": attempt.error,
            "structured_output": attempt.parsed_output or {},
        }
        write_message_dossier(dossier_file, dossier_payload)

    def _build_prompt_package(self, *, config: dict[str, Any], structured_input: dict[str, Any]) -> dict[str, str]:
        prompts = config["prompts"]
        policies = config["text_policies"]
        allowed_modes = config["allowed_response_modes"]

        system_parts: list[str] = []
        system_prompt = prompts["system_prompt"]
        if system_prompt["enabled"] and system_prompt["text"]:
            system_parts.append(system_prompt["text"])

        support_context = prompts["static_support_context"]
        if support_context["enabled"] and support_context["text"]:
            system_parts.append("STATIC SUPPORT CONTEXT:\n" + support_context["text"])

        enabled_policies = [policy for policy in policies.values() if policy["enabled"] and policy["text"]]
        if enabled_policies:
            policy_lines = []
            for policy in enabled_policies:
                policy_lines.append(f"- {policy['block_id']}: {policy['text']}")
            system_parts.append("TEXT POLICIES:\n" + "\n".join(policy_lines))

        contract = {
            "required_fields": REQUIRED_OUTPUT_FIELDS,
            "optional_fields": ["risk_level", "needs_human"],
            "test_mode_explanation_fields": {
                "understanding_note": "Short human-readable explanation of what the model understood. This is not a client reply.",
                "response_mode_reason": "Short explanation of why this response_mode was selected.",
                "suggested_next_step": "Short operational next step for the next pipeline layer or operator. This is not a client reply.",
            },
            "allowed_response_modes": allowed_modes,
            "entities_shape": {
                "type": "list",
                "item_shape": {"type": "string", "value": "string"},
            },
            "confidence_range": "0.0 .. 1.0",
            "risk_level_allowed": sorted(VALID_RISK_LEVELS),
        }
        system_parts.append(
            "OUTPUT CONTRACT:\n"
            "Return STRICT JSON ONLY. No markdown. No comments. No explanations outside JSON.\n"
            + json.dumps(contract, ensure_ascii=False, indent=2)
        )

        task_parts: list[str] = []
        task_prompt = prompts["task_prompt"]
        if task_prompt["enabled"] and task_prompt["text"]:
            task_parts.append(task_prompt["text"])
        task_parts.append("DOSSIER INPUT:\n" + json.dumps(structured_input, ensure_ascii=False, indent=2))

        return {
            "system_prompt": "\n\n".join(part for part in system_parts if part.strip()),
            "user_prompt": "\n\n".join(part for part in task_parts if part.strip()),
        }

    def _build_structured_input(self, dossier_payload: dict[str, Any], flags: dict[str, Any]) -> dict[str, Any]:
        headers = dossier_payload.get("headers") or {}
        modules = dossier_payload.get("modules") or {}
        attachment = modules.get("attachment_extraction") or {}
        enrichment = modules.get("identity_context_enrichment") or {}
        binding = modules.get("case_thread_binding") or {}

        technical_flags = {
            "is_bounce": bool(dossier_payload.get("is_bounce")),
            "is_auto_reply": bool(dossier_payload.get("is_auto_reply")),
            "is_mailing_like": bool(dossier_payload.get("is_mailing_like")),
            "is_system_generated_likely": bool(dossier_payload.get("is_system_generated_likely")),
        }

        attachment_items = []
        for item in attachment.get("items") or []:
            attachment_items.append(
                {
                    "filename": str(item.get("filename_saved") or item.get("filename_original") or "").strip(),
                    "content_type": str(item.get("content_type", "") or "").strip(),
                    "text_found": bool(item.get("text_found")),
                    "text_preview": str(item.get("text_preview", "") or "").strip(),
                    "extraction_method": str(item.get("extraction_method", "") or "").strip(),
                    "skip_reason": str(item.get("skip_reason", "") or "").strip(),
                }
            )

        enrichment_result = enrichment.get("result") or {}
        ticket_debug = (((enrichment.get("debug") or {}).get("providers") or {}).get("ticket_db") or {})
        top_candidates = []
        if bool(flags.get('include_top_ticket_candidates', True)):
            for candidate in (ticket_debug.get("candidates") or [])[:3]:
                top_candidates.append(
                    {
                        "emailClient": candidate.get("emailClient"),
                        "idTrading": candidate.get("idTrading"),
                        "ticket": candidate.get("ticket"),
                        "event": candidate.get("event"),
                        "dateShow": candidate.get("dateShow"),
                        "timeShow": candidate.get("timeShow"),
                        "theater": candidate.get("theater"),
                        "rescue_score": candidate.get("rescue_score"),
                    }
                )

        thread_history = []
        if bool(flags.get('include_thread_history', True)):
            for item in (binding.get("thread_history") or [])[-5:]:
                thread_history.append(
                    {
                        "message_id": str(item.get("message_id", "") or "").strip(),
                        "direction": str(item.get("direction", "") or "").strip(),
                        "sender": str(item.get("sender", "") or "").strip(),
                        "subject": str(item.get("subject", "") or "").strip(),
                        "sent_at": str(item.get("sent_at", "") or "").strip(),
                        "binding_rule": str(item.get("binding_rule", "") or "").strip(),
                        "status": str(item.get("status", "") or "").strip(),
                    }
                )

        return {
            "message": {
                "uid": self._resolve_uid(dossier_payload),
                "message_id": str(dossier_payload.get("message_id", "") or "").strip(),
                "subject": str(headers.get("subject", "") or "").strip(),
                "sender": str(headers.get("sender", "") or "").strip(),
                "to": headers.get("to") or [],
                "cc": headers.get("cc") or [],
                "sent_at": str(headers.get("sent_at", "") or "").strip(),
                "preferred_body_source": str(dossier_payload.get("preferred_body_source", "") or "").strip(),
                "body_text": str(dossier_payload.get("body_text", "") or "").strip(),
                "technical_flags": technical_flags,
            },
            "attachments": {
                "count": len(attachment_items),
                "items": attachment_items,
            },
            "factual_enrichment": {
                "lookup_emails": enrichment_result.get("lookup_emails") or [],
                "selected_lookup_email": enrichment_result.get("selected_lookup_email"),
                "ticket_db_status": enrichment_result.get("ticket_db_status"),
                "crm_users_status": enrichment_result.get("crm_users_status"),
                "payment_refund_status": enrichment_result.get("payment_refund_status"),
                "confidence": enrichment_result.get("confidence"),
                "candidates_count": enrichment_result.get("candidates_count"),
                "resolved_match": enrichment_result.get("resolved_match"),
                "note": enrichment_result.get("note"),
                "top_ticket_candidates": top_candidates,
            },
            "case_thread_context": {
                "case_id": binding.get("case_id"),
                "thread_id": binding.get("thread_id"),
                "binding_rule": binding.get("binding_rule"),
                "matched_message_id": binding.get("matched_message_id"),
                "thread_history": thread_history,
            },
        }

    def _call_backend(self, *, config: dict[str, Any], prompt_package: dict[str, str], retry_hint: str) -> str:
        backend = config["backend"]
        settings = config["settings"]
        system_prompt = prompt_package["system_prompt"]
        user_prompt = prompt_package["user_prompt"] + retry_hint
        if backend == "ollama":
            base_url = str(settings.get("ollama_base_url", "") or "").rstrip("/")
            model = str(settings.get("ollama_model", "") or "").strip()
            timeout_sec = int(settings.get("ollama_timeout_sec", 60) or 60)
            temperature = float(settings.get("ollama_temperature", 0.0) or 0.0)
            prompt = system_prompt + "\n\nUSER TASK:\n" + user_prompt
            response = requests.post(
                f"{base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": temperature},
                },
                timeout=timeout_sec,
            )
            response.raise_for_status()
            payload = response.json()
            return str(payload.get("response") or "").strip()

        if backend == "openai":
            base_url = str(settings.get("openai_base_url", "https://api.openai.com/v1") or "").rstrip("/")
            model = str(settings.get("openai_model", "") or "").strip()
            timeout_sec = int(settings.get("openai_timeout_sec", 60) or 60)
            temperature = float(settings.get("openai_temperature", 0.0) or 0.0)
            api_key = self._resolve_openai_api_key(settings)
            response = requests.post(
                f"{base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "temperature": temperature,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
                timeout=timeout_sec,
            )
            response.raise_for_status()
            payload = response.json()
            choices = payload.get("choices") or []
            if not choices:
                raise RuntimeError("OpenAI response missing choices")
            message = choices[0].get("message") or {}
            return str(message.get("content") or "").strip()

        raise RuntimeError(f"Unsupported llm_backend: {backend}")

    def _resolve_openai_api_key(self, settings: dict[str, Any]) -> str:
        direct_key = str(settings.get("openai_api_key", "") or "").strip()
        if direct_key:
            return direct_key
        env_name = str(settings.get("openai_api_key_env", "OPENAI_API_KEY") or "OPENAI_API_KEY").strip()
        env_value = os.getenv(env_name, "").strip()
        if env_value:
            return env_value
        raise RuntimeError(f"OpenAI API key not found in settings and env {env_name}")

    def _parse_and_validate_output(self, *, raw_response_text: str, allowed_response_modes: list[str]) -> dict[str, Any]:
        parsed = self._parse_json_object(raw_response_text)
        if not isinstance(parsed, dict):
            raise RuntimeError("LLM output must be a JSON object")

        required_fields = REQUIRED_OUTPUT_FIELDS
        missing = [field for field in required_fields if field not in parsed]
        if missing:
            raise RuntimeError(f"LLM output missing required fields: {', '.join(missing)}")

        summary = str(parsed.get("summary") or "").strip()
        topic = str(parsed.get("topic") or "").strip()
        customer_need = str(parsed.get("customer_need") or "").strip()
        entities_raw = parsed.get("entities")
        confidence_raw = parsed.get("confidence")
        response_mode = str(parsed.get("response_mode") or "").strip()
        understanding_note = str(parsed.get("understanding_note") or "").strip()
        response_mode_reason = str(parsed.get("response_mode_reason") or "").strip()
        suggested_next_step = str(parsed.get("suggested_next_step") or "").strip()
        risk_level_raw = parsed.get("risk_level")
        needs_human_raw = parsed.get("needs_human")

        if not summary:
            raise RuntimeError("LLM output field 'summary' must be a non-empty string")
        if not topic:
            raise RuntimeError("LLM output field 'topic' must be a non-empty string")
        if not customer_need:
            raise RuntimeError("LLM output field 'customer_need' must be a non-empty string")
        if not understanding_note:
            raise RuntimeError("LLM output field 'understanding_note' must be a non-empty string")
        if not response_mode_reason:
            raise RuntimeError("LLM output field 'response_mode_reason' must be a non-empty string")
        if not suggested_next_step:
            raise RuntimeError("LLM output field 'suggested_next_step' must be a non-empty string")
        if response_mode not in allowed_response_modes:
            raise RuntimeError(
                f"LLM output field 'response_mode' must be one of: {', '.join(allowed_response_modes)}"
            )
        if response_mode not in CANONICAL_RESPONSE_MODES:
            raise RuntimeError(f"response_mode '{response_mode}' is outside canonical set")

        try:
            confidence = float(confidence_raw)
        except Exception as exc:
            raise RuntimeError(f"LLM output field 'confidence' must be numeric: {exc}") from exc
        if confidence < 0.0 or confidence > 1.0:
            raise RuntimeError("LLM output field 'confidence' must be in range 0.0..1.0")

        if not isinstance(entities_raw, list):
            raise RuntimeError("LLM output field 'entities' must be a list")
        entities: list[dict[str, str]] = []
        for index, entity in enumerate(entities_raw):
            if not isinstance(entity, dict):
                raise RuntimeError(f"entities[{index}] must be an object")
            entity_type = str(entity.get("type") or "").strip()
            entity_value = str(entity.get("value") or "").strip()
            if not entity_type or not entity_value:
                raise RuntimeError(f"entities[{index}] must contain non-empty type and value")
            entities.append({"type": entity_type, "value": entity_value})

        risk_level: str | None = None
        if risk_level_raw not in (None, ""):
            risk_level = str(risk_level_raw).strip()
            if risk_level not in VALID_RISK_LEVELS:
                raise RuntimeError(f"risk_level must be one of: {', '.join(sorted(VALID_RISK_LEVELS))}")

        needs_human: bool | None = None
        if needs_human_raw not in (None, ""):
            if isinstance(needs_human_raw, bool):
                needs_human = needs_human_raw
            else:
                text = str(needs_human_raw).strip().lower()
                if text not in {"true", "false", "1", "0"}:
                    raise RuntimeError("needs_human must be boolean")
                needs_human = text in {"true", "1"}

        normalized: dict[str, Any] = {
            "summary": summary,
            "topic": topic,
            "customer_need": customer_need,
            "entities": entities,
            "confidence": round(confidence, 4),
            "response_mode": response_mode,
            "understanding_note": understanding_note,
            "response_mode_reason": response_mode_reason,
            "suggested_next_step": suggested_next_step,
        }
        if risk_level is not None:
            normalized["risk_level"] = risk_level
        if needs_human is not None:
            normalized["needs_human"] = needs_human
        return normalized

    def _parse_json_object(self, raw_response_text: str) -> Any:
        stripped = raw_response_text.strip()
        try:
            return json.loads(stripped)
        except Exception:
            pass

        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, flags=re.DOTALL | re.IGNORECASE)
        if fenced:
            return json.loads(fenced.group(1))

        object_match = re.search(r"(\{.*\})", stripped, flags=re.DOTALL)
        if object_match:
            return json.loads(object_match.group(1))

        raise RuntimeError("LLM output is not valid JSON")

    def _retry_hint(self) -> str:
        return (
            "\n\nREMINDER: your previous output was invalid. "
            "Return STRICT JSON ONLY with the exact required keys, valid response_mode, "
            "and non-empty understanding_note, response_mode_reason, suggested_next_step."
        )

    def _resolve_model(self, config: dict[str, Any]) -> str:
        settings = config["settings"]
        if config["backend"] == "ollama":
            return str(settings.get("ollama_model", "") or "")
        return str(settings.get("openai_model", "") or "")

    def _resolve_uid(self, dossier_payload: dict[str, Any]) -> str:
        metadata = dossier_payload.get("metadata") or {}
        uid = str(metadata.get("uid", "") or "").strip()
        if uid:
            return uid
        return str(dossier_payload.get("uid", "") or "unknown")
