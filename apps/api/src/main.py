import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from apps.api.src.app_logging import configure_logging, get_logger
from apps.api.src.config import MODEL_NAME
from apps.api.src.error_handling import APIError, UnauthorizedError, UnsupportedIntentError
from apps.api.src.domain.authorization import is_authorized
from apps.api.src.domain.intents import SUPPORTED_INTENTS
from apps.api.src.domain.sql_templates import SQL_TEMPLATES
from apps.api.src.infra.session_store import SessionStore
from apps.api.src.infra.cache import IntentCache
from apps.api.src.infra.sandbox import validate_sql
from apps.api.src.llm.azure_openai import classify_intent
from apps.api.src.llm.prompts import SYSTEM_PROMPT

configure_logging()
logger = get_logger("inventory-api")

session_store = SessionStore()
intent_cache = IntentCache()


class ChatHandler(BaseHTTPRequestHandler):

    def _respond(self, payload: dict, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_POST(self):
        if self.path != "/api/chat":
            self._respond({"status": "error", "message": "Not found"}, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))

            session_id = payload.get("session_id")
            message = payload.get("message")
            role = payload.get("context", {}).get("role", "viewer")

            if not message:
                raise APIError("Message is required")

            messages = session_store.get(session_id)
            messages.append({"role": "user", "content": message})

            cached_intent = intent_cache.get(message)
            start = time.monotonic()

            if cached_intent:
                intent = cached_intent
                latency_ms = 0
            else:
                llm_messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ]

                llm_response_text, latency_ms = classify_intent(llm_messages)

                try:
                    parsed = json.loads(llm_response_text)
                    intent = parsed["intent"]
                except (json.JSONDecodeError, KeyError):
                    logger.error("Invalid LLM response: %s", llm_response_text)
                    raise APIError("Invalid LLM response format")

                intent_cache.set(message, intent)

            if intent not in SUPPORTED_INTENTS:
                raise UnsupportedIntentError()

            if not is_authorized(role, intent):
                raise UnauthorizedError()

            answer_template, sql = SQL_TEMPLATES[intent]
            validate_sql(sql)
    
            session_store.save(session_id, messages)

            self._respond({
                "status": "ok",
                "intent": intent,
                "natural_language_answer": answer_template.format(value="X"),
                "sql_query": sql.strip(),
                "latency_ms": latency_ms,
                "provider": "azure",
                "model": MODEL_NAME,
            })

        except APIError as e:
            logger.warning("Handled API error: %s", e.message)
            self._respond(e.to_response(), e.status_code)

        except Exception:
            logger.exception("Unhandled server error")
            self._respond(
                {"status": "error", "message": "Internal server error"},
                500,
            )


def run():
    logger.info("Starting Inventory API on port 8000")
    HTTPServer(("0.0.0.0", 8000), ChatHandler).serve_forever()


if __name__ == "__main__":
    run()