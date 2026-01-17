import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from app_logging import configure_logging, get_logger
from config import MODEL_NAME
from error_handling import APIError, UnauthorizedError, UnsupportedIntentError
from domain.authorization import is_authorized
from domain.intents import SUPPORTED_INTENTS
from domain.sql_templates import SQL_TEMPLATES
from infra.session_store import SessionStore
from infra.cache import IntentCache
from infra.sandbox import validate_sql
from llm.azure_openai import classify_intent
from llm.prompts import SYSTEM_PROMPT

configure_logging()
logger = get_logger("inventory-api")

session_store = SessionStore()
intent_cache = IntentCache()


class ChatHandler(BaseHTTPRequestHandler):

    def _respond(self, payload: dict, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

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

            cached = intent_cache.get(message)
            start = time.monotonic()

            if cached:
                intent = cached
                latency_ms = 0
                body = {}
            else:
                llm_messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ]
                body, latency_ms = classify_intent(llm_messages)
                intent = json.loads(body["choices"][0]["message"]["content"])["intent"]
                intent_cache.set(message, intent)

            if intent not in SUPPORTED_INTENTS:
                raise UnsupportedIntentError()

            if not is_authorized(role, intent):
                raise UnauthorizedError()

            answer, sql = SQL_TEMPLATES[intent]
            validate_sql(sql)

            session_store.save(session_id, messages)

            self._respond({
                "natural_language_answer": answer.format(value="X"),
                "sql_query": sql.strip(),
                "token_usage": body.get("usage", {}),
                "latency_ms": latency_ms,
                "provider": "azure",
                "model": MODEL_NAME,
                "status": "ok",
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