import json
import time
import urllib.request
from apps.api.src.app_logging import get_logger
from apps.api.src.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_KEY,
)

logger = get_logger(__name__)

API_VERSION = "2024-12-01-preview"


def classify_intent(messages):
    if not AZURE_OPENAI_ENDPOINT.startswith("https://"):
        raise RuntimeError("Invalid AZURE_OPENAI_ENDPOINT")

    url = (
        f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}"
        f"/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}"
        f"/chat/completions?api-version={API_VERSION}"
    )

    payload = {
        "messages": messages,
        "temperature": 0,
        "max_tokens": 256,
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    start = time.monotonic()

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            latency_ms = int((time.monotonic() - start) * 1000)
            body = json.loads(resp.read().decode("utf-8"))

            message = body["choices"][0]["message"]["content"]
            usage = body.get("usage", {})

            token_usage = {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            }

            return message, latency_ms, token_usage

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        logger.error("Azure OpenAI HTTP error %s: %s", e.code, error_body)
        raise RuntimeError("Azure OpenAI request failed")